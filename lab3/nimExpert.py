import logging
import random
from collections import namedtuple
import copy

Nimply = namedtuple("Nimply", "row, num_objects")
Gene = namedtuple("Gene", ["condition","action","place"])
Individual = namedtuple("Individual", ["genome", "fitness"])

nim_rows = 5
eval_amount = 2000
genome_size = 3
population_size = 20
offspring_size = 50
generations = 10
mutation_rate = 0.5

class Nim:
    def __init__(self, num_rows: int, k: int = None) -> None:
        self._rows = [2*i + 1 for i in range(num_rows)]
        self._k = k

    def fromRows(rows):
        self._rows=rows

    def nimming(self, ply:Nimply) -> None:
        if ply is None:
            self._rows=[0 for _ in self._rows]
            #for i, _ in self._rows:
            #    self._rows[i] = 0
            return
        row, num_objects=ply
        assert num_objects>0
        assert self._rows[row] >= num_objects
        assert self._k is None or num_objects <= self._k
        self._rows[row] -= num_objects

        if self._rows[row]==0:
            self._rows.pop(row)

        #if sum(self._rows) == 0:
        #    logging.info("You lost")
    def __bool__(self):
        return sum(self._rows) > 0
    def __str__(self):
        return "<" + " ".join(str(_) for _ in self._rows) + ">"
    @property
    def rows(self) -> tuple:
        return tuple(self._rows) #[row for row in self._rows if row!=0]) #list comprehension faster (~0.07) than tuple(filter(lambda num: num!=0,self._rows)) (~0.09)
    @property
    def k(self) -> int:
        return self._k

    def endTest(self):
        if sum(self._rows) == 0:
            logging.info("You lost")
            return 1
        return 0

    def board(self)->None:
        for i,row in enumerate(self._rows):
            print(i,":",end=" ")
            for j in range(row):
                print("|", end=' ')
            print("\n")
                                            ####################### Conditions #################
def even_elems_if(state: Nim) -> bool:
    return sum(state.rows)%2 == 0

def odd_elems_if(state: Nim) -> bool:
    return sum(state.rows)%2 != 0

def even_stacks_if(state: Nim) -> bool:
    return len(state.rows)%2 == 0

def odd_stacks_if(state: Nim) -> bool:
    return len(state.rows)%2 != 0

def nimsum_if(state: Nim) -> bool:
    return nimSum(state.rows)!=0

conditions = {"even_elems": even_elems_if, "odd_elems": odd_elems_if, "even_stacks": even_stacks_if, "odd_stacks": odd_stacks_if,"true":lambda x:True} #"nimsum": nimsum_if

                                                            ###################  Action  ###############
def all_get(state: Nim, row: int) -> Nimply:
    num_objects = state.rows[row]
    return Nimply(row, num_objects)

def one_get(state: Nim, row: int) -> Nimply:
    num_objects = 1
    return Nimply(row, num_objects)

