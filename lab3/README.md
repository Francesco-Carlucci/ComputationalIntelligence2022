# Computational Intelligence

## Lab3: Nim

by Matteo Colucci (@MattColu) and Francesco Carlucci (@Francesco-Carlucci)

## 3.1: Expert system

An agent that plays with the optimal mathematical strategy, using nim sum.


## 3.2: Genetic algorithm for Nim

The genetic algorithm generates rule-based agents combining conditions (when to apply the rule)
places (on which heap) and actions (how many elements to take). The fitness is the win ratio 
against a pure random player. To check the correctness of the algorithm we added the condition,
action and place of the expert system, it actually converged to a nimsum agent. Without the xor operator,
combining our rules only it achieve about 85% win ratio against pure random.

results:
Solution : genome=[('even_elems', 'half', 'most'), ('odd_stacks', 'half', 'most'), ('even_stacks', 'all', 'most')] (fitness=87.8%)

## 3.3: minmax

An implementation of the minmax algorithm for nim. It's able to exhaustively solve the game up to
a nim size of 5 using alfa-beta pruning. For higher sizes, 7, at a certain depth it does random 
sampling evaluating only a fration of the possible branches.

## 3.4 Reinforcement learning

A reinforcement learning strategy for nim. It learns from multiple games classifying each state
in the game with a reward.