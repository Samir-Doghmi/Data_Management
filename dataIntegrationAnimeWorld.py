import json 
import mysql.connector 
import os 
from dotenv import load_dotenv 
import re

load_dotenv() 
 
USERNAME = os.getenv('databaseUser') 
PASSWORD = os.getenv('databasePassword') 
regex = r"<dd>\d+\s+\w+\s+(\d+)</dd>"
HOST = os.getenv('host')

mydb = mysql.connector.connect( 
    host = HOST, 
    user = USERNAME, 
    password = PASSWORD,
    database = 'sam'
)
def contains_ita(string):
    return 1 if "(ITA)" in string else 0

dataset = {} 
with open('items_listAnimeWorld.json', 'r', encoding="utf-8") as infile: 
    dataset = json.load(infile) 
 
 
cursor = mydb.cursor() 
 
for anime in dataset["records"]: 
    idAnime = anime["MyAnimeList"] 
 
    if(idAnime is None): 
        print("") 
    else: 
        idAnime = idAnime.split("/anime/",1)[1].strip() 
        print(idAnime)
        visualizzazioni = anime["Visualizzazioni"] 
        scoreAnimeWorld = anime["Rating"] 
        titolo = anime["Title"] 
        dub = str(contains_ita(titolo))
        descrizione = anime["Description"] 
        stagione = anime["Stagione"]
        annoUscita = anime["Data_uscita"]

        cursor.execute("select * from anime where id = " + str(idAnime))
        records = cursor.fetchall()

        print("idAnime = " + idAnime + ", titolo = " + titolo) 

        match = re.search(regex, annoUscita)
        anno = 0
        if match:
            anno = match.group(1)

        if(records == []):
            sql = "INSERT INTO anime (id, dub, titolo, stagione, dataUscita, visualizzazioneAnimeWorld, descrizione) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (idAnime, dub, titolo, stagione, anno, int(visualizzazioni.replace(".","")), descrizione)
            cursor.execute(sql, val)
        else:
            sql = "UPDATE anime SET visualizzazioneAnimeWorld = %s WHERE id = %s and dub = %s"
            val = (int(visualizzazioni.replace(".","")), idAnime, dub)
            cursor.execute(sql, val)

            sql = "UPDATE anime SET visualizzazioneAnimeWorld = %s, titolo=%s WHERE id = %s and dub = %s and titolo IS NULL"
            val = (int(visualizzazioni.replace(".","")), titolo, idAnime, dub)
            cursor.execute(sql, val)

        for episodios in anime["Link-ep"]: 
            for episodio in episodios:
                linkAnime = episodios[episodio] 
                cursor.execute("select * from episodi where idAnime = " + str(idAnime) + " AND dub = " + dub + " AND numeroEpisodio = " + episodio) 
                records = cursor.fetchall() 
             
                if(records == []): 
                    sql = "INSERT INTO episodi (numeroEpisodio, idAnime, dub, linkAnimeWorld) VALUES (%s, %s, %s, %s)" 
                    val = (episodio, int(idAnime), dub,  linkAnime) 
 
                    # print(val) 
                    cursor.execute(sql, val) 
                else: 
                    sql = "UPDATE episodi SET linkAnimeWorld = %s  WHERE idAnime = %s and dub = %s and numeroEpisodio=%s" 
                    val = (linkAnime, int(idAnime), dub, episodio) 
                    #print("esiste gia")

                    # print(val) 
                    cursor.execute(sql, val) 
        
        cursor.execute("select * from score where id = " + str(idAnime) + " and dub = " + dub)
        records = cursor.fetchall()

        if(records == []):
            sql = "INSERT INTO score (id, dub, animeworld) VALUES (%s, %s, %s)"
            val = (idAnime, dub, scoreAnimeWorld)
            cursor.execute(sql, val)
        else:
            sql = "UPDATE score SET animeworld = %s WHERE id = %s AND dub = %s"
            val = (scoreAnimeWorld, idAnime, dub)
            cursor.execute(sql, val)

mydb.commit()
cursor.close()
mydb.close()