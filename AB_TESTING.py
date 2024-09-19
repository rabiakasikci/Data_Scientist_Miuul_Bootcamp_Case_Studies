#####################################################
# AB Testi ile BiddingYöntemlerinin Dönüşümünün Karşılaştırılması
#####################################################

#####################################################
# İş Problemi
#####################################################

# Facebook kısa süre önce mevcut "maximumbidding" adı verilen teklif verme türüne alternatif
# olarak yeni bir teklif türü olan "average bidding"’i tanıttı. Müşterilerimizden biri olan bombabomba.com,
# bu yeni özelliği test etmeye karar verdi veaveragebidding'in maximumbidding'den daha fazla dönüşüm
# getirip getirmediğini anlamak için bir A/B testi yapmak istiyor.A/B testi 1 aydır devam ediyor ve
# bombabomba.com şimdi sizden bu A/B testinin sonuçlarını analiz etmenizi bekliyor.Bombabomba.com için
# nihai başarı ölçütü Purchase'dır. Bu nedenle, istatistiksel testler için Purchasemetriğine odaklanılmalıdır.




#####################################################
# Veri Seti Hikayesi
#####################################################

# Bir firmanın web site bilgilerini içeren bu veri setinde kullanıcıların gördükleri ve tıkladıkları
# reklam sayıları gibi bilgilerin yanı sıra buradan gelen kazanç bilgileri yer almaktadır.Kontrol ve Test
# grubu olmak üzere iki ayrı veri seti vardır. Bu veri setleriab_testing.xlsxexcel’ininayrı sayfalarında yer
# almaktadır. Kontrol grubuna Maximum Bidding, test grubuna AverageBiddinguygulanmıştır.

# impression: Reklam görüntüleme sayısı
# Click: Görüntülenen reklama tıklama sayısı
# Purchase: Tıklanan reklamlar sonrası satın alınan ürün sayısı
# Earning: Satın alınan ürünler sonrası elde edilen kazanç



#####################################################
# Proje Görevleri
#####################################################

######################################################
# AB Testing (Bağımsız İki Örneklem T Testi)
######################################################

# 1. Hipotezleri Kur
# 2. Varsayım Kontrolü
#   - 1. Normallik Varsayımı (shapiro)
#   - 2. Varyans Homojenliği (levene)
# 3. Hipotezin Uygulanması
#   - 1. Varsayımlar sağlanıyorsa bağımsız iki örneklem t testi
#   - 2. Varsayımlar sağlanmıyorsa mannwhitneyu testi
# 4. p-value değerine göre sonuçları yorumla
# Not:
# - Normallik sağlanmıyorsa direkt 2 numara. Varyans homojenliği sağlanmıyorsa 1 numaraya arguman girilir.
# - Normallik incelemesi öncesi aykırı değer incelemesi ve düzeltmesi yapmak faydalı olabilir.




#####################################################
# Görev 1:  Veriyi Hazırlama ve Analiz Etme
#####################################################

# Adım 1:  ab_testing_data.xlsx adlı kontrol ve test grubu verilerinden oluşan veri setini okutunuz. Kontrol ve test grubu verilerini ayrı değişkenlere atayınız.

import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest



pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)




control_df = pd.read_excel("ab_testing.xlsx", sheet_name="Control Group")
test_df = pd.read_excel("ab_testing.xlsx", sheet_name="Test Group")

# Adım 2: Kontrol ve test grubu verilerini analiz ediniz.

control_df.describe().T
test_df.describe().T


sms.DescrStatsW(control_df["Purchase"]).tconfint_mean()
sms.DescrStatsW(control_df["Click"]).tconfint_mean()


# Adım 3: Analiz işleminden sonra concat metodunu kullanarak kontrol ve test grubu verilerini birleştiriniz.

all_df = pd.concat([control_df, test_df], axis=0)

control_df.columns
control_df.columns = ['Control_Impression', 'Control_Click', 'Control_Purchase', 'Control_Earning']
test_df.columns = ['Test_Impression', 'Test_Click', 'Test_Purchase', 'Test_Earning']


all_df = pd.concat([control_df, test_df], axis=1)



#####################################################
# Görev 2:  A/B Testinin Hipotezinin Tanımlanması
#####################################################

# Adım 1: Hipotezi tanımlayınız.

"""
############################
# 1. Hipotezi Kur
############################
M=purchase
# H0: M1 = M2
# H1: M1 != M2

############################
# 2. Varsayım Kontrolü
############################

# Normallik Varsayımı
# Varyans Homojenliği

############################
# Normallik Varsayımı
############################

# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1:..sağlanmamaktadır.


"""


# Adım 2: Kontrol ve test grubu için purchase(kazanç) ortalamalarını analiz ediniz

all_df.columns

all_df["Control_Purchase"].mean()
all_df["Test_Purchase"].mean()

"""
550.8940587702316
582.1060966484677
"""
#####################################################
# GÖREV 3: Hipotez Testinin Gerçekleştirilmesi
#####################################################

######################################################
# AB Testing (Bağımsız İki Örneklem T Testi)
######################################################


test_stat, pvalue = shapiro(all_df["Control_Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

test_stat, pvalue = shapiro(all_df["Test_Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# p-value < ise 0.05'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.
#Reddedemeyiz


# Adım 1: Hipotez testi yapılmadan önce varsayım kontrollerini yapınız.Bunlar Normallik Varsayımı ve Varyans Homojenliğidir.

test_stat, pvalue = levene(all_df["Control_Purchase"],
                           all_df["Test_Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# p-value < ise 0.05 'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.

#Rededilemez



# Kontrol ve test grubunun normallik varsayımına uyup uymadığını Purchase değişkeni üzerinden ayrı ayrı test ediniz





# Adım 2: Normallik Varsayımı ve Varyans Homojenliği sonuçlarına göre uygun testi seçiniz



""" Varsayımlar sağlanmaktadır """


test_stat, pvalue = ttest_ind(all_df["Control_Purchase"],
                              all_df["Test_Purchase"],
                              equal_var=True)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# p-value < ise 0.05 'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.

""" Null hipotezi Reddedilmez Eşittir Anlamlı bir fark yoktur"""

# Adım 3: Test sonucunda elde edilen p_value değerini göz önünde bulundurarak kontrol ve test grubu satın alma
# ortalamaları arasında istatistiki olarak anlamlı bir fark olup olmadığını yorumlayınız.


""" Null hipotezi Reddedilmez Eşittir Anlamlı bir fark yoktur. Şanssal bir şekilde ortaya çıkmıştır."""

##############################################################
# GÖREV 4 : Sonuçların Analizi
##############################################################

# Adım 1: Hangi testi kullandınız, sebeplerini belirtiniz.

"""
2 varsayım sağlandığı için bağımsız 2 örneklem t testi uygulandı 
p>0,05 olduğu için redddedilemez bu da 2 grup arası fark yoktur demek. Oluşan farklılık şanslar şekilde oluşmuştur.
"""


# Adım 2: Elde ettiğiniz test sonuçlarına göre müşteriye tavsiyede bulununuz.

