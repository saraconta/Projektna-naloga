from model import Stanje, Predmet, Ocena

IME_DATOTEKE = "stanje.json"
try:
    moj_model = Stanje.preberi_iz_datoteke(IME_DATOTEKE)
except FileNotFoundError:
    moj_model = Stanje()

DODAJ_PREDMET = 1
POBRISI_PREDMET = 2
ZAMENJAJ_PREDMET = 3
DODAJ_OCENO = 4
POBRISI_OCENO = 5
IZHOD = 6


def preberi_stevilo():
    while True:
        vnos = input("> ")
        try:
            return int(vnos)
        except ValueError:
            print("Vnesti morate število.")


def izberi_moznost(moznosti):
    """Uporabniku našteje možnosti ter vrne izbrano."""
    for i, (_moznost, opis) in enumerate(moznosti, 1):
        print(f"{i}) {opis}")
    while True:
        i = preberi_stevilo()
        if 1 <= i <= len(moznosti):
            moznost, _opis = moznosti[i - 1]
            return moznost
        else:
            print(f"Vnesti morate število med 1 in {len(moznosti)}.")


def prikaz_predmeta(predmet):
    vsa = predmet.stevilo_vseh()
    return f"{predmet.ime} ({vsa})"


def prikaz_ocene(ocena):
    return f"{ocena.vrednost}"


def izberi_predmet(model):
    return izberi_moznost([(predmet, prikaz_predmeta(predmet)) for predmet in model.predmeti])


def izberi_oceno(model):
    return izberi_moznost(
        [
            (ocena, prikaz_ocene(ocena))
            for ocena in model.trenutni_predmet.ocene
        ]
    )


def tekstovni_vmesnik():
    prikazi_pozdravno_sporocilo()
    while True:
        prikazi_trenutni_predmet()
        ukaz = izberi_moznost(
            [
                (DODAJ_PREDMET, "dodaj nov predmet"),
                (POBRISI_PREDMET, "pobriši predmet"),
                (ZAMENJAJ_PREDMET, "prikaži drug predmet"),
                (DODAJ_OCENO, "dodaj novo oceno"),
                (POBRISI_OCENO, "pobriši oceno"),
                (IZHOD, "zapri program"),
            ]
        )
        if ukaz == DODAJ_PREDMET:
            dodaj_predmet()
        elif ukaz == POBRISI_PREDMET:
            pobrisi_predmet()
        elif ukaz == ZAMENJAJ_PREDMET:
            zamenjaj_predmet()
        elif ukaz == DODAJ_OCENO:
            dodaj_oceno()
        elif ukaz == POBRISI_OCENO:
            pobrisi_oceno()
        elif ukaz == IZHOD:
            moj_model.shrani_v_datoteko(IME_DATOTEKE)
            print("Nasvidenje!")
            break


def prikazi_pozdravno_sporocilo():
    print("Pozdravljeni!")


def prikazi_trenutni_predmet():
    if moj_model.trenutni_predmet:
        for predmet in moj_model.trenutni_predmet.ocene:
            print(f"- {prikaz_ocene(ocena)}")
    else:
        print("Ker nimate še nobenega predmeta, morate enega ustvariti.")
        dodaj_predmet()


def dodaj_predmet():
    print("Vnesite podatke novega predmeta.")
    ime = input("Ime> ")
    nov_predmet = Predmet(ime)
    moj_model.dodaj_predmet(nov_predmet)


def pobrisi_predmet():
    predmet = izberi_predmet(moj_model)
    moj_model.pobrisi_predmet(predmet)


def zamenjaj_predmet():
    print("Izberite predmet, na katerega bi preklopili.")
    predmet = izberi_predmet(moj_model)
    moj_model.zamenjaj_predmet(predmet)


def dodaj_oceno():
    print("Vnesite podatke nove ocene.")
    vrednost = input("Vrednost> ")
    nova_ocena = Ocena(vrednost)
    moj_model.dodaj_oceno(nova_ocena)


def pobrisi_oceno():
    ocena = izberi_oceno(moj_model)
    moj_model.pobrisi_oceno(ocena)


tekstovni_vmesnik()