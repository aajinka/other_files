# Hrací kostka simulující náhodnost ve "stolní" hře
# definice vlastního konstruktoru

class Kostka:
    # počet stěn
    # generátor náhodných čísel, random, metoda randint()
    # přidat privátní atributy, dvě podtržítka
    # kostruktor se deklaruje jako metoda, můžeme až dvě __new__()-volá se při vytvoření objektu a __init__()-při inicializaci objektu
    # vystacíme si s init, metoda bude prázdná (tedy jen self) a pak vložíme PASS, toto KW říká, aby python nic nedělal, jinak vyhodí chybu neb čeká blok příkazů
    def __init__(self, pocet_sten = 6): # v této metodě, když vytvoříme nějakou proměnnou, tak po ukončení metody zanikne, proto počet stěn bude atribut
        #pass
        self.__pocet_sten = pocet_sten 
        # nechci aby mi někdo měnil počet stěn, proto nastavíme
    def __repr__(self): # vrací textovou reprezentaci kostky
        return str ("Kostka({0})".format(self.__pocet_sten))

    def vracet_pocet_sten(self): # vrátí hodnotu atributu počet stěn a tento atribut nastavíme jako neveřejný, atribut není vidět, ale víme, že tam je díky metodě, nelze ho měnit je tzv. read-only
                                 # __ před atribut ho zneviditelní 
        return self.__pocet_sten

    def hod(self): # metoda, která vrátí náhodné číslo od 1 do počtu stěn
        import random as _random # importujeme modul vnitřně
        return _random.randint(1, self.__pocet_sten)
    def __str__(self): # vrací textovou reprezentaci kostky
        return str("Kostka s {0} stěnami.".format(self.__pocet_sten))


# vytvoření kostek
desetistenna = Kostka(10) # ted se zavolá konstruktor s parametrem 10
                    # pokud mám parametr počet stěn a né jasně dané self.__pocet_sten = 6, tak už ta závorka nesmí být prázdná
                    # nebo může být: Kostka(pocet_sten=10)

sestistenna = Kostka() # pokud nastavím výchozí hodnotu první kostky, rovnou do parametru pocet_sten=6, tak může být prázdná
                
                #print(desetistenna.vracet_pocet_sten()) 
                #print(sestistenna .vracet_pocet_sten()) 

# házení kostkami
    #6
#print(sestistenna)
#for _ in range(10):
    #print(sestistenna.hod(), end=" ")

    #10
#print("\n",desetistenna, sep="") # \n a sep="" dáme, aby nám výpis začínal na novém řádku a bez mezer
#for _ in range(10):
    #print(desetistenna.hod(), end=" ")


# Třída reprezentující bojovníka arény.

class Bojovnik:
    def __init__(self, jmeno, zivot, utok, obrana, kostka):
        self._jmeno = jmeno    # jmeno bojovnika
        self._zivot = zivot  
        self._max_zivot = zivot  # maximální počet životů
        self._utok = utok      # útok bojovníka
        self._obrana = obrana  # obrana bojovníka
        self._kostka = kostka  # instance kostky
        self.__zprava = ""                          # tento necháme jako privátní, jde o logiku hry, ta je mágovi k ničemu

    def __str__(self): # vrátí jméno bojovníka
        return str (self._jmeno)

    def __repr__(self): # vrátí v řetězci kód konstruktoru pro funkci eval()
        return str ("Bojovník({0},{1},{2},{3},{4})".format(self._jmeno, self._max_zivot, self._utok, self._obrana, self._kostka))

    
    @property # tzv. dekorátor = vylepšuje metodu a mění metodu na vlastnost
    def nazivu(self):
        return self._zivot> 0 # samotný výraz self.__zivot>0 je logická hodnota, můžu jí rovnou vrátit nebo viz podtím

        #if self.__zivot > 0:
            #return True
        #else:
            #False

