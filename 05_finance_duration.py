import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette="Blues")

df = pd.read_csv("enrollments_full.csv", encoding="utf-8-sig")
df["start_date"] = pd.to_datetime(df["start_date"])
df = df.drop_duplicates()

# Фильтр
df_fin = df[df["status"].isin(["completed", "dropped"])].copy()
df_fin["is_completed"] = (df_fin["status"] == "completed").astype(int)

# Агрегация по длительности курса
agg_duration = df_fin.groupby("duration_weeks").agg(
    total=("enroll_id", "count"),
    completed=("is_completed", "sum"),
    avg_score=("final_score", "mean"),
).reset_index()
agg_duration["completion_rate"] = agg_duration["completed"] / agg_duration["total"] * 100
agg_duration = agg_duration.sort_values("duration_weeks")

print("--- Завершаемость по длительности курса ---")
print(agg_duration.to_string(index=False))

# Пузырьковая диаграмма
fig, ax1 = plt.subplots(figsize=(11, 6.5), dpi=100)

sizes = agg_duration["total"] / agg_duration["total"].max() * 900 + 80

scatter = ax1.scatter(
    agg_duration["duration_weeks"], agg_duration["completion_rate"],
    s=sizes, c=agg_duration["avg_score"], cmap="Blues",
    edgecolor="black", linewidth=0.5, alpha=0.8,
)

cbar = fig.colorbar(scatter, ax=ax1)
cbar.set_label("Средняя оценка (1–5)", fontsize=10, color="#1a237e")

ax1.set_xlabel("Длительность курса, недель", fontsize=11, color="#1a237e")
ax1.set_ylabel("Завершаемость, %", fontsize=11, color="#1a237e")
ax1.set_ylim(0, 110)


for row in agg_duration.itertuples():
    ax1.annotate(f"{row.completion_rate:.0f}%",
                 (row.duration_weeks, row.completion_rate),
                 textcoords="offset points", xytext=(0, 10),
                 ha="center", fontsize=10, fontweight="bold",
                 color="#1a237e")

ax2 = ax1.twinx()
ax2.plot(agg_duration["duration_weeks"], agg_duration["total"],
         color="#00838f", linewidth=2.5, linestyle="--",
         marker="s", markersize=6, alpha=0.8,
         label="Кол-во записей")
ax2.set_ylabel("Количество записей", fontsize=11, color="#00838f")
ax2.grid(False)

for row in agg_duration.itertuples():
    ax2.annotate(f"{int(row.total)}",
                 (row.duration_weeks, row.total),
                 textcoords="offset points", xytext=(8, -4),
                 ha="left", va="center", fontsize=9,
                 color="#00838f", fontweight="bold")

ax2.set_ylim(0, agg_duration["total"].max() * 1.35)

ax1.set_title("Завершаемость и объём записей по длительности курса\n"
              "(размер круга = кол-во записей, цвет = средняя оценка)",
              fontsize=12, fontweight="bold", color="#1a237e")

ax2.legend(loc="upper right", fontsize=9)

plt.tight_layout()
plt.show()
