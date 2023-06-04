# -*- coding: utf-8 -*-
"""Morales,_Moreno,_Lemus_Trabajo_Final_Segunda_Entrega_Analítica_1 (2).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZW8RoOA6S95FbefRg9gR_wBpXOU_l7aU
    
FACULTAD DE INGENIERÍA<br>
DEPARTAMENTO DE INGENIERÍA INDUSTRIAL<br>
INTRODUCCIÓN A LA ANALÍTICA DE NEGOCIOS<br>
TRABAJO DEL CURSO - SEGUNDA ENTREGA: 15% <br>
Semestre 2023-01<br>

Equipo de trabajo: Aura Luz Moreno Díaz, Marcelo Lemus, Verónica Andrea Morales González

---

# **Carga de datos**

*Carga de las librerias necesarias para la ejecución del código. En este caso usaremos Pandas y Numpy renombrándolas como pd y np*
"""

#Carga de las librerias necesarias para la ejecución del código
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots

#Realizamos pruebas para verificar que haya conexión a la base de datos
AH  = pd.read_csv('https://www.4minds.solutions/tarea/final/BDALARMAHUMO.csv', sep=';',  low_memory=False) #Base de datos de Alarmas de Humo
MOR = pd.read_csv('https://www.4minds.solutions/tarea/final/BDMORTALIDAD.csv', sep=';',  low_memory=False) #Base de datos de Mortalidad
ROC = pd.read_csv('https://www.4minds.solutions/tarea/final/BDROCIADORES.csv', sep=';',  low_memory=False) #Base de datos de Rociadores
DES = pd.read_csv('https://www.4minds.solutions/tarea/final/BDGENERALDESASTRES.csv', sep=';',  low_memory=False) #Base de datos de Desastres en general

MOR.rename(columns={'GEO':'GEO','Casualties':'Incidents&Casualties', 'REF_DATE':'YEAR'}, inplace=True)

ROC.rename(columns={'GEO':'GEO','Incidents and casualties':'Incidents&Casualties','Performance of sprinkler system, structural fires':'performance_of_system','REF_DATE':'YEAR'}, inplace=True)

AH.rename(columns={'GEO':'GEO','Incidents and casualties':'Incidents&Casualties','Performance of smoke alarm device, residential fires':'performance_of_system','REF_DATE':'YEAR'},inplace=True)

#DE la base de datos de desastres quitaremos los puntos para poder hacer bien los cálculos numéricos
DES['ESTIMATED TOTAL COST'] = DES['ESTIMATED TOTAL COST'].str.replace('.', '')

#DE la base de datos de desastres quitaremos los puntos para poder hacer bien los cálculos numéricos
DES['NORMALIZED TOTAL COST'] = DES['NORMALIZED TOTAL COST'].astype(str)
DES['NORMALIZED TOTAL COST'] = DES['NORMALIZED TOTAL COST'].str.replace('.', '')

# concatenar las bases
CON = pd.concat([AH, MOR, ROC])

#Quitamos los espacios en blanco y pasamos a minusculas de la nueva tabla
CON['GEO'] = CON['GEO'].apply(lambda x: x.lower().strip() if pd.notnull(x) else x )
CON['performance_of_system'] = CON['performance_of_system'].apply(lambda x: x.lower().strip() if pd.notnull(x) else x )
CON['Incidents&Casualties'] = CON['Incidents&Casualties'].apply(lambda x: x.lower().strip() if pd.notnull(x) else x )
CON['Status of casualty'] = CON['Status of casualty'].apply(lambda x: x.lower().strip() if pd.notnull(x) else x )
CON['Type of structure'] = CON['Type of structure'].apply(lambda x: x.lower().strip() if pd.notnull(x) else x )

#Quitamos los espacios en blanco y pasamos a minusculas de la tabla general de desastres
DES['EVENT GROUP'] = DES['EVENT GROUP'].apply(lambda x: x.lower().strip() if pd.notnull(x) else x )
DES['EVENT SUBGROUP'] = DES['EVENT SUBGROUP'].apply(lambda x: x.lower().strip() if pd.notnull(x) else x )
DES['EVENT TYPE'] = DES['EVENT TYPE'].apply(lambda x: x.lower().strip() if pd.notnull(x) else x )
DES['PLACE'] = DES['PLACE'].apply(lambda x: x.lower().strip() if pd.notnull(x) else x )

