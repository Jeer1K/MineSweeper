import haravasto
import random
import math
import time

tila = {
    "kentta": None, #Kenttä, jossa tieto miinojen sijainnista.
    "tilanne": None, #Kertoo onko ohjelma pelissä("peli"), valikossa ("valikossa") vai lopetuksessa("lopetus"). 
    "kentan_koko": None, #Sisältää monikon, jossa on leveys, korkeus sekä miinojen määrä mainitussa järjestyksessä.
    "miinojen_maara": None, #Miinojen määrä
    "pelin_kesto": [None, None, 0] #Sisältää listan jossa on aloitus- ja lopetusaika sekä pelin kesto vuoroissa mainitussa järjestyksessä.
}

def valikko():
    """
    Pyytää käyttäjää valitsemaan pelin, valikon tai tilastot.
    Palauttaa virheviestin, jos annetaan virheellinen syote.
    """
    print("\nValitse jokin seuraavista: Aloita peli: a, Katso tilastoja: t tai Lopeta peli: l.")
    while True:
        valinta = input("Anna valinta: ").lower()
        if valinta == "a":
            tila["tilanne"] = "peli"
            break
        elif valinta == "t":
            tila["tilanne"] = "tilasto"
            break
        elif valinta == "l":
            tila["tilanne"] = "lopetus"
            break
        else:
            print("Virheellinen syöte! Valitse a, t tai l")

def kysy_kentan_koko():
    """
    Kysyy käyttäjältä kentän leveyden, korkeuden ja miinojen määrän
    sekä tarkistaa ovatko syotteet kokonaislukuja.
    """
    while True:
        leveys = input("Anna kentän leveys: ")
        korkeus = input("Anna kentän korkeus: ")
        miinojen_maara = input("Anna miinojen maara: ")
        try:
            leveys = int(leveys)
            korkeus = int(korkeus)
            miinojen_maara = int(miinojen_maara)
        except NameError:
            print("Anna leveys, korkeus ja miinojen määrä kokonaislukuna!")
        except ValueError:
            print("Anna leveys, korkeus ja miinojen määrä kokonaislukuna!")
        else:
            if miinojen_maara <= 0 or korkeus <= 0 or leveys <= 0:
                print("Lukujen täytyy olla kokonaislukuja, jotka ovat suurempia kuin 0.")
            elif korkeus * leveys + 1 <= miinojen_maara:
                print("Miinojen määrä ei voi olla suurempi kuin kentän pinta-ala.")
            elif isinstance(leveys, int) and isinstance(korkeus, int):
                tila["kentan_koko"] = (leveys, korkeus)
                tila["miinojen_maara"] = miinojen_maara
                break
            else:
                print("Anna kentän leveys, korkeus ja miinojen määrä kokonaislukuna!")

def alusta_kentta():
    """
    Luo tyhjän kentän ja asettaa kentällä N kpl miinoja satunnaisiin paikkoihin.
    """
    #Luo tyhjän kentän
    leveys, korkeus = tila["kentan_koko"]
    tyhja_kentta = []
    for rivi in range(korkeus):
        tyhja_kentta.append([])
        for sarake in range(leveys):
            tyhja_kentta[-1].append(" ")
    tila["kentta"] = tyhja_kentta
    
    #Miinoittaa kentän
    jaljella = []
    for x in range(leveys):
        for y in range(korkeus):
            jaljella.append((x, y))
    for i in range(tila["miinojen_maara"]):
        while True:
            vapaus = False
            miinoitusleveys = random.randint(0, len(tila["kentta"][0]) - 1)
            miinoituskorkeus = random.randint(0, len(tila["kentta"]) - 1)
            for i2 in range(len(jaljella)):   #Käy läpi vapaat ruudut ja vertaa niitä koordinaatteihin
                if jaljella[i2] == (miinoitusleveys, miinoituskorkeus):
                    jaljella.pop(i2)
                    vapaus = True
                    break
            if vapaus:
                tila["kentta"][miinoituskorkeus][miinoitusleveys] = "x"
                break

def tulvataytto(kentta, x, y):
    """
    Merkitsee kentällä olevat tuntemattomat alueet turvalliseksi siten, 
    että täyttö aloitetaan annetusta x, y -pisteestä. Täyttö pysähtyy kentän reunaan, miinaan tai numero-ruutuun.
    """
    lista = [(x, y)]
    x, y = lista[0]
    if kentta[y][x] == "x":
        lista.pop(0)
    while True:
        if len(lista) == 0:
            break
        x, y = lista[len(lista) - 1]
        lista.pop()
        miinojen_maara_ymparilla = laske_miinat_ymparilta(x, y)
        kentta[y][x] = miinojen_maara_ymparilla
        for x1 in range(3):
            for y1 in range(3):
                if tarkista_koordinaatit(x1 + x - 1, y1 + y - 1):
                    pass
                elif kentta[y + y1 - 1][x + x1 - 1] == "listassa" or laske_miinat_ymparilta(x, y) != "0":
                    pass
                elif kentta[y + y1 - 1][x + x1 - 1] == " ":
                    kentta[y + y1 - 1][x + x1 - 1] = "listassa"
                    lista.append((x1 + x - 1, y1 + y - 1))

