import csv
from bs4 import BeautifulSoup
import lxml
import requests


# Kommt noch: Ist für die wenigen Artikel die mit <div> eingekleistert worden
def divWorker(artikel):
    """Extra funktion um mit den blöden divs umzugehen

    :param artikel:
    :return:
    """
    print("do smth")
    return #(nameLaden, ladenBesitzer,ort,dasBesondere,Webseite,Bundesland)


def pScraper(artikel):
    """Bekommt den artikel soup und returnt die gescrapten Informationen aus den p-Elementen

    :param artikel: Soup
    :return: bundesland, nameLaden,ladenBesitzer,ort,dasBesondere,webseite,onlineShop,faceBook,instagram
    """

    # Leere Listen
    rbundesland = []
    rnameLaden = []
    rladenBesitzer = []
    rort = []
    rdasBesondere = []
    rwebseite = []
    ronlineShop = []
    rfaceBook = []
    rinstagram = []

    bundesland = None

    for eintrag in artikel.find_all({'p', 'h2'})[1:]:
        nameLaden = None
        ladenBesitzer = None
        ort = None
        dasBesondere = None
        webseite = None
        onlineShop = None
        faceBook = None
        instagram = None

        # Einzelne Linien durchgehen, da die Webseite keine Schöne Unterteilung bereitstellt
        for line in eintrag.text.splitlines():
            # print("\n"+line)
            match line.split():

                case ["Wer:", *ladenB]:
                    ladenBesitzer = ladenB
                case ["Wo:", *location]:
                    ort = location
                    # print(location)
                    # print(ort)
                case ["Das", "Besondere:", *text]:
                    dasBesondere = text
                    # print(text)
                case ["Webseite:", *link] | ["Website:", *link]:
                    webseite = link

                # überhaupt nicht schön:
                case ['Website:www.füllgut-regensburg.de' | 'Website:www.unverpackt-fulda.de/' as ws]:
                    we = ws.split(":")[1]
                    webseite = we
                case ["Online-Shop:", linkO]:
                    onlineShop = linkO

                case [
                    "Saarland" | "Niedersachsen" | "Baden-Württemberg" | "Bayern" | "Berlin" | "Brandenburg" | "Bremen" | "Hamburg" | "Hessen" | "Mecklenburg-Vorpommern" | "Nordrhein-Westfalen" | "Rheinland-Pfalz" | "Sachsen" | "Sachsen-Anhalt" | "Schleswig-Holstein" | "Thüringen" as bl]:
                    # print(bl)
                    bundesland = bl
                case ["Facebook:", fb]:
                    faceBook = fb
                case ["Instagram:", ig]:
                    instagram = ig
                case [*x]:
                    nameLaden = x

        # Nicht leere Strings zusammenfügen:
        if nameLaden:
            nameLaden = (" ".join(nameLaden))
        if dasBesondere:
            dasBesondere = (" ".join(dasBesondere))
        if ladenBesitzer:
            ladenBesitzer = (" ".join(ladenBesitzer))
        if ort:
            ort = (" ".join(ort))

        # Falls z.B. nur Bundesland gegeben ist:
        if bundesland and nameLaden == None and ladenBesitzer == None:
            continue
        #print(
        #    f"Name: {nameLaden}, Wer: {ladenBesitzer}, Wo?: {ort}, Irgentwas besonderes?: {dasBesondere} und sonst? {webseite, onlineShop, faceBook, instagram}")

        # appendieren an die Liste mit den gewonnenden Einträgen
        rbundesland.append(bundesland)
        rnameLaden.append(nameLaden)
        rladenBesitzer.append(ladenBesitzer)
        rort.append(ort)
        rdasBesondere.append(dasBesondere)
        rwebseite.append(webseite)
        ronlineShop.append(onlineShop)
        rfaceBook.append(faceBook)
        rinstagram.append(instagram)

        # Abbrechen nach der letzten webseite:
        if webseite and 'www.fandli.de' in webseite:
            break

    return (rbundesland, rnameLaden,rladenBesitzer,rort,rdasBesondere,rwebseite,ronlineShop,rfaceBook,rinstagram)



def main():

    # Öffnen einer Webseite, hier unverpackt Laden
    source = requests.get('https://enorm-magazin.de/lebensstil/nachhaltiger-konsum/zero-waste/unverpackt-laeden-deutschland').text

    # Erstellen der Suppe
    soup = BeautifulSoup(source, 'lxml')

    # print(soup.prettify())

    artikel = soup.find('div', id="article__content-body")

    csv_file = open('unverpacktLaden_scrape.csv', 'w')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Bundesland","Ladenname","Name Besitzer","Ort","Besonderes","Webseite","OnlineShop","FaceBook","Instagram"])
    bundesland, nameLaden, ladenBesitzer, ort, dasBesondere, webseite, onlineShop, faceBook, instagram = pScraper(artikel)

    for a,b,c,d,e,f,g,h,i in zip(bundesland, nameLaden,ladenBesitzer,ort,dasBesondere,webseite,onlineShop,faceBook,instagram):
        try:
            csv_writer.writerow([a,b,c,d,e,f,g,h,i])
        except UnicodeEncodeError as b:
            print(b)
            print(a,b,c,d,e,f,g,h,i)

    # Schließen der File
    csv_file.close()


if __name__ == '__main__':
    a = ['abcde']
    print(a)
    print(a[0])
    main()
