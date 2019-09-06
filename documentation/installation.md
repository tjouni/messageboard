### Installation instructions

#### Local installation with sqlite3

   * Install python version 3.5 or newer
   * Install sqlite3
   * Download and extract the project
   * Create virtual environment `python3 -m venv venv`
   * Activate virtual environment `source venv/bin/activate`
   * Upgrade pip `pip install --upgrade pip`
   * Install project dependencies `pip install -r requirements.txt`
   * Run the application `python3 run.py`
   * Use a web browser to navigate to `localhost:5000`
   * Register an account using the register link at the top
      * To set the first admin in the system, look up `user id` in user listing view (1 for the first user registered)
      * Navigate to application folder
      * Open database with sqlite3 `sqlite3 messageboard.db`
      * Insert many-to-many relation for admin privileges into database
      ```
      INSERT INTO account (account_id, role_id) VALUES (user id, 1);
      ```
      * Further role/category changes can be done via UI with the admin account


#### Heroku deployment

  * Install Heroku CLI tools
  * Navigate to project folder and initialize git for the project `git init`
  * Create a repository for the project in github and connect it to the project `git remote add origin [REPO-URL]`
  * Push the project to github
    ```
    git add .
    git push -u origin master
    ```
  * Set up Heroku
    ```
    heroku create [PROJECT-NAME]
    heroku config:set HEROKU=1
    heroku config:set TZ=Europe/Helsinki
    heroku addons:add heroku-postgresql:hobby-dev
    git remote add heroku https://git.heroku.com/[PROJECT-NAME].git
    ```
  * Application is now available at https://[PROJECT-NAME].herokuapp.com
    * Register an account using the register link at the top
    * To set the first admin in the system, look up `user id` in user listing view (1 for the first user registered)
    * Navigate to application folder
    * Open database with heroku psql `heroku pg:psql`
    * Insert many-to-many relation for admin privileges into database
      ```
      INSERT INTO account (account_id, role_id) VALUES (user id, 1);
      ```
    * Further role/category changes can be done via UI with the admin account