# guardamos el df con las columnas definidas para ser analizadas de acuerdo con el contenido de las tres bases concatenadas.
CONS = CON.loc[:, ['YEAR', 'GEO', 'performance_of_system', 'Incidents&Casualties', 'VALUE', 'Status of casualty', 'Type of structure']]

# guardamos el df con las columnas definidas para ser analizadas de acuerdo con su contenido - para la base general de incendios
DESA = DES.loc[:, ['EVENT GROUP', 'EVENT SUBGROUP', 'EVENT TYPE', 'EVENT START DATE', 'FATALITIES', 'INJURED / INFECTED', 'ESTIMATED TOTAL COST', 'NORMALIZED TOTAL COST', 'MAGNITUDE', 'PLACE']]


# remplazar las categorías en GEO -Homologacion
CONS['GEO'] = CONS['GEO'].replace(['canadian armed forces'], 'canada')

# reemplazar las categorías en EVENT GROUP
DESA['EVENT GROUP'] = DESA['EVENT GROUP'].replace(['0', '1', '2', '47', '93'], 'SIN')

# remplazar las categorías en EVENT SUBGROUP
DESA['EVENT SUBGROUP'] = DESA['EVENT SUBGROUP'].replace(['0', '25', '45', '6'], 'SIN')
DESA['EVENT SUBGROUP'] = DESA['EVENT SUBGROUP'].replace(['arson'], 'fire')
DESA['EVENT SUBGROUP'] = DESA['EVENT SUBGROUP'].replace(['hijacking'], 'civil incident')

# remplazar las categorías en EVENT TYPE
DESA['EVENT TYPE'] = DESA['EVENT TYPE'].replace(['3000', '10000', '1400', '4900', '3200', '65000', '500', '560', '0', '2000'], 'SIN')
DESA['EVENT TYPE'] = DESA['EVENT TYPE'].replace(['storms and severe thunderstorms', 'winter storm', 'hurricane / typhoon / tropical storm', 'storm - unspecified / other', 'geomagnetic storm'], 'storm')
DESA['EVENT TYPE'] = DESA['EVENT TYPE'].replace(['tornado'], 'air')
DESA['EVENT TYPE'] = DESA['EVENT TYPE'].replace(['wildfire'], 'fire')
DESA['EVENT TYPE'] = DESA['EVENT TYPE'].replace(['heat event','drought' ], 'head event/drought')
DESA['EVENT TYPE'] = DESA['EVENT TYPE'].replace(['vehicle','vehicle release', 'transportation'], 'vehicle')
DESA['EVENT TYPE'] = DESA['EVENT TYPE'].replace(['rioting'], 'disturbance / demonstrations')
DESA['EVENT TYPE'] = DESA['EVENT TYPE'].replace(['pandemic', 'infestation', 'epidemic'], 'infestation/epidemic/pandemic')


#Para performance_of_system, value, status of casualty y type of structure agruparemos los nulos en "n.i." que significa que no hay información para que queden allá todos los no identificados
CONS['performance_of_system'] = CONS['performance_of_system'].fillna('SIN')
CONS['VALUE'] = CONS['VALUE'].fillna('SIN')
CONS['Status of casualty'] = CONS['Status of casualty'].fillna('SIN')
CONS['Type of structure'] = CONS['Type of structure'].fillna('SIN')

DESA['EVENT GROUP'] = DESA['EVENT GROUP'].fillna('SIN')
DESA['EVENT SUBGROUP'] = DESA['EVENT SUBGROUP'].fillna('SIN')
DESA['EVENT TYPE'] = DESA['EVENT TYPE'].fillna('SIN')
DESA['EVENT START DATE'] = DESA['EVENT START DATE'].fillna('SIN')
DESA['FATALITIES'] = DESA['FATALITIES'].fillna('SIN')
DESA['INJURED / INFECTED'] = DESA['INJURED / INFECTED'].fillna('SIN')
DESA['MAGNITUDE'] = DESA['MAGNITUDE'].fillna('SIN')


DESA.head()

CONS.head()


#Convertimos la columna "EVENT START DATE" a formato de datetime - TRANSFORMACIONES
DESA['EVENT START DATE']=pd.to_datetime(DESA['EVENT START DATE'],errors='coerce')

