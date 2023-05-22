import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import os
import seaborn as sns

def bmi_strata_plot(prs_df):
    
    bins_imc = [0, 30, np.inf]
    cat = ["Normal", "Obesidade"]

    prs_df["imc_cat"] = pd.cut(prs_df["imc"], bins=bins_imc, labels=cat)
    prs_df["prs_quantile"] = pd.qcut(prs_df["prs"], q=[0, 0.10, 0.20, 0.40, 0.60, 0.80, 0.90, 0.95, 0.99, 1.0], labels= ["(0, 0.1]", "(0.1, 0.2]", "(0.2, 0.4]", "(0.4, 0.6]", "(0.6, 0.8]",
                                                        "(0.8, 0.9]", "(0.9, 0.95]", "(0.95, 0.99]", "(0.99, 1.0]"])
    
    fig = px.strip(prs_df, x="prs_quantile", y="imc", color="imc_cat", stripmode="overlay",  category_orders={"prs_quantile": ["(0, 0.1]", "(0.1, 0.2]", "(0.2, 0.4]", "(0.4, 0.6]", "(0.6, 0.8]",
                                                        "(0.8, 0.9]", "(0.9, 0.95]", "(0.95, 0.99]", "(0.99, 1.0]"]})

    fig.update_xaxes(tickangle=45)

    if not os.path.exists("prs_plots"):
        os.mkdir("prs_plots")


    fig.write_html("prs_plots/strata_plot.html")

def bmi_per_quantile(prs_df):
    #Separando os dados em 20 quantis
    labels = [f"{n}" for n in range(1, 21)]

    prs_df_q20 = prs_df

    prs_df_q20["prs_quantile"] = pd.qcut(prs_df_q20["prs"], q=20, labels=labels)

    fig = sns.boxplot(data=prs_df_q20, x="prs_quantile", y="imc")

    fig.figure.savefig("prs_plots/prs_q20_plot.png")

def prs_distribution(prs_df):
    fig = sns.kdeplot(data=prs_df["prs"])

    fig.figure.savefig("prs_plots/prs_distribution.png")

def prevalence_per_quantile(prs_df):
    prev_df = prs_df.groupby(["prs_quantile", "imc_cat"]).size() / prs_df.groupby(["prs_quantile"]).size()

    fig = plt.subplots(figsize=(10, 5))

    ax = sns.lineplot(prev_df.loc[:, "Obesidade"], marker=".", markersize=15, color="black")

    ax.figure.savefig("prs_plots/prevalence_per_quantile.png")



#Gráficos que faltam
# Ancestralidade (barplot)
# Correlação entre ancestralidade e PRS
# Variância explicada
prs_df = pd.read_csv(dataframe)