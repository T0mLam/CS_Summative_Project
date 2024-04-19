# CS_Summative_Project
ideas: https://docs.google.com/document/d/1PjHyx3oUo5CyIJFBlcl2JTdJCbSXaTWiw3DgXN5wi1Q/edit?usp=sharing <br />
contributions: https://docs.google.com/document/d/1syaOCdkSoAIZYQWNzE3ENHQJu3C2wdXCBobd5nMAENo/edit?usp=sharing
USER GUIDE: https://docs.google.com/document/d/15RRUfeAwbyMsStFzGfrKrn4ljrcbwHTceDP3UpF9z74/edit?usp=sharing

## Install Dependencies
The `requirements.txt` file contains all external libraries required to run the app.

To install all dependencies, execute the following command from the project's root directory:
```bash
pip install -r requirements.text
```

## Run App
The `graph_game/` folder contains `app.py` and other modules for the game logic, data stuctures and database.

To run the app, execute the following command from the project's root directory:
```bash
python -m graph_game.app
```

## Run Unit Tests
The `tests/` folder contains unit tests for the modules in `graph_game/`.

To run the tests, execute the following command from the project's root directory:
```bash
python -m unittest tests.{test module}
```
Replace `{test module}` with the name of the test module, e.g. `test_node` to run the tests 
