import pandas as pd
from itertools import combinations
from scipy.stats import shapiro, friedmanchisquare, wilcoxon
from statsmodels.stats.multitest import multipletests

# read csv (wide format)
df = pd.read_csv("data.csv")
conditions = df.columns[1:].tolist()

# Perform normality test for each condition
print("=== Normality Test ===")
for cond in conditions:
    stat, p_value = shapiro(df[cond].values)
    print(f"ExpCond: {cond} \nStatistic: {stat:.4f}, P-value: {p_value:.4f}")
    if p_value > 0.05:
        print("Data is normally distributed (fail to reject H0).\n")
    else:
        print("Data is not normally distributed (reject H0).\n")

print("=== Friedman Test ===")
# perform Friedman test
stat, p_value = friedmanchisquare(*[df[cond].values for cond in conditions])
df_val = len(conditions) - 1
print(f"Friedman Test \ndf: {df_val}, Statistic (chi-square): {stat:.4f}, P-value: {p_value:.6f}")
if p_value < 0.05:
    print("There is a statistically significant difference between conditions.")
else:
    print("No statistically significant difference between conditions.")

print("\n=== Post-hoc Analysis (Wilcoxon signed-rank test with Bonferroni correction) ===")
# post-hoc: Wilcoxon signed-rank test with Bonferroni correction
pairwise_p = []
pairwise_z = []
comparisons = list(combinations(range(len(conditions)), 2))

for i, j in comparisons:
    res = wilcoxon(df[conditions[i]].values, df[conditions[j]].values, method='approx')
    pairwise_p.append(res.pvalue)
    pairwise_z.append(res.zstatistic)

corrected_pvals = multipletests(pairwise_p, method='bonferroni')[1]

for (i, j), z, p_val in zip(comparisons, pairwise_z, corrected_pvals):
    print(f"{conditions[i]} vs {conditions[j]}: Z = {z:.4f}, Adjusted P-value = {p_val:.6f}")
