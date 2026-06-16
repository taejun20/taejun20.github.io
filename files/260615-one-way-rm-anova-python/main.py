import pandas as pd
from statsmodels.stats.anova import AnovaRM
import pingouin as pg
from scipy import stats

# read csv (wide format) and reshape to long format
df = pd.read_csv("data.csv")
conditions = df.columns[1:].tolist()
df = df.melt(id_vars=[df.columns[0]], var_name='ExpCond', value_name='value')

# Perform normality test for each condition
print("=== Normality Test ===")
for cond in conditions:
    samples = df[df['ExpCond'] == cond]['value']
    stat, p_value = stats.shapiro(samples)
    print(f"ExpCond: {cond} \nStatistic: {stat:.4f}, P-value: {p_value:.4f}")
    if p_value > 0.05:
        print("Data is normally distributed (fail to reject H0).\n")
    else:
        print("Data is not normally distributed (reject H0).\n")

print("=== One-way RM ANOVA ===")
# perform RM-ANOVA: statsmodels AnovaRM
testingMeasure = 'value'
anovaRM = AnovaRM(data=df, depvar=testingMeasure, subject='Participant', within=['ExpCond'])
res = anovaRM.fit()
print(res.anova_table.to_string(formatters={'Pr > F': '{:.6f}'.format}))

print("\n=== Post-hoc Analysis (paired t-test with Bonferroni correction) ===")
# post-hoc: pairwise t-test with Bonferroni correction
pairwise_results = pg.pairwise_tests(dv=testingMeasure, within='ExpCond', subject='Participant', data=df, padjust='bonferroni')
print(pairwise_results[['A', 'B', 'T', 'dof', 'p_unc', 'p_corr']].to_string(index=False, formatters={'T': '{:.4f}'.format, 'dof': '{:.0f}'.format, 'p_unc': '{:.6f}'.format, 'p_corr': '{:.6f}'.format}))
