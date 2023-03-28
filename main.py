# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import csv


# Press the green button in the gutter to run the script.

#Diese Klasse speichert nur die Werte die ausgelesen werden
class CrawledArticle():
    def __init__(self, title, emoji, content, image):
        self.title = title
        self.emoji = emoji
        self.content = content
        self.image = image

#Diese Klasse liest die Seite aus und erstellt Instanzen von CrawledArticle
class ArticleFetcher():
    def fetch(self):
        #Hier setzen wir den Zähler für die verschiedenen Seiten und setzen die index.php als ersten Eintrag
        pagecounter = 1
        url = "http://python.beispiel.programmierenlernen.io/index.php"

        #Hier geschieht die erste Abfrage auf dem Webserver
        r = requests.get(url)
        doc = BeautifulSoup(r.text, "html.parser")
        articles = []

        #So lange es einen Weiter-Button gibt, machen wir weiter
        while len(doc.select(".btn-primary")) != 0:
            #Natürlich ändern wir die URL beim ersten Durchlauf nicht
            if pagecounter > 1:
                url = urljoin(url, f"index.php?page={pagecounter}")

            #Hier schonen wir ein bisschen den Webserver^^
            print(f"Seite {pagecounter}")
            time.sleep(1)
            print(url)
            #Widerspricht dem DRY-Prinzip, aber auf die Schnelle geht das schon... Das IF ist da, damit wir nicht zwei Mal eine Abfrage am Webserver stellen
            if pagecounter > 1:
                r = requests.get(url)

            #Hier parsen wir die Webseite und filtern sie nach den einzelnen Artiklen, also Cards
            doc = BeautifulSoup(r.text, "html.parser")
            cards = doc.select(".card")

            #Hier lesen wir den Inhalt der Cards aus und erstellen CrawlerArticle-Objekte pro Durchlauf
            for card in cards:
                emoji = card.select_one(".emoji").text
                title = card.select(".card-title span")[1].text
                content = card.select_one(".card-text").text
                image = card.select_one("img").attrs["src"]
                full_image_path = urljoin("http://python.beispiel.programmierenlernen.io/", image)
                crawled = CrawledArticle(title, emoji, content, full_image_path)
                articles.append(crawled)
            #Hier zählen wir eins hoch um die nächste Seite zu ermitteln
            pagecounter += 1
            next_page = urljoin(url, f"index.php?page={pagecounter}")

        return articles


if __name__ == '__main__':

    artikels = ArticleFetcher().fetch()

    #Wir lesen die Artikel aus und schreiben sie in eine CSV... duuuh :O
    with open('programmieren.csv','w',newline='', encoding='utf-8') as csvFile:
        writer = csv.writer(csvFile, delimiter=';',quotechar='"')
        for artikel in artikels:
            writer.writerow([artikel.emoji, artikel.title, artikel.content])
        csvFile.close()
