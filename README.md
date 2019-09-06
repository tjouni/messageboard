# messageboard

Flaskilla ja sqlalchemyllä toteutettu keskustelufoorumi, jossa on käyttäjiä. Jokainen käyttäjä voi kuulua useampaan kategoriaan. Viestiketjut näkyvät käyttäjille, jos käyttäjä ja ketju kuuluvat samaan kategoriaan. Yksi ketju kuuluu aina vain yhteen kategoriaan. Käyttäjät voivat kirjoittaa viestejä ketjuihin, joihin heillä on oikeudet. Ylläpitäjä voi muokata ja poistaa kaikkien kirjoittamia viestejä, lisätä/poistaa/muokata kategorioita ja rooleja, sekä asettaa käyttäjille kategorioita ja rooleja.


### Links to documentation (in English)

  * [Relational diagram and CREATE TABLE -statements](https://github.com/tjouni/messageboard/blob/master/documentation/db_info.md)
  * [Use cases](https://github.com/tjouni/messageboard/blob/master/documentation/usecases.md)
  * [Installation](https://github.com/tjouni/messageboard/blob/master/documentation/installation.md)
  * [Usage instructions](https://github.com/tjouni/messageboard/blob/master/documentation/user_manual.md)
  * [Application in heroku](https://tjouni-messageboard.herokuapp.com/)
    * basic user: erkki/esimerkki
    * admin role user: admin/1234
