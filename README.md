# TechTori

Yksinkertainen markkinapaikka tietokonekomponenttien ostamiseen ja myymiseen. Luo ilmoituksia, selaa osia kaikki yhdessä paikassa.

## Sovelluksen toiminta

- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään.
- Käyttäjä pystyy luomaan ilmoituksen, muokkaamaan ja poistamaan sen.
- Käyttäjä pystyy selaamaan ilmoituksia ja etsimään tiettyjä osia.
- Käyttäjä pystyy lisäämään ilmoituksia suosikkeihin.
- Sovelluksessa on käyttäjäsivut, jossa näkyvät käyttäjän ilmoitukset.
- Käyttäjä pystyy valitsemaan ilmoitukselle yhden tai useamman luokituksen (esim. osan tyyppi, merkki, tavaran kunto jne.)
- Käyttäjä pystyy "ostamaan" ilmoituksen, jolloin se poistuu aktiiivisista ilmoituksista.

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
## Testidataraportti

Sovellusta on testattu suurella tietomäärällä `seed.py` tiedoston avulla ja todettu toimivan tehokkuudeltaan hyvin. Isoin korjaus oli sivutuksen lisääminen tuotteiden hakuun.

### Testidatan suurus

Testidata sisälsi 1000 käyttäjää 10^5 ilmoitusta ja 10^5 tykkäystä.
```python
user_count = 1000
listing_count = 10**5
favorite_count = 10**5
```

### Ajat eri operaatioissa

- Etusivu (10 ilmoituksella): 0.01s
- Kirjautuminen / Rekistöröityminen: 0.01s
- 1000:n sivun lataaminen: 0.01s
- Suosikkeihin lisääminen: 0.01s
- Tuoteen ostaminen: 0.01s

Lyhyellä testauksella huomaamme että melkein kaikkien operaatoiden hakemisessa kestää sen 0.01s.

### Lisätyt indeksit

```sql
CREATE INDEX idx_listing_title ON listings(title);
CREATE INDEX idx_category_name ON categories(name);
```

Tehostaakseen tietokantaa olisi indeksejä voinut lisätä muitakin, mutta aikojen ollessaan jo valmiiksi nopeita, ei lisäindeksoinnille ollut tarvetta.


## Credits

Ikonit ladattu [Radix UI Icons](https://www.radix-ui.com/icons) -kirjastosta. (MIT License)
