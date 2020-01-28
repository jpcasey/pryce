# Pryce
This will be updated periodically as we get further along.
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
  * `python main.py` will start the dev server on http://localhost:8080

### Deployments
This repository is configured to use Travis CI.  There are not any tests being run yet.  But, Travis does handle the automated deployments to our [Google App Engine](https://console.cloud.google.com/) instance.  Any pushes to master will be subsequently deployed to app engine, so we should aim to commit any breaking changes to a branch and create a Pull Request to merge into master once everything looks OK.