# Creamos las nuevas variables YEAR , MONTH , DAY 
DESA.insert(0,'YEAR', DESA.loc[DESA['EVENT START DATE'].notnull(), 'EVENT START DATE'].dt.year)
DESA.insert(1,'MONTH', DESA.loc[DESA['EVENT START DATE'].notnull(), 'EVENT START DATE'].dt.month)
DESA.insert(2,'DAY', DESA.loc[DESA['EVENT START DATE'].notnull(), 'EVENT START DATE'].dt.day)

#Las columnas YEAR , MONTH , DAY quedaron como flotantes, por haber valores null en las fechas. Convertimos los valores null de estos nuevos campos al valor entero 0.
DESA['YEAR']=DESA['YEAR'].fillna(0).astype(int)
DESA['MONTH']=DESA['MONTH'].fillna(0).astype(int)
DESA['DAY']=DESA['DAY'].fillna(0).astype(int)

#Ahora convertimos los campos a valor entero.
DESA['YEAR']=DESA['YEAR'].astype(int)
DESA['MONTH']=DESA['MONTH'].astype(int)
DESA['DAY']=DESA['DAY'].astype(int)

#Queremos que en el campo MONTH aparezca el nombre del mes y no un numero entero. 
import calendar
DESA['MONTH'] = DESA['MONTH'].apply(lambda x: calendar.month_abbr[x] if x != 0 else '')

DESA.head()

#EVENT START DATE contiene valores nulos, ya que fue una columna que fue desglosada, procedemos a eliminarla.
DESA = DESA.drop('EVENT START DATE', axis=1)

###Desastres en Canadá: influencia sobre la población y un enfoque sobre los incendios

# **Se revisa a nivel general, cómo es la distribución de la cantidad de desastres por cada tipo y cuál es el que tiene mayor ocurrencia en el periodo.**

desastre=DESA['EVENT TYPE'].value_counts()
desastre_df = pd.DataFrame({'EVENT TYPE': desastre.index, 'Cantidad desastres': desastre.values})
figd = px.bar(desastre_df, x='EVENT TYPE', y='Cantidad desastres', labels={'EVENT TYPE': 'Tipo de desastre', 'desastre_df': 'Tipo de desastre'})

figd.show()
### Dentro de la base general de desastres, se encuentra que el desastre de mayor ocurrencia es el de *inundaciones*, en segundo lugar las *tormentas* y en tercer lugar los *incendios*, por lo tanto, hacer énfases en el tipo de desastres de incendios vale la pena, ya que está en el top 3 de ocurrencia, sin embargo, sería interesante indagar sobre algunos datos de las inundaciones y de las tormentas, aunque estos tipos de desastres, tienen menos posibilidades de ser controlados.

# **Se realiza el ejercicio de ocurrencia de desastres por inundaciones por año**

#Filtramos los registros que corresponden a inundaciones
inundaciones = DESA[DESA['EVENT TYPE'] == 'flood']

#calculamos la cantidad de inundaciones por año
cantidad_Inundaciones_por_año = inundaciones['YEAR'].value_counts().sort_index()

dataI = pd.DataFrame({'Año': cantidad_Inundaciones_por_año.index, 'Cantidad de Inundaciones': cantidad_Inundaciones_por_año.values})

dataI.plot( 'Año' , 'Cantidad de Inundaciones' )

# En comparación con la ocurrencia de incendios, se tiene una misma tendencia, ya que la mayor cantidad de ocurrencia de este tipo desastres ha sido durante los últimos años; de 1970 y 1980 en adelante.

# **Se realiza también el ejercicio de ocurrencia de desastres por tormentas por año para ver su comportamiento en el tiempo**

import numpy as np
import matplotlib.pyplot as plt

#Filtramos los registros que corresponden a tormentas
tormentas = DESA[DESA['EVENT TYPE'] == 'storm']

#calculamos la cantidad de tormentas por año
cantidad_tormentas_por_año = tormentas['YEAR'].value_counts().sort_index()

dataT = pd.DataFrame({'Año': cantidad_tormentas_por_año.index, 'Cantidad de tormentas': cantidad_tormentas_por_año.values})

