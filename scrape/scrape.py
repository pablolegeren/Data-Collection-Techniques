import datetime
import pandas as pd
import requests
import eurostat
import json


file_name = 'C://Users//pablo//Desktop//MASTER//RECOGIDA DE DATOS//ENTREGAS'
time_stamp = datetime.datetime.now().strftime('%Y%m%d_h%Hm%M')
file_name = file_name + time_stamp + '.csv'

url = 'https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/20674?page=1'

r = requests.get(url)
data = r.json()
ine = data[0]
datos = ine['Data']
datos_df = pd.DataFrame(datos)
datos_ine = datos_df[['Valor']].T.rename(columns=datos_df['Anyo']).reset_index()
datos_ine['Country'] = ['ES']
ine_df = datos_ine.iloc[:,::-1].iloc[:,:-2]
ine_df_melted = pd.melt(ine_df, id_vars=['Country'], var_name='Periodo', value_name='Valor')
ine_df_melted

tabla_eu = eurostat.get_data_df('demo_ndivdur')
datos = tabla_eu.dropna()
data1 = datos[['geo\TIME_PERIOD','2013','2014','2015',
                  '2016','2017', '2018','2019','2020','2021']].reset_index().drop(columns = 'index')
eu_df = data1.rename(columns = {'geo\TIME_PERIOD':'Country'})
eu_df_melted = pd.melt(eu_df, id_vars=['Country'], var_name='Periodo', value_name='Valor')

ine_eu = pd.merge(ine_df_melted,eu_df_melted, how = 'outer')

ine_eu['DUMMY'] = 1

ine_eu.to_csv(file_name, sep=',', encoding='utf-8')