# -*- coding: utf-8 -*-
"""
Created on Fri May 17 14:01:02 2019

@author: Tats
"""

import requests
import lxml.html
import csv

Salida = []
with open(r'C:\Users\Tats\Documents\MINE\Sistemas_de_Recomendacion\Talleres_2019\Taller_3\ml_latest\links_1.csv') as f:
    lis = [line.split() for line in f]        # create a list of lists
    for i in lis: 
        lis1 = i[0].split(';')
        movie_ID = lis1[0]
        imdb_URI = lis1[1]
        theMovie_Id = lis1[2]
        html = requests.get('https://www.themoviedb.org/movie/'+theMovie_Id)
        doc = lxml.html.fromstring(html.content)
        Director = doc.xpath('//li[@class="profile"]//*/a/text()')
        edge = 'Director'
        #print(Director)
        Cast = doc.xpath('//li[@class="card"]//*/a/text()')
        Edge_2='Actores'
        Actores = ', '.join(Cast)
        #print(Cast)
        #print(Actores)
        Salida.append((movie_ID, edge, Director, Edge_2, Actores)) 
        #print(Salida)

        
myFile = open('C:\\Users\Tats\Documents\MINE\Sistemas_de_Recomendacion\Talleres_2019\Taller_3\ml_latest\example2.csv','w',encoding='utf-8')
with myFile:
    writer = csv.writer(myFile)
    writer.writerows(Salida)
     
print("Writing complete")
        




 
        
        
        
        
        