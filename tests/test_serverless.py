"""Checks for the simulated serverless aggregation (Task 3)."""

import json
from pathlib import Path

import pandas as pd

from lambda_function import MACROS, OUTPUT_FILE, average_macros

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_DIETS = {"dash", "keto", "mediterranean", "paleo", "vegan"}


def test_average_macros_groups_by_diet():
    df = pd.DataFrame(
        {
            "Diet_type": ["keto", "keto", "vegan"],
            "Protein(g)": [10.0, 20.0, 5.0],
            "Carbs(g)": [1.0, 3.0, 40.0],
            "Fat(g)": [8.0, 12.0, 2.0],
        }
    )
    avg = average_macros(df)
    assert list(avg.columns) == MACROS
    assert avg.loc["keto", "Protein(g)"] == 15.0
    assert avg.loc["keto", "Carbs(g)"] == 2.0
    assert avg.loc["vegan", "Fat(g)"] == 2.0


def test_saved_nosql_results_cover_every_diet():
    results_path = ROOT / OUTPUT_FILE
    records = json.loads(results_path.read_text())
    diets = {row["Diet_type"] for row in records}
    assert diets == EXPECTED_DIETS
    for row in records:
        for column in MACROS:
            assert row[column] > 0
