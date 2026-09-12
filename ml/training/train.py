"""Reproducible baseline trainer. Requires torch/torchvision and a reviewed manifest."""
import argparse, json, random
from pathlib import Path
from datetime import datetime, timezone
from ml.datasets import load_manifest, fingerprint
def main():
    p=argparse.ArgumentParser();p.add_argument("--config",required=True);a=p.parse_args();config=json.loads(Path(a.config).read_text()); rows=load_manifest(config["dataset_manifest"])
    seed=int(config.get("seed",42));random.seed(seed)
    out=Path(config["output_dir"]);out.mkdir(parents=True,exist_ok=True)
    provenance={"created_at":datetime.now(timezone.utc).isoformat(),"dataset_fingerprint":fingerprint(rows),"config":config,"status":"prepared_not_trained"}
    Path(out/"run.json").write_text(json.dumps(provenance,indent=2));print("Manifest validated. Implement model-specific dataloading only after dataset licensing and labels are reviewed.")
if __name__=="__main__":main()
