import json
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv('databaseUser')
PASSWORD = os.getenv('databasePassword')
HOST = os.getenv('host')

mydb = mysql.connector.connect(
    host = HOST,
    user = USERNAME,
    password = PASSWORD,
    database = 'sam'
)

dataset = {}
with open('dataAnimeUnity.json', 'r') as infile:
    dataset = json.load(infile)

cursor = mydb.cursor()

for anime in dataset["records"]:
    idAnime = anime["mal_id"]
    if idAnime is not None:
        titolo = anime["title"]
        stagione = anime["season"]
        tipoAnime = anime["type"]
        dataUscita = anime["date"]
        numeroEpisodi=anime["episodes_count"]
        durataEpisodi = anime["episodes_length"]
        studio = anime["studio"]
        visualizzazioni = anime["visite"]
        dub = str(anime["dub"])
        descrizione = anime["plot"]
        preferiti = anime["favorites"]

        if titolo is not None:
            print("idAnime =", idAnime, ", titolo =", titolo)
        else:
            print("idAnime =", idAnime, ", titolo non disponibile")


        cursor.execute("select * from anime where id = " + str(idAnime) + " and dub = " + dub)
        records = cursor.fetchall()

        if(records == []):
            sql = "INSERT INTO anime (id, dub, titolo, stagione, tipoAnime, dataUscita, numeroEpisodi, visualizzazioneAnimeUnity, descrizione, studio, preferitiAnimeUnity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (idAnime, dub, titolo, stagione, tipoAnime, int(dataUscita), numeroEpisodi, visualizzazioni, descrizione, studio, preferiti)
            cursor.execute(sql, val)
        
        for episodio in anime["episodes"]:
             visualizzazioniEpisodio = episodio["visite"]
             linkAnimeUnity = episodio["link"]
             numeroEpisodio = episodio["number"]
        
             cursor.execute("select * from episodi where idAnime = " + str(idAnime) + " and dub = "+ dub + " and numeroEpisodio = " + numeroEpisodio)
             records = cursor.fetchall()

             if(records == []):
                 sql = "INSERT INTO episodi (numeroEpisodio, idAnime, dub, linkAnimeUnity, visiteAnimeUnity) VALUES (%s, %s, %s, %s, %s)"
                 val = (numeroEpisodio, int(idAnime), dub, linkAnimeUnity, int(visualizzazioniEpisodio))
                 cursor.execute(sql, val)
             else:
                print("ciao")
                
        scoreAnimeUnity = anime["score"]

        cursor.execute("select * from score where id = " + str(idAnime) + " and dub = " + dub)
        records = cursor.fetchall()

        if(records == []):
            sql = "INSERT INTO score (id,dub, animeunity) VALUES (%s, %s, %s)"
            val = (idAnime, dub, scoreAnimeUnity)
            cursor.execute(sql, val)

    
mydb.commit()
cursor.close()
mydb.close()