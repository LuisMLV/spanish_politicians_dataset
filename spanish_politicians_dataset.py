# -*- coding: utf-8 -*-


"""
En este script de python descargo los tweets escritos por los diferentes políticos españoles (la mayoría de ministros y figuras
principales del gobierno español y los líderes de los principales partidos de la oposición) durante cierto rango de tiempo.
De estos tweets extraeré distintos datos con el objetivo de crear un dataset con información de interés sobre la actividad
de políticos en twitter.

"""

#Las librerías usadas:

import tweepy
from tweepy import OAuthHandler
import pandas as pd
import datetime 


#Definimos las credenciales con las que accederemos a twitter a través de la api:
    
api_key = 'HHfVWZ6kKmqQuUTLQyNjcdOvW'
api_secret = '5jWfZ8a31ln64joKGORGCXmDT0x3nWVxSdGh0Y1xHR5jd4G9Xw'
access_token = '1319405929872445446-I9mRpYZJFFC2ZefRiF337QTWAjlWUh'
access_token_secret = 'zeIF9jx0O4ZjFUowfOZcsr6iHp7XE98i1QOqH9EQ9TM2k'


#Nos autentificamos:
    
authentification = OAuthHandler(api_key , api_secret)

authentification.set_access_token (access_token, access_token_secret)

api = tweepy.API(authentification)


#En una lista, introducimos los nombres de usuario de las cuentas de twitter de la que queremos
#descargarnos tweets:

politicians = ['sanchezcastejon','ierrejon', 'pablocasado_',  'Santi_ABASCAL', 'PabloIglesias','InesArrimadas', 
              'carmencalvo_', 'NadiaCalvino', 'Teresaribera', 'AranchaGlezLaya', 'Jccampm', 'mjmonteroc',
              'abalosmeco', 'CelaaIsabel', 'Yolanda_Diaz_', 'MarotoReyes', 'LuisPlanas',
              'salvadorilla', 'astro_duque', 'IreneMontero', 'agarzon', ]


#Aquí definimos las distintas listas que nos servirán para guardar la información
#de los twitters descargados separada por los campos que tendrá el conjunto de datos que 
#queremos crear:

tweets = [] #tweet completo.
tweet_idx = [] #index del correspondiente tweet en el conjunto de datos.

user = [] #El usuario (el político) que escribió el tweet.

date = [] #La fecha en la que el tweet se escribió---> dd-mm-yyyy

hour = [] #Hora en la que se escribió el tweet

retweets = [] #Veces que el tweet fue retweeteado.


favs = [] #Favs que tuvo el tweet.

#Definimos una variable que marcará la fecha límite inferior del periodo de tiempo al
#que pertenecerán los tweets descargados. La api de twitter descarga/muestra los tweets 
#hacia atrás en la dimensión temporal, comenzando por el tweet más reciente:

limit_date = datetime.datetime(2020,6, 13, 0,0,0)  


#Creamos la función que descargará  la información de los tweets  según el usuario
#o político:

def politician_downld(politicians_list, limit_date):
     
    page = 1 #Usaremos páginas para progresar en la navegación a través de los tweets.
    idx = 0 #La variable idx irá asignando un índice a cada tweet introducido en el conjunto de datos.
    
    for p in politicians_list: #Por cada usuario/político en la lista
        
 #Creamos la variable, ptweets, que irá llamando a las distintas páginas del timeline
 #del usuario/político:
  
      ptweets = api.user_timeline(id=politician, wait_on_rate_limit=True) 
   
#El siguiente bucle irá progresando a través del timeline del usuario/político 
#mientras el último tweet de la página correspondiente no sea de una fecha anterior a la fecha 
#límite:
    
    while (ptweets[-1].created_at > limit_date):
        
      #Redefinimos la variable ptweets usando la variable página para ir avanzando a través del timeline.
      #"wait_on_rate_limit" hará que el script espere cuando se haya alcanzado el número máximo de peticiones
      #a la api, en lugar de pararse. "Tweet_mode='extended'" permitirá acceder a los tweets completos:
          
        ptweets = api.user_timeline(id=politician, tweet_mode='extended',page=page, wait_on_rate_limit=True)
      
      #Ahora, por cada tweet en la página actual de la timeline...
      
        for tweet in ptweets:
          
      #Y Si el tweet no es retweet y su fecha de publicación es inferior a la fecha límite (nos interesa sólo los tweets publicados genuinamente por el respectivo político)...    
          
           if 'RT' not in tweet.full_text and tweet.created_at > limit_date:
             
            tweet_idx.append(idx) #añadimos el índice al tweet.
            tweets.append(tweet.full_text) #añadimos el tweet completo (full_text).
            user.append(politician) # añadimos el usuario del político en twitter.
            print(politician)
            twdatetime=tweet.created_at #Creamos una variable con la fecha del tweet.
            twdate = str(twdatetime.day) + '-' + str(twdatetime.month) + '-' + str(twdatetime.year) #Manipulamos sus componentes para tener el formato de fecha "dd-mm-yyyy".
            date.append(twdate) #Añadimos la fecha a su respectiva lista/respectivo campo.
            hour.append(str(twdatetime.hour) + ':' + str(twdatetime.minute)) #Añadimos la hora.
            retweets.append(tweet.retweet_count) #Añadimos los retweets.
            favs.append(tweet.favorite_count)  #Y añadimos finalmente los favs.
                      
            idx += 1 #Redefinimos la variable índice sumándole uno. Así, podremos asignar a cada tweet del conjunto de datos índices consecutivos, de uno en uno.
               
        page += 1 #Redefinimos la página sumándole una para ir progresando en la paginación del timeline. 
      

         
#Ahora, añadimos la lista de users de políticos antes definida y aplicamos la
#función politician_downld para descargar los tweets y obtener la información de interés: 

politician_downld(politicians, limit_date)
    
    
#Creamos un dataframe que contendrá el conjunto de datos, con los diferentes
#campos que queremos incluir:
    
politic_data = pd. DataFrame(columns=['tweet_idx','user','tweet', 'date', 'hour', 'retweets', 'favs'])


#E introducimos en cada campo los datos contenidos en sus respectivas listas homónimas:
    
politic_data['tweet_idx'] = tweet_idx
politic_data['user'] = user
politic_data['tweet'] = tweets
politic_data['date'] = date
politic_data['hour'] = hour
politic_data['retweets'] = retweets
politic_data['favs'] = favs


#Posteriormente creamos un document csv a partir del dataframe, que contendrá el dataset creado en este script:
    
politic_data.to_csv ('spanishpoliticians_tweets.csv', index= False)
