import pandas as pd
path = "C:/Users/fvegamaza/PycharmProjects/challenger_brain_network"

df = pd.read_spss(path + "/Base Ejercicio BRN 2020.sav")
df["responseID"] = df["responseID"].astype(int)

df = df.melt(id_vars=['responseID'])
df = df.sort_values(by = ["responseID","variable"])
df = df.rename(columns={'value':'valor'})
df = df.set_index("responseID")
df.to_csv("BRN 2020.csv",sep=",", header=True)



df[df["variable"] == "Q24"].value_counts() #Para graficar antiguedad