# "grafika" 
# vykreslí ukazatel života 

    def graficky_ukazatel(self, aktualni, maximalni):
        celkem = 20
        pocet = int(aktualni/maximalni * celkem)
        if (pocet == 0 and self.nazivu):
            pocet = 1
        return "[{0}{1}]".format("#"*pocet, " "*(celkem-pocet))

    def graficky_zivot(self):
        return self.graficky_ukazatel(self._zivot, self._max_zivot)

         #celkem = 20
         #pocet = int(self._zivot/self._max_zivot* celkem)
         # pocet dílku aktuálního zdraví
         # self_zivot je život odpovídající počtu dílků
         # self.__max_zivot odpovídá celkem dílkům  
         # ještě podmínka, že život je tak nízký, že je počet dílků 0, ale bojovník je stále naživu, takže vykreslíme 1 dílek, aby to nevypadalo, že je mrtvý
         #if (pocet == 0 and self.nazivu):
          #   pocet == 1
         #return "[{0}{1}]".format("#"*pocet, " "*(celkem-pocet))

    def bran_se(self, uder): # bránit se úderu, jehož síla je jako parametr předaná metodě
        zraneni = uder - (self._obrana + self._kostka.hod())
        if zraneni > 0:
            zprava = "{0} utrpěl poškození {1} hp.".format(self._jmeno, zraneni)
            self._zivot = self._zivot - zraneni
            if self._zivot < 0:
                self._zivot = 0
                zprava = zprava[:-1] + "a zemřel."
        else: 
            zprava = "{0} odrazil útok.".format(self._jmeno)
        self._nastav_zpravu(zprava)

    def utoc(self,souper):
        uder = self._utok + self._kostka.hod()
        zprava = "{0} odrazil útok o síle {1} hp.".format(self._jmeno, uder)
        self._nastav_zpravu(zprava)
        souper.bran_se(uder)
       
    def _nastav_zpravu(self, zprava):
        self.__zprava = zprava
    
    def vrat_posledni_zpravu(self):
        return self.__zprava

##kostka = Kostka(10)
##bojovnik = Bojovnik("Zalgorem",100,20,10,kostka)
#print("Bojovnik: {0}".format(bojovnik)) # test __str__()
#print("Naživu:{0}".format(bojovnik.nazivu)) # test naživu
##print("Život: {0}".format(bojovnik.graficky_zivot())) # test graficky_zivot()
#bojovnik.utoc(bojovnik)
#print("Život po útoku: {0}".format(bojovnik.graficky_zivot()))

# útok našeho bojovníka
##souper = Bojovnik("Shadow",60,18,10,kostka)
##souper.utoc(bojovnik)
##print(souper.vrat_posledni_zpravu())
##print("Život: {0}".format(bojovnik.graficky_zivot())) 

