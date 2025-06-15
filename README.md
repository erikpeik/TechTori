# TechTori

Yksinkertainen markkinapaikka tietokonekomponenttien ostamiseen ja myymiseen. Luo ilmoituksia, selaa osia kaikki yhdessä paikassa.

## Sovelluksen toiminta

- [x] Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään.
- [x] Käyttäjä pystyy luomaan ilmoituksen, muokkaamaan ja poistamaan sen.
- [ ] Käyttäjä pystyy selaamaan ilmoituksia ja etsimään tiettyjä osia.
- [x] Käyttäjä pystyy lisäämään ilmoituksia suosikkeihin.
- [x] Sovelluksessa on käyttäjäsivut, jossa näkyvät käyttäjän ilmoitukset.
- [x] Käyttäjä pystyy valitsemaan ilmoitukselle yhden tai useamman luokituksen (esim. osan tyyppi, merkki, tavaran kunto jne.)
- [x] Käyttäjä pystyy "ostamaan" ilmoituksen, jolloin se poistuu aktiiivisista ilmoituksista.

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

## Credits

Ikonit ladattu [Radix UI Icons](https://www.radix-ui.com/icons) -kirjastosta. (MIT License)
