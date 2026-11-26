import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette="Blues")

df = pd.read_csv("enrollments_full.csv", encoding="utf-8-sig")
df["start_date"] = pd.to_datetime(df["start_date"])
df = df.drop_duplicates()

df_fin = df[df["status"].isin(["completed", "dropped"])].copy()
df_fin["is_completed"] = (df_fin["status"] == "completed").astype(int)

# Агрегация по категориям
agg_category = df_fin.groupby("category").agg(
    total=("enroll_id", "count"),
    completed=("is_completed", "sum"),
    avg_score=("final_score", "mean"),
    avg_progress=("progress_pct", "mean"),
).reset_index()
agg_category["completion_rate"] = agg_category["completed"] / agg_category["total"] * 100
agg_category = agg_category.sort_values("completion_rate", ascending=True)

print("--- Завершаемость по категориям курсов ---")
print(agg_category.to_string(index=False))

# Диаграмма: распределение финальных оценок по категориям
fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
sns.violinplot(
    data=df_fin[df_fin["status"] == "completed"],
    x="final_score", y="category", ax=ax,
    palette="Blues", inner="quart",
)
ax.set_title("Распределение финальных оценок по категориям курсов",
             fontsize=13, fontweight="bold", color="#1a237e")
ax.set_xlabel("Финальная оценка (1–5)")
ax.set_ylabel("Категория курса")
ax.set_xlim(1.5, 5.5)
plt.tight_layout()
plt.show()

# Диаграмма: bar — завершаемость по категориям
fig, ax = plt.subplots(figsize=(10, 6), dpi=100)

colors = ['#7986cb', '#5c6bc0', '#3949ab', '#283593', '#1a237e']
colors = colors[:len(agg_category)]
ax.barh(agg_category["category"], agg_category["completion_rate"],
        color=colors, edgecolor="white")

# Подписи значений
for i, row in enumerate(agg_category.itertuples()):
    ax.text(row.completion_rate + 1.5, i,
            f"{row.completion_rate:.1f}%  ({row.completed}/{row.total})",
            va="center", ha="left", fontsize=10,
            fontweight="bold", color="#1a237e")

ax.set_title("Завершаемость по категориям курсов",
             fontsize=13, fontweight="bold", color="#1a237e")
ax.set_xlabel("Завершаемость, %")
ax.set_ylabel("Категория курса")
ax.set_xlim(0, 115)
ax.grid(axis="x", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.show()