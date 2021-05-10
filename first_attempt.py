import pandas as pd
import re
path = "C:/Users/fvegamaza/PycharmProjects/challenger_brain_network"

df = pd.read_spss(path + "/Base Ejercicio BRN 2020.sav")
df["responseID"] = df["responseID"].astype(int)

df = df.melt(id_vars=['responseID'])
df = df.sort_values(by = ["responseID","variable"])
df = df.rename(columns={'value':'valor'})
df = df.set_index("responseID")
df.to_csv("BRN 2020.csv",sep=",", header=True)



df1 = df[df["variable"] == "Q24"] #Para obtener la antiguedad con sus respectivos ids
df1.to_csv("antiguedad.csv",sep=",", header=True)



df2 = df[df["variable"].str.contains("Q48")].copy(deep= True) #Filter by string https://stackoverflow.com/questions/48020296/how-to-filter-pandas-dataframe-by-string
df2.isna().sum() #4454 na - Asumo que cuando las respuesta multiples no se marca se lo computa como na
df2 = df2.dropna()
df2["valor"].value_counts() #402 string vacios - verificaria si no hay un error en el procesamiento
df2["valor"].iloc[3] #ejemplo
df2 = df2[df2["valor"] != '']
