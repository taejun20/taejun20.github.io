import pandas as pd
import pingouin as pg
from scipy import stats

# read csv (wide format) and reshape to long format
df = pd.read_csv("data.csv")
conditions = df.columns[1:].tolist()
subject_col = df.columns[0]
df = df.melt(id_vars=[subject_col], var_name='ExpCond', value_name='value')

# Normality Test Start
print("=== Normality Test ===")
for cond in conditions:
    samples = df[df['ExpCond'] == cond]['value']
    stat, p_value = stats.shapiro(samples)
    print(f"ExpCond: {cond} \nStatistic: {stat:.4f}, P-value: {p_value:.4f}")
    if p_value > 0.05:
        print("Data is normally distributed (fail to reject H0).\n")
    else:
        print("Data is not normally distributed (reject H0).\n")

# Sphericity Check Start
print("=== Sphericity Check ===")
aov = pg.rm_anova(data=df, dv='value', within='ExpCond', subject=subject_col, detailed=True)
F_val = aov['F'].values[0]
df_num = int(aov['DF'].values[0])
n_subjects = df[subject_col].nunique()
df_denom = (n_subjects - 1) * df_num
eps = aov['eps'].values[0]
p_unc = aov['p_unc'].values[0]
p_GG = stats.f.sf(F_val, df_num * eps, df_denom * eps)
eps_HF = min((n_subjects * df_num * eps - 2) / (df_num * (n_subjects - 1 - df_num * eps)), 1.0)
p_HF = stats.f.sf(F_val, df_num * eps_HF, df_denom * eps_HF)

if len(conditions) <= 2:
    print("Sphericity: automatically satisfied (only 2 levels)")
    p_report, use_col = p_unc, 'p-unc'
else:
    spher_result = pg.sphericity(data=df, dv='value', within='ExpCond', subject=subject_col)
    W, p_spher = spher_result.W, spher_result.pval
    if p_spher > 0.05:
        p_report, use_col = p_unc, 'p-unc'
    elif eps < 0.75:
        p_report, use_col = p_GG, 'p-GG-corr'
    else:
        p_report, use_col = p_HF, 'p-HF-corr'
    p_cond = 'p-sphericity > 0.05' if p_spher > 0.05 else 'p-sphericity ≤ 0.05'
    eps_cond = 'ε ≥ 0.75' if eps >= 0.75 else 'ε < 0.75'
    print(f"Sphericity (Mauchly's): W = {W:.2f}, p-sphericity = {p_spher:.3f}, ε = {eps:.3f}\n{p_cond} & {eps_cond} -> use {use_col}")

# One-way RM ANOVA Start
print("\n=== One-way RM ANOVA ===")
aov_effect = aov.iloc[[0]].copy()
aov_effect['df_denom'] = df_denom
aov_effect['p-GG-corr'] = p_GG
aov_effect['p-HF-corr'] = p_HF
p_col = 'p_unc' if use_col == 'p-unc' else use_col
print(aov_effect[['Source', 'DF', 'df_denom', 'F', p_col]].to_string(index=False, formatters={'F': '{:.6f}'.format, p_col: '{:.6f}'.format}))
print(f"\n→ p-value to report: {p_report:.6f} ({use_col})")

# Post-hoc Analysis Start
print("\n=== Post-hoc Analysis (paired t-test with Bonferroni correction) ===")
pairwise_results = pg.pairwise_tests(dv='value', within='ExpCond', subject=subject_col, data=df, padjust='bonferroni')
print(pairwise_results[['A', 'B', 'T', 'dof', 'p_unc', 'p_corr']].to_string(index=False, formatters={'T': '{:.4f}'.format, 'dof': '{:.0f}'.format, 'p_unc': '{:.6f}'.format, 'p_corr': '{:.6f}'.format}))
