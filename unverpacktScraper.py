import csv
from bs4 import BeautifulSoup
import lxml
import requests


# Kommt noch: Ist für die wenigen Artikel die mit <div> eingekleistert worden
def divScraper(artikel):
    """Extra funktion um mit den blöden divs umzugehen

    :param artikel:
    :return:
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

    nameLaden = None
    newnameLaden = None
    ladenBesitzer = None
    ort = None
    dasBesondere = None
    webseite = None
    bundesland = None

    for eintrag in artikel.find_all({'div', 'h2'})[1:]:

        onlineShop = None
        faceBook = None
        instagram = None

        for line in eintrag.text.splitlines():
            #print(line)
            match line.split():

                case ["Wer:", *ladenB]:
                    ladenBesitzer = ladenB
                case ["Wo:", *location]:
                    ort = location
                    # print(location)
                    # print(ort)
                case ["Das", "Besondere:", *text]|["Besonderes:", *text]:
                    dasBesondere = text
                    # print(text)
                case ["Webseite:", *link] | ["Website:", *link]:
                    webseite = link

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
                    if x:
                        # Wenn es bereits einen namen laden gibt, dann setzen wir x dem neuen Namen laden
                        # ist für den 1. Ladennamen wichtig, da sonst deren details nicht gespeichert werden.
                        if nameLaden:
                            newnameLaden = x

                        # Für den 1. Ladennamen
                        else:
                            nameLaden = x



            if bundesland and (nameLaden == None or ladenBesitzer == None or ort == None or webseite == None or dasBesondere == None):
                continue

            # Schauen, ob es einen neuen laden gibt -> dann alten Laden mit information speichern, da alles
            # über diesen folglich bekannt ist
            if newnameLaden:
                if nameLaden:
                    nameLaden = (" ".join(nameLaden))
                if dasBesondere:
                    dasBesondere = (" ".join(dasBesondere))
                if ladenBesitzer:
                    ladenBesitzer = (" ".join(ladenBesitzer))
                if ort:
                    ort = (" ".join(ort))

                rbundesland.append(bundesland)
                rnameLaden.append(nameLaden)
                rladenBesitzer.append(ladenBesitzer)
                rort.append(ort)
                rdasBesondere.append(dasBesondere)
                rwebseite.append(webseite)
                ronlineShop.append(onlineShop)
                rfaceBook.append(faceBook)
                rinstagram.append(instagram)
                nameLaden = newnameLaden
                newnameLaden = None
                ladenBesitzer = None
                ort = None
                webseite = None
                dasBesondere = None
                onlineShop = None
                faceBook = None
                instagram = None

    # print(
    #    f"BLand: {rbundesland}Name: {rnameLaden}, Wer: {rladenBesitzer}, Wo?: {rort}, Irgentwas besonderes?: {rdasBesondere} und sonst? {rwebseite, ronlineShop, rfaceBook, rinstagram}")
    return (rbundesland, rnameLaden,rladenBesitzer,rort,rdasBesondere,rwebseite,ronlineShop,rfaceBook,rinstagram)


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
                    if x:
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
    csv_file = open('unverpacktLadenDiv_scrape.csv', 'w')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Bundesland","Ladenname","Name Besitzer","Ort","Besonderes","Webseite","OnlineShop","FaceBook","Instagram"])

    bundesland_t, nameLaden_t, ladenBesitzer_t, ort_t, dasBesondere_t, webseite_t, onlineShop_t, faceBook_t, instagram_t = divScraper(artikel)

    bundesland, nameLaden, ladenBesitzer, ort, dasBesondere, webseite, onlineShop, faceBook, instagram = pScraper(artikel)

    for bl, nL, lB, oT, dB, wS, oS, fB, ig in zip (bundesland_t, nameLaden_t, ladenBesitzer_t, ort_t, dasBesondere_t, webseite_t, onlineShop_t, faceBook_t, instagram_t):

        bundesland.append(bl)
        nameLaden.append(nL)
        ladenBesitzer.append(lB)
        ort.append(oT)
        dasBesondere.append(dB)
        webseite.append(wS)
        onlineShop.append(oS)
        faceBook.append(fB)
        instagram.append(ig)

    for a,b,c,d,e,f,g,h,i in zip(bundesland, nameLaden,ladenBesitzer,ort,dasBesondere,webseite,onlineShop,faceBook,instagram):
        try:
            csv_writer.writerow([a,b,c,d,e,f,g,h,i])
        except UnicodeEncodeError as b:
            print(b)
            print(a,b,c,d,e,f,g,h,i)

    # Schließen der File
    csv_file.close()


if __name__ == '__main__':
    main()
