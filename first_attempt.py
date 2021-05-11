# Hola! Mi intención en este script es comentar como fui haciendo las tablas para luego obtener los graficos en tableau.
#Cualquier feedback es bienvenido :D


#En cuanto a la automatizacion, utilicé tableau public conectado a google docs. Respetando el nombre de las variables y
#de las hojas no tuve problema en agregar o quitar hojas y/o tablas. Basicamente guardé los .csv exportados aqui y luego los subi a mi drive
# Sé que existe una api para cierta version de tableau como asi tambien
# es posible conectar tableau public a google docs y manejarlo con python a traves de la api de google.
# No utilicé estas opciones porque entiendo que no son gratuitas.


#Libreria necesaria
import pandas as pd
#Lectura de datos
path = "C:/Users/fvegamaza/PycharmProjects/challenger_brain_network"
df = pd.read_spss(path + "/Base Ejercicio BRN 2020.sav")
#Transformo a enteros el ID
df["responseID"] = df["responseID"].astype(int)

#Actividad 1
df = df.melt(id_vars=['responseID'])
#Es usual para mi usar el Melt(), por lo que lo conocía.
#Sobretodo en algunas predicciones porque es necesario para tener eventos unicos formando el id del usuario(acá el melt) y luego un merge con alguna marca temporal

df = df.sort_values(by = ["responseID","variable"])
df = df.rename(columns={'value':'valor'})
df = df.set_index("responseID")
df.to_csv("BRN 2020.csv",sep=",", header=True) #Aquí la actividad 1 es copletada


#Q24 Antiguedad
df1 = df[df["variable"] == "Q24"] #Para obtener la antiguedad con sus respectivos ids
df1.to_csv("antiguedad.csv",sep=",", header=True)

#Q48 Banco Operativo
df2 = df[df["variable"].str.contains("Q48")].copy(deep= True) #No recordaba como hacerlo, lo obtuve de aquí: Filter by string https://stackoverflow.com/questions/48020296/how-to-filter-pandas-dataframe-by-string
df2.isna().sum() #4454 na - Asumo que cuando las respuestas multiples no se marcan se lo computa como nan
df2 = df2.dropna()
df2["valor"].value_counts() #402 string vacios
df2["valor"].iloc[3] #ejemplo
df2 = df2[df2["valor"] != ''] #Me quedo con todos los string diferentes a ''
df2["valor"].value_counts() #Esta ok para exportar
df2.to_csv("Q48.csv",sep=",", header=True, encoding= "utf-8") # Con esta tabla elaboré los graficos acerca en qué banco operan los encuestados

#Q49 Banco Principal
df3 = df[df["variable"] == "Q49"].copy(deep=True)
df3.value_counts()
df3.valor.iloc[6] #Limpio errores de codificacion
df3 = df3["valor"].replace('17. ITAÃš', "17. ITAU").replace('9. NACIÃ“N','9. NACION').replace('29. PROV. DE CORDOBA (BANCOR)','29. BANCOR')
df3 = pd.DataFrame(df3)
df3.to_csv("Q49.csv", sep= ",", header=True)


#Q52 Recomendacion
df4 = df[df["variable"].str.contains("Q52")].copy(deep= True)
df4.isna().sum() #4454 na - Asumo que cuando las respuesta multiples no se marcan se lo computa como nan
df4 = df4.dropna()
df4["variable"].value_counts()

#En este momento al comparar el df4 y el df2 correspondientes a las preguntas A13 Y A9 respectivamente
# me di cuenta que la segunda parte del nombre de las variables "Q52R7", el valor luego de la R corresponde
# al numero de celda y no necesariamente a la codificacion por banco presentada en la columnas
# Por ejemplo, el banco Patagonia tiene asignado el numero 13 en el cuestionario, pero en el df las filas correspondientes a este banco son las "R10"

listado= {
"Q52R1":"SANTANDER",
"Q52R2":"BAPRO",
"Q52R3":"GALICIA ",
"Q52R4":"HSBC ",
"Q52R5":"CREDICOOP",
"Q52R6":"ICBC",
"Q52R7":"BBVA",
"Q52R8":"NACIÓN",
"Q52R9":"MACRO",
"Q52R10":"PATAGONIA",
"Q52R11":"CIUDAD ",
"Q52R12":"COMAFI",
"Q52R13":"ITAÚ",
"Q52R14":"SUPERVIELLE",
"Q52R15":"MUNICIPAL DE ROSARIO",
"Q52R17":"BANCOR",
"Q52R30":"nan"} #Esto lo hice con un editor de texto, es solo para identificar los bancos
df4= df4.replace({"variable":listado}) #Aqui reemplazo
df4["variable"].value_counts()

df4.drop((df4[df4["valor"] == 'NS/NC'].index),inplace=True) #Asumo como Nulos las resppuestas "NS/NC"

df4["valor2"] = "reemplazar" # Creo una nueva columna para reemplazar luego

df4["valor"] = df4["valor"].astype(int) #Me fue necesario convertirlo a int para utilizar operadores logicos

#La siguiente parte del codigo fue la solución que encontré para modificar "manualmente" los bins, dado que
#luego de intentar en Tableau no logré hacerlo como espeficicaba la consigna. Este codigo hace el trabajo igualmente:

df4.loc[df4["valor"] <= 6, "valor2"] = "1 a 6"
df4.loc[df4["valor"] == 7, "valor2"] = "7 y 8"
df4.loc[df4["valor"] == 8, "valor2"] = "7 y 8"
df4.loc[df4["valor"] == 9, "valor2"] = "9 y 10"
df4.loc[df4["valor"] == 10, "valor2"] = "9 y 10"
df4.to_csv("Q52.csv", sep= ",", header=True)

#Q51 #Satisfacción
df5 = df[df["variable"].str.contains("Q51")].copy(deep= True) #El mismo filtrado que las variables anterior. Si contiene "Q51" sin importar lo siguiente es util en este punto
df5.isna().sum() #4454 na
df5 = df5.dropna()
df5.drop((df5[df5["valor"] == 'NS/NC'].index),inplace=True)
df5["valor"].value_counts() #402 string vacios

# Dado que ya utilicé un listado para matchear y que las respuestas en el cuestionarios de a12 y a13 se responden en concordancia a lo respondido en a9
# Hice un outer join basandome en el ID de los encuestados para luegos sacar el promedio
df5_df4_outer = pd.merge(df4, df5, on='responseID', how='outer')
del df5_df4_outer["valor2"],df5_df4_outer["variable_y"]
df5_df4_outer = df5_df4_outer.dropna()
df5_df4_outer["valor_y"] = df5_df4_outer["valor_y"].astype(int)
df5_df4_outer["avg_xy"] = (df5_df4_outer["valor_x"] + df5_df4_outer["valor_y"]) // 2
df5_df4_outer.to_csv("Q51.csv", sep= ",", header=True)