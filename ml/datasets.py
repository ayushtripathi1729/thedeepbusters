import json, random
from pathlib import Path

def load_manifest(path):
    """JSONL: path,label,split,source_id,identity_id. Split before training to avoid leakage."""
    rows=[]
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        row=json.loads(line)
        if row.get("label") not in {0,1}: raise ValueError("labels must be 0 (authentic) or 1 (manipulated)")
        if not row.get("path") or not row.get("split"): raise ValueError("manifest requires path and split")
        rows.append(row)
    groups={}
    for row in rows: groups.setdefault(row.get("identity_id") or row.get("source_id") or row["path"],set()).add(row["split"])
    if any(len(s)>1 for s in groups.values()): raise ValueError("identity/source leakage detected across splits")
    return rows
def fingerprint(rows):
    import hashlib
    return hashlib.sha256("\n".join(sorted(r["path"] for r in rows)).encode()).hexdigest()
