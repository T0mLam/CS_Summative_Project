# Graph Game
This work is submitted as my computer science foundation year summative project.

## Project Description
The Graph Game is a game that revolves around a randomly generated fully connected graph. <br>
A player wins by randomly selecting a path that is shorter than the unknown generated distance.

## Install Dependencies
The `requirements.txt` file contains all external libraries required to run the app.

To install all dependencies, execute the following command from the project's root directory:
```bash
pip install -r requirements.txt
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

## Import Data Structures
The `graph_game/data_structures` contains all the data structures utilized in the game.

To import and use the data structure independently, add the following code in your program:
```python
from graph_game.data_structures.{module} import {data structure}
```
Replace `{module}` with the name of the module, `{data structure}` with the name of the class, e.g.
```python
# Import the trie data structure
from graph_game.data_structures.trie import Trie
```
