#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 23:10:28 2021

@author: BSc. Angel Santiago Garay Moreyra
"""

import os
import tabula
import glob
import pandas as pd

# Detecta cualquier pdf en la carpeta

pdf_1 = glob.glob('*.pdf')
rem_stad = ['std', '50%', 'count']
columns = ['Time', 'T01', 'T02', 'T03', 'T04', 'T05',
           'T06', 'T07', 'T08', 'T09',  'T10', 'T11', 'T12']
sensors = ['T01', 'T02', 'T03', 'T04', 'T05', 'T06',
           'T07', 'T08', 'T09',  'T10', 'T11', 'T12']
sensors2 = []
date = input('Ingrese la fecha, ejm: 03-mar-2020 :')
number = float(input('Ingrese la temperatura :'))
# Detecta los valores del pdf
for doc in pdf_1:
    df = tabula.read_pdf(doc, pages='all')
    row1 = df.index[df[date] == 'Start Interval: Exp Start'].tolist()
    row2 = df.index[df[date] == 'Stop Interval: Exp End'].tolist()
    if  (row1[0]%40)/40 < 0.5:
        i_page = round(row1[0]/40)+2
    else:
        i_page = round(row1[0]/40)+1
    if  (row2[0]%40)/40 < 0.5:
        e_page = round(row2[0]/40)+2
    else:
        e_page = round(row2[0]/40)+1  
    df1 = pd.DataFrame()
    df2 = pd.DataFrame()
    df3 = pd.DataFrame()
    for i in range(i_page, e_page+1):
        if i != i_page:
            if i!= e_page:
                for j in range(i_page+1, e_page):
                    j = tabula.read_pdf(doc, pages=i, area=(
                        124.245, 37.125, 526.185, 675.675))
                    df2 = pd.concat([j],ignore_index=True)
                    df2.set_axis(columns, axis='columns', inplace=True)
        if i == i_page:
            a = row1[0]-(40*(i-2))+2
            new1 = 107.245 + 10.402 * a
            df1 = tabula.read_pdf(doc, pages=i, area=(
                new1, 37.125, 526.185, 675.675))
            df1.set_axis(columns, axis='columns', inplace=True)
        if i == e_page:
            b = row2[0]-(40*(i-2))
            new2 = 107.245 + 10.402 * b
            df3 = tabula.read_pdf(doc, pages=i, area=(
                124.245, 37.125, new2, 675.675))
            df3.set_axis(columns, axis='columns', inplace=True)
    dfinal = pd.concat([df1, df2, df3], ignore_index=True)  
# Limpia los valores del pdf
for sensor in sensors:
    dfinal[sensor] = dfinal[sensor].str.replace(' °C', '')
    if dfinal.iloc[0][sensor] == 'OPEN':
        dfinal.pop(sensor)
    else:
        dfinal[sensor] = dfinal[sensor].astype(float)
        sensors2.append(sensor)
# Información estadística de cada sensor en toda la exposición
time = dfinal.drop((sensors2), axis=1)
stics1 = dfinal.describe(percentiles=[]).round(2)
stics1.loc['DTT'] = stics1.loc['max'] - stics1.loc['min']
stics1 = stics1.drop(rem_stad)
# Información estadística de cada sensor en cada tiempo
stics2 = dfinal.drop(['Time'], axis=1)
stics2['mean'] = stics2.mean(axis=1).round(2)
sensors3 = []
for sensor in sensors2:
    stics2[sensor+'dm'] = abs(stics2['mean'] - stics2[sensor])
    sensors3.append(sensor+'dm')
stics2['Desv Max'] = stics2[sensors3].max(axis=1)
stics2 = stics2.drop(columns=sensors3)
stics2['DTE'] = stics2[sensors2].max(axis=1) - stics2[sensors2].min(axis=1)
stics2['s vs e'] = number - stics2['T12']
stics2.loc['mean'] = stics2[['mean', 's vs e']].mean().round(2)
# Final
result_final = pd.concat([stics2, stics1])
result_final.loc['Maximus'] = result_final[['Desv Max', 'DTE']].max().round(2)
result_final.to_excel("aver.xlsx")


#    if df1['03-mar-2020'].str.contains('Start Interval: Exp Start').any():
        # print(True)
    # else:
        # print(False)
    #pd.set_option("display.max_rows", None, "display.max_columns", None)
# Limpia los valores del pdf
