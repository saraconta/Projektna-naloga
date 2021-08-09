import bottle
from model import Stanje, Ocena, Predmet


def nalozi_uporabnikovo_stanje():
    uporabnisko_ime = bottle.request.get_cookie("uporabnisko_ime")
    if uporabnisko_ime:
        try:
            stanje = Stanje.preberi_iz_datoteke(uporabnisko_ime)
        except FileNotFoundError:
            stanje = Stanje()
        return stanje
    else:
        bottle.redirect("/prijava/")


def shrani_uporabnikovo_stanje(stanje):
    uporabnisko_ime = bottle.request.get_cookie("uporabnisko_ime")
    stanje.shrani_v_datoteko(uporabnisko_ime)


@bottle.get("/")
def osnovna_stran():
    stanje = nalozi_uporabnikovo_stanje()
    return bottle.template(
        "osnovna_stran.html",
        ocene=stanje.trenutni_predmet.ocene if stanje.trenutni_predmet else [],
        predmeti=stanje.predmeti,
        trenutni_predmet=stanje.trenutni_predmet,
        uporabnisko_ime=bottle.request.get_cookie("uporabnisko_ime"),
    )


@bottle.get("/prijava/")
def prijava_get():
    return bottle.template("prijava.html", napake={}, polja={}, uporabnisko_ime=None)


@bottle.post("/prijava/")
def prijava_post():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    bottle.response.set_cookie("uporabnisko_ime", uporabnisko_ime, path="/")
    bottle.redirect("/")


@bottle.post("/odjava/")
def odjava_post():
    bottle.response.delete_cookie("uporabnisko_ime", path="/")
    print("piškotek uspešno pobrisan")
    bottle.redirect("/")


@bottle.post("/dodaj/")
def dodaj_predmet():
    ime = bottle.request.forms.getunicode("ime")
    opis = bottle.request.forms.getunicode("opis")
    poskus = bottle.request.forms.getunicode("poskus")
    predmet = Predmet(ime, opis, poskus)
    stanje = nalozi_uporabnikovo_stanje()
    stanje.dodaj_predmet(predmet)
    shrani_uporabnikovo_stanje(stanje)
    bottle.redirect("/")


@bottle.get("/dodaj-oceno/")
def dodaj_oceno_get():
    return bottle.template("dodaj_oceno.html", napake={}, polja={})


@bottle.post("/dodaj-oceno/")
def dodaj_oceno_post():
    vrednost = bottle.request.forms.getunicode("vrednost")
    polja = {"vrednost": vrednost}
    stanje = nalozi_uporabnikovo_stanje()
    napake = stanje.preveri_podatke_novega_predmeta(vrednost)
    if napake:
        return bottle.template("dodaj_oceno.html", napake=napake, polja=polja)
    else:
        ocena = Ocena(vrednost)
        stanje.dodaj_oceno(ocena)
        shrani_uporabnikovo_stanje(stanje)
        bottle.redirect("/")


@bottle.post("/zamenjaj-trenutni-predmet/")
def zamenjaj_trenutni_predmet():
    print(dict(bottle.request.forms))
    indeks = bottle.request.forms.getunicode("indeks")
    stanje = nalozi_uporabnikovo_stanje()
    ocena = stanje.ocene[int(indeks)]
    stanje.trenutni_predmet = ocena
    shrani_uporabnikovo_stanje(stanje)
    bottle.redirect("/")


@bottle.error(404)
def error_404(error):
    return "Ta stran ne obstaja!"


bottle.run(reloader=True, debug=True)