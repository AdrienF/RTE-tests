#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 20:33:49 2018

@author: afontvielle
"""

import numpy as np
import pandas as pd
from datetime import datetime

# read the full dataset
# Available from https://www.rte-france.com/fr/eco2mix/eco2mix-telechargement
dataset = pd.read_csv('eCO2mix_RTE_energie_M.csv', encoding='latin1', sep=';')
# Select only national data
dataset_for_france = dataset.loc[dataset.Territoire == 'France']
dff = dataset_for_france.set_index('Mois')
dff.drop('0000-00', inplace=True)
dff.index.set_names('Periode', inplace=True)
#convert strings to datetime objects
dff.index = pd.to_datetime(dff.index)

#convert monthly timestamps to year period (summing monthly productions)
dff_years = dff.resample('Y', kind='period').sum()
print(dff_years)