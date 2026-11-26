# тема: Анализ завершаемости онлайн-курсов на платформе обучеия

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="white", palette="Blues")

# 1. Загрузка данных
df_enrollments = pd.read_csv("enrollments.csv", encoding="utf-8-sig")

print("Загрузка данных:")
print(f"  Записей: {len(df_enrollments)}")

# преобразование дат
df_enrollments["start_date"] = pd.to_datetime(df_enrollments["start_date"])

# Очистка дубликатов
df_enrollments = df_enrollments.drop_duplicates()

# оставляем только completed и dropped
df_fin = df_enrollments[df_enrollments["status"].isin(["completed", "dropped"])].copy()
print(f"\nПосле фильтра (completed + dropped): {len(df_fin)} записей")

# расчёт KPI
n_total = len(df_fin)
n_completed = len(df_fin[df_fin["status"] == "completed"])
n_dropped = len(df_fin[df_fin["status"] == "dropped"])
completion_rate = n_completed / n_total * 100
avg_score = df_fin["final_score"].mean()
n_students = len(df_fin["student_id"].unique())
n_courses = len(df_fin["course_id"].unique())

print("\n--- KPI-показатели ---")
print(f"  Общая завершаемость:  {completion_rate:.1f}%")
print(f"  Средняя оценка:       {avg_score:.2f} / 5.0")
print(f"  Уникальных студентов: {n_students}")
print(f"  Уникальных курсов:    {n_courses}")
print(f"  Брошено курсов:       {n_dropped}")

# KPI-карточки
fig, axes = plt.subplots(1, 4, figsize=(16, 4), dpi=100)

kpis = [
    {
        'title': 'ЗАВЕРШАЕМОСТЬ',
        'value': f'{completion_rate:.1f}%',
        'subtitle': f'{n_completed} из {n_total} курсов',
        'fg': '#1a237e',
        'bg': '#f5f5f5',
    },
    {
        'title': 'СРЕДНЯЯ ОЦЕНКА',
        'value': f'{avg_score:.2f}',
        'subtitle': 'по 5-балльной шкале',
        'fg': '#00838f',
        'bg': '#f5f5f5',
    },
    {
        'title': 'УНИКАЛЬНЫХ СТУДЕНТОВ',
        'value': f'{n_students:,}',
        'subtitle': f'на {n_courses} курсах',
        'fg': '#3949ab',
        'bg': '#f5f5f5',
    },
    {
        'title': 'БРОШЕНО КУРСОВ',
        'value': f'{n_dropped:,}',
        'subtitle': f'отток {100 - completion_rate:.1f}%',
        'fg': '#c62828',
        'bg': '#f5f5f5',
    },
]

for i, kpi in enumerate(kpis):
    ax = axes[i]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)


    ax.text(0.5, 0.5, '', ha='center', va='center',
            bbox=dict(boxstyle="round,pad=0.9", fc=kpi['bg'],
                      ec=kpi['fg'], lw=2.5), fontsize=1)

    ax.text(0.5, 0.80, kpi['title'], ha='center', va='center',
            fontsize=11, fontweight='bold', color='#1a237e')

    ax.text(0.5, 0.48, kpi['value'], ha='center', va='center',
            fontsize=26, fontweight='bold', color=kpi['fg'])

    ax.text(0.5, 0.18, kpi['subtitle'], ha='center', va='center',
            fontsize=10, color='#9e9e9e')

    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

fig.suptitle('Ключевые показатели эффективности (KPI) онлайн платформы для обучения',
             fontsize=14, fontweight='bold', color='#1a237e')
plt.tight_layout()
plt.show()