dataT.plot( 'Año' , 'Cantidad de tormentas' )
# En comparación con la ocurrencia de incendios y la ocurrencia de inundaciones, se tiene una misma tendencia, ya que la mayor cantidad de ocurrencia de este tipo desastres ha sido durante los últimos años; de 1970 y 1980 en adelante.
# A nivel general, puede decirse que el top 3 de desastres, conformado por inundaciones, tormentas e incendios, tienen una misma tendencia de comportamiento en el tiempo en cuanto a la cantidad de eventos ocurridos. Podría especularse, que a principios de siglo, quizá la ocurrencia haya sido similar, pero los datos no hayan quedado registrados, ya que la diferencia de la variación entre la frecuencia y cantidad de eventos a principio de siglo y a final de siglo, es bastante notoria.
###Finalmente, se revisa la cantidad de muertes generadas por estos tres principales tipos de desastre para tener un comparativo de ocurrencia versus impactos.**

filtro_eventos = DESA['EVENT TYPE'].isin(eventos)
datos_filtrados = DESA[filtro_eventos]
muertes = datos_filtrados.groupby('EVENT TYPE')['FATALITIES'].sum().reset_index()
df_muertes = pd.DataFrame({'Tipo de evento': muertes['EVENT TYPE'], 'Cantidad de muertes': muertes['FATALITIES']})
fig = px.bar(df_muertes, x='Tipo de evento', y='Cantidad de muertes',labels={'Tipo de evento': 'Tipo de evento', 'Cantidad de muertes': 'Cantidad de muertes'},title='Cantidad de muertes por tipo de evento')

fig.show()
# Se tiene como resultado que que las tormentas son las que tienen mayor número de muertes con 1725 casos, luego sigue incendios con 388 casos y finalmente las inundaciones a pesar de que tienen mayor ocurrencia como se vio anteriormente, tienen la menor cantidad de muertes en estos tres tipos de desastre con 124 casos."""

# 1. ¿Cuál es el costo promedio de la normalización por tipo de desastre ?

import pandas as pd
import numpy as np

#Convertimos a tipo string y removemos separador de miles y la convertimos a tipo numerico haciendo coerción en los errores para que los valores no numéricos se conviertan en NaN.
DESA['NORMALIZED TOTAL COST'] = DESA['NORMALIZED TOTAL COST'].astype(str)
DESA['NORMALIZED TOTAL COST'] = DESA['NORMALIZED TOTAL COST'].str.replace('.', '')
DESA['NORMALIZED TOTAL COST'] = pd.to_numeric(DESA['NORMALIZED TOTAL COST'], errors='coerce')

#Calculamos ahora si el costo promedio por tipo de desastre, teniendo en cuenta solo los valores no nulos y los ordenamos ascendentemente
costo_promedio = DESA.groupby('EVENT TYPE')['NORMALIZED TOTAL COST'].mean()
costo_promedio_ordenado = costo_promedio.sort_values(ascending=False)

# Como da un número tan grande, entonces formateamos el costo promedio en formato alargado y sin decimales con símbolo de dólar y separador de miles para que se entienda mejor
costo_promedio_formateado = costo_promedio_ordenado.apply(lambda x: "${:,.0f}".format(x))

# Crear una tabla a partir del costo promedio ordenado y formateado para que se pueda visualizar mejor
#tabla_costo_promedio = pd.DataFrame({'EVENT TYPE': costo_promedio_ordenado.index, 'Costo Promedio': costo_promedio_formateado}).reset_index()
tabla_costo_promedio = pd.DataFrame({'Costo Promedio': costo_promedio_formateado}).reset_index()

### Se tiene que los desastres que implican mayores costos para la normalización están grandemente marcados en un top 6 con respecto al resto de desastres, en primer lugar están los terremotos dada su naturaleza y poder de afectación estructural con costo promedio de 84,126,702,800,000. En segundo lugar están los incendios de todo tipo, que claramente pueden acabar con todo a su paso si no es controlado y cuyo costo es inferior al 50% del costo de los terremotos, estando en $39,595,179,216,216, luego están las inundaciones que pueden acabar también con  los enseres y estructuras muy fácilmente. Despúes están los ciclones y desastres por aire. En séptimo lugar ya se ubican otros tipos de desastres cuya diferencia en costos de normalización es notablemente inferior con respecto a este top seis descrito aquí.

#2. ¿Cual es el porcentaje de incendios con respecto al resto de desastres?

import plotly.express as px
import pandas as pd

#Calculamos el número de incendios y el número total de desastres
num_incendios = DESA[DESA['EVENT TYPE'] == 'fire'].shape[0]
num_total_desastres = DESA.shape[0]

# Calculamos el número de desastres que no son incendios para poder configurar bien la torta
num_desastres_no_incendios = num_total_desastres - num_incendios
porcentaje_incendios = (num_incendios / num_total_desastres) * 100
porcentaje_no_incendios = 100 - porcentaje_incendios

