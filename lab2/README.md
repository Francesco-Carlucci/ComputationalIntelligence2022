# Lab 2: Set Covering with Genetic Algorithms
The aim of this lab is to solve the pseudo set cover problem, as formalized in the first lab, with genetic algorithms.
My solution is a basic genetic algorithm, that use two genetic operators, one mutation and one crossover and generate
offsprings with either one or the other. The genome of the individuals is represented as a tuple of tuples, not
an array of boolean flags.

## Fitness and Tournament functions
The tournament size is always two, we pick two random individuals and select the fittest. The fitness function
is a tuple of two elements, first the number of covered elements and then the difference between N and the 
solution length. The first element selects valid solutions or measure how far from feasibility a solution is.
This allows also unfeasible solutions in the population that may bring a good solution in future generations,
tests shows that is almost equivalent to a hard check that discard unfeasible offsprings.
The second term ranks solution with regard to their distance from the optimal one, called bloat at the end.

## Genetic operators
The genetic operators used are really straightforward, the mutation swap a list in the solution with another
left out list (picking from "available"), tweaking a solution with a different list that may make it valid 
or reduce the number of repeated numbers.

The crossover operator select a cut point for each parent and then create the offspring selecting the first
lists from parent 1 and the rest from parent 2. This modifies also the overall length of the solution, contrary
to mutation.

## Genetic Algorithm
The genetic algorithm initializes the population selecting random lists in each individual. Then at each 
generation it generates offsprings using either mutation or crossover. Offsprings are added to the 
previous population. Unfeasible solutions are discarded only at the end.

## Results
With parameters:

    POPULATION_SIZE = 100
    OFFSPRING_SIZE = 40
    NUM_GENERATIONS = 1000
    MUTATION_RATE=0.7
    STEADY_LIMIT=200
we obtain the following values, average of ten experiments:

    Solution for N=5:    w=5      (bloat=0%)      fitness calls: 8192
    Solution for N=10:   w=10.1   (bloat=1%)      fitness calls: 9372
    Solution for N=20:   w=24.9   (bloat=24.5%)   fitness calls: 9664
    Solution for N=100:  w=190.1  (bloat=90.1%)   fitness calls: 17724
    Solution for N=500:  w=1441.9 (bloat=188.4%)  fitness calls: 23036
    Solution for N=1000: w=3448.9 (bloat=244.89%) fitness calls: 21860