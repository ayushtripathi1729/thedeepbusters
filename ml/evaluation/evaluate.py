import argparse, json
from pathlib import Path
from ml.datasets import load_manifest, fingerprint
from ml.metrics import binary_metrics, expected_calibration_error
def main():
    p=argparse.ArgumentParser();p.add_argument("--predictions",required=True,help="JSONL with label and score");p.add_argument("--output",required=True);a=p.parse_args()
    rows=[json.loads(x) for x in Path(a.predictions).read_text().splitlines()]; labels=[r["label"] for r in rows];scores=[r["score"] for r in rows]
    report={"count":len(rows),"metrics":binary_metrics(labels,scores),"expected_calibration_error":expected_calibration_error(labels,scores)};Path(a.output).write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
if __name__=="__main__":main()
