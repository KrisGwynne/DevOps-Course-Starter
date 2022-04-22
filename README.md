# DevOps Apprenticeship: Project Exercise

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install Poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py -UseBasicParsing).Content | python -
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

In order to add all the required environment variables needed to run the project you must first create a Trello account [here](https://trello.com/signup). After creating an account you will then be able to generate an API key and token following the instructions [here](https://trello.com/app-key). Ask a member of the team to give you access to the board, and the value for the `BOARD_ID` environment variable.
## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the Poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Docker
You can also run the app in docker, for both development and production. To do this you must first build the docker image (changing the target and tag to the correct environment):
```bash
docker build --target <production|development> --tag todo-app:<prod|dev> . 
```
You can then run the docker image eg:
```bash
docker run -p 5000:8080 --env-file ./.env  todo-app:<prod|dev>
```
In order to run the app in docker during local development you can mount the project files, so that flask will hot reload when changes are made:
```bash
docker run -p 5000:8080 --env-file ./.env --mount type=bind,source=(pwd)/todo_app,target=/src/todo_app  todo-app:dev 
```

## Testing
The repo contains a testing directory under `./tests`, using the pytest library. To run the tests ensure you are in the tests directory and run:
```bash
$ poetry run pytest
```

To run an individual test run the above command with the path to the test and the name of the test eg:
```bash
$ poetry run pytest view_models/item_view_model_test.py -k 'test_getting_to_do_items_returns_only_to_do_items'
```
### E2e Tests
This repo contains e2e selenium tests. In order to run the tests you must firt ensure that you have firefox installed along with geckodriver to allow selenium to control it. The e2e tests can be found in the e2e_tests diectory. The e2e tests set up a new testing board in trello. In order to allow this to happen you need to add the value of `ORGANISATION_ID` to your .env file.

### Running the ansible playbook
The ansible playbook can be used to deploy and run the todo app on virtual environments included in the ansible-inventory. The playbook can be run using the following command:
```bash
$ ansible-playbook ansible-playbook.yml -i ansible-inventory 
```

## Sytem Archetecture
Diagrams of the system architecture can be found in `/documentation` directory. The diagrams follow the [c4 Model](https://c4model.com/), and can be edited using [this web app](https://app.diagrams.net/).