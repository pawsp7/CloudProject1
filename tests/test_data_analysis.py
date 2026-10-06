"""Checks for the Task 1 analysis script used by the container image."""

import os
import subprocess
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "All_Diets.csv"
MACROS = ["Protein(g)", "Carbs(g)", "Fat(g)"]
EXPECTED_DIETS = {"dash", "keto", "mediterranean", "paleo", "vegan"}


def test_dataset_has_expected_diets_and_macros():
    df = pd.read_csv(CSV)
    assert len(df) > 1000
    assert EXPECTED_DIETS <= set(df["Diet_type"].unique())
    for column in MACROS:
        assert column in df.columns
        assert df[column].notna().any()


def test_keto_is_lower_carb_and_higher_protein_than_vegan():
    df = pd.read_csv(CSV)
    df[MACROS] = df[MACROS].fillna(df[MACROS].mean())
    avg = df.groupby("Diet_type")[MACROS].mean()
    assert avg.loc["keto", "Carbs(g)"] < avg.loc["vegan", "Carbs(g)"]
    assert avg.loc["keto", "Protein(g)"] > avg.loc["vegan", "Protein(g)"]
    assert avg.loc["keto", "Fat(g)"] > avg.loc["vegan", "Fat(g)"]


def test_analysis_script_prints_insights():
    env = os.environ.copy()
    env["SHOW"] = "0"
    env["MPLBACKEND"] = "Agg"
    result = subprocess.run(
        [sys.executable, "data_analysis.py"],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "average macros by diet" in result.stdout
    assert "highest average protein diet:" in result.stdout
    assert "single highest protein recipe:" in result.stdout
    for diet in EXPECTED_DIETS:
        assert diet in result.stdout
    assert (ROOT / "figures" / "avg_macros_bar.png").is_file()
    assert (ROOT / "figures" / "macros_heatmap.png").is_file()
    assert (ROOT / "figures" / "top_protein_scatter.png").is_file()