def laske_miinat_ymparilta(xk, yk):
    """
    Laskee yhden ruudun ympärillä olevat miinat ja palauttaa niiden lukumäärän merkkijonona.
    """
    leveys, korkeus = tila["kentan_koko"]
    miinat = 0
    for y in range(3):
        for x in range(3):
            if tarkista_koordinaatit(x + xk - 1, y + yk - 1):
                miinat
            elif tila["kentta"][y + yk - 1][x + xk - 1] == "x":
                miinat = miinat + 1
            elif tila["kentta"][y + yk - 1][x + xk - 1] == "lippu_jonka_alla_miina":
                miinat = miinat + 1
    return str(miinat)

def tarkista_koordinaatit(xk, yk):
    """
    Tarkistaa ovatko annetut x, y -koordinaatit annettujen rajojen ulkopuolella.
    Palauttaa False, jos koordinaatit ovat rajojen sisällä; muuten palautetaan True.
    """
    leveys, korkeus = tila["kentan_koko"]
    if xk >= leveys or xk < 0 or yk >= korkeus or yk < 0:
        return True
    else: 
        return False

def hiiri_kasittelija(x, y, nappi, muokkausnapit):
    """
    Tätä funktiota kutsutaan kun käyttäjä klikkaa sovellusikkunaa hiirellä.
    Riippuen painetusta painikkeesta ja pelin tilanteesta tekee erilaisia asioita.
    """
    if nappi == 4:
        nappi = "oikea"
    elif nappi == 2:
        nappi = "keski"
    elif nappi == 1:
        nappi = "vasen"
    leveys, korkeus = tila["kentan_koko"]
    
    if tila["tilanne"] == "peli":
        tila["pelin_kesto"][2] = tila["pelin_kesto"][2] + 1
        sarake = math.ceil((x + 1) / 40) - 1 #Laskee milllä sarakkeella(pystyrivillä) hiiren näppäintä painettiin
        rivi = math.ceil((y + 1) / 40) - 1 #Laskee millä rivillä(vaakarivillä) hiiren näppäintä painettiin
        if nappi == "vasen":
            miinojen_maara_ymparilla = laske_miinat_ymparilta(sarake, rivi)
            if tila["kentta"][rivi][sarake] != "x" and tila["kentta"][rivi][sarake] != " ":
                pass
            elif tila["kentta"][rivi][sarake] == "x":
                print("Miina! Hävisit pelin.")
                tilastot()
                haravasto.lopeta()
                main()
            elif miinojen_maara_ymparilla == "0":
                tulvataytto(tila["kentta"], sarake, rivi)
                piirra_kentta()
            elif miinojen_maara_ymparilla != "0":
                tila["kentta"][rivi][sarake] = miinojen_maara_ymparilla
                piirra_kentta()
        
        elif nappi == "oikea":
            if tila["kentta"][rivi][sarake] == "f":
                tila["kentta"][rivi][sarake] = " "
                piirra_kentta()
            elif tila["kentta"][rivi][sarake] == "lippu_jonka_alla_miina":
                tila["kentta"][rivi][sarake] = "x"
                piirra_kentta()
            elif tila["kentta"][rivi][sarake] == "x":
                tila["kentta"][rivi][sarake] = "lippu_jonka_alla_miina"
                piirra_kentta()
            elif tila["kentta"][rivi][sarake] != " ":
                pass
            else:
                tila["kentta"][rivi][sarake] = "f"
                piirra_kentta()
        aukaistut_ruudut = 0
        for yk in range(korkeus):
            for xk in range(leveys):
                if tila["kentta"][yk][xk] != "x" and tila["kentta"][yk][xk] != "lippu_jonka_alla_miina":
                    if tila["kentta"][yk][xk] != " " and tila["kentta"][yk][xk] != "f":
                        aukaistut_ruudut = aukaistut_ruudut + 1
        if aukaistut_ruudut == leveys * korkeus - tila["miinojen_maara"]:
            print("Kaikki miinattomat ruudut on aukaistu, voitit pelin!")
            tilastot()
            haravasto.lopeta()
            main()

