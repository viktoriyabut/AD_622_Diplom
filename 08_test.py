import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="white", palette="Blues")

df = pd.read_csv("enrollments_full.csv", encoding="utf-8-sig")
df["start_date"] = pd.to_datetime(df["start_date"])
df = df.drop_duplicates()

df_fin = df[df["status"].isin(["completed", "dropped"])].copy()
df_fin["is_completed"] = (df_fin["status"] == "completed").astype(int)
df_fin["is_paid"] = (df_fin["price"] > 0).astype(int)

paid = df_fin[df_fin["is_paid"] == 1]
free = df_fin[df_fin["is_paid"] == 0]

n_paid = len(paid)
n_free = len(free)
x_paid = paid["is_completed"].sum()
x_free = free["is_completed"].sum()

p_paid = x_paid / n_paid
p_free = x_free / n_free

p_pooled = (x_paid + x_free) / (n_paid + n_free)

se = np.sqrt(p_pooled * (1 - p_pooled) * (1 / n_paid + 1 / n_free))

# Z-статистика
z_stat = (p_paid - p_free) / se

p_value = 2 * (1 - 0.5 * (1 + math.erf(abs(z_stat) / np.sqrt(2))))

alpha = 0.05

print("--- Результаты Z-теста для долей (платные vs бесплатные) ---")
print(f"Платные курсы:    {x_paid} завершено из {n_paid} -> {p_paid * 100:.1f}%")
print(f"Бесплатные курсы: {x_free} завершено из {n_free} -> {p_free * 100:.1f}%")
print(f"Объединённая доля (p_pooled): {p_pooled:.4f}")
print(f"Стандартная ошибка (SE):      {se:.4f}")
print(f"Z-статистика:                 {z_stat:.4f}")
print(f"P-value:                      {p_value:.6f}")
print(f"Уровень значимости (alpha):   {alpha}")

print("\n--- Вывод ---")
if p_value < alpha:
    print(f"P-value ({p_value:.6f}) < alpha ({alpha})")
    print("ОТКЛОНЯЕМ H0. Различие в завершаемости платных и бесплатных")
    print("курсов СТАТИСТИЧЕСКИ ЗНАЧИМО.")
    if p_paid > p_free:
        print(f"Платные курсы завершают чаще ({p_paid * 100:.1f}% > {p_free * 100:.1f}%).")
    else:
        print(f"Бесплатные курсы завершают чаще ({p_free * 100:.1f}% > {p_paid * 100:.1f}%).")
else:
    print(f"P-value ({p_value:.6f}) >= alpha ({alpha})")
    print("НЕ ОТКЛОНЯЕМ H0. Различие в завершаемости платных и бесплатных")
    print("курсов НЕ является статистически значимым.")

ci_paid = 1.96 * np.sqrt(p_paid * (1 - p_paid) / n_paid)
ci_free = 1.96 * np.sqrt(p_free * (1 - p_free) / n_free)

fig, ax = plt.subplots(figsize=(8, 6), dpi=100)

groups = ["Платные\nкурсы", "Бесплатные\nкурсы"]
rates = [p_paid * 100, p_free * 100]
errors = [ci_paid * 100, ci_free * 100]

colors = ["#1a237e", "#00838f"]

ax.bar(groups, rates, yerr=errors, color=colors,
       edgecolor="white", linewidth=1.5, width=0.5)

for i, (rate, err) in enumerate(zip(rates, errors)):
    ax.text(i, rate + err + 2.5, f"{rate:.1f}%",
            ha="center", va="bottom", fontsize=14,
            fontweight="bold", color=colors[i])

ax.set_ylabel("Доля завершаемости, %", fontsize=11, color="#1a237e")
ax.set_ylim(0, 110)
ax.set_title("Сравнение завершаемости платных и бесплатных курсов\n"
             "(Z-тест для долей, 95% доверительные интервалы)",
             fontsize=12, fontweight="bold", color="#1a237e")

ax.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.show()

fig, ax = plt.subplots(figsize=(10, 6), dpi=100)

x = np.linspace(-4, 4, 500)
y = (1 / np.sqrt(2 * np.pi)) * np.exp(-x ** 2 / 2)
ax.plot(x, y, color="#1a237e", linewidth=2.5,
        label="Стандартное нормальное N(0,1)")

z_critical = 1.96
ax.fill_between(x, y, where=(x >= z_critical), color="#c62828",
                alpha=0.5, label="Критическая зона (α=0.05)")
ax.fill_between(x, y, where=(x <= -z_critical), color="#c62828", alpha=0.5)

ax.axvline(z_stat, color="#c62828", linestyle="--", linewidth=2,
           label=f"Z-статистика = {z_stat:.2f}")

ax.axvline(z_critical, color="#00838f", linestyle=":", linewidth=2,
           label=f"Z критическое = ±{z_critical}")
ax.axvline(-z_critical, color="#00838f", linestyle=":", linewidth=2)

ax.set_title("Z-тест: позиция статистики на кривой нормального распределения",
             fontsize=12, fontweight="bold", color="#1a237e")
ax.set_xlabel("Z-значение")
ax.set_ylabel("Плотность вероятности")
ax.legend(loc="upper right", fontsize=10)
ax.grid(linestyle="--", alpha=0.3)
plt.tight_layout()
plt.show()