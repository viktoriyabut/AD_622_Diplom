import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="white")

# Загрузка данных
df_students = pd.read_csv("students.csv", encoding="utf-8-sig")
df_students["reg_date"] = pd.to_datetime(df_students["reg_date"])
df_students = df_students.drop_duplicates()

total_students = len(df_students)
source_counts = df_students["source"].value_counts()

print("--- Структура студентов по источникам привлечения ---")
print(source_counts)
print(f"\nВсего студентов: {total_students}")

# Круговая диаграмма
fig, ax = plt.subplots(figsize=(9, 7), dpi=100)

colors = ['#1a237e', '#00838f', '#3949ab']

ax.pie(source_counts.values,
       labels=source_counts.index,
       colors=colors,
       autopct='%1.1f%%',
       startangle=140)

ax.set_title('Структура студентов по источникам привлечения',
             fontsize=13, fontweight='bold', color='#1a237e')

ax.axis('equal')

plt.tight_layout()
plt.show()