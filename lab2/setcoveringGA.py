import random
import logging
from collections import Counter

POPULATION_SIZE = 100
OFFSPRING_SIZE = 40
NUM_GENERATIONS = 1000

logging.basicConfig(format="%(message)s", level=logging.INFO)
#Individual = namedtuple("Individual", ["selected","solution","available"])

def problem(N, seed=None):
    state = random.getstate()
    random.seed(seed)
    return [
        list(set(random.randint(0, N - 1) for n in range(random.randint(N // 5, N // 2))))
        for n in range(random.randint(N, N * 5))
    ]
    random.setstate(state)

def isvalid(solution):
    selected = set()
    for _ in solution:
        selected = selected | set(_)
    return selected==set(range(N))

#@profile
def fitness(state):
    solution = state[0]

    selected = set()
    for _ in solution:
        selected=selected | set(_)
    return len(selected),-(sum(len(_) for _ in solution) - N)  #-len(set(newlist) | selected)
    """
    cnt = Counter()
    cnt.update(sum((e for e in solution), start=()))
    return  (sum(cnt[c] == 1 for c in cnt) ,-sum(cnt[c] - 1 for c in cnt if cnt[c] > 1),)
    """

def tournament(population,tournament_size=2):
    return max(random.choices(population,k=tournament_size), key=lambda i:i[2])

#@profile
def mutation(state):
    solution,available,_=state

    removeIdx=random.randint(0,len(solution)-1) if len(solution)>0 else 0
    addIdx=random.randint(0,len(available)-1) if len(available)>0 else 0

    solution=solution[:removeIdx]+solution[removeIdx+1:]
    if len(available)>0:
        solution+=(available[addIdx],)
    available=available[:addIdx]+available[addIdx+1:]+(solution[removeIdx],)
    """
    removeTuple = random.choice(solution) if len(solution) > 0 else ()
    addTuple = random.choice(available) if len(available) > 0 else ()
    available=tuple(x for x in available if x!=addTuple)
    solution=(*(x for x in solution if x!=removeTuple),addTuple)
    """
    f=fitness((solution,available))
    return (solution,available,f)  #selected,

#@profile
def crossover(p1,p2):
    solution1, available, _ = p1
    solution2, _, _ = p2
    cut1=random.randint(0,len(solution1))
    cut2 = random.randint(0, len(solution2))

    solution = tuple(set((*solution1[: cut1], *solution2[cut2 :])))
    newAvailable=tuple((set(solution1)|set(available))-set(solution))
    f = fitness((solution, available))
    return (solution, newAvailable,f)

#@profile
def main():

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
        f=fitness((tuple(set(genome)), available))
        population.append((tuple(set(genome)),available,f)) #eve add fitness  selected,

    population.append((tuples,tuple(),fitness((tuples,tuple()))))
    #fitness_log = [(0, fitness(i)) for i in population]

    for g in range(NUM_GENERATIONS):
        offspring = list()
        for i in range(OFFSPRING_SIZE):
            if random.random() < 0.7:
                p = tournament(population)
                o = mutation(p)
            else:
                p1 = tournament(population)
                p2 = tournament(population)
                o = crossover(p1, p2)
            #f = fitness(o)
            #fitness_log.append((g + 1, f))
            offspring.append(o)
        population += offspring
        # sort and select the fittest mu

        population = tuple(_ for _ in population if isvalid(_[0]))
        population = sorted(population, key=lambda i: i[2], reverse=True)[:POPULATION_SIZE]
        if(population[2]==N):   #insert steady state
            break
    population=tuple(_ for _ in population if isvalid(_[0]))
    solution=population[0][0]


    file.write(f"Problem size:{N} tuples:\n")
    file.write(str(tuples))
    file.write("solution found:\n")
    file.write(str(solution))

    print(f"Solution for N={N}: w={sum(len(_) for _ in solution)} (bloat={(sum(len(_) for _ in solution) - N) / N * 100:.0f}%)")

if __name__=="__main__":
    with open('solutions.txt', 'w') as file:
        for N in [5,10,20,100,500,1000]:
            main()