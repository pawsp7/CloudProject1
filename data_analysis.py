# Task 1. Run from this folder: python3 data_analysis.py
CSV_PATH = "All_Diets.csv"  # next to this script
FIG_DIR = "figures"  # saved charts, windows also open for screenshots
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Host screenshots: SHOW=1 python3 data_analysis.py
# Containers stay headless (Dockerfile sets MPLBACKEND=Agg).
SHOW = os.environ.get("SHOW", "0") == "1"

MACROS = ["Protein(g)", "Carbs(g)", "Fat(g)"]


def main():
	os.makedirs(FIG_DIR, exist_ok=True)
	df = pd.read_csv(CSV_PATH)
	print("rows", len(df))
	missing = df[MACROS].isna().sum()
	print("missing before fill")
	print(missing.to_string())
	df[MACROS] = df[MACROS].fillna(df[MACROS].mean())  # lab: null macros become the column mean
	print("missing after fill")
	print(df[MACROS].isna().sum().to_string())
	avg = df.groupby("Diet_type")[MACROS].mean().sort_values("Protein(g)", ascending=False)
	print("\naverage macros by diet")
	print(avg.round(2).to_string())
	top_diet = avg["Protein(g)"].idxmax()
	print("\nhighest average protein diet:", top_diet, round(avg.loc[top_diet, "Protein(g)"], 2), "g")
	richest = df.loc[df["Protein(g)"].idxmax()]
	print("single highest protein recipe:", richest["Recipe_name"], "|", richest["Diet_type"], "|", round(richest["Protein(g)"], 2), "g")
	top5 = df.sort_values("Protein(g)", ascending=False).groupby("Diet_type", group_keys=False).head(5)
	print("\ntop 5 protein recipes per diet")
	print(top5[["Diet_type", "Recipe_name", "Cuisine_type", "Protein(g)"]].to_string(index=False))
	print("\nmost common cuisine per diet")
	for diet, group in df.groupby("Diet_type"):
		counts = group["Cuisine_type"].value_counts()
		print(diet, counts.index[0], int(counts.iloc[0]))
	df["Protein_to_Carbs_ratio"] = df["Protein(g)"] / df["Carbs(g)"]
	df["Carbs_to_Fat_ratio"] = df["Carbs(g)"] / df["Fat(g)"].where(df["Fat(g)"] != 0)  # 0 fat would be infinite
	print("\nratios, carbs/fat left blank where fat is 0:", int(df["Carbs_to_Fat_ratio"].isna().sum()))
	print(df[["Protein_to_Carbs_ratio", "Carbs_to_Fat_ratio"]].describe().round(2).to_string())
	sns.set_theme(style="whitegrid")
	# grouped bars, one chart for all three averages
	long = avg.reset_index().melt("Diet_type", MACROS, var_name="Macro", value_name="Grams")
	plt.figure(figsize=(10, 5))
	sns.barplot(data=long, x="Diet_type", y="Grams", hue="Macro")
	plt.title("Average macronutrients by diet type")
	plt.ylabel("Average (g)")
	plt.tight_layout()
	plt.savefig(os.path.join(FIG_DIR, "avg_macros_bar.png"), dpi=150)
	if SHOW:
		plt.show()
	plt.figure(figsize=(8, 4))
	sns.heatmap(avg, annot=True, fmt=".1f", cmap="YlGnBu")
	plt.title("Macronutrients by diet type")
	plt.tight_layout()
	plt.savefig(os.path.join(FIG_DIR, "macros_heatmap.png"), dpi=150)
	if SHOW:
		plt.show()
	plt.figure(figsize=(12, 5))
	sns.scatterplot(data=top5, x="Cuisine_type", y="Protein(g)", hue="Diet_type", s=80)
	plt.title("Top 5 protein recipes per diet, by cuisine")
	plt.xticks(rotation=45, ha="right")
	plt.tight_layout()
	plt.savefig(os.path.join(FIG_DIR, "top_protein_scatter.png"), dpi=150)
	if SHOW:
		plt.show()
	print("\nsaved", FIG_DIR)


if __name__ == "__main__":
	main()
