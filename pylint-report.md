# Pylint-raportti

Pylint antaa seuraavan raportin sovelluksesta komennolla `pylint *.py`:

```
************* Module app
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:5:0: E0401: Unable to import 'flask' (import-error)
app.py:14:0: C0103: Constant name "app" doesn't conform to UPPER_CASE naming style (invalid-name)
app.py:18:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:23:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:31:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:38:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:51:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:58:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:96:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:135:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:155:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:163:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:213:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:226:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:281:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:302:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:334:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:364:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:380:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:391:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module categories
categories.py:1:0: C0114: Missing module docstring (missing-module-docstring)
categories.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
categories.py:9:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module conditions
conditions.py:1:0: C0114: Missing module docstring (missing-module-docstring)
conditions.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
conditions.py:9:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module config
config.py:1:0: C0114: Missing module docstring (missing-module-docstring)
************* Module db
db.py:1:0: C0114: Missing module docstring (missing-module-docstring)
db.py:2:0: E0401: Unable to import 'flask' (import-error)
db.py:5:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:12:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:20:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:24:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module favorites
favorites.py:1:0: C0114: Missing module docstring (missing-module-docstring)
favorites.py:1:0: E0401: Unable to import 'flask' (import-error)
favorites.py:5:0: C0116: Missing function or method docstring (missing-function-docstring)
favorites.py:19:0: C0116: Missing function or method docstring (missing-function-docstring)
favorites.py:33:0: C0116: Missing function or method docstring (missing-function-docstring)
favorites.py:45:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module listings
listings.py:1:0: C0114: Missing module docstring (missing-module-docstring)
listings.py:2:0: E0401: Unable to import 'flask' (import-error)
listings.py:6:0: C0116: Missing function or method docstring (missing-function-docstring)
listings.py:54:0: C0116: Missing function or method docstring (missing-function-docstring)
listings.py:84:0: C0116: Missing function or method docstring (missing-function-docstring)
listings.py:101:0: C0116: Missing function or method docstring (missing-function-docstring)
listings.py:135:0: C0116: Missing function or method docstring (missing-function-docstring)
listings.py:151:0: C0116: Missing function or method docstring (missing-function-docstring)
listings.py:160:0: C0116: Missing function or method docstring (missing-function-docstring)
listings.py:169:0: C0116: Missing function or method docstring (missing-function-docstring)
listings.py:177:0: C0116: Missing function or method docstring (missing-function-docstring)
listings.py:198:0: C0116: Missing function or method docstring (missing-function-docstring)
listings.py:208:0: C0116: Missing function or method docstring (missing-function-docstring)
listings.py:218:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module seed
seed.py:1:0: C0114: Missing module docstring (missing-module-docstring)
************* Module users
users.py:1:0: C0114: Missing module docstring (missing-module-docstring)
users.py:1:0: E0401: Unable to import 'werkzeug.security' (import-error)
users.py:6:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:13:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:28:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:36:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:44:0: C0116: Missing function or method docstring (missing-function-docstring)

------------------------------------------------------------------
Your code has been rated at 8.19/10 (previous run: 8.19/10, +0.00)
```

## Docstring-ilmoitukset

Suuri osa raportin ilmoituksista liittyy puuuttuviin docstringeihin:

```
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:18:0: C0116: Missing function or method docstring (missing-function-docstring)
```
Sovelluksen kehityksessä on tehty tietoisesti päätös, ettei docstringejä lisätä.

## Import-ilmoitukset

Raportissa on useita import-ilmoituksia, kuten:

```
app.py:5:0: E0401: Unable to import 'flask' (import-error)
db.py:2:0: E0401: Unable to import 'flask' (import-error)
favorites.py:1:0: E0401: Unable to import 'flask' (import-error)
listings.py:2:0: E0401: Unable to import 'flask' (import-error)
users.py:1:0: E0401: Unable to import 'werkzeug.security' (import-error)
```

Pylint ei löydä kirjastoja, vaikka ne on asennettuna. Kuitenkin sovelluksessa ei ole ongelmaa kirjastojen kanssa.

## Vakionimien ilmoitus
Raportissa on myös vakionimien ilmoitus:

```
app.py:14:0: C0103: Constant name "app" doesn't conform to UPPER_CASE naming style (invalid-name)
```

Tässä koodin päätasolla määritelty muuttuja tulkitaan vakioksi. Pylint suosittelee vakiomuotoa, mutta tässä tapauksessa on järkevämpää käyttää `app`-muuttujaa Flask-sovelluksen nimenä. Muut vakionimi-ilmoitukset ovat sovelluksessa korjattuja.
