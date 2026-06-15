import pandas as pd
from statsmodels.stats.anova import AnovaRM
import pingouin as pg
from scipy import stats

# read csv (wide format) and reshape to long format
df = pd.read_csv("data.csv")
df = df.melt(id_vars=['Participant'], var_name='ExpCond', value_name='value')

# define conditions
conditions = ["Condition A", "Condition B", "Condition C"]

# Perform normality test for each condition
for cond in conditions:
    samples = df[df['ExpCond'] == cond]['value']
    stat, p_value = stats.shapiro(samples)
    print(f"ExpCond: {cond} \nStatistic: {stat:.4f}, P-value: {p_value:.4f}")
    if p_value > 0.05:
        print("Data is normally distributed (fail to reject H0).\n")
    else:
        print("Data is not normally distributed (reject H0).\n")

# perform RM-ANOVA: statsmodels AnovaRM
testingMeasure = 'value'
anovaRM = AnovaRM(data=df, depvar=testingMeasure, subject='Participant', within=['ExpCond'])
res = anovaRM.fit()
print(res)

# post-hoc: pairwise t-test with Bonferroni correction
pairwise_results = pg.pairwise_ttests(dv=testingMeasure, within='ExpCond', subject='Participant', data=df, padjust='bonferroni')
pg.print_table(pairwise_results)
