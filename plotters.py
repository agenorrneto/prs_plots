import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import os
import seaborn as sns
 

def bmi_strata_plot(prs_df):
    
    bins_imc = [0, 30, np.inf]
    cat = ["Normal", "Obesidade"]
    df_to_plot = prs_df.copy()
    df_to_plot["imc_cat"] = pd.cut(df_to_plot["imc"], bins=bins_imc, labels=cat)
    df_to_plot["prs_quantile"] = pd.qcut(df_to_plot["prs"], q=[0, 0.10, 0.20, 0.40, 0.60, 0.80, 0.90, 0.95, 0.99, 1.0], labels= ["(0, 0.1]", "(0.1, 0.2]", "(0.2, 0.4]", "(0.4, 0.6]", "(0.6, 0.8]",
                                                        "(0.8, 0.9]", "(0.9, 0.95]", "(0.95, 0.99]", "(0.99, 1.0]"])
    
    fig = px.strip(df_to_plot, x="prs_quantile", y="imc", color="imc_cat", stripmode="overlay",  
                   category_orders={"prs_quantile": ["(0, 0.1]", "(0.1, 0.2]", "(0.2, 0.4]", "(0.4, 0.6]", "(0.6, 0.8]",
                                                    "(0.8, 0.9]", "(0.9, 0.95]", "(0.95, 0.99]", "(0.99, 1.0]"]}, labels={"prs_quantile": "Quantis do PRS de IMC",
                            "imc": "IMC (kg/m²)"}, title="Gráfico estratificado de PRS vs IMC")

    fig.update_xaxes(tickangle=45)

    if not os.path.exists("prs_plots"):
        os.mkdir("prs_plots")


    fig.write_html("prs_plots/strata_plot_2.html")
    return df_to_plot

def bmi_per_quantile(prs_df):
    #Separando os dados em 20 quantis
    labels = [f"{n}" for n in range(1, 21)]

    prs_df_q20 = prs_df.copy()

    prs_df_q20["prs_quantile"] = pd.qcut(prs_df_q20["prs"], q=20, labels=labels)

    fig = sns.boxplot(data=prs_df_q20, x="prs_quantile", y="imc").set(title='Quantile Plot (Quantiles versus BMI)', xlabel='Quantiles for BMI PRS', ylabel='BMI (kg/m²)')

    plt.savefig("prs_plots/prs_q20_plot.png")

def prs_distribution(prs_df):
    fig_dis = sns.kdeplot(data=prs_df["prs"])

    fig_dis.figure.savefig("prs_plots/prs_distribution.png")

def prevalence_per_quantile(prs_df):
    #TODO: fazer por prevalência de obesidade severa
    prev_df = prs_df.groupby(["prs_quantile", "imc_cat"]).size() / prs_df.groupby(["prs_quantile"]).size()

    fig = plt.subplots(figsize=(10, 5))

    ax = sns.lineplot(prev_df.loc[:, "Obesidade"], marker=".", markersize=15, color="black")

    ax.figure.savefig("prs_plots/prevalence_per_quantile.png")

def scatter_anc(prs_df, anc):
    fig_scatter = plt.subplots(figsize=(10, 5))

    ax_scat = sns.scatterplot(data=prs_df, x="prs", y=anc)

    ax_scat.figure.savefig(f"prs_plots/prs_{anc}_scatterplot.png")



#Gráficos que faltam
# Ancestralidade (barplot)
# Correlação entre ancestralidade e PRS
# Variância explicada