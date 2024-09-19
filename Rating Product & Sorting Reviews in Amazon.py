
###################################################
# PROJE: Rating Product & Sorting Reviews in Amazon
###################################################

###################################################
# İş Problemi
###################################################

# E-ticaretteki en önemli problemlerden bir tanesi ürünlere satış sonrası verilen puanların doğru şekilde hesaplanmasıdır.
# Bu problemin çözümü e-ticaret sitesi için daha fazla müşteri memnuniyeti sağlamak, satıcılar için ürünün öne çıkması ve satın
# alanlar için sorunsuz bir alışveriş deneyimi demektir. Bir diğer problem ise ürünlere verilen yorumların doğru bir şekilde sıralanması
# olarak karşımıza çıkmaktadır. Yanıltıcı yorumların öne çıkması ürünün satışını doğrudan etkileyeceğinden dolayı hem maddi kayıp
# hem de müşteri kaybına neden olacaktır. Bu 2 temel problemin çözümünde e-ticaret sitesi ve satıcılar satışlarını arttırırken müşteriler
# ise satın alma yolculuğunu sorunsuz olarak tamamlayacaktır.

###################################################
# Veri Seti Hikayesi
###################################################

# Amazon ürün verilerini içeren bu veri seti ürün kategorileri ile çeşitli metadataları içermektedir.
# Elektronik kategorisindeki en fazla yorum alan ürünün kullanıcı puanları ve yorumları vardır.

# Değişkenler:
# reviewerID: Kullanıcı ID’si
# asin: Ürün ID’si
# reviewerName: Kullanıcı Adı
# helpful: Faydalı değerlendirme derecesi
# reviewText: Değerlendirme
# overall: Ürün rating’i
# summary: Değerlendirme özeti
# unixReviewTime: Değerlendirme zamanı
# reviewTime: Değerlendirme zamanı Raw
# day_diff: Değerlendirmeden itibaren geçen gün sayısı
# helpful_yes: Değerlendirmenin faydalı bulunma sayısı
# total_vote: Değerlendirmeye verilen oy sayısı



###################################################
# GÖREV 1: Average Rating'i Güncel Yorumlara Göre Hesaplayınız ve Var Olan Average Rating ile Kıyaslayınız.
###################################################

# Paylaşılan veri setinde kullanıcılar bir ürüne puanlar vermiş ve yorumlar yapmıştır.
# Bu görevde amacımız verilen puanları tarihe göre ağırlıklandırarak değerlendirmek.
# İlk ortalama puan ile elde edilecek tarihe göre ağırlıklı puanın karşılaştırılması gerekmektedir.


###################################################
# Adım 1: Veri Setini Okutunuz ve Ürünün Ortalama Puanını Hesaplayınız.
###################################################

import pandas as pd
import numpy as np
import scipy.stats as st
import math



pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)

df = pd.read_csv("amazon_review.csv")


df.head(10)


average_rating = df['overall'].mean()
print("Ürünün ortalama puanı:", average_rating)

###################################################
# Adım 2: Tarihe Göre Ağırlıklı Puan Ortalamasını Hesaplayınız.
###################################################
df.columns

df["reviewTime"] = pd.to_datetime(df["reviewTime"] )


df.sort_values("reviewTime",ascending=False).head(20)
current_date = pd.to_datetime("2014-12-09")
df["days"] = (current_date - df["reviewTime"]).dt.days


def time_wise_rating(df, w1=28, w2=26, w3=24, w4=22):
    result = (
    df.loc[df["day_diff"] <= 30, "overall"].mean() * w1 / 100
    + df.loc[(df["day_diff"] > 30) & (df["day_diff"] <= 60), "overall"].mean() * w2 / 100
    + df.loc[(df["day_diff"] > 60) & (df["day_diff"] <= 90), "overall"].mean() * w3 / 100
    + df.loc[df["day_diff"] > 90, "overall"].mean() * w4 / 100
)
    
    return result
       
time_wise_rating(df, 30, 26, 22, 22)


if time_wise_rating(df, 30, 26, 22, 22) > average_rating:
    print("Son zamanlardaki yorumlar daha olumlu.")
elif time_wise_rating(df, 30, 26, 22, 22) < average_rating:
    print("Son zamanlardaki yorumlar daha olumsuz.")
else:
    print("Yorumlar zaman içinde dengeli verilmiş.")



###################################################
# Görev 2: Ürün için Ürün Detay Sayfasında Görüntülenecek 20 Review'i Belirleyiniz.
###################################################





###################################################
# Adım 1. helpful_no Değişkenini Üretiniz
###################################################

# Not:
# total_vote bir yoruma verilen toplam up-down sayısıdır.
# up, helpful demektir.
# veri setinde helpful_no değişkeni yoktur, var olan değişkenler üzerinden üretilmesi gerekmektedir.

df["helpful_no"] = df["total_vote"] - df["helpful_yes"]


###################################################
# Adım 2. score_pos_neg_diff, score_average_rating ve wilson_lower_bound Skorlarını Hesaplayıp Veriye Ekleyiniz
###################################################

def score_pos_neg_diff(df):
    df["score_pos_neg_diff"] = df["helpful_yes"] - df["helpful_no"]
    return df["score_pos_neg_diff"]

score_pos_neg_diff(df)


def score_average_rating(df):
    df["score_average_rating"] = df["helpful_yes"] / df["total_vote"]
    return df["score_average_rating"]

score_average_rating(df)



def wilson_lower_bound(up, down, confidence=0.95):
    """
    Wilson Lower Bound Score hesapla

    - Bernoulli parametresi p için hesaplanacak güven aralığının alt sınırı WLB skoru olarak kabul edilir.
    - Hesaplanacak skor ürün sıralaması için kullanılır.
    - Not:
    Eğer skorlar 1-5 arasıdaysa 1-3 negatif, 4-5 pozitif olarak işaretlenir ve bernoulli'ye uygun hale getirilebilir.
    Bu beraberinde bazı problemleri de getirir. Bu sebeple bayesian average rating yapmak gerekir.

    Parameters
    ----------
    up: int
        up count
    down: int
        down count
    confidence: float
        confidence

    Returns
    -------
    wilson score: float

    """
    n = up + down
    if n == 0:
        return 0
    z = st.norm.ppf(1 - (1 - confidence) / 2)
    phat = 1.0 * up / n
    return (phat + z * z / (2 * n) - z * math.sqrt((phat * (1 - phat) + z * z / (4 * n)) / n)) / (1 + z * z / n)


df["wilson_lower_bound"] = df.apply(lambda x: wilson_lower_bound(x["helpful_yes"], x["helpful_no"]), axis=1)


##################################################
# Adım 3. 20 Yorumu Belirleyiniz ve Sonuçları Yorumlayınız.
###################################################

top_20_comments = df.nlargest(20, 'wilson_lower_bound')
df.sort_values("wilson_lower_bound", ascending=False).head(20)
