import json

class Stanje:
    def __init__(self):
        self.predmeti = []
        self.trenutni_predmet = None

    def dodaj_predmet(self, predmet):
        self.predmeti.append(predmet)
        if not self.trenutni_predmet:
            self.trenutni_predmet = predmet

    def pobrisi_predmet(self, predmet):
        self.predmeti.remove(predmet)

    def zamenjaj_predmet(self, predmet):
        self.trenutni_predmet = predmet

    def dodaj_oceno(self, ocena):
        self.trenutni_predmet.dodaj_oceno(ocena)

    def pobrisi_oceno(self, ocena):
        self.trenutni_predmet.pobrisi_oceno(ocena)

    def v_slovar(self):
        return {
            "predmeti": [predmet.v_slovar() for predmet in self.predmeti],
            "trenutni_predmet": self.predmeti.index(self.trenutni_predmet)
            if self.trenutni_predmet
            else None,
        }

    @staticmethod
    def iz_slovarja(slovar):
        stanje = Stanje()
        stanje.predmeti = [
            Predmet.iz_slovarja(sl_predmeta) for sl_predmeta in slovar["predmeti"]
        ]
        if slovar["trenutni_predmet"] is not None:
            stanje.trenutni_predmet = stanje.predmeti[slovar["trenutni_predmet"]]
        return stanje

    def shrani_v_datoteko(self, ime_datoteke):
        with open(ime_datoteke, "w", encoding="utf-8") as dat:
            slovar = self.v_slovar()
            json.dump(slovar, dat)

    @staticmethod
    def preberi_iz_datoteke(ime_datoteke):
        with open(ime_datoteke) as dat:
            slovar = json.load(dat)
            return Stanje.iz_slovarja(slovar)

    def preveri_podatke_novega_predmeta(self, ime):
        napake = {}
        if not ime:
            napake["ime"] = "Ime ne sme biti prazno."
        for predmet in self.predmeti:
            if predmet.ime == ime:
                napake["ime"] = "Ime je že uporabljeno."
        return napake


class Predmet:
    def __init__(self, ime):
        self.ime = ime
        self.predmeti = []

    def dodaj_oceno(self, ocena):
        self.opravila.append(ocena)

    def stevilo_vseh(self):
        return len(self.ocene)

    def v_slovar(self):
        return {
            "ime": self.ime,
            "ocene": [ocena.v_slovar() for ocena in self.ocene],
        }

    @staticmethod
    def iz_slovarja(slovar):
        predmet = Predmet(slovar["ime"])
        predmet.ocene = [
            Ocena.iz_slovarja(sl_ocene) for sl_ocene in slovar["ocene"]
        ]
        return predmet


class Ocena:
    def __init__(self, vrednost):
        self.vrednost = vrednost

    def v_slovar(self):
        return {
            "vrednost": self.vrednost,
        }

    @staticmethod
    def iz_slovarja(slovar):
        return Ocena(
            slovar["vrednost"],
        )