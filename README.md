# PongDog
Sniffing ID cards for Ping Pong data

### Crispdog

To run PongDog locally, better known as CrispDog, execute the following from the top directory;

```
py -m pongdog
```
This will launch the web app.

#### Crispdog scores

The local crispdog scores are expected to be stores in the scores.txt file. This file has the following format:
```
Line 1: Start time
Line 2: p1_id, p1_name, p1_elo, p1_score
Line 3: p2_id, p2_name, p2_elo, p2_score
```