data = pd.DataFrame({'Tipo de Desastre': ['Incendios', 'Otros Desastres'], 'Porcentaje': [porcentaje_incendios, porcentaje_no_incendios]})

fig = px.pie(data, values='Porcentaje', names='Tipo de Desastre', hole=0.5)
fig.show()

### Se tiene que el 8.97% del total de desastres están dados por incendios, lo cual es un número importante si se tiene en cuenta que dentro de la base hay 32 tipos de desastres en total, y que una distribución promedio sería de 3,1% para cada desastre.

# 3.  ¿Cuál es la cantidad de incendios por año?

#Filtramos los registros que corresponden a incendios
incendios = DESA[DESA['EVENT TYPE'] == 'fire']

#calculamos la cantidad de incendios por año
cantidad_incendios_por_año = incendios['YEAR'].value_counts().sort_index()

data = pd.DataFrame({'Año': cantidad_incendios_por_año.index, 'Cantidad de Incendios': cantidad_incendios_por_año.values})
data.plot( 'Año' , 'Cantidad de Incendios' )
### Puede observarse en el gráfico, que la mayor cantidad de incendios se han venido presentando en los últimos 40 años, ya que entre los años 1900 y 1980 se presentaron solo 15 incendios, mientras que después de 1980 y hasta el 2020, se presentaron 115 incendios.Esto también se puede presentar cuando no existe información disponible o bien se empezó a tomar oficialmente después de un año en particular, cuando ya se tenía establecido todo el sistema para prevención de desastres.

# 4.  ¿Cuál es la tasa de mortalidad de los incendios por año?

###            Total de incendios con muertos/ Total de incendios. Se presenta en gráfico de barras.

# Convertimos las columnas a tipo numerico
DESA['FATALITIES'] = pd.to_numeric(DESA['FATALITIES'], errors='coerce')
DESA['YEAR'] = pd.to_numeric(DESA['YEAR'], errors='coerce')

#Sacamos solo los que digan Fire y calculamos el total por año y cuales con muertos
incendios = DESA[DESA['EVENT TYPE'] == 'fire']
total_incendios = incendios.groupby('YEAR').size()
incendios_muertos = incendios.groupby('YEAR')['FATALITIES'].count()

#Ahora si calculamos la tasa de mortalidad y creamos el dataframe*1
tasa_mortalidad = round(((incendios_muertos / total_incendios)*100),2)
tasa_mortalidad_df = pd.DataFrame({'YEAR': tasa_mortalidad.index, 'tasa de Mortalidad (%)': tasa_mortalidad.values})
figm = px.bar(tasa_mortalidad_df, x='YEAR', y='tasa de Mortalidad (%)', labels={'Año': 'Año', 'tasa_mortalidad_df': 'tasa de Mortalidad (%)'})

figm.show()
### Se observa que la tasa de mortalidad en generales alta en los incendios ocurridos durante 1900 y 1998, sin embargo, para los 22 años siguientes,  la mortalidad en cada evento varió entre el 20% y el 100%.

# 5. ¿Cómo es la distribución de ocurrencia de incendios por día de la semana?  

import plotly.express as px

# Convertir las columnas 'YEAR', 'MONTH' y 'DAY' a tipo fecha para poder concatenar la fecha y sacar el dia de la semana específico
DESA['YEAR'] = pd.to_datetime(DESA['YEAR'], format='%Y', errors='coerce')
DESA['MONTH'] = pd.to_datetime(DESA['MONTH'], format='%m', errors='coerce')
DESA['DAY'] = pd.to_datetime(DESA['DAY'], format='%d', errors='coerce')

#Creamos la columna weekday para determinar el dia de la semana y filtramos por incendios
DESA['WEEKDAY'] = DESA['DAY'].dt.day_name()
incendios = DESA[DESA['EVENT TYPE'] == 'fire']
ocurrencia_incendios = incendios['WEEKDAY'].value_counts()

df_ocurrencia_incendios = pd.DataFrame({'Día de la semana': ocurrencia_incendios.index, 'Ocurrencia': ocurrencia_incendios.values})
dias_semana_ordenados = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
df_ocurrencia_incendios['Día de la semana'] = pd.Categorical(df_ocurrencia_incendios['Día de la semana'], categories=dias_semana_ordenados, ordered=True)
df_ocurrencia_incendios = df_ocurrencia_incendios.sort_values('Día de la semana')
fig = px.bar(df_ocurrencia_incendios, x='Día de la semana', y='Ocurrencia', color='Día de la semana',title='Ocurrencia de Incendios por Día de la Semana', )
fig.show()