def half_get(state: Nim, row: int) -> Nimply:
    num_objects = max(1,state.rows[row]//2)
    return Nimply(row, num_objects)

def rand_get(state: Nim, row: int) -> Nimply:
    num_objects = random.randint(1, state.rows[row])
    return Nimply(row, num_objects)

def nimsum_get(state: Nim, row: int) -> Nimply:
    rows=state.rows
    totNimSum=nimSum(rows)

    if checkMisere(rows)!=-1:
        if len(rows)%2==0:
            return Nimply(row, rows[row])
        elif rows[row]>1:
            return Nimply(row, rows[row]-1)

    lineNimSum=nimSum([totNimSum,rows[row]])
    if (lineNimSum < rows[row]):
        return Nimply(row,rows[row]-lineNimSum)
    ply=rand_get(state,row)
    return ply

actions = {"all": all_get, "one": one_get, "half": half_get, "rand": rand_get}  #, "nimsum": nimsum_get

                                                                #######################  Place  #####################
def rand_place(state: Nim) -> int:
    row = random.randrange(0,len(state.rows))
    #print('rand place choose row: ', state, row)
    return row

def most_place(state: Nim) -> int:
    row = state.rows.index(max(state.rows))
    #print('most place choose row: ', state, row)
    return row

def least_place(state: Nim) -> int:
    row = state.rows.index(min([c for r, c in enumerate(state.rows) if c > 0]))
    return row

def nimsum_place(state: Nim) -> int:
    rows=state.rows
    totNimSum=nimSum(rows)
    if(totNimSum!=0):
        nonOneRow=checkMisere(rows)
        if nonOneRow!=-1:
            return nonOneRow
        for i,row in enumerate(rows):
            lineNimSum=nimSum([totNimSum,row])
            if(lineNimSum<row):
                return i
    return rand_place(state)

places = {"rand": rand_place, "most": most_place, "least": least_place}  #, "nimsum": nimsum_place

#Fitness
def evaluate(genome: list) -> float:
    win_count = 0
    for _ in range(eval_amount):
        game = Nim(random.randint(5,21))
        turn=1   #inizia l'individuo turno 0, random turno 1
        while not game.endTest():
            turn = 1 - turn
            if not turn:
                game.nimming(play(game,genome))
            else:
                game.nimming(pure_random(game))
        if turn:   #gioco finito e ultima mossa di random
            win_count += 1
    return win_count/eval_amount
                                            #################  Full strategies  #################

def pure_random(state: Nim) -> Nimply:
    row = random.choice([r for r, c in enumerate(state.rows) if c > 0])
    num_objects = random.randint(1, state.rows[row])
    return Nimply(row, num_objects)

def dumb(state: Nim) -> Nimply:
    """Pick always the maximum possible number of the lowest row"""
    possible_moves = [(r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1)]
    return Nimply(*max(possible_moves, key=lambda m: (-m[0], m[1])))

def nimSum(rows):  #pass to reduce
    sum=rows[0]
    for i in rows[1:]:
        sum^=i
    return sum

def checkMisere(rows):
    cnt=0
    nonOneRow=-1
    for i,row in enumerate(rows):
        if row>=2:
            cnt+=1
            nonOneRow=i
        if cnt==2:
            return -1
    return nonOneRow

def expert(game):
    rows=game.rows
    totNimSum=nimSum(rows)
    if(totNimSum!=0):
        OneRow=checkMisere(rows)
        if OneRow!=-1:
            if len([_ for _ in rows if _!=0])%2==0:
                return Nimply(OneRow,rows[OneRow])
            else:
                return Nimply(OneRow, rows[OneRow]-1)
        for i,row in enumerate(rows):
            lineNimSum=nimSum([totNimSum,row])
            if(lineNimSum<row):
                print(f"removing {row-lineNimSum} elements from row {i}")
                #game.nimming(i,row-lineNimSum)
                return Nimply(i,row-lineNimSum)
    #altrimenti somma zero, siamo in posizione perdente
    return pure_random(game)

def human_play(game):   #human play
    while 1:
        str=input("Enter row index and number of elements to remove: ")
        rowIdx, n=str.split(" ")
        if int(rowIdx)>=len(game.rows):
            print("Invalid row!")
        elif int(n)>game.rows[int(rowIdx)]:
            print("Invalid number, convert to maximum!")
            n=game.rows[int(rowIdx)]
            return int(rowIdx), int(n)
        else:
            return int(rowIdx),int(n)

def lose_game() -> Nimply:
    return None

def play(state: Nim, genome: list) -> Nimply:  #1 condition 2 action 3 place
    for g in genome:
        if (conditions[g[0]](state)):
            move=actions[g[1]](state, places[g[2]](state))
            #print(g, 'state: ',state,'move: ', move)
            return move  #MODIFICARE con Nimply all'esterno Nimply(place,action) - (row,numObj)
    return lose_game()
#GA Functions

def generate_population(population_size):
    population = list()
    for _ in range(population_size):
        genome = list()
        for _ in range(genome_size):
            gene = (random.choice(list(conditions.keys())), random.choice(list(actions.keys())), random.choice(list(places.keys())))
            genome.append(gene)
        population.append(Individual(genome, evaluate(genome)))
    return population

def mutation(indiv: Individual) -> Individual:
    mutable = [conditions, actions, places]

    mut_gene_idx = random.randrange(0, genome_size)
    mut_attr_idx = random.randrange(0, 3)   #len(Gene) 3=gene_size
    attr = indiv.genome[mut_gene_idx][mut_attr_idx]

    acceptable = list(mutable[mut_attr_idx].keys())
    acceptable.remove(attr)
    new_attr = random.choice(acceptable)
    new_genome=copy.deepcopy(indiv.genome)   #.deepcopy()
    new_genome[mut_gene_idx]=indiv.genome[mut_gene_idx][:mut_attr_idx]+(new_attr,)+indiv.genome[mut_gene_idx][mut_attr_idx+1:]
    #new_genome = indiv.genome[:mut_gene_idx] + new_gene + indiv.genome[mut_gene_idx + 1:]
    fitness = evaluate(new_genome)
    return Individual(new_genome,fitness)

def cross_over(i1: Individual, i2: Individual) -> Individual:
    cross_over_point = random.randrange(1, genome_size)
    new_genome = list()
    for i in range(genome_size):
        if (i < cross_over_point):
            new_genome.append(i1.genome[i])
        else:
            new_genome.append(i2.genome[i])
    return Individual(new_genome, evaluate(new_genome))

def tournament(population,tournament_size=2):
    return max(random.choices(population,k=tournament_size), key=lambda i:i[1])

def evolution():
    population=generate_population(population_size)

    for g in range(generations):
        offspring = list()
        for i in range(offspring_size):
            if random.random() < 0.7:
                p = tournament(population)
                o = mutation(p)
            else:
                p1 = tournament(population)
                p2 = tournament(population)
                o = cross_over(p1, p2)
            # f = fitness(o)
            # fitness_log.append((g + 1, f))
            offspring.append(o)
        population += offspring
        # sort and select the fittest mu

        #population = tuple(_ for _ in population if isvalid(_[0]))
        population = sorted(population, key=lambda i: i[1], reverse=True)[:population_size]

        #if Individual already 1: stop

    #population = tuple(_ for _ in population if isvalid(_[0]))
    solution = population[0]
    print(f"Solution : genome={solution[0]} (fitness={solution[1]*100}%)")
    return solution

#CONDITIONS:  "even_elems", "odd_elems", "even_stacks", "odd_stacks", "nimsum","true"
#PLACES:      "rand", "most", "least", "nimsum"
#ACTIONS:     "all", "one", "half", "rand", "nimsum"

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    game = Nim(5)
    genome=list()
    for _ in range(genome_size):
        gene = (
        random.choice(list(conditions.keys())), random.choice(list(actions.keys())), random.choice(list(places.keys())))
        genome.append(gene)
    print(genome)
    player1=Individual(genome, evaluate(genome))
    print("generated:",player1)

    genome2=[("true",'all',"least")]
    player2=Individual(genome2,evaluate(genome2))
    print("dumb-by gabriele:",player2)

    genome3 = [("true", 'rand', "rand"),("true", 'rand', "rand"),("true", 'rand', "rand")]
    player3 = Individual(genome3, evaluate(genome3))
    print("random:", player3)

    solution=evolution()
    print(evaluate(solution[0]))
    print(evaluate(solution[0]))
    print(evaluate(solution[0]))

    genome4=[('even_elems', 'half', 'least'), ('odd_elems', 'one', 'most'), ('odd_stacks', 'rand', 'least')]
    player4=Individual(genome4,evaluate(genome4))
    print("evoluted: ",player4)
    #print(evaluate([('true', 'nimsum', 'rand'), ('true', 'rand', 'least'), ('nimsum', 'half', 'rand')]))
    #print(evaluate([('nimsum', 'nimsum', 'nimsum'), ('even_elems', 'all', 'least'), ('nimsum', 'one', 'most')]))
    #print(evaluate([('even_elems', 'all', 'rand'), ('even_stacks', 'nimsum', 'most'), ('true', 'nimsum', 'nimsum')]))

    #[('even_elems', 'nimsum', 'least'), ('even_stacks', 'nimsum', 'most'), ('even_stacks', 'half', 'least')]
    #[('even_elems', 'all', 'least'), ('nimsum', 'one', 'nimsum'), ('even_stacks', 'one', 'most')]
    #Individual(genome=[('even_stacks', 'nimsum', 'least'), ('even_stacks', 'one', 'most'), ('true', 'nimsum', 'rand')], fitness=0.999)
    #Individual(genome=[('true', 'one', 'nimsum'), ('even_stacks', 'half', 'rand'), ('even_stacks', 'one', 'rand')],fitness=1.0)
    #Individual(genome=[('nimsum', 'nimsum', 'nimsum'), ('even_elems', 'rand', 'rand'), ('even_stacks', 'half', 'most')], fitness=1.0)
    #Individual(genome=[('true', 'all', 'rand'), ('even_stacks', 'rand', 'nimsum'), ('true', 'one', 'rand')], fitness=1.0)

    #very low fitness:[('even_stacks', 'nimsum', 'rand'), ('even_elems', 'one', 'least'), ('even_elems', 'rand', 'least')] 0.06

    """
    game=Nim(5)
    game.board()
    print("current nim sum: ",nimSum(game._rows))
    turn=1
    while not game.endTest():
        turn = 1 - turn
        if not turn:
            print("Your turn:")
            game.nimming(human_play(game))
        else:
            print("Agent turn:")
            game.nimming(expert(game))
        game.board()
    if not turn:
        print("You lost")
    else:
        print("Agent lost")
    """


