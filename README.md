# Chess.com's Public Data API

### About
I'm an avid chess player and have been using chess.com consistently for the past two years. I recently learned that chess.com archives just about every game you play. Turns out they also have an extremely convenient and easy to use [API](https://www.chess.com/news/view/published-data-api), which allows you to get access to all that data. My goal was to use the API to compile data on every game, which I could then use to conduct some basic analysis. The program collects data on the following fields for each game: 
* **Player Data**

   Username, Rating, Nationality, Side(white or black), Result (win, lose, etc.), and First Move.

* **Opponent Data**
 
   Username, Rating, Nationality, Side(white or black), Result (win, lose, etc.), and First Move.

* **General Game Data**
 
   Variation, Termination, Number of Moves, and End Date. 

Most data from the API gets processed during the execution of the program, so extending the fields collected each game should be very easy. For example, although the program doesn't (yet) save the moves played, they are all parsed and organized into a Python dictionary.

The ultimate goal for this project is to use my game data to build a chess bot that plays similar to me. Not sure how I'll get there, but I think its a good goal to strive towards, and I hope to learn alot along the way.


### Set Up
* This Project uses Python 3.6
* request-html module to make API requests
* Pipenv is used to manage the virtual environment

 If you haven't installed Pipenv yet here's a link to the [documentation](https://docs.pipenv.org/install/#installing-pipenv). If you've cloned this repository and have Pipenv installed,  run:
```
$ pipenv install
```
You'll also need a `.env` file. Pipenv will use this file to load environment variables. The only environment variable that you'll be setting is your chess.com username. Create and open the `.env` file. 
```
$ touch .env && open .env
```
Then type(without the brackets): 
```
#.env
USERNAME={your username}
```
Alternatively, you can set the USERNAME variable directly  in chess_com/settings.py.
```python
#chess_com/settings.py
USERNAME = 'your username'
```

Although usernames aren't as sensitive as passwords, I'd only recommend this if you don't plan on uploading the code anywhere, or don't mind other people knowing what your chess.com username is.

Once you've set the USERNAME variable, start the virtual environment
```
$ pipenv shell
```

### Testing
This project uses Pythons unittest library for testing. To ensure everything is working properly you should run the tests. 
```
$: python -m unittest
```

```
#output
sss....s..........s..................

--------------------------------------------------------------

Ran 37 tests in 0.019s

OK (skipped=5)
```
If you want to ensure that live API tests are run, set the LIVE_TEST variable in chess_com/settings.py to True.
```python
#chess_com/settings.py
LIVE_TEST = True
```
Running the test with LIVE_TEST set to True will ensure that all tests are run. As long as you don't get any errors While running live tests you'll be good to go.

### Program Execution
To execute the program and build your chess dataset run:
```
$: python chess_com/main.py
```
**Note**: Depending on how many games you've played on chess.com's site this could take several minutes to run. However, subsequent executions of the program should be much quicker as data that required additional requests to chess.com's servers should have been stored in CSVs/nationality.csv.

Along with CSVs/nationality.csv, CSVs/chess_data.csv is created. chess_data.csv contains all the data acquired from the API.


Jupyter Notebook with analysis of the data coming soon!
