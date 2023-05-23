from plotters import bmi_strata_plot, bmi_per_quantile, prs_distribution, prevalence_per_quantile, scatter_anc
import pandas as pd
df = pd.read_csv("/home/agenor/genera/resultados_prs.csv")
#bmi_strata_plot(df)
#bmi_per_quantile(df)
#prs_distribution(df)
#prevalence_per_quantile(bmi_strata_plot(df))
scatter_anc(df, "AsiaV3")
