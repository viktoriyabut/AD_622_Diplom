import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="white", palette="Blues")

df = pd.read_csv("enrollments_full.csv", encoding="utf-8-sig")
df["start_date"] = pd.to_datetime(df["start_date"])
df = df.drop_duplicates()

# Фильтр
df_fin = df[df["status"].isin(["completed", "dropped"])].copy()
df_fin["is_completed"] = (df_fin["status"] == "completed").astype(int)

# Агрегация по форматам
agg_format = df_fin.groupby("format").agg(
    total=("enroll_id", "count"),
    completed=("is_completed", "sum"),
    avg_score=("final_score", "mean"),
).reset_index()
agg_format["completion_rate"] = agg_format["completed"] / agg_format["total"] * 100
agg_format = agg_format.sort_values("completion_rate", ascending=False)

print("--- Завершаемость по форматам обучения ---")
print(agg_format.to_string(index=False))

# Диаграмма: KPI-карточки

n = len(agg_format)
fig, axes = plt.subplots(1, n, figsize=(5 * n, 5), dpi=100)

if n == 1:
    axes = [axes]

palette = ["#1a237e", "#00838f", "#3949ab"]

for i, row in enumerate(agg_format.itertuples()):
    ax = axes[i]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    color = palette[i % len(palette)]
    bg = '#f5f5f5'  # светло-серый фон

    ax.text(0.5, 0.5, '', ha='center', va='center',
            bbox=dict(boxstyle="round,pad=0.8", fc=bg,
                      ec=color, lw=2.5), fontsize=1)

    ax.text(0.5, 0.80, f"ФОРМАТ:\n{row.format.upper()}",
            ha='center', va='center', fontsize=11,
            fontweight='bold', color='#1a237e')

    ax.text(0.5, 0.45, f"{row.completion_rate:.1f}%",
            ha='center', va='center', fontsize=28,
            fontweight='bold', color=color)

    ax.text(0.5, 0.15, f"{row.completed} из {row.total} записей\n"
            f"ср. оценка: {row.avg_score:.2f}",
            ha='center', va='center', fontsize=9,
            color='#9e9e9e')

    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

fig.suptitle("Завершаемость по форматам обучения",
             fontsize=14, fontweight='bold', color='#1a237e')
plt.tight_layout()
plt.show()

# Диаграмма bar - средняя оценка по форматам
fig, ax = plt.subplots(figsize=(9, 4.5), dpi=100)

colors2 = palette[:n]
ax.barh(agg_format["format"][::-1], agg_format["avg_score"][::-1],
        color=colors2[::-1], edgecolor="white", height=0.55)

for i, row in enumerate(agg_format.itertuples()):
    y_pos = n - 1 - i
    ax.text(row.avg_score + 0.05, y_pos,
            f"{row.avg_score:.2f}", va="center", ha="left",
            fontsize=11, fontweight="bold", color="#1a237e")

ax.set_xlim(0, 5.5)
ax.set_xlabel("Средняя финальная оценка (1–5)", fontsize=11, color="#1a237e")
ax.set_title("Средняя оценка по форматам обучения",
             fontsize=13, fontweight="bold", color="#1a237e")
ax.grid(axis="x", linestyle="--", alpha=0.4, color="#9e9e9e")
plt.tight_layout()
plt.show()
