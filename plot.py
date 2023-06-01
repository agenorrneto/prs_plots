from plotters import bmi_strata_plot, bmi_per_quantile, prs_distribution, prevalence_per_quantile, scatter_anc, z_score_dis
import pandas as pd
df = pd.read_csv("/home/agenor/genera/resultados_prs.csv")
bmi_strata_plot(df, avg=True, anc_cat="EuropaV3", anc=True)
#bmi_per_quantile(df, 10)
#prs_distribution(df, avg=True)
#prevalence_per_quantile(df , q=10, anc_cat="EuropaV3", anc=True, avg=True)
#scatter_anc(df, "EuropaV3")
#z_score_dis(df)
