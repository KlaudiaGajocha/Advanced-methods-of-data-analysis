# -*- coding: utf-8 -*-
"""ADA - DBSCAN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tPamwoa5sXGwlyV-6k6dDujSNlzpCqIU
"""

import pandas as pd 
import numpy as np

df= pd.read_csv('Marketing.csv', sep=";")

df

df.info()

#Obliczenie wieku każdego klienta.
df['Wiek'] = 2022-(df['RokUrodzenia'])
df

#Wyliczenie, ile dni minęło od chwili rejestracji klienta do dzisiaj.
import datetime
today = datetime.datetime.now()
today

df['DataRejestracji'] = pd.to_datetime(df['DataRejestracji'])

df['DniOdRejestracji'] = today-(df['DataRejestracji'])
df

df.drop('DataRejestracji', axis=1, inplace=True)
df.drop('RokUrodzenia', axis=1, inplace=True)

df

#Obliczenie liczby osób w rodzinie klienta.
df['StanCywilny'] = [1 if x in ['Wolny.', 'Rozwiedziony.', 'Wdowa/Wdowiec.'] else 2 for x in df['StanCywilny']]

df['RozmiarRodziny'] = df['StanCywilny']+df['DzieciMale']+df['Nastolatki']
df

df.drop(['DzieciMale', 'Nastolatki', 'StanCywilny'], axis=1, inplace=True)

#4. Określenie, ile poprzednich kampanii marketingowych było zaakceptowanych przez każdego klienta.
df['LiczbaZaakceptowanych'] = df['AkceptacjaKampanii1']+df['AkceptacjaKampanii2']+df['AkceptacjaKampanii3']+df['AkceptacjaKampanii4']+df['AkceptacjaKampanii5']
df

df.drop(['AkceptacjaKampanii1', 'AkceptacjaKampanii2', 'AkceptacjaKampanii3', 'AkceptacjaKampanii4', 'AkceptacjaKampanii5'], axis=1, inplace=True)

#Obliczenie całkowitej kwoty jaka została wydana przez każdego klienta na wszystkie kategorie produktów (Wina, owoce, mięso, ryby, słodycze, złoto).
df['SumaCalkowita'] = df['SumaWina']+df['SumaOwoce']+df['SumaMieso']+df['SumaRyby']+df['SumaSlodycze']+df['SumaZloto']
df

df.drop(['SumaWina', 'SumaOwoce', 'SumaMieso', 'SumaRyby', 'SumaSlodycze', 'SumaZloto'], axis=1, inplace=True)

#Sprawdzenie brakujących wartości i ich zastąpienie wartością średnią wyliczoną dla danej kolumny.
df.isnull().sum()

#zastąpienie wartością średnią wyliczoną z kolumny dochod
df['Dochod'].fillna((df['Dochod'].mean()), inplace=True)

#brak warości zerowych 
df.isnull().sum()

#Wizualizację danych (graficzne przedstawienie korelacji atrybutów ze zmienną Odpowiedz za pomocą mapy ciepła, wykresy rozrzutu 5 zmiennych, które mają najwyższą korelację z atrybutem Odpowiedz).
import matplotlib.pyplot as plt
import seaborn as sns
pearsoncorr = df.corr(method='pearson')
pearsoncorr

sns.heatmap(pearsoncorr, 
            xticklabels=pearsoncorr.columns,
            yticklabels=pearsoncorr.columns,
            cmap='RdBu_r',
#            annot=True,
            linewidth=0.5)

import seaborn as sns
sns.scatterplot(x=df['Odpowiedz'], y=df['LiczbaZaakceptowanych'])

sns.scatterplot(x=df['Odpowiedz'], y=df['SumaCalkowita'])

sns.scatterplot(x=df['Odpowiedz'], y=df['LiczbaZakupowKatalog'])

sns.scatterplot(x=df['Odpowiedz'], y=df['LiczbaZakupowPromocja'])

sns.scatterplot(x=df['Odpowiedz'], y=df['LiczbaZakupowOnline'])

df.DniOdRejestracji=df.DniOdRejestracji.astype(int)   

def get_redundant_pairs(df):
    '''Get diagonal and lower triangular pairs of correlation matrix'''
    pairs_to_drop = set()
    cols = df.columns
    for i in range(0, df.shape[1]):
        for j in range(0, i+1):
            pairs_to_drop.add((cols[i], cols[j]))
    return pairs_to_drop

def get_top_abs_correlations(df, n=5):
    au_corr = df.corr().abs().unstack()
    labels_to_drop = get_redundant_pairs(df)
    au_corr = au_corr.drop(labels=labels_to_drop).sort_values(ascending=False)
    return au_corr[0:n]

print("Top Absolute Correlations")
print(get_top_abs_correlations(df, 5))

df.drop('Odpowiedz', axis=1, inplace=True)

df.info()

#Skalowanie zmiennych numerycznych.
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
scaler.fit(df)
scaled_df = pd.DataFrame(scaler.transform(df),columns= df.columns )
print("Wszystkie wartości są teraz zeskalowane")

#Redukcję wymiarowości do 3 wymiarów z wykorzystaniem metody PCA.
from sklearn.decomposition import PCA
pca = PCA(n_components=3)
pca.fit(scaled_df)
PCA_df = pd.DataFrame(pca.transform(scaled_df), columns=(["col1","col2", "col3"]))
PCA_df.describe().T

#Grupowanie klientów z wykorzystaniem metody DBSCAN.
from sklearn.cluster import DBSCAN
clustering = DBSCAN(eps=3, min_samples=2).fit(df)
clustering.labels_
clustering

db = DBSCAN(eps=0.4, min_samples=20)
db.fit(df)

#eps — maksymalna odległość między dwiema próbkami, przy której jedna jest uważana za sąsiadującą z drugą. 
#min_sample — liczba próbek (lub całkowita waga) w sąsiedztwie dla punktu, który należy uznać za punkt centralny.

#etykiety/labels — etykiety klastrowe dla każdego punktu w zbiorze danych przekazanym funkcji fit(). Zaszumione próbki otrzymują etykietę -1.
labels = db.labels_

no_clusters = len(np.unique(labels) )
no_noise = np.sum(np.array(labels) == -1, axis=0)

print('Szacowana liczba klastrów: %d' % no_clusters)
print('Szacowana liczba punktów szumiących: %d' % no_noise)