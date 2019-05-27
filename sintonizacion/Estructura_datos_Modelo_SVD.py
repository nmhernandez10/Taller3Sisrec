# -*- coding: utf-8 -*-
"""
Created on Tue May 14 20:39:00 2019

@author: Tats
"""

import pandas as pd
import numpy as np; np.random.seed(1)
import datetime
from surprise import Reader
from surprise import Dataset
from surprise.model_selection import train_test_split
from surprise import evaluate, print_perf
from surprise import accuracy
from surprise.model_selection import GridSearchCV
from surprise import SVD



"Lectura del archivo"
dataset=pd.read_csv(r'C:\Users\Tats\Documents\MINE\Sistemas_de_Recomendacion\Talleres_2019\Taller_3\ml_latest\ratings.csv', sep=',')
    
print(dataset.shape)
dataset.head()
list(dataset)  

dataset['fecha']=pd.to_datetime(dataset.timestamp, unit='s')
dataset['year']=dataset['fecha'].dt.year

print(dataset.shape)
dataset.head()
list(dataset)  

dataset.groupby(['year'])['rating'].describe()
'Selecciona periodo de análisis'
last_years=dataset[dataset['year'] >= 2011]
last_years.groupby(['year'])['rating'].describe()

' ************ Generación Datasets ********************************'

"Genera dataset Punto 2.c.i - Muestra de desarrollo - Training & Testing"
df_1=last_years[last_years['year'] <= 2013]
df_1.groupby('year')['rating'].hist()
Base_i=df_1.sample(frac=0.1, random_state=2)
print(Base_i.shape)
Base_i.groupby('year')['rating'].hist()

"Selección muestra de entrenamiento"
Training=Base_i.sample(frac=0.6, random_state=2)
Training.shape
Training.groupby('year')['rating'].hist()

"Selección muestra de Testing"
Testing=Base_i.sample(frac=0.4, random_state=2)
Testing.shape
Testing.groupby('year')['rating'].hist()

"Valida si las muestras de training y prubas son distintas"
Training.equals(Testing)

"Genera dataset Punto 2.c.i - Muestra de desarrollo - Validation"
df_1=last_years[last_years['year'] == 2014]
df_1.groupby('year')['rating'].hist()
Validation=df_1.sample(frac=0.1, random_state=2)
print(Validation.shape)
Validation.groupby('year')['rating'].hist()

"Genera dataset Punto 2.c.ii - Simulación flujo de datos"
periodo=['2016', '2015']
df_1=dataset[dataset.year.isin(periodo)]
df_1.groupby(['year'])['rating'].describe()
df_1.groupby(['year'])['rating'].hist()
Base_ii=df_1.sample(frac=0.1, random_state=2)
Base_ii.groupby(['year'])['rating'].hist()


"Genera dataset Punto 2.c.iii - Validación objetivo de recomendación"
df_1=dataset[dataset['year'] >= 2017]
df_1.groupby(['year'])['rating'].hist()
Base_iii=df_1.sample(frac=0.1, random_state=2)
Base_iii.groupby(['year'])['rating'].hist()

' ************ Modelo Filtrado Colaborativo - SVD ********************************'

"Establece el rango de Raitings aceptados"
reader = Reader( rating_scale = ( 0.5, 5 ) )

"Transforma dataset de entrenamiento para Surprice"
Training_data = Dataset.load_from_df(Training[ [ 'userId', 'movieId', 'rating' ] ], reader )
Training_set = Training_data.build_full_trainset()
Train_set_check = Training_set.build_testset()

"Transforma dataset de testing para Surprice"
Test_data = Dataset.load_from_df(Testing[ [ 'userId', 'movieId', 'rating'] ], reader )
Test_set = Test_data.build_full_trainset()
Test_set_check = Test_set.build_testset()

"Transforma dataset de Validation para Surprice"
valid_data = Dataset.load_from_df(Validation[ [ 'userId', 'movieId', 'rating'] ], reader )
valid_set = valid_data.build_full_trainset()
valid_set_check = valid_set.build_testset()

" Generacion del modelo"
"Identificación de parámetros optimos - para inicializar la experimentacion"
param_grid = {'n_epochs': [5, 20], 'lr_all': [0.0001, 0.1], 'reg_all': [0.1, 0.9]}
gs = GridSearchCV(SVD, param_grid, measures=['rmse', 'mae'], cv=5)

"Ajuste del modelo para identificación de parámetros óptimos que minimizan el RMSE y el MEA"
gs.fit(Training_data)

# best RMSE score
print(gs.best_score['rmse']) 

# combination of parameters that gave the best RMSE score
print(gs.best_params['rmse'])

# best MAE score
print(gs.best_score['mae'])

# combination of parameters that gave the best MAE score
print(gs.best_params['mae'])

"Modelo SVD"
#Parámeros del modelo final
algo = SVD( n_factors = 15, n_epochs = 45, biased = True, lr_all = 0.1, reg_all = 0.001, init_mean = 0, init_std_dev = 0.01, verbose = True )
algo.fit(Training_set)

"Evaluación de predicciones"
predictions_train = algo.test(Train_set_check)
predictions_test = algo.test(Test_set_check)
predictions_validation = algo.test(valid_set_check)


" Ajuste por RMSE"
accuracy.rmse( predictions_train, verbose = True )
accuracy.rmse( predictions_test, verbose = True )
accuracy.rmse( predictions_validation, verbose = True )


" Ajuste por MAE"
accuracy.mae( predictions_train, verbose = True )
accuracy.mae( predictions_test, verbose = True )
accuracy.mae( predictions_validation, verbose = True )

'****************** Corrección de la muestra *************'

df_1=last_years[last_years['year'] <= 2014]
Base_i=df_1.sample(frac=0.1, random_state=2)

"Selección muestra de entrenamiento"
Training=Base_i.sample(frac=0.6, random_state=2)
Training.shape
Training.groupby('year')['rating'].hist()

"Selección muestra de Testing"
Testing=Base_i.sample(frac=0.2, random_state=2)
Testing.shape
Testing.groupby('year')['rating'].hist()

"Selección muestra de Testing"
Validation=Base_i.sample(frac=0.2, random_state=5)
Validation.shape
Validation.groupby('year')['rating'].hist()

"Valida si las muestras sean distintas"
Training.equals(Testing)
Training.equals(Validation)
Testing.equals(Validation)








