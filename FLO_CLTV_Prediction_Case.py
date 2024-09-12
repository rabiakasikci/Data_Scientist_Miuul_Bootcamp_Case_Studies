##############################################################
# BG-NBD ve Gamma-Gamma ile CLTV Prediction
##############################################################

###############################################################
# İş Problemi (Business Problem)
###############################################################
# FLO satış ve pazarlama faaliyetleri için roadmap belirlemek istemektedir.
# Şirketin orta uzun vadeli plan yapabilmesi için var olan müşterilerin gelecekte şirkete sağlayacakları potansiyel değerin tahmin edilmesi gerekmektedir.


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

import pandas as pd
import numpy as np
import seaborn as sn
import matplotlib.pyplot as plt
import datetime as dt 

###############################################################
# GÖREVLER
###############################################################
# GÖREV 1: Veriyi Hazırlama
           # 1. flo_data_20K.csv verisini okuyunuz.Dataframe’in kopyasını oluşturunuz.

pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)

df_ = pd.read_csv("flo_data_20K.csv")
df = df_.copy()
           # 2. Aykırı değerleri baskılamak için gerekli olan outlier_thresholds ve replace_with_thresholds fonksiyonlarını tanımlayınız.
def outlier_thresholds(dataframe, variable):
    quartile1 = dataframe[variable].quantile(0.01)
    quartile3 = dataframe[variable].quantile(0.99)
    interquantile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquantile_range
    low_limit = quartile1 - 1.5 * interquantile_range
    return low_limit, up_limit

def replace_with_thresholds(dataframe, variable):
    low_limit, up_limit = outlier_thresholds(dataframe, variable)    
    low_limit = round(low_limit)
    up_limit = round(up_limit)
    dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit
    dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit
    
    
    
           # 3. "order_num_total_ever_online","order_num_total_ever_offline","customer_value_total_ever_offline","customer_value_total_ever_online" değişkenlerinin
           # aykırı değerleri varsa baskılayanız.
columns_outlier = ["order_num_total_ever_online", "order_num_total_ever_offline", "customer_value_total_ever_offline", "customer_value_total_ever_online"]

[replace_with_thresholds(df, i) for i in columns_outlier]
           # 4. Omnichannel müşterilerin hem online'dan hemde offline platformlardan alışveriş yaptığını ifade etmektedir. Herbir müşterinin toplam
           # alışveriş sayısı ve harcaması için yeni değişkenler oluşturun.
