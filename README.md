# messageboard

Flaskilla ja sqlalchemyllä toteutettu keskustelufoorumi, jossa on käyttäjiä. Jokainen käyttäjä voi kuulua useampaan kategoriaan. Viestiketjut näkyvät käyttäjille, jos käyttäjä ja ketju kuuluvat samaan kategoriaan. Yksi ketju kuuluu aina vain yhteen kategoriaan. Käyttäjät voivat kirjoittaa viestejä ketjuihin, joihin heillä on oikeudet. Ylläpitäjä voi muokata ja poistaa kaikkien kirjoittamia viestejä, lisätä/poistaa/muokata kategorioita ja rooleja, sekä asettaa käyttäjille kategorioita ja rooleja.

  * [Tietokantakaavio ja CREATE TABLE -lausekkeet](https://github.com/tjouni/messageboard/blob/master/documentation/db_info.md)
  * [Käyttötapaukset](https://github.com/tjouni/messageboard/blob/master/documentation/usecases.md)
  * [Asennusohjeet](https://github.com/tjouni/messageboard/blob/master/documentation/installation.md)
  
  * [Sovellus herokussa](https://tjouni-messageboard.herokuapp.com/)
    * peruskäyttäjä: user/pass: erkki/esimerkki
    * admin: admin/1234
