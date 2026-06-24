#!/usr/bin/env python3
"""Tier-2 semantic sibling dedup via Pioneer (claude-opus-4-8). Resumable.
Packs small parents per call; single call per medium parent; chunks giant parents.
Split-on-failure isolates a poison parent so it can't kill its unit-mates.
Resume retries any parent whose last result carried an 'error'."""
import os, sys, json, time, re, unicodedata, urllib.request, urllib.error, concurrent.futures as cf, threading

KEY     = os.environ.get("DEDUP_KEY") or os.environ["PIONEER_API_KEY"]
MODEL   = os.environ.get("DEDUP_MODEL","claude-opus-4-8")
URL     = os.environ.get("DEDUP_URL","https://api.pioneer.ai/v1/chat/completions")
API     = os.environ.get("DEDUP_API","openai")   # "openai" (chat/completions) or "anthropic" (/v1/messages)
HERE    = os.path.dirname(os.path.abspath(__file__))
IN      = os.path.join(HERE,"tier2_batches.jsonl")
OUT     = os.environ.get("DEDUP_OUT", os.path.join(HERE,"tier2_results.jsonl"))
WORKERS = int(os.environ.get("DEDUP_WORKERS","10"))
CHUNK   = 60   # max siblings per LLM call
MAXTOK  = int(os.environ.get("DEDUP_MAXTOK","4096"))

SYSTEM = (
"You are an expert American legal taxonomist curating an open SKOS legal-issue taxonomy. "
"You are given groups of sibling concepts; in each group all concepts share the SAME parent. "
"Each sibling is a recurring American legal issue stated in its parent's context. For EACH group, "
"cluster ONLY the siblings whose preferred labels denote the SAME legal concept (true synonyms, "
"rephrasings, word-order or singular/plural variants, or American-law equivalent terminology).\n"
"CRITICAL RULES:\n"
"1. Merge ONLY genuine synonyms. MERGE example: 'HUSBAND AND WIFE' = 'MARITAL RELATIONS' = "
"'MARRIAGE AND MARITAL RELATIONS' = 'MARITAL RELATIONSHIPS' (all the spousal-relationship concept).\n"
"2. NEVER merge merely-related or distinct concepts. DISTINCT example: 'MARRIAGE AND DIVORCE', "
"'MARITAL PROPERTY', 'MARITAL STATUS', 'SPOUSAL SUPPORT', 'PARENT AND CHILD', 'MARITAL AGREEMENTS' "
"are each different from one another and from the spousal-relationship concept — keep separate.\n"
"3. NEGATION/ANTONYM GUARD: never merge a label with its opposite. Words/prefixes like NON-, NO, "
"NOT, WITHOUT, ANTI-, UN-, DIS-, EX-, FORMER, and VOLUNTARY vs INVOLUNTARY flip meaning. "
"E.g. NEVER merge 'RECOGNITION OF GAIN' with 'NONRECOGNITION OF GAIN', 'MARITAL' with 'NON-MARITAL', "
"'LIABILITY' with 'NONLIABILITY', 'DISCLOSED' with 'UNDISCLOSED'.\n"
"4. When uncertain, DO NOT merge. Precision over recall. If the only honest reason would contain the "
"words 'distinct', 'separate', 'different', or 'but', then DO NOT cluster those members.\n"
"5. A cluster needs >=2 members; identify members by their bracketed notation code.\n"
"Return STRICT minified JSON only, no prose, no markdown fences, escape all inner quotes: "
"{\"groups\":[{\"parent\":\"CODE\",\"clusters\":[{\"members\":[\"c\",\"c\"],\"reason\":\"short\"}]}]}."
)

def call(payload, tries=5):
    data=json.dumps(payload).encode()
    if API=="anthropic":
        hdr={"Content-Type":"application/json","x-api-key":KEY,"anthropic-version":"2023-06-01"}
    else:
        hdr={"Content-Type":"application/json","Authorization":f"Bearer {KEY}"}
    for i in range(tries):
        req=urllib.request.Request(URL,data=data,headers=hdr)
        try:
            with urllib.request.urlopen(req,timeout=240) as r: return json.loads(r.read())
        except urllib.error.HTTPError as e:
            body=e.read().decode()[:160]
            if e.code in (408,409,429,500,502,503,529) and i<tries-1: time.sleep(2**i); continue
            raise RuntimeError(f"HTTP {e.code}: {body}")
        except Exception:
            if i<tries-1: time.sleep(2**i); continue
            raise
    raise RuntimeError("exhausted")

def extract_json(text):
    s=text.strip()
    if "```" in s:
        m=re.search(r"```(?:json)?\s*(.*?)```",s,re.S)
        if m: s=m.group(1).strip()
    a=s.find("{"); b=s.rfind("}")
    s=s[a:b+1]
    dec=json.JSONDecoder()
    try:
        obj,_=dec.raw_decode(s)   # parse first complete object, ignore any trailing data
        return obj
    except json.JSONDecodeError:
        # cleanup pass: normalize smart quotes/dashes, strip control chars, drop trailing commas
        t=unicodedata.normalize("NFKC",s)
        t=t.replace("“",'"').replace("”",'"').replace("‘","'").replace("’","'")
        t="".join(ch for ch in t if ch>="\x20" or ch in "\t")
        t=re.sub(r",\s*([}\]])",r"\1",t)
        obj,_=dec.raw_decode(t)
        return obj

