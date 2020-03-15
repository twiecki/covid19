import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pandas as pd
import seaborn as sns
from typing import List

sns.set_context('talk')
plt.style.use('seaborn-whitegrid')
def plot_predicted_per_county(n_countries: int,
                              countries: List[str],
                              df_sign: pd.DataFrame,
                              post_pred: pd.DataFrame,
                              common_country_axis: bool = False):
    fig, axs = plt.subplots(nrows=n_countries // 3, ncols=3, figsize=(15, 30), sharex=True)

    for ax, country in zip(axs.flatten(), countries):
        df_country = df_sign.loc[lambda x: x.country == country]
        ax.plot(df_country.days_since_100, df_country.cases, color='r')
        ax.plot(np.arange(0, post_pred[country].shape[1]), post_pred[country].T, alpha=.05, color='.5')
        ax.plot(df_country.days_since_100, df_country.cases, color='r')
        #ax.set_yscale('log')
        #ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
        if common_country_axis:
            ax.set_ylim(0, df_sign.cases.max()*15)
        else:
            ax.set_ylim(0, df_country.cases.iloc[-1] * 15)
        ax.set_title(country)
        
    axs[0, 0].legend(['data', 'model prediction'])
    [ax.set(xlabel='Days since 100 cases') for ax in axs[-1, :]]
    [ax.set(ylabel='Confirmed cases') for ax in axs[:, 0]]
    fig.tight_layout()
    return fig

def plot_predicted_per_county_log(n_countries: int,
                                  countries: List[str],
                                  df_sign: pd.DataFrame,
                                  post_pred: pd.DataFrame,
                                  common_country_axis: bool = False):
    fig, axs = plt.subplots(nrows=n_countries // 3, ncols=3, figsize=(15, 30), sharex=True)

    for ax, country in zip(axs.flatten(), countries):
        df_country = df_sign.loc[lambda x: x.country == country]
        ax.plot(df_country.days_since_100, df_country.cases, color='r')
        ax.plot(np.arange(0, post_pred[country].shape[1]), post_pred[country].T, alpha=.05, color='.5')
        ax.plot(df_country.days_since_100, df_country.cases, color='r')
        ax.set_yscale('log')
        ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
        if common_country_axis:
            ax.set_ylim(100, df_sign.cases.max() * 4.5)
        ax.set_title(country)
        
    axs[0, 0].legend(['data', 'model prediction'])
    [ax.set(xlabel='Days since 100 cases') for ax in axs[-1, :]]
    [ax.set(ylabel='Confirmed cases') for ax in axs[:, 0]]
    fig.tight_layout()
    return fig