class Arena: # kód pro obsluhu bojovníků a výpis zpráv uživateli
    def __init__(self, bojovnik, souper, kostka):
        self.__bojovnik = bojovnik
        self.__souper = souper
        self.__kostka = kostka

    # metody: simulace zápasu, třída Arena aby rovnou přistupovala ke konzoli a né bojovnici, 
    # je třeba metodu která vykreslí obrazovku s aktuálními údaji o kole a životy
    # zprávy o útoku a obraně chceme vypsat s velkou pauzou pro efekt - tzn. pomocná metoda

    def __vykresli_obrazovku(self):
        self.__vycisti_obrazovku() # uvnitř objektu se metoda volá self.název_metody
        print("-------------Aréna------------- \n")
        print("Bojovníci: \n")
        self.__vypis_bojovnika(self.__bojovnik)
        self.__vypis_bojovnika(self.__souper)
        print("")
        #print("{0} {1}".format(self.__bojovnik, self.__bojovnik.graficky_zivot()))  místo sefl.----
        #print("{0} {1}".format(self.__souper, self.__souper.graficky_zivot()))

    def __vycisti_obrazovku(self):
        import sys as _sys                  # moduly sys a subprocess jsou nutné pro vymazání obrazovky konzole
        import subprocess as _subprocess
        if _sys.platform.startswith("win"): # podle OS zavoláme příkaz k vymazání obrazovky
            _subprocess.call(["cmd.exe", "/C", "cls"])
        else:
            _subprocess.call(["clear"])

    def __vypis_zpravu(self, zprava): # další privátní metoda na výpis zprávy s dramatickou pauzou
        import time as _time
        print(zprava)
        _time.sleep(0.75)

    def zapas(self): # bez paramatru ani nebude nic vracet, cyklus bude volat nahodile útoky bojovníků a vypisovat info.obrazovku a zprávy
        
        import random as _random
        print("Vítej v aréně!")
        print("Dnes se utkají {0} s {1}!".format(self.__bojovnik, self.__souper))
        print("Zápas může začít...", end=" ")
        # prohození bojovníků
        if _random.randint(0,1):
            (self.__bojovnik, self.__souper) = (self.__souper, self.__bojovnik) # doporučená šířka řádku je 80 znaků, tohle už je dlouhý :-)

        # cyklus s bojem (jede, dokud jsou oba naživu)
        while (self.__bojovnik.nazivu and self.__souper.nazivu):
            self.__bojovnik.utoc(self.__souper)
            self.__vykresli_obrazovku()
            self.__vypis_zpravu(self.__bojovnik.vrat_posledni_zpravu())
            self.__vypis_zpravu(self.__souper.vrat_posledni_zpravu())
            if self.__souper.nazivu:
                self.__souper.utoc(self.__bojovnik)
                self.__vykresli_obrazovku()
                self.__vypis_zpravu(self.__souper.vrat_posledni_zpravu())
                self.__vypis_zpravu(self.__bojovnik.vrat_posledni_zpravu())
            print("")

    def __vypis_bojovnika(self, bojovnik):
        print(bojovnik)
        print("Život: {0}". format(bojovnik.graficky_zivot()))
        if isinstance(bojovnik, Mag):
            print("Mana: {0}".format(bojovnik.graficka_mana()))


# dědičnost a polymorfismus
# přidáme Mága, bude dědit z Bojovnika, bude mít manu, ta bude 100% a dá mu magický útok, tím e vybije na 0, magický útok bude mít větší damege
# dál bude muset bojovat normálně, s každým útokem se mu bude mana nabíjet např. o 10hp než bude plná
class Mag(Bojovnik): # mág dědí z bojovníka, ale nevidí privátní atributy, tak je nastavíme na VNITRNI, stačí jen kostka a jméno
    def __init__(self, jmeno, zivot, utok, obrana, kostka, mana, magicky_utok):
        super().__init__(jmeno, zivot, utok, obrana, kostka)
        self.__mana = mana
        self.__max_mana = mana
        self.__magicky_utok = magicky_utok


    def utoc(self, souper):
    # mana není naplněna
        if self.__mana < self.__max_mana:
            self.__mana = self.__mana + 10
            if self.__mana > self.__max_mana:
                self.__mana = self.__max_mana
            super().utoc(souper)
    #magický útok
        else:
            uder = self.__magicky_utok + self._kostka.hod()
            zprava = "{0} použil magii za {1} hp.".format(self._jmeno, uder)
            self._nastav_zpravu(zprava)
            self.__mana = 0
            souper.bran_se(uder)

    def graficka_mana(self):
        return self.graficky_ukazatel(self.__mana, self.__max_mana)


    
          

# vytvoření objektů
kostka = Kostka (10)
zalgoren = Bojovnik ("Zalgoren",100,20,10,kostka)
#shadow = Bojovnik("Shadow",60,18,15,kostka)
# použití:mága, místo druhého bojovnika
gandalf = Mag("Gandalf",60,15,12,kostka,30,45)
arena = Arena (zalgoren, gandalf, kostka)

# zápas
arena.zapas()

        