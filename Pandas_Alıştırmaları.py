# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 15:51:04 2024

@author: Rabia KAŞIKCI
"""



##################################################
# Pandas Alıştırmalar
##################################################

import numpy as np
import seaborn as sns
import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

#########################################
# Görev 1: Seaborn kütüphanesi içerisinden Titanic veri setini tanımlayınız.
#########################################
df = sns.load_dataset("titanic")

#########################################
# Görev 2: Yukarıda tanımlanan Titanic veri setindeki kadın ve erkek yolcuların sayısını bulunuz.
#########################################
gender_counts = df["sex"].value_counts()
print(gender_counts)


#########################################
# Görev 3: Her bir sutuna ait unique değerlerin sayısını bulunuz.
#########################################


for col in df.columns:
    print(col)
    print(len(df[col].unique()))
    
df.nunique()


#########################################
# Görev 4: pclass değişkeninin unique değerleri bulunuz.
#########################################

print(df["pclass"].unique())


#########################################
# Görev 5:  pclass ve parch değişkenlerinin unique değerlerinin sayısını bulunuz.
#########################################

print(len(df["pclass"].unique()))
print(len(df["parch"].unique()))


#########################################
# Görev 6: embarked değişkeninin tipini kontrol ediniz. Tipini category olarak değiştiriniz. Tekrar tipini kontrol ediniz.
#########################################
print(df["embarked"].dtype)
df["embarked"] = df["embarked"].astype("category")
print(df["embarked"].dtype)


#########################################
# Görev 7: embarked değeri C olanların tüm bilgelerini gösteriniz.
#########################################

print(df[df["embarked"] == "C"])


#########################################
# Görev 8: embarked değeri S olmayanların tüm bilgelerini gösteriniz.
#########################################

print(df[df["embarked"] != "S"])


#########################################
# Görev 9: Yaşı 30 dan küçük ve kadın olan yolcuların tüm bilgilerini gösteriniz.
#########################################
print(df[(df["age"] < 30) & (df["sex"] == "female")])


#########################################
# Görev 10: Fare'i 500'den büyük veya yaşı 70 den büyük yolcuların bilgilerini gösteriniz.
#########################################

print(df[(df["fare"] > 500 ) | (df["age"] > 70)])


#########################################
# Görev 11: Her bir değişkendeki boş değerlerin toplamını bulunuz.
#########################################

for col in df.columns:
    print(df[col].isnull().sum())


#########################################
# Görev 12: who değişkenini dataframe'den düşürün.
#########################################

df = df.drop(columns=['who'])


#########################################
# Görev 13: deck değikenindeki boş değerleri deck değişkenin en çok tekrar eden değeri (mode) ile doldurunuz.
#########################################

df["deck"].fillna(df['deck'].mode()[0], inplace=True)



#########################################
# Görev 14: age değikenindeki boş değerleri age değişkenin medyanı ile doldurun.
#########################################

df['age'].fillna(df['age'].median(), inplace=True)


#########################################
# Görev 15: survived değişkeninin Pclass ve Cinsiyet değişkenleri kırılımınında sum, count, mean değerlerini bulunuz.
#########################################

print(df.groupby(["pclass", "sex"])["survived"].agg(["sum", "count" ,"mean"]).reset_index())

#########################################
# Görev 16:  30 yaşın altında olanlar 1, 30'a eşit ve üstünde olanlara 0 vericek bir fonksiyon yazınız.
# Yazdığınız fonksiyonu kullanarak titanik veri setinde age_flag adında bir değişken oluşturunuz oluşturunuz. (apply ve lambda yapılarını kullanınız)
#########################################


df["age_flag"] = df["age"].apply(lambda x: 1 if x < 30 else 0 )


#########################################
# Görev 17: Seaborn kütüphanesi içerisinden Tips veri setini tanımlayınız.
#########################################

df_tips = sns.load_dataset("tips")



#########################################
# Görev 18: Time değişkeninin kategorilerine (Dinner, Lunch) göre total_bill  değerlerinin toplamını, min, max ve ortalamasını bulunuz.
#########################################

print(df_tips.groupby(["time"])["total_bill"].agg(["sum","min", "max" ,"mean"]).reset_index())

#########################################
# Görev 19: Günlere ve time göre total_bill değerlerinin toplamını, min, max ve ortalamasını bulunuz.
#########################################

print(df_tips.groupby(["time", "day"])["total_bill"].agg(["sum","min", "max" ,"mean"]).reset_index())


#########################################
# Görev 20:Lunch zamanına ve kadın müşterilere ait total_bill ve tip  değerlerinin day'e göre toplamını, min, max ve ortalamasını bulunuz.
#########################################

filtered_df_tips = df_tips[(df_tips["time"] == "Lunch") & ((df_tips["sex"] == "Female"))]

result = filtered_df_tips.groupby('day').agg({'total_bill': ['sum', 'min', 'max', 'mean'],
                                          'tip': ['sum', 'min', 'max', 'mean']}).reset_index()

#########################################
# Görev 21: size'i 3'ten küçük, total_bill'i 10'dan büyük olan siparişlerin ortalaması nedir?
#########################################
average_order  = df_tips[(df_tips["size"] < 3 ) & (df_tips["total_bill"] > 10)]
mean_values = average_order[['total_bill', 'tip', 'size']].mean()

#########################################
# Görev 22: total_bill_tip_sum adında yeni bir değişken oluşturun. Her bir müşterinin ödediği totalbill ve tip in toplamını versin.
#########################################

df_tips["total_bill_tip_sum"] = df_tips['total_bill'] + df_tips['tip']


#########################################
# Görev 23: total_bill_tip_sum değişkenine göre büyükten küçüğe sıralayınız ve ilk 30 kişiyi yeni bir dataframe'e atayınız.
#########################################

df_tips = df_tips.sort_values(by='total_bill_tip_sum', ascending=False)
fist_30 = df_tips[:30]