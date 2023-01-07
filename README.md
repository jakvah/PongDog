# PongDog

**Sniffing ID cards for Ping Pong data.** PongDog is a simple system for tracking games of ping pong. By connecting two buttons to a RaspberryPi the score of each ping pong player is tracked by the players pressing the button corresponding to their side of the table each time they score a point. When the game is over (one player has enought points for a victory) the results are published to a server. This server keeps track of all games played and updates the players statistics and respective [elo scores](https://en.wikipedia.org/wiki/Elo_rating_system)

Visit jakobvahlin.com/pongdog for a live demo! If you are a student at NTNU, you can register using your student card.

![img](/imgs/pongdog.png)

## PongDog system overview


The PongDog game tracker runs locally on a RaspberryPi (or other computer) connected to a card reader and a set of buttons attached to a pingpong table. The PongDog game tracker waits for to cards to be tapped at the card reader. When two unique cards are detected 

## Setup

To get started, clone this repository

```
git clone https://github.com/jakvah/PongDog.git
```

### Run with Docker

First, ensure that the ``DOCKER`` parameter is set to ```True``` in the [PongDog config file](/pongdog/config/pongdog_config.py).

Then, from the top directory in the repository, execute 

```bash
docker-compose up -d
```
This will build the PongDog docker image. After running this command, allow up to 20 seconds for the docker image to setup the MySQL database. To ensure that the MySQL database is ready, run 

```
docker logs gamedb
```

and ensure that the last or next to last row of the outputs reads:

```
[Note] mysqld: ready for connections.
```

Finally, to run the PongDog docker container, run

```
docker-compose run -d -p 5000:5000 app
```

The docker container should be up and running. The PongDog application can be accessed at ``localhost:5000``

### Run without Docker
To run without docker, ensure that the ``DOCKER`` parameter is set to ```False``` in the [PongDog config file](/pongdog/config/pongdog_config.py). Then, from the top directory execute

```
python -m pongdog
```
The PongDog application can be accessed at ``localhost:5000``
