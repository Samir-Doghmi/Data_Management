import scrapy
import mysql.connector
import os
from dotenv import load_dotenv
import re
from bs4 import BeautifulSoup

load_dotenv()

USERNAME = os.getenv('databaseUser')
PASSWORD = os.getenv('databasePassword')
HOST = os.getenv('host')

class AnimeSpider(scrapy.Spider):
    name = "anime"
    
    def __init__(self, *args, **kwargs):
        super(AnimeSpider, self).__init__(*args, **kwargs)
       
        mydb = mysql.connector.connect(
            host="192.168.1.140",
            user=USERNAME,
            password=PASSWORD,
            database="animedb2"
        )
        cursor = mydb.cursor(dictionary=True)

        cursor.execute("SELECT id FROM anime")
        self.records = cursor.fetchall()
        
        cursor.close()
        mydb.close()

        self.start_urls = ["https://myanimelist.net/anime/" + str(riga["id"]) for riga in self.records]
        #self.start_urls = ["https://myanimelist.net/anime/1"]
        
    def parse(self, response):
        # Gestione del parsing della risposta
        idAnime = response.url.split("/")[-1]

        title = response.css("#contentWrapper .h1-title .title-name ::text").extract_first()
        score = response.css('span.score-label ::text').extract_first()
        ranked = response.css("span.ranked strong ::text").extract_first().replace('#', '')
        members = response.css("span.members strong ::text").extract_first().replace(',','')
        popularity = response.css("span.popularity strong ::text").extract_first().replace('#', '')

        print("idAnime = " + idAnime + ", titolo = " + title) 

        mydb = mysql.connector.connect(
            host="192.168.1.140",
            user=USERNAME,
            password=PASSWORD,
            database="animedb2"
        )
        cursor = mydb.cursor(dictionary=True)

        print("score =" + score)
        print("ranked =" + ranked)
        print("members =" + members)
        print("popularity =" + popularity)

        favoriti = 0
        genres = []
        demographic = []
        for information in response.css('.spaceit_pad').getall():
            cercaFavourites = "Favorites:"
            cercaGeneri = "Genr"
            cercaDemographic = "Demographic:"
            #htmlParsed = BeautifulSoup(information, 'html.parser')
            

            if cercaGeneri in information:
                soup = BeautifulSoup(information, 'html.parser')
            
                for link in soup.find_all('span', itemprop='genre'):
                    genres.append(link.text)

            #elemento_span = htmlParsed.find('span', text=cercaSeEsisteFavourites)
            if cercaFavourites in information:
                informationCleaned = information.replace('<span class="dark_text">Favorites:</span>', '')
                favoriti = int(informationCleaned.replace('<div class="spaceit_pad">', '').replace('</div>', '').replace(',','').strip())
            

            if cercaDemographic in information:
                soup = BeautifulSoup(information, 'html.parser')
            
                for link in soup.find_all('span', itemprop='genre'):
                    demographic.append(link.text)

        print(favoriti)

        #prelevare tutti i personaggi e i loro ruoli
        contatore1 = 0
        nomiPersonaggi = []
        for nomePersonaggio in response.css(".h3_characters_voice_actors a ::text").getall():
            contatore1 = contatore1 + 1
            nomiPersonaggi.append(nomePersonaggio)

        contatore2 = 0
        ruoliPersonaggi = []
        for ruoloPersonaggio in response.css('.detail-characters-list table td .spaceit_pad small ::text').getall():
            if contatore1 == contatore2:
                break
            contatore2 = contatore2 + 1
            ruoliPersonaggi.append(ruoloPersonaggio)

        print(nomiPersonaggi)
        print("###")
        print(ruoliPersonaggi)
        
        print(demographic)
        print(genres)

        for genere in genres:
            cursor.execute("select * from generi where idAnime = " + str(idAnime) + " and generi = '"+ genere+"'")
            records = cursor.fetchall()
            
            if(records == []):
                sql = "INSERT INTO generi (idAnime, dub, generi ) VALUES (%s, %s, %s)"
                val = (idAnime, 0, genere)
                cursor.execute(sql, val)

                cursor.execute("select * from anime where id = " + str(idAnime) + " and dub = 1 ")
                records = cursor.fetchall()

                if(records == []):
                    val = (idAnime, 1, genere)
                    cursor.execute(sql, val)

        contatore1 = 0
        for personaggio in nomiPersonaggi:
            cursor.execute('select * from personaggi where id = ' + str(idAnime) + ' and nome = "'+ personaggio + '"')
            records = cursor.fetchall()
            if(records == []):

                sql = "INSERT INTO personaggi (idAnime, dub, nome, ruolo) VALUES (%s, %s, %s, %s)"
                val = (idAnime, 0, personaggio, ruoliPersonaggi[contatore1])
                cursor.execute(sql, val)

                cursor.execute("select * from anime where id = " + str(idAnime) + " and dub = 1 ")
                records = cursor.fetchall()

                if(records == []):
                    val = (idAnime, 1, personaggio, ruoliPersonaggi[contatore1])
                    cursor.execute(sql, val)

            contatore1 = contatore1 + 1     
        sql = "UPDATE score SET myanimelist = %s WHERE id = %s and dub = %s"
        val = (score, idAnime, 0)
        print(val)
        cursor.execute(sql, val)

        cursor.execute("select * from anime where id = " + str(idAnime) + " and dub = 1 ")
        records = cursor.fetchall()

        if(records == []):
            val = (score, idAnime, 1)
            cursor.execute(sql, val)

        sql = "UPDATE anime SET rank = %s, popularity = %s, members = %s, favoriti = %s, title_en = %s  WHERE id = %s and dub = %s"
        val = (ranked, popularity, members, favoriti, title, idAnime, 0)
        cursor.execute(sql, val)

        cursor.execute("select * from anime where id = " + str(idAnime) + " and dub = 1 ")
        records = cursor.fetchall()

        if(records == []):
            val = (ranked, popularity, members, favoriti, title, idAnime, 0)
            cursor.execute(sql, val)
        
        
        mydb.commit()
        cursor.close()
        mydb.close()
        pass