def block(p):
    head=f"### GROUP parent=[{p['parent']}] {p['parent_label']}"
    body="\n".join(f"[{x['notation']}] {x['label']}  (sources={x['sources']},children={x['children']})" for x in p["siblings"])
    return head+"\n"+body

def llm_groups(ps):
    """One LLM call over a list of parent blocks. Returns {parent: [clusters]}. Raises on parse fail."""
    user=("Cluster synonymous siblings in each group below. Return strict JSON keyed by parent.\n\n"
          +"\n\n".join(block(p) for p in ps))
    if API=="responses":   # OpenAI Responses API (gpt-5.5-pro and other reasoning/pro models)
        payload={"model":MODEL,"instructions":SYSTEM,"input":user,"max_output_tokens":MAXTOK}
        eff=os.environ.get("DEDUP_EFFORT")
        if eff: payload["reasoning"]={"effort":eff}
        resp=call(payload)
        txt=resp.get("output_text","")
        if not txt:
            for item in resp.get("output",[]):
                for c in item.get("content",[]):
                    if c.get("type")=="output_text": txt+=c["text"]
        parsed=extract_json(txt)
    elif API=="anthropic":
        payload={"model":MODEL,"system":SYSTEM,"messages":[{"role":"user","content":user}],
                 "max_tokens":MAXTOK,"temperature":0}
        resp=call(payload)
        parsed=extract_json(resp["content"][0]["text"])
    else:
        payload={"model":MODEL,"messages":[{"role":"system","content":SYSTEM},{"role":"user","content":user}],
                 "max_tokens":MAXTOK,"temperature":0}
        if os.environ.get("DEDUP_NOREASON"): payload["reasoning"]={"enabled":False}
        resp=call(payload)
        parsed=extract_json(resp["choices"][0]["message"]["content"])
    got={g["parent"]:g.get("clusters",[]) for g in parsed.get("groups",[])}
    out={}
    for p in ps:
        v={x["notation"] for x in p["siblings"]}; cl=[]
        for c in got.get(p["parent"],[]):
            mem=sorted({m for m in c.get("members",[]) if m in v})
            if len(mem)>=2: cl.append({"members":mem,"reason":c.get("reason","")})
        out[p["parent"]]=cl
    return out

def res(p,clusters,error=None):
    r={"parent":p["parent"],"parent_label":p["parent_label"],"n_siblings":p["_n"],"clusters":clusters}
    if error: r["error"]=error[:160]
    return r

def process_multi(ps):
    """Packed small parents. Split-on-failure to isolate poison parents."""
    try:
        g=llm_groups(ps)
        return [res(p,g[p["parent"]]) for p in ps]
    except Exception as e:
        if len(ps)==1:
            return [res(ps[0],[],str(e))]
        mid=len(ps)//2
        return process_multi(ps[:mid])+process_multi(ps[mid:])

def process_one(p):
    """Single parent; chunk internally if large, combine chunk clusters."""
    sibs=p["siblings"]
    if len(sibs)<=CHUNK:
        try: return [res(p,llm_groups([p])[p["parent"]])]
        except Exception as e: return [res(p,[],str(e))]
    ordered=sorted(sibs,key=lambda x:x["label"])
    combined=[]; errs=[]
    for i in range(0,len(ordered),CHUNK):
        sub=dict(p,siblings=ordered[i:i+CHUNK])
        try: combined+=llm_groups([sub])[p["parent"]]
        except Exception as e: errs.append(str(e))
    return [res(p,combined,"; ".join(errs) if errs else None)]

def main():
    done=set()
    if os.path.exists(OUT):
        for line in open(OUT):
            try:
                r=json.loads(line)
                if not r.get("error"): done.add(r["parent"])   # retry errored parents on resume
            except: pass
    batches=[json.loads(l) for l in open(IN) if l.strip()]
    for b in batches: b["_n"]=len(b["siblings"])
    batches=[b for b in batches if b["parent"] not in done]
    small=[b for b in batches if b["_n"]<=10]
    big  =[b for b in batches if b["_n"]>10]
    print(f"pending parents: small={len(small)} bigger={len(big)} (done={len(done)})",flush=True)

    units=[]   # (kind, payload)
    cur=[]; cap=0
    for b in small:
        if cur and (cap+b["_n"]>50 or len(cur)>=12):
            units.append(("multi",cur)); cur=[]; cap=0
        cur.append(b); cap+=b["_n"]
    if cur: units.append(("multi",cur))
    for b in big: units.append(("one",b))
    print(f"total units: {len(units)}",flush=True)

    lock=threading.Lock(); n=[0]; wrote=[0]
    def work(unit):
        kind,pl=unit
        return process_multi(pl) if kind=="multi" else process_one(pl)
    with open(OUT,"a") as fout, cf.ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs=[ex.submit(work,u) for u in units]
        for fut in cf.as_completed(futs):
            rs=fut.result()
            with lock:
                for r in rs:
                    fout.write(json.dumps(r)+"\n"); wrote[0]+=1
                fout.flush(); n[0]+=1
                if n[0]%25==0: print(f"  units {n[0]}/{len(units)}  parents_written={wrote[0]}",flush=True)
    print(f"done. parents_written={wrote[0]}")

if __name__=="__main__": main()
