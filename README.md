Welcome to HQ game

This is an online multiplayer trivia question competition via telnet. 

Once the game server is started, it will continue to allow players to connect. Once there are enough players 
in the players pool, a game room will be created to host a game for all the players in the player pool. 

There can be multiple game room in parallel and each of them will have a independent game running

The question is in the format of multiple choice questions with no more than 5 choices. The player will have 10 seconds
to select a choice otherwise it will be considered as skipped. A invalid input from the player will also be considered as
skipped. At the end of each question, the correct answer and the  statistics will be showed. If all the players in the 
game room already answered the question, the correct answer and statistics is immediately display rather than waiting for
the full 10 seconds

A player is eliminated if he/she answers the question incorrectly. The remaing player in the game room will be entering
the next stage with a new question. The game will stop when there is only one player left or when all the players are 
eliminated. 

The question is the in json format. You can easily add more question by expanding the json. If you are interested to see
where the questions are coming from, take a look at this https://opentdb.com/api_config.php

To start the game server:

    python3 GameMaster.py [host] [port] [minPlayers]