def tilastot():
    """
    Tallentaa tilastot tilastot.txt tiedostoon tai lukee tilastot tilastot.txt tiedostosta.
    """
    if tila["tilanne"] == "tilasto":
        try:
            with open("tilastot.txt") as luku_tiedosto:
                print("Tilastot peleistäsi:")
                riveja_tulostettu = 0
                for line in luku_tiedosto.readlines():
                    read_line(line)
                    riveja_tulostettu = riveja_tulostettu + 1
                    if riveja_tulostettu == 10:
                        input("Paina enter jatkaaksesi seuraavalle sivulle.")
                        riveja_tulostettu = 0
        except FileNotFoundError:
            print("Et ole pelannut yhtään peliä joten tilasto-tiedostoa ei vielä ole.")
        else:
            input("Paina enter jatkaaksesi.")
            main()
    elif tila["tilanne"] == "peli":
        tila["pelin_kesto"][1] = time.time()
        pelin_kesto_minuuteissa = math.floor((tila["pelin_kesto"][1] - tila["pelin_kesto"][0]) / 60)
        paivamaara = "{:02}-{:02}-{}".format(time.localtime()[2], time.localtime()[1], time.localtime()[0])
        kellonaika = "{:02}.{:02}".format(time.localtime()[3], time.localtime()[4])
        leveys, korkeus = tila["kentan_koko"]
        miinojen_maara = tila["miinojen_maara"]
        
        with open("tilastot.txt", "a") as tallennus_tiedosto:
            tallennus_tiedosto.write("{}, {}, {}, {}, {}, {}, {}\n".format(
                paivamaara, kellonaika, pelin_kesto_minuuteissa, tila["pelin_kesto"][2], leveys, korkeus, miinojen_maara
                ))
        
        tila["pelin_kesto"][0], tila["pelin_kesto"][1], tila["pelin_kesto"][2] = None, None, 0

def read_line(line):
    """
    Lukee tiedostosta tulevan rivin ja tulostaa sen käyttäjälle.
    """
    paivamaara, kellonaika, pelin_kesto_minuuteissa, pelin_kesto_vuoroissa, leveys, korkeus, miinojen_maara = line.split(", ")
    print("Pvm: {}, Klo: {}, Pelin kesto(min): {}, Pelin kesto(vuoroja): {}, Kentän koko: {}x{}, Miinojen määrä: {}".format(
        paivamaara, kellonaika, pelin_kesto_minuuteissa, pelin_kesto_vuoroissa, leveys, korkeus, miinojen_maara
        ))

def piirra_kentta():
    """
    Käsittelijäfunktio, joka piirtää kaksiulotteisena listana 
    kuvatun miinakentän ruudut näkyviin peli-ikkunaan. 
    Funktiota kutsutaan aina kun pelimoottori pyytää ruudun näkymän päivitystä.
    """
    leveys, korkeus = tila["kentan_koko"]
    haravasto.tyhjaa_ikkuna()
    haravasto.piirra_tausta()
    haravasto.aloita_ruutujen_piirto()
    for y in range(len(tila["kentta"])):
        for x in range(len(tila["kentta"][0])):
            if tila["kentta"][y][x] == "x":
                haravasto.lisaa_piirrettava_ruutu(" ",x * 40, y * 40)
            elif tila["kentta"][y][x] == "lippu_jonka_alla_miina":
                haravasto.lisaa_piirrettava_ruutu("f",x * 40, y * 40)
            else:
                haravasto.lisaa_piirrettava_ruutu(tila["kentta"][y][x],x * 40, y * 40)
    haravasto.piirra_ruudut()

def main():
    """
    Toimii pääfunktiona jonka kautta valikot ja kentän alustus sekä kentän piirron alustus toimii.
    """
    try:
        valikko()
    except KeyboardInterrupt:
        print("\nPakotit ohjelman sammumaan painamalla Ctrl + C")
        return
    if tila["tilanne"] == "peli":
        try:
            kysy_kentan_koko()
        except KeyboardInterrupt:
            print("\nPakotit ohjelman sammumaan painamalla Ctrl + C")
            return
        leveys, korkeus = tila["kentan_koko"]
        alusta_kentta()
        haravasto.lataa_kuvat("spritet")
        haravasto.luo_ikkuna(leveys * 40, korkeus * 40)
        haravasto.aseta_hiiri_kasittelija(hiiri_kasittelija)
        haravasto.aseta_piirto_kasittelija(piirra_kentta)
        tila["pelin_kesto"][0] = time.time()
        haravasto.aloita()
    elif tila["tilanne"] == "tilasto":
        tilastot()

if __name__ == "__main__":
    try:
        print("Tervetuloa pelaamaan miinaharavaa!")
        main()
    except KeyboardInterrupt:
        print("\nPakotit ohjelman sammumaan painamalla Ctrl + C")