##Se observa que hay mayor incidencia de incendios el Lunes, seguido del Martes y luego el Miércoles.

# 6. ¿Cuál es el número de incendios por localidad?

incendios_por_localidad = CONS['GEO'].value_counts()
df_incendios = pd.DataFrame({'Localidad': incendios_por_localidad.index, 'Número de Incendios': incendios_por_localidad.values})
# Definir una lista de colores para las barras
colores = ['Yellow', 'orange', 'red', 'purple', 'blue', 'green']  # Puedes agregar más colores si es necesario

fig = px.bar(df_incendios, x='Localidad', y='Número de Incendios', title='Número de Incendios por Localidad', color='Localidad', color_discrete_sequence=colores)

# Mostrar el gráfico
fig.show()
# Se observa que extrañamente la localidad de Canadá es la única con datos diferentes al resto de localidades, las cuales tienen un número simila3r de eventos correspondiente a 4440.#

# 7. ¿Cuál es la distribución de los incendios (residenciales/no residenciales)?

event_types = DESA['EVENT SUBGROUP'].unique()


event_types = DESA['EVENT TYPE'].unique()


fire_rows = DESA[(DESA['EVENT TYPE'] == 'residential') & (DESA['EVENT SUBGROUP'] == 'fire')]

residenciales = DESA[DESA['EVENT TYPE'] == 'residential'][DESA['EVENT SUBGROUP'] == 'fire']
cantidad_residenciales = len(residenciales)
no_residenciales = DESA[DESA['EVENT TYPE'] == 'non-residential'][DESA['EVENT SUBGROUP'] != 'fire']
cantidad_no_residenciales = len(no_residenciales)
df_incendios = pd.DataFrame({'Tipo de Incendio': ['Residenciales', 'No Residenciales'], 'Cantidad': [cantidad_residenciales, cantidad_no_residenciales]})
fig = px.pie(df_incendios, values='Cantidad', names='Tipo de Incendio', title='Distribución de Incendios Residenciales y No Residenciales')
fig.show()
# Se tiene que los incndios no residenciales son los que más se presentan con un 53.9% en comparación con los incendios residenciales.

# 8. ¿Cuál es el porcentaje de incendios en los que funcionaron efectivamente los rociadores?  tasa de efectividad= Total de incendios apagados por rociadoress/total de incendios

conteo_eventos = ROC['performance_of_system'].value_counts()

conteo_performance = ROC['performance_of_system'].value_counts()
incendios_con_rociadores = conteo_performance['Sprinkler operated']
total_incendios = ROC.shape[0]
porcentaje_efectividad = (incendios_con_rociadores / total_incendios) * 100

conteo_performance = ROC['performance_of_system'].value_counts()
incendios_con_rociadores = conteo_performance['Sprinkler operated']
incendios_sin_rociadores = total_incendios - incendios_con_rociadores
data = {'Resultado': ['No funcionaron', 'Si funcionaron'],'Cantidad': [incendios_con_rociadores, incendios_sin_rociadores]}

df = pd.DataFrame(data)

fig = px.pie(df, values='Cantidad', names='Resultado', title='Porcentaje de Efectividad de Rociadores')
fig.show()

print("El porcentaje de efectividad de los rociadores es:", porcentaje_efectividad)
# 9.  ¿Cuál es el porcentaje de incendios en los que funcionaron efectivamente  las alarmas de humo?

conteo_eventos = AH['performance_of_system'].value_counts()

conteo_performance = AH['performance_of_system'].value_counts()
incendios_con_alarma = conteo_performance['Alarm activated']
incendios_sin_alarma = total_incendios - incendios_con_alarma
data = {'Resultado': ['Alarmas Activadas', 'Alarmas No Activadas'],'Cantidad': [incendios_con_alarma, incendios_sin_alarma]}

df = pd.DataFrame(data)

fig = px.pie(df, values='Cantidad', names='Resultado', title='Tasa de Efectividad de Alarmas de Humo')

fig.show()
#El porcentaje o tasa de efectividad  de funcionamiento de las alarmas de humo es del 20%."""
