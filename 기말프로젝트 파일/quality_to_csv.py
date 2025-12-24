# quality_to_csv.py
from __future__ import annotations
import argparse, json, csv, xml.etree.ElementTree as ET
from pathlib import Path
from collections import Counter

def read_junit(path: Path) -> dict:
    root = ET.parse(path).getroot()
    suites = [root] if root.tag == "testsuite" else root.findall("testsuite")
    total = failures = errors = skipped = 0; time_sum = 0.0; cases=[]
    for s in suites:
        total += int(s.get("tests", 0)); failures += int(s.get("failures", 0))
        errors += int(s.get("errors", 0)); skipped += int(s.get("skipped", 0))
        time_sum += float(s.get("time", 0.0) or 0.0)
        for tc in s.findall("testcase"):
            status = "ok"
            if tc.find("failure") is not None: status="failure"
            elif tc.find("error") is not None: status="error"
            elif tc.find("skipped") is not None: status="skipped"
            cases.append({
                "classname": tc.get("classname") or "",
                "name": tc.get("name") or "",
                "time": float(tc.get("time", 0.0) or 0.0),
                "status": status
            })
    return {"total": total,"failures": failures,"errors": errors,"skipped": skipped,"time": time_sum,"cases": cases}

def read_coverage(path: Path) -> dict:
    root = ET.parse(path).getroot()
    line_rate = float(root.get("line-rate", 0.0) or 0.0)
    files=[]
    for cls in root.findall(".//class"):
        fn = cls.get("filename")
        lr = cls.get("line-rate")
        if fn:
            files.append({"filename": fn, "line_rate": float(lr) if lr else 0.0})
    return {"line_rate": line_rate, "files": files}

def read_ruff(path: Path) -> list[dict]:
    if not path.exists() or path.stat().st_size == 0: return []
    data = json.loads(path.read_text(encoding="utf-8"))
    items = data.get("diagnostics", []) if isinstance(data, dict) else data
    out=[]
    for it in items:
        filename = it.get("filename") or it.get("path") or ""
        code = it.get("code") or (it.get("rule") or {}).get("code") or "NA"
        msg = it.get("message") or (it.get("diagnostic") or {}).get("message") or ""
        line = 0; col = 0
        if isinstance(it.get("location"), dict):
            line = it["location"].get("row") or it["location"].get("line") or 0
            col  = it["location"].get("column") or it["location"].get("col") or 0
        elif isinstance(it.get("range"), dict):
            start = it["range"].get("start") or {}
            line = start.get("line", 0); col = start.get("character", 0)
        out.append({"filename": filename, "line": int(line), "col": int(col), "code": str(code), "message": msg})
    return out

def write_csvs(outdir: Path, junit: dict, cov: dict, ruffs: list[dict]) -> None:
    outdir.mkdir(parents=True, exist_ok=True)

    # 1) 요약
    passed = junit["total"] - junit["failures"] - junit["errors"] - junit["skipped"]
    with open(outdir/"summary.csv","w",newline="",encoding="utf-8") as f:
        w=csv.writer(f)
        w.writerow(["metric","value"])
        w.writerow(["tests_total", junit["total"]])
        w.writerow(["tests_passed", passed])
        w.writerow(["tests_failed", junit["failures"] + junit["errors"]])
        w.writerow(["tests_skipped", junit["skipped"]])
        w.writerow(["tests_time_sec", round(junit["time"],3)])
        w.writerow(["coverage_percent", round(cov["line_rate"]*100,2)])
        w.writerow(["lint_issues", len(ruffs)])

    # 2) 테스트 케이스
    with open(outdir/"tests.csv","w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["classname","name","status","time_sec"])
        for c in junit["cases"]:
            w.writerow([c["classname"], c["name"], c["status"], round(c["time"],4)])

    # 3) 파일별 커버리지
    with open(outdir/"coverage_files.csv","w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["filename","coverage_percent"])
        for fobj in cov["files"]:
            w.writerow([fobj["filename"], round(fobj["line_rate"]*100,2)])

    # 4) 린트 목록
    with open(outdir/"lint.csv","w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["filename","line","col","code","message"])
        for it in ruffs:
            w.writerow([it["filename"], it["line"], it["col"], it["code"], it["message"]])

    # 5) 린트 규칙 Top5
    cnt = Counter([it["code"] for it in ruffs])
    with open(outdir/"lint_top5.csv","w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["rank","rule","count"])
        for i,(rule,n) in enumerate(cnt.most_common(5),1):
            w.writerow([i, rule, n])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--junit", required=True)
    ap.add_argument("--coverage", required=True)
    ap.add_argument("--ruff", required=True)
    ap.add_argument("--outdir", default="out_csv")
    args = ap.parse_args()

    junit = read_junit(Path(args.junit))
    cov   = read_coverage(Path(args.coverage))
    ruffs = read_ruff(Path(args.ruff))

    write_csvs(Path(args.outdir), junit, cov, ruffs)
    print("CSV 생성:", Path(args.outdir).resolve())

if __name__ == "__main__":
    main()
