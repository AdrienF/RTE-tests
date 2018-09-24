#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 20:33:49 2018

@author: afontvielle
"""

import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt


#%% Energy production
# Read the full dataset of Energy production
# Available from https://www.rte-france.com/fr/eco2mix/eco2mix-telechargement
dataset = pd.read_csv('eCO2mix_RTE_energie_M.csv', encoding='latin1', sep=';')

# Select only national data
dataset_for_france = dataset.loc[dataset.Territoire == 'France']
dff = dataset_for_france.set_index('Mois')
dff.drop('0000-00', inplace=True)
dff.index.set_names('Periode', inplace=True)
#convert strings to datetime objects
dff.index = pd.to_datetime(dff.index)

#remove data of the current year
current_year = str(datetime.today().year)
dff = dff[dff.index < current_year]

#convert monthly timestamps to year period (summing monthly productions)
dff_years = dff.resample('Y', kind='period').sum()
dff_months = dff.resample('M', kind='period').sum()

def plotDataProduction(dataframe):
    #data slices
    periods = np.array(dataframe.index.to_timestamp())
    productions = dataframe.loc[:, 'Production totale':'Production bio-énergies']
    productions_s = dataframe.loc[:, 'Production solaire']
    productions_e = dataframe.loc[:, 'Production éolien']
    consommation = dataframe['Consommation totale']
    echanges = dataframe.loc[:, 'Echanges export':'Echanges avec l\'Allemagne et la Belgique']

    #Cumulative plots
    #plot productions type (remove total and 'thermique total')
    idx = [1, 3, 4, 5, 6, 7, 8, 9]
    plt.figure()
    ax0 = plt.subplot(211)
    plt.stackplot(periods, np.array(productions.iloc[:, idx].T), baseline='zero')
    plt.plot(periods, np.array(consommation), '--k', linewidth=1)
    plt.legend(np.concatenate(( ['Consommation'], np.array(productions.columns[idx])), axis=0))
    plt.ylabel('GWh')
    plt.title('Production électrique en France par moyen de production')
    plt.gcf().autofmt_xdate()

    plt.subplot(212, sharex=ax0)
    plt.plot(periods, np.array(productions.iloc[:, idx]))
    plt.plot(periods, np.array(productions_e), '2k')
    plt.plot(periods, np.array(productions_s), color='k', marker=(8, 1, 0), linestyle='None')
    plt.legend(np.concatenate(( ['Consommation'], np.array(productions.columns[idx])), axis=0))
    plt.ylabel('GWh')
    plt.gcf().autofmt_xdate()


#%% Energy Production Capacity
dataset_parc = pd.read_csv('parc_prod_par_filiere.csv', encoding='latin1', sep=';')
dp = dataset_parc.set_index('Annee')
dp.index = pd.to_datetime(dp.index, format='%Y')
dp.sort_index(inplace=True)
dp.index = dp.index.to_period('Y')

def plotProductionOverCapacity(productionDataFrame, capacityDataFrame, freq='Y'):
    #resample both dataframe to monthly values
    pdf = productionDataFrame.resample(freq).sum()
    cdf = capacityDataFrame.resample(freq).pad()
    productions_s = pdf.loc[:, 'Production solaire']
    productions_e = pdf.loc[:, 'Production éolien']
    capacite_s = cdf.loc[:, 'Parc solaire (MW)']
    capacite_e = cdf.loc[:, 'Parc eolien (MW)']
    t0 = capacite_s.index[0]
    period_delta = t0.to_timestamp(freq='H',how='End') - t0.to_timestamp(freq='H', how='Start')
    n_heure_par_periode = period_delta.total_seconds()/3600
    print('n_heure_par_periode (', freq, ')', n_heure_par_periode)

    charge_s = productions_s * 1000 / capacite_s / n_heure_par_periode * 100
    charge_e = productions_e * 1000 / capacite_e / n_heure_par_periode * 100
    period = charge_s.index.to_timestamp()

    plt.figure()
    plt.plot(period, charge_s, marker=(8, 1, 0), label='solaire')
    plt.plot(period, charge_e, marker='2', label='eolien')
    plt.legend()
    plt.ylabel('charge du parc (%)')


#%% Plot things
# Production
plotDataProduction(dff_months)
# Capacity
plotProductionOverCapacity(dff_months, dp, 'M')
plotProductionOverCapacity(dff_months, dp, 'Y')
plotProductionOverCapacity(dff_months, dp, 'Q')

