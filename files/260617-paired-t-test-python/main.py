import pandas as pd
import pingouin as pg
from scipy import stats

df = pd.read_csv("data.csv")
conditions = df.columns[1:].tolist()

# Normality Test Start
print("=== Normality Test ===")
for cond in conditions:
    stat, p_value = stats.shapiro(df[cond])
    print(f"ExpCond: {cond} \nStatistic: {stat:.4f}, P-value: {p_value:.4f}")
    if p_value > 0.05:
        print("Data is normally distributed (fail to reject H0).\n")
    else:
        print("Data is not normally distributed (reject H0).\n")

# Paired T-Test Start
print("=== Paired T-Test ===")
result = pg.ttest(df[conditions[0]], df[conditions[1]], paired=True)
print(result[['T', 'dof', 'p_val', 'cohen_d']].to_string(index=False, formatters={'T': '{:.4f}'.format, 'dof': '{:.0f}'.format, 'p_val': '{:.6f}'.format, 'cohen_d': '{:.4f}'.format}))
