import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import os
import seaborn as sns
 

def bmi_strata_plot(prs_df, avg=False, anc_cat="",anc=False):
    bins_imc = [0, 30, np.inf]
    cat = ["Normal", "Obesidade"]
    df_to_plot = prs_df.copy()
    if anc:
        df_to_plot["major_group"] = df_to_plot[['EuropaV3', 'Oriente_MedioV3', 'AmericasV3',
       'AfricaV3', 'JudaicaV3', 'OceaniaV3', 'AsiaV3']].idxmax(axis=1)
        
        conditions = [df_to_plot["major_group"] == anc_cat, df_to_plot["major_group"] != anc_cat]
        choices = [anc_cat, f"non-{anc_cat}"]

        df_to_plot[f"{anc_cat}_cat"] = np.select(conditions, choices, default=np.nan)
    if not avg:
        df_to_plot["imc_cat"] = pd.cut(df_to_plot["imc"], bins=bins_imc, labels=cat)
        df_to_plot["prs_quantile"] = pd.qcut(df_to_plot["prs"], q=[0, 0.10, 0.20, 0.40, 0.60, 0.80, 0.90, 0.95, 0.99, 1.0], labels= ["(0, 0.1]", "(0.1, 0.2]", "(0.2, 0.4]", "(0.4, 0.6]", "(0.6, 0.8]",
                                                            "(0.8, 0.9]", "(0.9, 0.95]", "(0.95, 0.99]", "(0.99, 1.0]"])
        
        fig = px.strip(df_to_plot, x="prs_quantile", y="imc", color="imc_cat", stripmode="overlay",  
                    category_orders={"prs_quantile": ["(0, 0.1]", "(0.1, 0.2]", "(0.2, 0.4]", "(0.4, 0.6]", "(0.6, 0.8]",
                                                        "(0.8, 0.9]", "(0.9, 0.95]", "(0.95, 0.99]", "(0.99, 1.0]"]}, labels={"prs_quantile": "Quantis do PRS de IMC",
                                "imc": "IMC (kg/m²)"}, title="Gráfico estratificado de PRS vs IMC")

        fig.update_xaxes(tickangle=45)
    else:
        df_to_plot["imc_cat"] = pd.cut(df_to_plot["imc"], bins=bins_imc, labels=cat)
        df_to_plot["avg_quantile"] = pd.qcut(df_to_plot["avg"], q=[0, 0.10, 0.20, 0.40, 0.60, 0.80, 0.90, 0.95, 0.99, 1.0], labels= ["(0, 0.1]", "(0.1, 0.2]", "(0.2, 0.4]", "(0.4, 0.6]", "(0.6, 0.8]",
                                                            "(0.8, 0.9]", "(0.9, 0.95]", "(0.95, 0.99]", "(0.99, 1.0]"])
        
        fig = px.strip(df_to_plot, x="avg_quantile", y="imc", color=f"{anc_cat}_cat", stripmode="overlay",  
                    category_orders={"avg_quantile": ["(0, 0.1]", "(0.1, 0.2]", "(0.2, 0.4]", "(0.4, 0.6]", "(0.6, 0.8]",
                                                        "(0.8, 0.9]", "(0.9, 0.95]", "(0.95, 0.99]", "(0.99, 1.0]"]}, labels={"prs_quantile": "Quantis do PRS de IMC",
                                "imc": "IMC (kg/m²)"}, title="Gráfico estratificado de PRS (AVG) vs IMC")

        fig.update_xaxes(tickangle=45)
        

    if not os.path.exists("prs_plots"):
        os.mkdir("prs_plots")

    if avg:
        fig.write_html("prs_plots/strata_plot_2_AVG.html")
    else:
        fig.write_html("prs_plots/strata_plot_2.html")
    return df_to_plot

def bmi_per_quantile(prs_df, q):
    #Separando os dados em q quantis
    labels = [f"{n}" for n in range(1, q + 1)]

    prs_df_q = prs_df.copy()

    prs_df_q["prs_quantile"] = pd.qcut(prs_df_q["prs"], q=q, labels=labels)

    fig = sns.boxplot(data=prs_df_q, x="prs_quantile", y="imc", palette="flare").set( xlabel='Quantis', ylabel='IMC (kg/m²)')

    fig2 = sns.lineplot(prs_df_q.groupby("prs_quantile")["imc"].mean(), marker="o", markersize=7, color="black")

    plt.savefig(f"prs_plots/prs_q{q}_plot.png")
    fig2.figure.savefig("prs_plots/lineplot_means.png")

