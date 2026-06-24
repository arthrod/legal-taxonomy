#!/usr/bin/env python3
"""Phase A (Isaacus): embed all distinct sibling labels with kanon-2-embedder (legal, 1792d).
Cached/resumable. Embeddings are unit-normalized by the API (dot product = cosine)."""
import os, json, time, pickle, urllib.request, urllib.error, concurrent.futures as cf, threading
HERE=os.path.dirname(os.path.abspath(__file__))
IK=os.environ["ISAACUS_API_KEY"]
URL="https://api.isaacus.com/v1/embeddings"
MODEL="kanon-2-embedder"
TASK=os.environ.get("ISAACUS_TASK","retrieval/document")
CACHE=os.path.join(HERE,"emb_isaacus.pkl")
BATCH=int(os.environ.get("EMB_BATCH","64")); WORKERS=int(os.environ.get("EMB_WORKERS","4"))

def batch(texts, tries=10):
    data=json.dumps({"model":MODEL,"texts":texts,"task":TASK}).encode()
    for i in range(tries):
        req=urllib.request.Request(URL,data=data,headers={"Authorization":f"Bearer {IK}","Content-Type":"application/json"})
        try:
            with urllib.request.urlopen(req,timeout=180) as r:
                d=json.loads(r.read())
            emb=sorted(d["embeddings"],key=lambda x:x.get("index",0))
            return [e["embedding"] for e in emb]
        except urllib.error.HTTPError as e:
            body=e.read().decode()[:160]
            if e.code in (429,500,502,503) and i<tries-1: time.sleep(min(90,4*(i+1))); continue
            raise RuntimeError(f"HTTP {e.code}: {body}")
        except Exception:
            if i<tries-1: time.sleep(3*(i+1)); continue
            raise
    raise RuntimeError("embed exhausted")

def main():
    labs=set()
    for l in open(os.path.join(HERE,"tier2_batches.jsonl")):
        if l.strip():
            for x in json.loads(l)["siblings"]: labs.add(x["label"])
    distinct=sorted(labs)
    cache=pickle.load(open(CACHE,"rb")) if os.path.exists(CACHE) else {}
    lock=threading.Lock()
    def work(ch): return list(zip(ch,batch(ch)))
    rounds=0
    while True:
        todo=[t for t in distinct if t not in cache]
        if not todo: print(f"complete. cached={len(cache)}",flush=True); break
        rounds+=1
        chunks=[todo[i:i+BATCH] for i in range(0,len(todo),BATCH)]
        print(f"round {rounds}: distinct={len(distinct)} cached={len(cache)} todo={len(todo)} chunks={len(chunks)}",flush=True)
        done=[0]; failed=[0]
        with cf.ThreadPoolExecutor(max_workers=WORKERS) as ex:
            futs={ex.submit(work,ch):ch for ch in chunks}
            for fut in cf.as_completed(futs):
                try: pairs=fut.result()
                except Exception: 
                    with lock: failed[0]+=1
                    continue
                with lock:
                    for t,v in pairs: cache[t]=v
                    done[0]+=1
                    if done[0]%20==0:
                        pickle.dump(cache,open(CACHE,"wb"))
                        print(f"  {done[0]}/{len(chunks)} batches cached={len(cache)}",flush=True)
        pickle.dump(cache,open(CACHE,"wb"))
        print(f"  round {rounds} end cached={len(cache)} failed={failed[0]}",flush=True)
        if rounds>=15: print("stop; remaining",len([t for t in distinct if t not in cache]),flush=True); break
        if failed[0]: time.sleep(15)

if __name__=="__main__": main()
