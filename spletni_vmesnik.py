import bottle
import os
from model import Stanje, Ocena, Predmet

SKRIVNOST = "danesjelepdan"

def nalozi_uporabnikovo_stanje():
    uporabnisko_ime = bottle.request.get_cookie("uporabnisko_ime", secret=SKRIVNOST)
    if uporabnisko_ime:
        try:
            stanje = Stanje.preberi_iz_datoteke(uporabnisko_ime)
        except FileNotFoundError:
            stanje = Stanje()
        return stanje
    else:
        bottle.redirect("/prijava/")


def shrani_uporabnikovo_stanje(stanje):
    uporabnisko_ime = bottle.request.get_cookie("uporabnisko_ime", secret=SKRIVNOST)
    stanje.shrani_v_datoteko(uporabnisko_ime)


@bottle.get("/")
def osnovna_stran():
    stanje = nalozi_uporabnikovo_stanje()
    return bottle.template(
        "osnovna_stran.html",
        predmeti = stanje.predmeti,
        trenutni_predmet = stanje.trenutni_predmet,
        ocene = stanje.predmeti[stanje.trenutni_predmet].ocene if stanje.trenutni_predmet is not None else [],
        uporabnisko_ime = bottle.request.get_cookie("uporabnisko_ime", secret=SKRIVNOST),
    )


@bottle.get("/prijava/")
def prijava_get():
    return bottle.template("prijava.html", napake={}, polja={}, uporabnisko_ime=None)


@bottle.post("/prijava/")
def prijava_post():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    bottle.response.set_cookie("uporabnisko_ime", uporabnisko_ime, path="/", secret=SKRIVNOST)
    bottle.redirect("/")


@bottle.post("/odjava/")
def odjava_post():
    bottle.response.delete_cookie("uporabnisko_ime", path="/", secret=SKRIVNOST)
    print("piškotek uspešno pobrisan")
    bottle.redirect("/")


@bottle.get("/registracija/")
def registracija_get():
    return bottle.template("registracija.html", napake={}, polja={}, uporabnisko_ime=None)


@bottle.post("/registracija/")
def registracija_post():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    if os.path.exists(uporabnisko_ime):
        napake = {"uporabnisko_ime": "Uporabniško ime že obstaja."}
        return bottle.template("registracija.html", napake=napake, polja={"uporabnisko_ime": uporabnisko_ime}, uporabnisko_ime=None)
    else:
        bottle.response.set_cookie("uporabnisko_ime", uporabnisko_ime, path="/", secret=SKRIVNOST)
        Stanje().shrani_v_datoteko(uporabnisko_ime)
        bottle.redirect("/")


@bottle.post("/dodaj/")
def dodaj_oceno():
    vrednost = bottle.request.forms.getunicode("vrednost")
    ocena = Ocena(vrednost)
    stanje = nalozi_uporabnikovo_stanje()
    stanje.dodaj_oceno(ocena)
    shrani_uporabnikovo_stanje(stanje)
    bottle.redirect("/")


@bottle.get("/dodaj-predmet/")
def dodaj_predmet_get():
    return bottle.template("dodaj_predmet.html", napake={}, polja={}, uporabnisko_ime=bottle.request.get_cookie("uporabnisko_ime", secret=SKRIVNOST))


@bottle.post("/dodaj-predmet/")
def dodaj_predmet_post():
    ime = bottle.request.forms.getunicode("ime")
    polja = {"ime": ime}
    stanje = nalozi_uporabnikovo_stanje()
    napake = stanje.preveri_podatke_novega_predmeta(ime)
    print(napake)
    if napake:
        return bottle.template("dodaj_predmet.html", napake=napake, polja=polja, uporabnisko_ime=bottle.request.get_cookie("uporabnisko_ime", secret=SKRIVNOST))
    else:
        predmet = Predmet(ime, ocene=[])
        stanje.dodaj_predmet(predmet)
        shrani_uporabnikovo_stanje(stanje)
        bottle.redirect("/")


@bottle.post("/zamenjaj-trenutni-predmet/")
def zamenjaj_trenutni_predmet():
    print(dict(bottle.request.forms))
    indeks = bottle.request.forms.getunicode("indeks")
    stanje = nalozi_uporabnikovo_stanje()
    stanje.trenutni_predmet = indeks
    shrani_uporabnikovo_stanje(stanje)
    bottle.redirect("/")


@bottle.error(404)
def error_404(error):
    return "Ta stran ne obstaja!"


bottle.run(reloader=True, debug=True)