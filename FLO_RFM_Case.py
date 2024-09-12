# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 11:24:46 2024

@author: Rabia KAŞIKCI
"""


###############################################################
# RFM ile Müşteri Segmentasyonu (Customer Segmentation with RFM)
###############################################################

###############################################################
# İş Problemi (Business Problem)
###############################################################
# FLO müşterilerini segmentlere ayırıp bu segmentlere göre pazarlama stratejileri belirlemek istiyor.
# Buna yönelik olarak müşterilerin davranışları tanımlanacak ve bu davranış öbeklenmelerine göre gruplar oluşturulacak..

###############################################################
# Veri Seti Hikayesi
###############################################################

# Veri seti son alışverişlerini 2020 - 2021 yıllarında OmniChannel(hem online hem offline alışveriş yapan) olarak yapan müşterilerin geçmiş alışveriş davranışlarından
# elde edilen bilgilerden oluşmaktadır.

# master_id: Eşsiz müşteri numarası
# order_channel : Alışveriş yapılan platforma ait hangi kanalın kullanıldığı (Android, ios, Desktop, Mobile, Offline)
# last_order_channel : En son alışverişin yapıldığı kanal
# first_order_date : Müşterinin yaptığı ilk alışveriş tarihi
# last_order_date : Müşterinin yaptığı son alışveriş tarihi
# last_order_date_online : Muşterinin online platformda yaptığı son alışveriş tarihi
# last_order_date_offline : Muşterinin offline platformda yaptığı son alışveriş tarihi
# order_num_total_ever_online : Müşterinin online platformda yaptığı toplam alışveriş sayısı
# order_num_total_ever_offline : Müşterinin offline'da yaptığı toplam alışveriş sayısı
# customer_value_total_ever_offline : Müşterinin offline alışverişlerinde ödediği toplam ücret
# customer_value_total_ever_online : Müşterinin online alışverişlerinde ödediği toplam ücret
# interested_in_categories_12 : Müşterinin son 12 ayda alışveriş yaptığı kategorilerin listesi

###############################################################
# GÖREVLER
###############################################################

import pandas as pd
import numpy as np
import seaborn as sn
import matplotlib.pyplot as plt
import datetime as dt 

pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)

df = pd.read_csv("flo_data_20K.csv")

# GÖREV 1: Veriyi Anlama (Data Understanding) ve Hazırlama
           # 1. flo_data_20K.csv verisini okuyunuz.
           # 2. Veri setinde
                     # a. İlk 10 gözlem,

df.head(10)
                     # b. Değişken isimleri,
df.columns
df.index

                     # c. Betimsel istatistik,
df.describe()
                     # d. Boş değer,
df.isnull().sum()
                     # e. Değişken tipleri, incelemesi yapınız.
df.dtypes
           # 3. Omnichannel müşterilerin hem online'dan hemde offline platformlardan alışveriş yaptığını ifade etmektedir. Herbir müşterinin toplam
           # alışveriş sayısı ve harcaması için yeni değişkenler oluşturun.
df["total_shopping"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
df["total_spending"] = df["customer_value_total_ever_offline"] + df["customer_value_total_ever_online"]
           # 4. Değişken tiplerini inceleyiniz. Tarih ifade eden değişkenlerin tipini date'e çeviriniz.
df.dtypes
date_cols = [cols for cols in df.columns if 'date' in cols]
df[date_cols] = df[date_cols].apply(pd.to_datetime)
df.dtypes


           # 5. Alışveriş kanallarındaki müşteri sayısının, ortalama alınan ürün sayısının ve ortalama harcamaların dağılımına bakınız.
df.groupby(["order_channel"]).agg(
    numberofcustomer=('master_id', 'count'),
    avgshopping=('total_shopping', 'mean'),
    avgspending=('total_spending', 'mean')
    ).reset_index()

"""
  order_channel  numberofcustomer  avgshopping  avgspending
