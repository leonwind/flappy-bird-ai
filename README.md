# Flappy-Bird-Ai

Implemented a genetic algorithm ([NEAT](https://en.wikipedia.org/wiki/Neuroevolution_of_augmenting_topologies)) to generate and optimize neural networks to play Flappy Bird.
It normally takes around 10 generations until at least one bird from the population evolves, which will not die anymore.

## Usage
To let the genetic algorithm train an agent, use:
```shell
python -m flappy_bird.game
```

To just play the game for yourself, use:
```shell 
python -m flappy_bird.game -play
```
