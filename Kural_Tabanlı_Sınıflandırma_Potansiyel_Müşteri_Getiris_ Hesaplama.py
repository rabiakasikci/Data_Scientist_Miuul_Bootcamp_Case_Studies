# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 17:01:15 2024

@author: Rabia KAŞIKCI
"""
import pandas as pd

df = pd.read_csv('persona.csv')

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)


#Görev 1
# Soru 2: Kaç unique SOURCE vardır? Frekansları nedir?

print(df["SOURCE"].unique())
print(df["SOURCE"].value_counts())


# Soru 3: Kaç unique PRICE vardır?
print(df["PRICE"].unique())

# Soru 4: Hangi PRICE'dan kaçar tane satış gerçekleşmiş?
print(df["PRICE"].value_counts())

# Soru 5: Hangi ülkeden kaçar tane satış olmuş?
print(df["COUNTRY"].value_counts())



# Soru 6: Ülkelere göre satışlardan toplam ne kadar kazanılmış?
print(df.groupby("COUNTRY")["PRICE"].sum())


# Soru 7: SOURCE türlerine göre satış sayıları nedir?
print(df.groupby("SOURCE")["PRICE"].count())

# Soru 8: Ülkelere göre PRICE ortalamaları nedir?
print(df.groupby("COUNTRY")["PRICE"].mean())


# Soru 9: SOURCE'lara göre PRICE ortalamaları nedir?
print(df.groupby("SOURCE")["PRICE"].mean())

# Soru 10: COUNTRY-SOURCE kırılımında PRICE ortalamaları nedir?
print(df.groupby(["COUNTRY","SOURCE"])["PRICE"].mean())


##########################################################################################


#Görev 2: COUNTRY, SOURCE, SEX, AGE kırılımında ortalama kazançlar nedir?

print(df.groupby(["COUNTRY","SOURCE", "SEX", "AGE"])["PRICE"].mean())


#Görev 3: Çıktıyı PRICE’a göre sıralayınız.

agg_df = df.groupby(["COUNTRY", "SOURCE", "SEX", "AGE"])["PRICE"].mean().sort_values(ascending=False)


#Görev 4: Indekste yer alan isimleri değişken ismine çeviriniz

agg_df = df.groupby(["COUNTRY", "SOURCE", "SEX", "AGE"])["PRICE"].mean().sort_values(ascending=False).reset_index()


#Görev 5: Age değişkenini kategorik değişkene çeviriniz ve agg_df’e ekleyiniz.

bins = [0, 18, 23, 30, 40, 70]
labels = ['0_18', '19_23', '24_30', '31_40', '41_70']
df['AGE_CATEGORY'] = pd.cut(df['AGE'], bins=bins, labels=labels, right=True)


#Görev 6: Yeni seviye tabanlı müşterileri (persona) tanımlayınız.

df["customers_level_based"] = (df["COUNTRY"].astype(str)+"_" + df["SOURCE"].astype(str)+"_" + df["SEX"].astype(str)+"_" + df["AGE_CATEGORY"].astype(str)).str.upper()

df.groupby(["customers_level_based"])["PRICE"].mean()


#Görev 7: Yeni müşterileri (personaları) segmentlere ayırınız.
agg_df['SEGMENT'] = pd.qcut(agg_df['PRICE'], q=4, labels=['Segment_1', 'Segment_2', 'Segment_3', 'Segment_4'])




#Görev 8: Yeni gelen müşterileri sınıflandırıp, ne kadar gelir getirebileceklerini tahmin ediniz.
# 33 yaşında ANDROID kullanan bir Türk kadını hangi segmente aittir ve ortalama ne kadar gelir kazandırması beklenir?
# 35 yaşında IOS kullanan bir Fransız kadını hangi segmente aittir ve ortalama ne kadar gelir kazandırması beklenir?

df[df["customers_level_based"] == "TUR_ANDROID_FEMALE_31_40"]["PRICE"].mean()
df[df["customers_level_based"] == "FRA_IOS_FEMALE_31_40"]["PRICE"].mean()