import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="white")

df_enrollments = pd.read_csv("enrollments.csv", encoding="utf-8-sig")
df_enrollments["start_date"] = pd.to_datetime(df_enrollments["start_date"])
df_enrollments = df_enrollments.drop_duplicates()

total_records = len(df_enrollments)
status_counts = df_enrollments["status"].value_counts()

n_completed = int(status_counts.get("completed", 0))
n_dropped = int(status_counts.get("dropped", 0))
n_in_progress = int(status_counts.get("in_progress", 0))
clean_records = n_completed + n_dropped

print(f"Общее число записей:           {total_records}")
print(f"В процессе обучения:           {n_in_progress}")
print(f"Завершено курсов:              {n_completed}")
print(f"Брошено курсов:                {n_dropped}")
print(f"Анализируемая выборка:         {clean_records}")
print(f"Доля выборки от всех записей:  {clean_records / total_records * 100:.1f}%")

# Круговая диаграмма
fig, ax = plt.subplots(figsize=(9, 7), dpi=100)

labels = [
    f"Завершено (completed) — {n_completed:,}",
    f"Брошено (dropped) — {n_dropped:,}",
    f"В процессе (in_progress) — {n_in_progress:,}",
]
sizes = [n_completed, n_dropped, n_in_progress]
colors = ['#00838f', '#c62828', '#9e9e9e']

explode = [0.06, 0.06, 0.0]

ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
       explode=explode, startangle=90)

ax.set_title(
    "Структура записей по статусам обучения\n"
    f"и доля анализируемой выборки после очистки данных "
    f"({clean_records:,} из {total_records:,} = "
    f"{clean_records / total_records * 100:.1f}%)",
    fontsize=13, fontweight='bold', color='#1a237e', pad=18
)

ax.axis('equal')

plt.tight_layout()
plt.show()