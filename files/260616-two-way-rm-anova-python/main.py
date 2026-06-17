import pandas as pd
import pingouin as pg
from scipy import stats

# read csv (wide format) and reshape to long format
df = pd.read_csv("data.csv")
conditions = df.columns[1:].tolist()
subject_col = df.columns[0]
df_long = df.melt(id_vars=[subject_col], var_name='Condition', value_name='value')
factor_cols = [f'Factor{chr(65+i)}' for i in range(len(conditions[0].split('_')))]
for i, col in enumerate(factor_cols):
    df_long[col] = df_long['Condition'].str.split('_').str[i]

# Normality Test Start
print("=== Normality Test ===")
for cond in conditions:
    stat, p_value = stats.shapiro(df[cond])
    print(f"ExpCond: {cond} \nStatistic: {stat:.4f}, P-value: {p_value:.4f}")
    if p_value > 0.05:
        print("Data is normally distributed (fail to reject H0).\n")
    else:
        print("Data is not normally distributed (reject H0).\n")

# Sphericity Check Start
print("=== Sphericity Check ===")
aov = pg.rm_anova(data=df_long, dv='value', within=factor_cols, subject=subject_col, detailed=True)
n_subjects = df_long[subject_col].nunique()

use_cols = {}
p_reports = {}

for idx, row in aov.iterrows():
    source = row['Source']
    F_val = row['F']
    df_num = int(row['ddof1'])
    df_denom = int(row['ddof2'])
    eps = row['eps']
    p_unc_val = row['p_unc']
    p_GG_val = row['p_GG_corr']
    eps_HF = min((n_subjects * df_num * eps - 2) / (df_num * (n_subjects - 1 - df_num * eps)), 1.0)
    p_HF_val = stats.f.sf(F_val, df_num * eps_HF, df_denom * eps_HF)
    aov.at[idx, 'p_HF_corr'] = p_HF_val

    if df_num == 1:
        print(f"[{source}] sphericity automatically satisfied (df = 1) -> use p_unc")
        use_cols[source] = 'p_unc'
        p_reports[source] = p_unc_val
    else:
        within = factor_cols if '*' in source else source
        spher_result = pg.sphericity(data=df_long, dv='value', within=within, subject=subject_col)
        W, p_spher = spher_result.W, spher_result.pval
        if p_spher > 0.05:
            use_cols[source] = 'p_unc'
            p_reports[source] = p_unc_val
        elif eps < 0.75:
            use_cols[source] = 'p_GG_corr'
            p_reports[source] = p_GG_val
        else:
            use_cols[source] = 'p_HF_corr'
            p_reports[source] = p_HF_val
        p_cond = 'p-sphericity > 0.05' if p_spher > 0.05 else 'p-sphericity ≤ 0.05'
        eps_cond = 'ε ≥ 0.75' if eps >= 0.75 else 'ε < 0.75'
        print(f"[{source}] Sphericity (Mauchly's): W = {W:.2f}, p-sphericity = {p_spher:.3f}, ε = {eps:.3f}")
        print(f"{p_cond} & {eps_cond} -> use {use_cols[source]}")

# Two-way RM ANOVA Start
print("\n=== Two-way RM ANOVA ===")
print(aov[['Source', 'ddof1', 'ddof2', 'F', 'p_unc', 'p_GG_corr', 'p_HF_corr']].to_string(index=False))
print("\n→ p-value to report:")
for source, col in use_cols.items():
    print(f"  [{source}] {p_reports[source]:.6f} ({col})")

# Post-hoc Analysis Start
print("\n=== Post-hoc Analysis (paired t-test with Bonferroni correction) ===")

# 1) when interaction effect is NOT significant:
#    average over the other factor and compare main effects (1+3=4 comparisons)
print("\n=== Case 1: Interaction NOT significant: main effects post-hoc ===")
print(f"\nPost-hoc {factor_cols[0]}:")
ph_a = pg.pairwise_tests(data=df_long, dv='value', within=factor_cols[0], subject=subject_col, padjust='bonferroni')
print(ph_a[['A', 'B', 'T', 'dof', 'p_unc']].to_string(index=False, formatters={'T': '{:.4f}'.format, 'dof': '{:.0f}'.format, 'p_unc': '{:.6f}'.format}))

print(f"\nPost-hoc {factor_cols[1]} (Bonferroni):")
ph_b = pg.pairwise_tests(data=df_long, dv='value', within=factor_cols[1], subject=subject_col, padjust='bonferroni')
print(ph_b[['A', 'B', 'T', 'dof', 'p_unc', 'p_corr']].to_string(index=False, formatters={'T': '{:.4f}'.format, 'dof': '{:.0f}'.format, 'p_unc': '{:.6f}'.format, 'p_corr': '{:.6f}'.format}))

# 2) when interaction effect IS significant:
#    can't average out; one factor's effect depends on the level of the other.
#    fix one factor's level and compare the other (simple effects, 3+6=9 comparisons)
print("\n=== Case 2: Interaction IS significant — simple effects ===")

# FactorA within each FactorB level (1 comparison each, Bonferroni not needed per group)
print(f"\nSimple effects: {factor_cols[0]} within each {factor_cols[1]} level:")
for b in sorted(df_long[factor_cols[1]].unique()):
    subset = df_long[df_long[factor_cols[1]] == b]
    ph = pg.pairwise_tests(data=subset, dv='value', within=factor_cols[0], subject=subject_col, padjust='bonferroni')
    print(f"  {factor_cols[1]} = {b}:")
    print(ph[['A', 'B', 'T', 'dof', 'p_unc']].to_string(index=False, formatters={'T': '{:.4f}'.format, 'dof': '{:.0f}'.format, 'p_unc': '{:.6f}'.format}))

# FactorB within each FactorA level (3 comparisons each, Bonferroni x3 per group)
print(f"\nSimple effects: {factor_cols[1]} within each {factor_cols[0]} level (Bonferroni):")
for a in sorted(df_long[factor_cols[0]].unique()):
    subset = df_long[df_long[factor_cols[0]] == a]
    ph = pg.pairwise_tests(data=subset, dv='value', within=factor_cols[1], subject=subject_col, padjust='bonferroni')
    print(f"  {factor_cols[0]} = {a}:")
    print(ph[['A', 'B', 'T', 'dof', 'p_unc', 'p_corr']].to_string(index=False, formatters={'T': '{:.4f}'.format, 'dof': '{:.0f}'.format, 'p_unc': '{:.6f}'.format, 'p_corr': '{:.6f}'.format}))
