# -*- coding: utf-8 -*-
"""
Created on Sat Aug 24 19:58:30 2024

@author: Rabia KAŞIKCI
"""

###############################################
# Python Alıştırmalar
###############################################

###############################################
# GÖREV 1: Veri yapılarının tipleriniz inceleyiniz.
###############################################

x = 8


y = 3.2


z = 8j + 18


a = "Hello World"


b = True


c = 23 < 22



l = [1, 2, 3, 4,"String",3.2, False]



d = {"Name": "Jake",
     "Age": [27,56],
     "Adress": "Downtown"}


t = ("Machine Learning", "Data Science")



s = {"Python", "Machine Learning", "Data Science","Python"}


print(type(x),type(y),type(z),type(a),type(b),type(c),type(l),type(d),type(t),type(s))

###############################################
# GÖREV 2: Verilen string ifadenin tüm harflerini büyük harfe çeviriniz. Virgül ve nokta yerine space koyunuz, kelime kelime ayırınız.
###############################################

text = "The goal is to turn data into information, and information into insight."
new_text = text.upper().replace(",", " ").replace(".", " ").split()

###############################################
# GÖREV 3: Verilen liste için aşağıdaki görevleri yapınız.
###############################################

lst = ["D","A","T","A","S","C","I","E","N","C","E"]

# Adım 1: Verilen listenin eleman sayısına bakın.
print(len(lst))

# Adım 2: Sıfırıncı ve onuncu index'teki elemanları çağırın.

print(lst[0],lst[10])

# Adım 3: Verilen liste üzerinden ["D","A","T","A"] listesi oluşturun.
print(lst[:4])

# Adım 4: Sekizinci index'teki elemanı silin.

lst.pop(8)

# Adım 5: Yeni bir eleman ekleyin.

lst.append("*")

# Adım 6: Sekizinci index'e  "N" elemanını tekrar ekleyin.

lst.insert(8, "N")

###############################################
# GÖREV 4: Verilen sözlük yapısına aşağıdaki adımları uygulayınız.
###############################################

dict = {'Christian': ["America",18],
        'Daisy':["England",12],
        'Antonio':["Spain",22],
        'Dante':["Italy",25]}


# Adım 1: Key değerlerine erişiniz.
keys = dict.keys()
print(keys)


# Adım 2: Value'lara erişiniz.

values = dict.values()
print(values)

# Adım 3: Daisy key'ine ait 12 değerini 13 olarak güncelleyiniz.
dict['Daisy'][1] = 13



# Adım 4: Key değeri Ahmet value değeri [Turkey,24] olan yeni bir değer ekleyiniz.

dict['Ahmet'] = ["Turkey", 24]


# Adım 5: Antonio'yu dictionary'den siliniz.


del dict['Antonio']



###############################################
# GÖREV 5: Arguman olarak bir liste alan, listenin içerisindeki tek ve çift sayıları ayrı listelere atıyan ve bu listeleri return eden fonskiyon yazınız.
###############################################

l = [2,13,18,93,22]

def separate_numbers(list_value):
    odd_number=[]
    even_number=[]
    for i in list_value:
        if i%2==0:
            even_number.append(i)
        else:
            odd_number.append(i)
    return odd_number,even_number

odd_number,even_number = separate_numbers(l)
print("Odd numbers:", odd_number)
print("Even numbers:", even_number)

###############################################
# GÖREV 6: Aşağıda verilen listede mühendislik ve tıp fakülterinde dereceye giren öğrencilerin isimleri bulunmaktadır.
# Sırasıyla ilk üç öğrenci mühendislik fakültesinin başarı sırasını temsil ederken son üç öğrenci de tıp fakültesi öğrenci sırasına aittir.
# Enumarate kullanarak öğrenci derecelerini fakülte özelinde yazdırınız.
###############################################

ogrenciler = ["Ali","Veli","Ayşe","Talat","Zeynep","Ece"]

for index, student in enumerate(ogrenciler[:3]):
    print("Mühendislik Fakültesi",index+1,". öğrenci", student  )

for index, student in enumerate(ogrenciler[3:]):
    print("Tıp Fakültesi",index+1,". öğrenci", student )

###############################################
# GÖREV 7: Aşağıda 3 adet liste verilmiştir. Listelerde sırası ile bir dersin kodu, kredisi ve kontenjan bilgileri yer almaktadır. Zip kullanarak ders bilgilerini bastırınız.
###############################################

ders_kodu = ["CMP1005","PSY1001","HUK1005","SEN2204"]
kredi = [3,4,2,4]
kontenjan = [30,75,150,25]

zipped_list = list(zip(ders_kodu,kredi,kontenjan))




for i in range(len(zipped_list)):
    print("Kredisi ",zipped_list[i][1],"olan",zipped_list[i][0],"kodlu dersin kontenjanı",zipped_list[i][2],"kişidr.")
###############################################
# GÖREV 8: Aşağıda 2 adet set verilmiştir.
# Sizden istenilen eğer 1. küme 2. kümeyi kapsiyor ise ortak elemanlarını eğer kapsamıyor ise 2. kümenin 1. kümeden farkını yazdıracak fonksiyonu tanımlamanız beklenmektedir.
###############################################

kume1 = set(["data", "python"])
kume2 = set(["data", "function", "qcut", "lambda", "python", "miuul"])





def find_similar(set_a, set_b):
    if set_a.issubset(set_b):  # set_a set_b'yi kapsıyor mu?
        print("Ortak Elemanlar:", set_a.intersection(set_b))
    else:
        print("Set B'de olup Set A'da olmayan:", set_b.difference(set_a))

find_similar(kume1, kume2)


