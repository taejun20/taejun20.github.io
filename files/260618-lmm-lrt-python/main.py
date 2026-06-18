import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats

df = pd.read_csv("data.csv")
conditions = df.columns[1:].tolist()
subject_col = df.columns[0]
df_long = df.melt(id_vars=[subject_col], var_name='Condition', value_name='value')

all_components = sorted(set(comp for cond in conditions for comp in cond.split('+')))
varying_components = [c for c in all_components if not all(c in cond.split('+') for cond in conditions)]
for comp in all_components:
    df_long[comp] = df_long['Condition'].apply(lambda x: 1 if comp in x.split('+') else 0)

# LMM + LRT Start
print("=== LMM + LRT ===")
full_model = smf.mixedlm("value ~ " + " + ".join(varying_components), data=df_long, groups=df_long[subject_col]).fit(reml=False)
for comp in varying_components:
    others = [c for c in varying_components if c != comp]
    reduced_model = smf.mixedlm("value ~ " + " + ".join(others), data=df_long, groups=df_long[subject_col]).fit(reml=False)
    chi2 = 2 * (full_model.llf - reduced_model.llf)
    p = stats.chi2.sf(chi2, df=1)
    print(f"Component {comp}: χ²(1) = {chi2:.2f}, p = {p:.4f}")
