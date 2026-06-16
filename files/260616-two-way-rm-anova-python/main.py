import pandas as pd
import pingouin as pg
from scipy import stats

# read csv (wide format) and reshape to long format
df = pd.read_csv("data.csv")
conditions = df.columns[1:].tolist()
subject_col = df.columns[0]
df_long = df.melt(id_vars=[subject_col], var_name='Condition', value_name='value')
df_long['FactorA'] = df_long['Condition'].str[:2]
df_long['FactorB'] = df_long['Condition'].str[2:]

# Perform normality test for each condition
for cond in conditions:
    stat, p_value = stats.shapiro(df[cond])
    print(f"ExpCond: {cond} \nStatistic: {stat:.4f}, P-value: {p_value:.4f}")
    if p_value > 0.05:
        print("Data is normally distributed (fail to reject H0).\n")
    else:
        print("Data is not normally distributed (reject H0).\n")

# perform two-way RM ANOVA
aov = pg.rm_anova(data=df_long, dv='value', within=['FactorA', 'FactorB'], subject=subject_col, detailed=True)
print(aov[['Source', 'ddof1', 'ddof2', 'F', 'p_unc']].to_string(index=False))

# post-hoc: pairwise t-test with Bonferroni correction
print("\nPost-hoc FactorA:")
ph_a = pg.pairwise_tests(data=df_long, dv='value', within='FactorA', subject=subject_col, padjust='bonferroni')
pg.print_table(ph_a[['A', 'B', 'T', 'dof', 'p_unc']])

print("\nPost-hoc FactorB (Bonferroni):")
ph_b = pg.pairwise_tests(data=df_long, dv='value', within='FactorB', subject=subject_col, padjust='bonferroni')
pg.print_table(ph_b[['A', 'B', 'T', 'dof', 'p_unc', 'p_corr']])