def prs_distribution(prs_df, avg=False): #TODO: fazer distribuição por ancestralidade
    if avg == True:
        fig_dis = sns.kdeplot(data=prs_df["avg"])
        fig_dis.set_xlabel("AVG")
    else:
        fig_dis = sns.kdeplot(data=prs_df["prs"])
        fig_dis.set_xlabel("PRS")
    
    fig_dis.set_ylabel("Densidade")
    if avg == True:
        fig_dis.figure.savefig("prs_plots/avg_distribution.png")
    else:
        fig_dis.figure.savefig("prs_plots/prs_distribution.png")

def prevalence_per_quantile(prs_df, q, anc_cat="", anc=False, avg=False):
    labels = [f"{n}" for n in range(1, q + 1)]
    bins_imc = [0, 30, np.inf]
    cat = ["Normal", "Obesidade"]
    if avg == True:
        if anc == True:
            prs_df = prs_df[prs_df[anc_cat] >= 70.0]
            prs_df["imc_cat"] = pd.cut(prs_df["imc"], bins=bins_imc, labels=cat)
            prs_df["avg_quantile"] = pd.qcut(prs_df["avg"], q=q, labels=labels)
        else:
            prs_df["imc_cat"] = pd.cut(prs_df["imc"], bins=bins_imc, labels=cat)
            prs_df["avg_quantile"] = pd.qcut(prs_df["avg"], q=q, labels=labels)
        
        prev_df = prs_df.groupby(["avg_quantile", "imc_cat"]).size() / prs_df.groupby(["avg_quantile"]).size()

        fig = plt.subplots(figsize=(10, 5))

        ax = sns.lineplot(prev_df.loc[:, "Obesidade"], marker=".", markersize=15, color="black")
        ax.set_xlabel("Quantis PRS (AVG)")
        ax.set_ylabel("Prevalência")
        if anc == True:
            ax.figure.savefig(f"prs_plots/prevalence_per_quantile_{anc_cat}_AVG.png")
        else:
            ax.figure.savefig("prs_plots/prevalence_per_quantile_AVG.png")
    else:
        if anc == True:
            prs_df = prs_df[prs_df[anc_cat] >= 70.0]
            prs_df["imc_cat"] = pd.cut(prs_df["imc"], bins=bins_imc, labels=cat)
            prs_df["prs_quantile"] = pd.qcut(prs_df["prs"], q=q, labels=labels)
        else:
            prs_df["imc_cat"] = pd.cut(prs_df["imc"], bins=bins_imc, labels=cat)
            prs_df["prs_quantile"] = pd.qcut(prs_df["prs"], q=q, labels=labels)
        
        prev_df = prs_df.groupby(["prs_quantile", "imc_cat"]).size() / prs_df.groupby(["prs_quantile"]).size()

        fig = plt.subplots(figsize=(10, 5))

        ax = sns.lineplot(prev_df.loc[:, "Obesidade"], marker=".", markersize=15, color="black")
        ax.set_xlabel("Quantis PRS")
        ax.set_ylabel("Prevalência")
        if anc == True:
            ax.figure.savefig(f"prs_plots/prevalence_per_quantile_{anc_cat}.png")
        else:
            ax.figure.savefig("prs_plots/prevalence_per_quantile.png")

def scatter_anc(prs_df, anc):

    fig_scatter = plt.subplots(figsize=(10, 5))

    ax_scat = sns.scatterplot(data=prs_df, x=anc, y="prs")

    ax_scat.figure.savefig(f"prs_plots/prs_{anc}_scatterplot.png")

def z_score_dis(prs_df, anc=""):

    prs_df["avg_z_score"] = (prs_df["avg"] - prs_df["avg"].mean()) / prs_df["avg"].std()
    prs_df["major_group"] = prs_df[['EuropaV3', 'Oriente_MedioV3', 'AmericasV3',
       'AfricaV3', 'JudaicaV3', 'OceaniaV3', 'AsiaV3']].idxmax(axis=1)
    fig_dis_z = sns.kdeplot(data=prs_df, bw_method=0.5, 
                            hue="major_group", x="avg_z_score")
    
    fig_dis_z.figure.savefig("prs_plots/z_score_distribution.png")



#Gráficos que faltam
# Variância explicada