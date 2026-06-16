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

# 1) when interaction effect is NOT significant:
#    average over the other factor and compare main effects (1+3=4 comparisons)
print("\n=== Case 1: Interaction NOT significant — main effects post-hoc ===")
print("\nPost-hoc FactorA:")
ph_a = pg.pairwise_tests(data=df_long, dv='value', within='FactorA', subject=subject_col, padjust='bonferroni')
print(ph_a[['A', 'B', 'T', 'dof', 'p_unc']].to_string(index=False, formatters={'T': '{:.4f}'.format, 'dof': '{:.0f}'.format, 'p_unc': '{:.6f}'.format}))

print("\nPost-hoc FactorB (Bonferroni):")
ph_b = pg.pairwise_tests(data=df_long, dv='value', within='FactorB', subject=subject_col, padjust='bonferroni')
print(ph_b[['A', 'B', 'T', 'dof', 'p_unc', 'p_corr']].to_string(index=False, formatters={'T': '{:.4f}'.format, 'dof': '{:.0f}'.format, 'p_unc': '{:.6f}'.format, 'p_corr': '{:.6f}'.format}))

# 2) when interaction effect IS significant:
#    can't average out — one factor's effect depends on the level of the other.
#    fix one factor's level and compare the other (simple effects, 3+6=9 comparisons)
print("\n=== Case 2: Interaction IS significant — simple effects ===")

# FactorA within each FactorB level (1 comparison each, Bonferroni not needed per group)
print("\nSimple effects: FactorA within each FactorB level:")
for b in sorted(df_long['FactorB'].unique()):
    subset = df_long[df_long['FactorB'] == b]
    ph = pg.pairwise_tests(data=subset, dv='value', within='FactorA', subject=subject_col, padjust='bonferroni')
    print(f"  FactorB = {b}:")
    print(ph[['A', 'B', 'T', 'dof', 'p_unc']].to_string(index=False, formatters={'T': '{:.4f}'.format, 'dof': '{:.0f}'.format, 'p_unc': '{:.6f}'.format}))

# FactorB within each FactorA level (3 comparisons each, Bonferroni x3 per group)
print("\nSimple effects: FactorB within each FactorA level (Bonferroni):")
for a in sorted(df_long['FactorA'].unique()):
    subset = df_long[df_long['FactorA'] == a]
    ph = pg.pairwise_tests(data=subset, dv='value', within='FactorB', subject=subject_col, padjust='bonferroni')
    print(f"  FactorA = {a}:")
    print(ph[['A', 'B', 'T', 'dof', 'p_unc', 'p_corr']].to_string(index=False, formatters={'T': '{:.4f}'.format, 'dof': '{:.0f}'.format, 'p_unc': '{:.6f}'.format, 'p_corr': '{:.6f}'.format}))
