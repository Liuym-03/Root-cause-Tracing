# -*- coding: utf-8 -*-
"""检查 CMAPSS 实验代码是否齐全。不读取数据集。"""
import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parent

MODULES = {
    "ckg_qrit/cmapss_model.py": "CMAPSS 根因定位模型：基线、知识图谱、因果干预、融合与实验流程",
    "experiments/compare_cmapss.py": "CMAPSS 对比实验",
    "experiments/sensitivity_cmapss.py": "CMAPSS 敏感性分析",
}

CHECKS = {
    "ckg_qrit/cmapss_model.py": [
        "score_baseline",
        "build_kg_priors",
        "score_causal_do",
        "fuse_log_opinion_pool",
        "train_a8_artifact",
        "predict_a8_full",
        "run_experiment",
    ],
    "experiments/compare_cmapss.py": ["score_apriori", "score_fta", "run_comparison"],
    "experiments/sensitivity_cmapss.py": [
        "run_sensitivity_bagging",
        "run_sensitivity_rule_beta",
        "run_sensitivity_anomaly_weight",
    ],
}

FORBIDDEN = ["def load_fd", "def make_weak_cause_labels", "def split_train_val", "pd.read_csv"]


def main() -> None:
    print("CKG-QRIT / CMAPSS")
    missing = False
    for rel, desc in MODULES.items():
        path = ROOT / rel
        ok = path.exists()
        missing = missing or not ok
        print(f"[{'OK' if ok else '缺失'}] {rel}  {desc}")
        if not ok:
            continue
        text = path.read_text(encoding="utf-8")
        ast.parse(text)
        for name in CHECKS.get(rel, []):
            if f"def {name}" not in text:
                missing = True
                print(f"    缺少函数 {name}")
        for token in FORBIDDEN:
            if token in text:
                missing = True
                print(f"    仍包含数据处理代码: {token}")
    if missing:
        raise SystemExit("分享包不符合要求")
    print("模块检查通过。仅保留 CMAPSS，且不包含数据读取与划分。")


if __name__ == "__main__":
    main()