0   Android App              9495        5.505      823.493
1       Desktop              2735        3.993      588.783
2       Ios App              2833        5.419      891.634
3        Mobile              4882        4.441      620.275
"""

           # 6. En fazla kazancı getiren ilk 10 müşteriyi sıralayınız.
df.groupby(["master_id"])["total_spending"].sum().sort_values(ascending=False).head(10)
           # 7. En fazla siparişi veren ilk 10 müşteriyi sıralayınız.
df.groupby(["master_id"])["total_shopping"].sum().sort_values(ascending=False).head(10)

           # 8. Veri ön hazırlık sürecini fonksiyonlaştırınız.



def data_preprocessing(df):
    print(df.head(10))
    print(df.columns)
    print(df.index)
    print(df.describe())
    print(df.isnull().sum())
    print(df.dtypes)
    df["total_shopping"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
    df["total_spending"] = df["customer_value_total_ever_offline"] + df["customer_value_total_ever_online"]
    date_cols = [cols for cols in df.columns if 'date' in cols]
    df[date_cols] = df[date_cols].apply(pd.to_datetime)
    print(df.groupby(["order_channel"]).agg(
        numberofcustomer=('master_id', 'count'),
        avgshopping=('total_shopping', 'mean'),
        avgspending=('total_spending', 'mean')
        ).reset_index())

    print(df.groupby(["master_id"])["total_spending"].sum().sort_values(ascending=False).head(10))
    print(df.groupby(["master_id"])["total_shopping"].sum().sort_values(ascending=False).head(10))

    
    
    
    return df 


df = pd.read_csv("flo_data_20K.csv")

data_preprocessing(df)


# GÖREV 2: RFM Metriklerinin Hesaplanması
today_date = dt.datetime(2021, 5, 29)
print("Belirlenen Tarih:", today_date)

rfm = df.groupby("master_id").agg(
    recency=('last_order_date', lambda x: (today_date - x.max()).days),  
    frequency=('total_shopping', 'sum'),  
    monetary=('total_spending', 'sum')  
).reset_index()


# GÖREV 3: RF ve RFM Skorlarının Hesaplanması


rfm["recency_score"] = pd.qcut(rfm['recency'], 5 , labels=[5, 4, 3, 2, 1])
rfm["frequency_score"] = pd.qcut(rfm['frequency'].rank(method="first"), 5 , labels=[1, 2, 3, 4, 5])
rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5 , labels=[1, 2, 3, 4, 5])
rfm["RFM_Score"] = (rfm['recency_score'].astype(str) +
                    rfm['frequency_score'].astype(str))
rfm.head()
rfm.describe().T

rfm[rfm["RFM_Score"] == "55"]

rfm[rfm["RFM_Score"] == "11"]
# GÖREV 4: RF Skorlarının Segment Olarak Tanımlanması

seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}
rfm['segment'] = rfm['RFM_Score'].replace(seg_map, regex=True)

rfm[["segment", "recency", "frequency", "monetary"]].groupby("segment").agg(["mean", "count"])

# GÖREV 5: Aksiyon zamanı!
           # 1. Segmentlerin recency, frequnecy ve monetary ortalamalarını inceleyiniz.
rfm.groupby(["segment"]).agg(["mean"])
           # 2. RFM analizi yardımı ile 2 case için ilgili profildeki müşterileri bulun ve müşteri id'lerini csv ye kaydediniz.
                   # a. FLO bünyesine yeni bir kadın ayakkabı markası dahil ediyor. Dahil ettiği markanın ürün fiyatları genel müşteri tercihlerinin üstünde. Bu nedenle markanın
                   # tanıtımı ve ürün satışları için ilgilenecek profildeki müşterilerle özel olarak iletişime geçeilmek isteniliyor. Sadık müşterilerinden(champions,loyal_customers),
                   # ortalama 250 TL üzeri ve kadın kategorisinden alışveriş yapan kişiler özel olarak iletişim kuralacak müşteriler. Bu müşterilerin id numaralarını csv dosyasına
                   # yeni_marka_hedef_müşteri_id.cvs olarak kaydediniz.
data = df.merge(rfm, on="master_id", how="left")
yeni_marka_hedef_müşteri_id = data[
    (data["segment"].isin(["champions", "loyal_customers"])) &  
    (data["interested_in_categories_12"].str.contains("KADIN", na=False)) &  
    (data["total_spending"] > 250)  
]["master_id"]
yeni_marka_hedef_müşteri_id.to_csv("yeni_marka_hedef_müşteri_id.csv", index=False)
                   # b. Erkek ve Çoçuk ürünlerinde %40'a yakın indirim planlanmaktadır. Bu indirimle ilgili kategorilerle ilgilenen geçmişte iyi müşteri olan ama uzun süredir
                   # alışveriş yapmayan kaybedilmemesi gereken müşteriler, uykuda olanlar ve yeni gelen müşteriler özel olarak hedef alınmak isteniliyor. Uygun profildeki müşterilerin id'lerini csv dosyasına indirim_hedef_müşteri_ids.csv
                   # olarak kaydediniz.

indirim_hedef_müşteri_ids = data[
    (data["segment"].isin(["cant_loose", "about_to_sleep", "new_customers", "need_attention"])) &  
    (data["interested_in_categories_12"].str.contains("ERKEK", na=False) |  
     data["interested_in_categories_12"].str.contains("ÇOCUK", na=False))  
]["master_id"]
indirim_hedef_müşteri_ids.to_csv("indirim_hedef_müşteri_ids.csv", index=False)

# GÖREV 6: Tüm süreci fonksiyonlaştırınız.



seg_map = {
        r'[1-2][1-2]': 'hibernating',
        r'[1-2][3-4]': 'at_Risk',
        r'[1-2]5': 'cant_loose',
        r'3[1-2]': 'about_to_sleep',
        r'33': 'need_attention',
        r'[3-4][4-5]': 'loyal_customers',
        r'41': 'promising',
        r'51': 'new_customers',
        r'[4-5][2-3]': 'potential_loyalists',
        r'5[4-5]': 'champions'
}

today_date = dt.datetime(2021, 5, 29)

def rfm_calculater(df):
    
    print("Belirlenen Tarih:", today_date)
    df["total_shopping"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
    df["total_spending"] = df["customer_value_total_ever_offline"] + df["customer_value_total_ever_online"]

    rfm = df.groupby("master_id").agg(
        recency=('last_order_date', lambda x: (today_date - x.max()).days),

        frequency=('total_shopping', 'sum'),  # Alışveriş sayısı
        monetary=('total_spending', 'sum')  # Toplam harcama
    ).reset_index()


    # GÖREV 3: RF ve RFM Skorlarının Hesaplanması


    rfm["recency_score"] = pd.qcut(rfm['recency'], 5 , labels=[5, 4, 3, 2, 1])
    rfm["frequency_score"] = pd.qcut(rfm['frequency'].rank(method="first"), 5 , labels=[1, 2, 3, 4, 5])
    rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5 , labels=[1, 2, 3, 4, 5])
    rfm["RFM_Score"] = (rfm['recency_score'].astype(str) +
                        rfm['frequency_score'].astype(str))
    rfm.head()
    rfm.describe().T

    rfm[rfm["RFM_Score"] == "55"]

    rfm[rfm["RFM_Score"] == "11"]
    # GÖREV 4: RF Skorlarının Segment Olarak Tanımlanması


    rfm['segment'] = rfm['RFM_Score'].replace(seg_map, regex=True)

    rfm[["segment", "recency", "frequency", "monetary"]].groupby("segment").agg(["mean", "count"])

    # GÖREV 5: Aksiyon zamanı!
               # 1. Segmentlerin recency, frequnecy ve monetary ortalamalarını inceleyiniz.
    rfm.groupby(["segment"]).agg(["mean"])
               # 2. RFM analizi yardımı ile 2 case için ilgili profildeki müşterileri bulun ve müşteri id'lerini csv ye kaydediniz.
                       # a. FLO bünyesine yeni bir kadın ayakkabı markası dahil ediyor. Dahil ettiği markanın ürün fiyatları genel müşteri tercihlerinin üstünde. Bu nedenle markanın
                       # tanıtımı ve ürün satışları için ilgilenecek profildeki müşterilerle özel olarak iletişime geçeilmek isteniliyor. Sadık müşterilerinden(champions,loyal_customers),
                       # ortalama 250 TL üzeri ve kadın kategorisinden alışveriş yapan kişiler özel olarak iletişim kuralacak müşteriler. Bu müşterilerin id numaralarını csv dosyasına
                       # yeni_marka_hedef_müşteri_id.cvs olarak kaydediniz.
    data = df.merge(rfm, on="master_id", how="left")
    return data

df = pd.read_csv("flo_data_20K.csv")
date_cols = [cols for cols in df.columns if 'date' in cols]
df[date_cols] = df[date_cols].apply(pd.to_datetime)
rfm_calculater(df)