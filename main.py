#Datasetini kontrol ve test olucak şekilde ayrı ayrı okumak
import pandas as pd
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import shapiro, levene, ttest_ind

pd.set_option('display.max_columns',None)
pd.set_option('display.expand_frame_repr',False)
pd.set_option('display.float_format',lambda x: '%.5f' %x)

df_control=pd.read_excel("ab_testing.xlsx",sheet_name="Control Group")
df_test=pd.read_excel("ab_testing.xlsx",sheet_name="Test Group")

#Datasetin özelliklerini görüntülemek için fonksiyon oluşturmak
def check_df(dataframe):
    print("#################SHAPE#################")
    print(dataframe.shape)
    print("#################TYPES#################")
    print(dataframe.dtypes)
    print("#################HEAD#################")
    print(dataframe.head())
    print("#################TAIL#################")
    print(dataframe.tail())
    print("#################NA#################")
    print(dataframe.isnull().sum())
    print("#################Quantiles#################")
    print(dataframe.quantile([0, 0.05, 0.50, 0.95, 0.99, 1]).T)

check_df(df_control)
check_df(df_test)

#Kontrol ve Test grubu verilerini datasetlerine dahil etmek ve daha sonra bu iki ayrı datasetini birleştirmek
df_control["group"]="control"
df_test["group"]="test"
df = pd.concat([df_control,df_test], axis=0,ignore_index=False)

#AB Hipotezinin Tanımlanması

# H0: M1=M2 (Kontrol grubu ve test grubu satın almaları arasında istatiksel bir farklılık yoktur)
# H1: M1!=M2 (Kontrol grubu ve test grubu satın almaları arasında istatiksel bir farklılık vardır)

#Kontrol ve test grubu için purchase(kazanç) ortalamasını incelemek
grouped_data=df.groupby("group").agg({"Purchase":"mean"})

# Çubuk grafik oluşturma
grouped_data.plot(kind='bar', legend=False)
plt.title('Grup Bazında Ortalama Satın Alma Miktarı')
plt.xlabel('Grup')
plt.ylabel('Ortalama Satın Alma Miktarı')
plt.show()

#Box Plot
sns.boxplot(x='group', y='Purchase', data=df)
plt.title('Ortalama Satın Alma Miktarı Grup Bazında')
plt.xlabel('Grup')
plt.ylabel('Ortalama Satın Alma Miktarı')
plt.show()

#Varsayım Kontrollerinin Yapılması
#1-)Normallik Varsayımı:
#H0: Normal dağılım varsayımı sağlanmaktadır.
#H1: Normal dağılım varsayımı sağlanmamaktadır.
#p< 0.05 H0 RED , p>0.05 H0 REDDEDİLEMEZ.

#2-)Varyans Homojenliği:
#H0: Varyanslar homojendir.
#H1: Varyanslar homojen değildir.
#p< 0.05 H0 RED , p>0.05 H0 REDDEDİLEMEZ.

#NORMALLİK VARSAYIMI
test_stat,pvalue=shapiro(df.loc[df["group"]=="control","Purchase"])
print(pvalue)
test_stat,pvalue=shapiro(df.loc[df["group"]=="test","Purchase"])
print(pvalue)

#Normallik varsayımı 2 kategori içinde sağlanmıştır çünkü 2 kategoride de pvalue>0.05
#H0 REDDEDİLEMEZ!

#VARYANS HOMOJENLİĞİ
test_stat,pvalue=levene(df.loc[df["group"]=="control","Purchase"],
                        df.loc[df["group"]=="test","Purchase"])
print(pvalue)

#Varyanslar homojendir çünkü pvalue>0.05. H0 REDDEDİLEMEZ!

#Varsayımlar sağlandığı için bağımsız iki örneklem t testi (parametrik test) uygulanmalıdır.
test_stat,pvalue=ttest_ind(df.loc[df["group"]=="control","Purchase"],
                        df.loc[df["group"]=="test","Purchase"],equal_var=True)
print(pvalue)

#H0 reddilemediğinden dolayı bu bağlamda satın alma anlamında bir fark yoktur.Satın alma yöntemlerinden birisi seçilebilir.(Diğer istatistiksel farklar göz ardı edinilmek koşuluyla)

