"""Genetically mutate rats to a weight of 50000 grams.

Imports:
    time - record runtime.
    random - generating random values.
    statistics - calculate statistics.
"""

import time
import random
import statistics
import matplotlib.pyplot as plt

#=============================================
# FREE TO PLAY WITH VALUES
# (weights in grams)
GOAL_WT = 50000
NUM_RATS = 20
INITIAL_MIN_WT = 200
INITIAL_MAX_WT = 600
INITIAL_MODE_WT = 300
MUTATE_ODDS = 0.01
MUTATE_MIN = 0.5
MUTATE_MAX = 1.2
LITTER_SIZE = 8
LITTERS_PER_YEAR = 10
GENERATION_LIMIT = 500

# Ensure even number of rats for breeding
if NUM_RATS % 2 != 0:
    NUM_RATS += 1

# DO NOT EDIT BELOW THIS LINE
#===========================================================

def populate(num_rats, min_wt, max_wt, mode_wt):
    """Initialize a population of rats with weights of a triangular dist.
    
    Arguments:
        num_rats - number of rats in population.
        min_wt - minimm weight of rat population.
        max_wt - maximum weight of rat population.
        mode_wt - weight appearing most in rat population.
    
    Returns:
        list of weights representing rat population.
    """
    return [int(random.triangular(min_wt, max_wt, mode_wt))\
            for i in range(num_rats)]

def fitness(population, goal_wt):
    """Determine if rats have reached goal weight.
    
    Returns:
        the proportion of average weight over goal weight.
    """
    average_wt = statistics.mean(population)
    return average_wt / goal_wt

def select(population, rats_to_retain):
    """Select specified number of rats based on weight.
    
    Returns:
        two lists of selected male, female rats
    """
    sorted_population = sorted(population)
    rats_to_retain_by_sex = rats_to_retain // 2
    # Seperate population in half and assume
    # left side weights are female and right side weights are male
    members_per_sex = len(sorted_population) // 2
    females = sorted_population[:members_per_sex]
    males = sorted_population[members_per_sex:]
    # Select the appropriate number of males and females to keep
    selected_females = females[-rats_to_retain_by_sex:]
    seleted_males = males[-rats_to_retain_by_sex:]
    return seleted_males, selected_females

def breed(males, females, litter_size):
    """Take in list of weights from males and females.
    
    Returns:
        list of child rats of litter_size.
    """
    random.shuffle(males)
    random.shuffle(females)
    children = []
    for male, female in zip(males, females):
        for child in range(litter_size):
            child = random.randint(female, male)
            children.append(child)
    return children

def mutate(children, mutate_odds, mutate_min, mutate_max):
    """Randomly mutate rat weight.
    
    Given the probability of mutating, select some rat and
    scale the weight using mutate_min and mutat_max distribution
    """
    for index, rat in enumerate(children):
        if mutate_odds >= random.random():
            children[index] = round(rat * random.uniform(mutate_min,
                                                         mutate_max))
    return children

def show_plot(generations_list, ave_wt):
    """Output a plot with generation on x-axis and ave_wt on y-axis"""
    plt.plot(generations_list, ave_wt)
    plt.xlabel('Generation')
    plt.ylabel('Average Weight')
    plt.title('Average Weight Evolution')
    plt.savefig('average_weight_plot.png')
    plt.show() 

def main():
    """Run program, initialize variables and display results"""
    generations = 0
    generations_list = []
    parents = populate(NUM_RATS, INITIAL_MIN_WT,
                       INITIAL_MAX_WT, INITIAL_MODE_WT)
    print(f'Initial weights in rat population: {parents}')
    population_fitness = fitness(parents, GOAL_WT)
    print(f'Initail fitness level of population: {population_fitness}')
    print(f'Number of rats to keep per generation: {NUM_RATS}')

    ave_wt = []

    while population_fitness < 1 and generations < GENERATION_LIMIT:
        selected_males, selected_females = select(parents, NUM_RATS)
        children = breed(selected_males, selected_females, LITTER_SIZE)
        children = mutate(children, MUTATE_ODDS, MUTATE_MIN, MUTATE_MAX)
        parents = selected_males + selected_females + children
        population_fitness = fitness(parents, GOAL_WT)
        print(f'Generation {generations} fitness level: {population_fitness:.4f}')
        ave_wt.append(int(statistics.mean(parents)))
        generations_list.append(generations)
        generations += 1

    print(f'\nAverage weight per generation: {ave_wt}')
    print(f'\nNumber of generations: {generations}')
    print(f'\nNumber of years: {int(generations / LITTERS_PER_YEAR)}')

    show_plot(generations_list, ave_wt)  

if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    duration = end_time - start_time
    print(f'\nProgram runtime was {duration} seconds.')