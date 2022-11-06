import random
import logging
from collections import namedtuple,Counter

POPULATION_SIZE = 100
OFFSPRING_SIZE = 50
NUM_GENERATIONS = 1000

logging.basicConfig(format="%(message)s", level=logging.INFO)
Individual = namedtuple("Individual", ["selected","solution","available"])

def problem(N, seed=None):
    random.seed(seed)
    return [
        list(set(random.randint(0, N - 1) for n in range(random.randint(N // 5, N // 2))))
        for n in range(random.randint(N, N * 5))
    ]

def fitness(state):
    #selected=state[0]
    solution = state[0]
    #return len(set(newlist) & selected), -len(set(newlist) | selected)
    cnt = Counter()
    cnt.update(sum((e for e in solution), start=()))
    return  sum(cnt[c] == 1 for c in cnt),0

def tournament(population,tournament_size=2):
    return max(random.choices(population,k=tournament_size), key=lambda i:fitness(i))
def mutation(state):
    solution,available=state  #selected,
    removeTuple=random.choice(solution) if len(solution)>0 else ()
    #if()
    addTuple=random.choice(available) if len(available)>0 else ()
    #selected=selected-set(removeTuple)
    #selected=selected|set(addTuple)
    available=tuple(x for x in available if x!=addTuple)
    solution=(*(x for x in solution if x!=removeTuple),addTuple)
    return (solution,available)  #selected,

def crossover(p1,p2):
    solution1, available = p1
    solution2, _ = p2
    cut1=random.randint(0,len(solution1))
    cut2 = random.randint(0, len(solution2))

    solution = tuple(set((*solution1[: cut1], *solution2[cut2 :])))
    newAvailable=tuple((set(solution1)|set(available))-set(solution))
    return (solution, newAvailable)

def main():
    for N in [5, 10, 20, 100,500,1000]:
        lists = sorted(problem(N, seed=42), key=lambda l: len(l))
        tuples = tuple(tuple(_) for _ in set(tuple(l) for l in lists))

        #tuples = tuple(tuple(sublist) for sublist in filteredLists)
        #print('\ntuples: ',tuples,'\n')

        population = list()
        # generate initial population, random
        for genome in [tuple(random.choices(tuples,k=random.randint(1,len(tuples)))) for _ in range(POPULATION_SIZE)]:
            #selected=set()
            #for _ in genome:
            #    selected=selected | set(_)
            available=tuple(set(tuples)-set(genome))
            population.append((tuple(set(genome)),available)) #eve add fitness  selected,

        fitness_log = [(0, fitness(i)) for i in population]

        for g in range(NUM_GENERATIONS):
            offspring = list()
            for i in range(OFFSPRING_SIZE):
                if random.random() < 0.2:
                    p = tournament(population)
                    o = mutation(p)
                else:
                    p1 = tournament(population)
                    p2 = tournament(population)
                    o = crossover(p1, p2)
                f = fitness(o)
                fitness_log.append((g + 1, f))
                offspring.append(o)
            population += offspring
            # sort and select the fittest mu
            population = sorted(population, key=lambda i: fitness(i), reverse=True)[:POPULATION_SIZE]
            if(fitness(population[0])[0]==N):
                break
        solution=population[0][0]
        print("solution found: ",solution)
        print(f"Solution for N={N}: w={sum(len(_) for _ in solution)} (bloat={(sum(len(_) for _ in solution) - N) / N * 100:.0f}%)")

        #print(f"Solution for N={N}: w={sum(len(_) for _ in solution)} (bloat={(sum(len(_) for _ in solution) - N) / N * 100:.0f}%)")

if __name__=="__main__":
    main()