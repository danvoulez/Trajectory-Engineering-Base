#!/usr/bin/env python3
import argparse, glob, json, os, hashlib, gzip, datetime as dt, re, sys

def blake_hex(path, algo):
    data = open(path,'rb').read()
    if algo=="blake3":
        # fallback usando blake2s (stdlib). Trocar para lib blake3 quando quiser.
        return hashlib.blake2s(data).hexdigest()
    if algo=="sha256":
        return hashlib.sha256(data).hexdigest()
    return hashlib.blake2s(data).hexdigest()

def guess_day_range_from_name(name):
    m = re.search(r"(20\d{2})-(\d{2})-(\d{2})", name)
    if not m:
        # fallback: usa mtime do arquivo
        ts = dt.datetime.utcfromtimestamp(os.path.getmtime(name)).date()
        start = dt.datetime.combine(ts, dt.time.min).isoformat()+"Z"
        end   = dt.datetime.combine(ts, dt.time.max).isoformat()+"Z"
        return [start,end]
    y,mn,d = map(int, m.groups())
    start = dt.datetime(y,mn,d,0,0,0).isoformat()+"Z"
    end   = dt.datetime(y,mn,d,23,59,59).isoformat()+"Z"
    return [start,end]

def count_spans(path):
    with open(path,'rb') as f:
        # 1a linha costuma ser header; se não for, a diferença é irrelevante para cap
        return sum(1 for _ in f) - 1

def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",",":")).encode()

def H(data, algo):
    a = algo.lower()
    if a=="sha256": return hashlib.sha256(data).digest()
    # preferido: blake3 (quando adicionar lib). Aqui usamos blake2s compatível.
    return hashlib.blake2s(data).digest()

def merkle(entries, algo):
    if not entries:
        return H(b"", algo).hex(), 0
    leaves = [ H(canonical(e), algo) for e in entries ]
    while len(leaves) > 1:
        nxt=[]
        for i in range(0,len(leaves),2):
            left = leaves[i]
            right = leaves[i] if i+1==len(leaves) else leaves[i+1]
            nxt.append(H(left+right, algo))
        leaves = nxt
    return leaves[0].hex(), len(entries)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--glob", required=True, help="glob dos TCAPs (ex: 'tcap/*.tcap.ndjson')")
    ap.add_argument("--out", required=True, help="arquivo de saída TBAC (ex: tbac/2025-12/tbac-2025-12.json)")
    ap.add_argument("--issuer", required=True, help="DID emissor (ex: did:dan:main)")
    ap.add_argument("--algo", default="blake2s", choices=["blake2s","sha256","blake3"])
    ap.add_argument("--sign", default=None, help="chave privada Ed25519 (PEM) para assinar TBAC")
    args = ap.parse_args()

    files = sorted(glob.glob(args.glob))
    entries=[]
    span_total=0

    for f in files:
        digest = blake_hex(f, args.algo)
        size = os.path.getsize(f)
        spans = max(0, count_spans(f))
        span_total += spans
        tr = guess_day_range_from_name(f)
        entries.append({
          "artifact": {
            "url": f,  # pode ser trocado por s3:// no pipeline
            "digest": { "algo": args.algo, "hex": digest },
            "size_bytes": size
          },
          "span_count": spans,
          "time_range": tr,
          "stats": { "lang": {}, "role": {}, "model": {} }  # agregado opcional
        })

    # ordena por digest p/ estabilidade
    entries = sorted(entries, key=lambda e: e["artifact"]["digest"]["hex"])

    root, leaf_count = merkle(entries, args.algo)

    tbac = {
      "tbac_version": "1",
      "issuer_did": args.issuer,
      "created_at": dt.datetime.utcnow().isoformat(timespec="seconds")+"Z",
      "entries": entries,
      "indexes": {},
      "merkle": { "algo": args.algo, "root": root, "leaf_count": leaf_count },
      "caps": { "bytes_max": 8*1024*1024, "gzip_max": 2*1024*1024, "entries_max": 50000 },
      "summary": { "span_total": span_total },
      "signature": None
    }

    # checa caps
    raw = canonical(tbac)
    gz  = gzip.compress(raw)
    if len(raw) > 8*1024*1024: sys.exit("CAP FAIL: raw > 8MB")
    if len(gz)  > 2*1024*1024: sys.exit("CAP FAIL: gzip > 2MB")

    # assina se pedirem
    if args.sign:
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.asymmetric import ed25519
        priv = serialization.load_pem_private_key(open(args.sign,"rb").read(), password=None)
        payload = json.loads(raw.decode("utf-8"))
        payload["signature"]=None
        blob = canonical(payload)
        sig = priv.sign(blob).hex()
        tbac["signature"] = sig

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    json.dump(tbac, open(args.out,"w",encoding="utf-8"), ensure_ascii=False, indent=2)

    print("OK TBAC:", args.out, "root=", root, "leaves=", leaf_count, "spans=", span_total)

if __name__ == "__main__":
    main()

