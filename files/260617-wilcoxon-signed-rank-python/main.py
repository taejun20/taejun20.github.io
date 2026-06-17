import pandas as pd
from scipy.stats import shapiro, wilcoxon

df = pd.read_csv("data.csv")
conditions = df.columns[1:].tolist()

# Normality Test Start
print("=== Normality Test ===")
for cond in conditions:
    stat, p_value = shapiro(df[cond])
    print(f"ExpCond: {cond} \nStatistic: {stat:.4f}, P-value: {p_value:.4f}")
    if p_value > 0.05:
        print("Data is normally distributed (fail to reject H0).\n")
    else:
        print("Data is not normally distributed (reject H0).\n")

# Wilcoxon Signed-Rank Test Start
print("=== Wilcoxon Signed-Rank Test ===")
result = wilcoxon(df[conditions[0]], df[conditions[1]], method='approx')
print(f"Z = {result.zstatistic:.4f}, P-value = {result.pvalue:.6f}")
