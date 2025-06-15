# TechTori

Yksinkertainen markkinapaikka tietokonekomponenttien ostamiseen ja myymiseen. Luo ilmoituksia, selaa osia kaikki yhdessä paikassa.

## Sovelluksen toiminta

- [x] Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään.
- [ ] Käyttäjä pystyy luomaan ilmoituksen, muokkaamaan ja poistamaan sen.
- [ ] Käyttäjä pystyy selaamaan ilmoituksia ja etsimään tiettyjä osia.
- [ ] Käyttäjä pystyy lisäämään ilmoituksia suosikkeihin.
- [ ] Sovelluksessa on käyttäjäsivut, jossa näkyvät käyttäjän ilmoitukset.
- [ ] Käyttäjä pystyy valitsemaan ilmoitukselle yhden tai useamman luokituksen (esim. osan tyyppi, merkki, tavaran kunto jne.)
- [ ] Käyttäjä pystyy "ostamaan" ilmoituksen, jolloin se poistuu aktiiivisista ilmoituksista.

## Sovelluksen asennus

Asenna `flask`-kirjasto:

```bash
pip install flask
```

Luodaan tietokanta taulu ja alustetaan se alkutiedoilla:

```bash
sqlite3 database.db < schema.sql
sqlite3 database.db < init.sql
```

Käynnistä sovellus:

```bash
flask run
```
