import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette="Blues")

df = pd.read_csv("enrollments_full_v2.csv", encoding="utf-8-sig")
df["start_date"] = pd.to_datetime(df["start_date"])
df = df.drop_duplicates()

df_fin = df[df["status"].isin(["completed", "dropped"])].copy()
df_fin["is_completed"] = (df_fin["status"] == "completed").astype(int)

labels = {
    "age": "Возраст",
    "duration_weeks": "Длительность",
    "price": "Цена",
    "progress_pct": "Прогресс",
    "final_score": "Оценка",
    "is_completed": "Завершено",
    "format": "Формат",
}

corr_cols = ["age", "duration_weeks", "price", "progress_pct",
             "final_score", "is_completed"]
corr_matrix = df_fin[corr_cols].corr()
corr_matrix.index = [labels[c] for c in corr_matrix.index]
corr_matrix.columns = [labels[c] for c in corr_matrix.columns]

print("--- Матрица корреляций факторов ---")
print(corr_matrix.round(2))

# Heatmap
fig, ax = plt.subplots(figsize=(8, 6), dpi=100)
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="Blues",
            linewidths=0.5, cbar_kws={"label": "Коэффициент корреляции"})
ax.set_title("Корреляция факторов (тепловая карта)",
             fontsize=13, fontweight="bold", color="#1a237e")
plt.tight_layout()
plt.show()