df["total_shopping"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
df["total_spending"] = df["customer_value_total_ever_offline"] + df["customer_value_total_ever_online"]
           # 5. Değişken tiplerini inceleyiniz. Tarih ifade eden değişkenlerin tipini date'e çeviriniz.
df.dtypes
date_cols = [cols for cols in df.columns if 'date' in cols]
df[date_cols] = df[date_cols].apply(pd.to_datetime)
df.dtypes

# GÖREV 2: CLTV Veri Yapısının Oluşturulması
           # 1.Veri setindeki en son alışverişin yapıldığı tarihten 2 gün sonrasını analiz tarihi olarak alınız.
analysis_date = dt.datetime(2021, 6, 2)
           # 2.customer_id, recency_cltv_weekly, T_weekly, frequency ve monetary_cltv_avg değerlerinin yer aldığı yeni bir cltv dataframe'i oluşturunuz.
# recency: Son satın alma üzerinden geçen zaman. Haftalık. (kullanıcı özelinde)
# T: Müşterinin yaşı. Haftalık. (analiz tarihinden ne kadar süre önce ilk satın alma yapılmış)
# frequency: tekrar eden toplam satın alma sayısı (frequency>1)
# monetary: satın alma başına ortalama kazanç          

#date_columns = ['first_order_date', 'last_order_date', 'last_order_date_online', 'last_order_date_offline',]
cltv = df.groupby("master_id").agg(
    recency_cltv_weekly=('last_order_date', lambda x: (analysis_date - x.max()).days),
    T_weekly=('first_order_date', lambda x: (analysis_date - x.min()).days),
    frequency=('total_shopping', 'sum'),
    monetary_cltv_avg=('total_spending', 'sum')
).reset_index()






           # Monetary değeri satın alma başına ortalama değer olarak, recency ve tenure değerleri ise haftalık cinsten ifade edilecek.
cltv["monetary_cltv_avg"] = cltv["monetary_cltv_avg"] / cltv["frequency"]
cltv["recency_cltv_weekly"] = cltv["recency_cltv_weekly"] / 7
cltv["T_weekly"] = cltv["T_weekly"] / 7
cltv = cltv[(cltv['frequency'] > 1)]

# GÖREV 3: BG/NBD, Gamma-Gamma Modellerinin Kurulması, CLTV'nin hesaplanması
from lifetimes import BetaGeoFitter
from lifetimes import GammaGammaFitter
from lifetimes.plotting import plot_period_transactions

           # 1. BG/NBD modelini fit ediniz.
"""
penalizer_coef = parametre bulmak için uyglanacak ceza katsayıdır.
"""
bgf = BetaGeoFitter(penalizer_coef=0.001)

bgf.fit(cltv['frequency'],
        cltv['recency_cltv_weekly'],
        cltv['T_weekly'])
                # a. 3 ay içerisinde müşterilerden beklenen satın almaları tahmin ediniz ve exp_sales_3_month olarak cltv dataframe'ine ekleyiniz.
cltv["exp_sales_3_month"] = bgf.predict(12,
            cltv['frequency'],
            cltv['recency_cltv_weekly'],
            cltv['T_weekly'])
                # b. 6 ay içerisinde müşterilerden beklenen satın almaları tahmin ediniz ve exp_sales_6_month olarak cltv dataframe'ine ekleyiniz.
cltv["exp_sales_6_month"] = bgf.predict(24,
            cltv['frequency'],
            cltv['recency_cltv_weekly'],
            cltv['T_weekly'])

plot_period_transactions(bgf)
plt.show()
           # 2. Gamma-Gamma modelini fit ediniz. Müşterilerin ortalama bırakacakları değeri tahminleyip exp_average_value olarak cltv dataframe'ine ekleyiniz.
ggf = GammaGammaFitter(penalizer_coef=0.01)
ggf.fit(cltv['frequency'], cltv['monetary_cltv_avg'])
cltv["exp_average_value"] = ggf.conditional_expected_average_profit(cltv['frequency'],
                                                                             cltv['monetary_cltv_avg'])
           # 3. 6 aylık CLTV hesaplayınız ve cltv ismiyle dataframe'e ekleyiniz.
cltv["cltv"] = ggf.customer_lifetime_value(bgf,
                                   cltv['frequency'],
                                   cltv['recency_cltv_weekly'],
                                   cltv['T_weekly'],
                                   cltv['monetary_cltv_avg'],
                                   time=6,  # 3 aylık
                                   freq="W",  # T'nin frekans bilgisi.
                                   discount_rate=0.01)
                # b. Cltv değeri en yüksek 20 kişiyi gözlemleyiniz.
cltv.sort_values("cltv", ascending=False).head(20)

# GÖREV 4: CLTV'ye Göre Segmentlerin Oluşturulması
           # 1. 6 aylık tüm müşterilerinizi 4 gruba (segmente) ayırınız ve grup isimlerini veri setine ekleyiniz. cltv_segment ismi ile dataframe'e ekleyiniz.
cltv["cltv_segment"] =  pd.qcut(cltv["cltv"] , 4 , labels =["D","C","B","A"])

           # 2. 4 grup içerisinden seçeceğiniz 2 grup için yönetime kısa kısa 6 aylık aksiyon önerilerinde bulununuz
"""
For Low CLTV Customers, the focus should be on re-engagement and increasing loyalty through targeted campaigns and incentives.
For High CLTV Customers, maintaining loyalty through exclusive offers and personalized experiences can help sustain and potentially increase their value to the company.
Yüksek için = yüzde 50 indirim
Düşük için = 2.ürüne yüzde 50 indiirim
"""
# BONUS: Tüm süreci fonksiyonlaştırınız.







