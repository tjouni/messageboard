# messageboard

Flaskilla ja sqlalchemyllä toteutettu keskustelufoorumi, jossa on käyttäjiä. Jokainen käyttäjä voi kuulua useampaan kategoriaan. Viestiketjut näkyvät käyttäjille, jos käyttäjä ja ketju kuuluvat samaan kategoriaan. Yksi ketju kuuluu aina vain yhteen kategoriaan. Käyttäjät voivat kirjoittaa viestejä ketjuihin, joihin heillä on oikeudet. Ylläpitäjä voi muokata ja poistaa kaikkien kirjoittamia viestejä, lisätä/poistaa/muokata kategorioita ja rooleja, sekä asettaa käyttäjille kategorioita ja rooleja.

#### Työhön jääneet puutteet

 * Viestiketjuun vastatessa sovellus siirtyy aina viestiketjun ensimmäiselle sivulle, vaikka järkevämpää olisi siirtyä ketjun loppuun
 * Ainoastaan admin-roolilla on ohjelmassa normaalikäyttäjästä poikkeavaa toiminnallisuutta


### Links to documentation (in English)

  * [Relational diagram and CREATE TABLE -statements](https://github.com/tjouni/messageboard/blob/master/documentation/db_info.md)
  * [Use cases](https://github.com/tjouni/messageboard/blob/master/documentation/usecases.md)
  * [Installation](https://github.com/tjouni/messageboard/blob/master/documentation/installation.md)
  * [Usage instructions](https://github.com/tjouni/messageboard/blob/master/documentation/user_manual.md)
  * [Application in heroku](https://tjouni-messageboard.herokuapp.com/)
    * basic user: erkki/esimerkki
    * admin role user: admin/1234

### Arvosanan 5 vaatimukset

- [X] Vähintään kolme tietokohdetta, eli vähintään 3 tietokantataulua joiden lisäksi mahdolliset liitostaulut.
  * 5 kpl
- [X] Kirjautumisen lisäksi käyttäjä on yhdistetty tietokannassa johonkin tietokohteeseen (ja tätä yhteyttä käytetään), eli käyttäjien tietoja ei tule käyttää pelkästään kirjautumisen osana.
  * Käyttäjä liittyy rooleihin, kategorioihin ja viesteihin. Osa toiminnoista on saavutettavissa vain admin roolilla, ja kategoriat rajoittavat näkyviä/saavutettavia lankoja (eli lankaan ei pääse vaikka olisi oikea osoite tiedossa)
- [X] Vähintään kahdesta tietokohteesta täysi CRUD (eli luomis-, lukemis-, päivitys-, ja poistotoiminnallisuus).
  * Täysi CRUD account-, role- ja category-tietokohteissa; message-taulun delete ei poista viestejä, vaan muuttaa lähettäjän nulliksi, muuten täysi
- [X] Yksi tai useampi monesta moneen -suhde.
  * 2 kpl, user-category ja user-role
- [X] Vähintään kaksi monimutkaisempaa useampaa tietokantataulua käyttävää yhteenvetokyselyä. Yhteenvetokyselyt ovat perustellusti (järkevä) osa sovelluksen käyttötapauksia ja toimintaa.
  * 3 kpl. Users, categories ja roles sivujen data tuotetaan yhteenvetokyselyillä, jotka löytyvät myös käyttötapauksista.
