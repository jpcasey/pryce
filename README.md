# Pryce
This will be updated periodically as we get further along.
## Preparing the Pryce Database
* Set the `SQLALCHEMY_DATABASE_URI` environment variable. An example of a value for this variable would be: `postgresql+psycopg2://<db_user>:<db_password>@localhost:5432/<db_name>`. YMMV given a different type of RDBMS (something other than PostgreSQL) and driver.
* Set the `FLASK_APP` environment variable to `pryce`:
```
export FLASK_APP=pryce
```
* Create a database for use by the application, ensuring that its name matches the name you use in the `SQLALCHEMY_DATABASE_URI` connection string.
* Execute `flask db upgrade -d ./pryce/database/migrations`. You should see output _similar_ to the following:
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.          
INFO  [alembic.runtime.migration] Will assume transactional DDL.               
INFO  [alembic.runtime.migration] Running upgrade bacf2d9c86f2 -> 41277ca11f79, adding name to list model
INFO  [alembic.runtime.migration] Running upgrade 41277ca11f79 -> c827ee4a1745, renaming list to pryce_list
```
This will create all of the tables and constraints necessary for the database to be populated.
* From the root of the project, run `python -m pryce.database.mock_factory`. This will populate the database with mock data.

## Application Server
### Setting Up Your Development Environment
* Make sure you have Python 3.7 or later installed and in your PATH
* `git clone` this repository and `cd` into it
* Create your virtual environment:
  * I think there are a few ways to do this.  I used [venv](https://docs.python.org/3/library/venv.html) to create a virtual environment in `~/envs/PryceEnv` like so:  
    * `python -m venv ~/envs/PryceEnv`
    * `source ~/envs/PryceEnv/bin/activate`
* Install dependencies:
  * `pip install -r requirements.txt`
* Run development server:
  * Set the `FLASK_ENV` environment variable to `development` for easier troubleshooting:
    ```   
    export FLASK_ENV=development
    ```
  * `flask run` will start the dev server on http://localhost:5000 

### Deployments
This repository is configured to use Travis CI.  There are not any tests being run yet.  But, Travis does handle the automated deployments to our [Google App Engine](https://console.cloud.google.com/) instance.  Any pushes to master will be subsequently deployed to app engine, so we should aim to commit any breaking changes to a branch and create a Pull Request to merge into master once everything looks OK.
