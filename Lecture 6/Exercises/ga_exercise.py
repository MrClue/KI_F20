import random
import math
from heapq import nlargest

p_mutation = 0.2
num_of_generations = 30


def genetic_algorithm(population, fitness_fn, minimal_fitness):
    for generation in range(num_of_generations):
        print("Generation {}:".format(generation))
        print_population(population, fitness_fn)

        new_population = set()

        for i in range(len(population)):
            mother, father = random_selection(population, fitness_fn)
            child = reproduce(mother, father)

            if random.uniform(0, 1) < p_mutation:
                child = mutate(child)

            new_population.add(child)

        # Add new population to population, use union to disregard
        # duplicate individuals
        population = population.union(new_population)

        fittest_individual = get_fittest_individual(population, fitness_fn)

        if minimal_fitness <= fitness_fn(fittest_individual):
            break

    print("Final generation {}:".format(generation))
    print_population(population, fitness_fn)

    return fittest_individual


def print_population(population, fitness_fn):
    for individual in population:
        fitness = fitness_fn(individual)
        print("{} - fitness: {}".format(individual, fitness))


def reproduce(mother, father):
    '''
    Reproduce two individuals with single-point crossover
    Return the child individual
    '''
    cross = random.randint(0, len(mother)-1)
    return mother[:cross] + father[cross:]


def mutate(individual):
    '''
    Mutate an individual by randomly assigning one of its bits
    Return the mutated individual
    '''
    individual = list(individual)
    i = random.randint(0,len(individual)-1)
    individual[i] = 1 if individual[i] == 0 else 0
    return tuple(individual)
    # return mutation


def random_selection(population, fitness_fn):
    """
    Compute fitness of each in population according to fitness_fn and add up
    the total. Then choose 2 from sequence based on percentage contribution to
    total fitness of population
    Return selected variable which holds two individuals that were chosen as
    the mother and the father
    """

    # Python sets are randomly ordered. Since we traverse the set twice, we
    # want to do it in the same order. So let's convert it temporarily to a
    # list.
    fit_dict = {}
    ordered_population = list(population)
    for i in range(len(ordered_population)):
        fit_dict[ordered_population[i]] = fitness_fn(ordered_population[i])
    two_best_fit = nlargest(2, fit_dict, key=fit_dict.get)
    print("Two_best_fit",two_best_fit)
    return two_best_fit[0], two_best_fit[1]


def fitness_function(individual):
    '''
    Computes the decimal value of the individual
    Return the fitness level of the individual

    Explanation:
    enumerate(list) returns a list of pairs (position, element):

    enumerate((4, 6, 2, 8)) -> [(0, 4), (1, 6), (2, 2), (3, 8)]

    enumerate(reversed((1, 1, 0))) -> [(0, 0), (1, 1), (2, 1)]
    '''
    return sum([individual[len(individual)-1-i]*math.pow(2, i) for i in range(len(individual))])
    # return fitness


def get_fittest_individual(iterable, func):
    return max(iterable, key=func)


def get_initial_population(n, count):
    '''
    Randomly generate count individuals of length n
    Note since its a set it disregards duplicate elements.
    '''
    return set([
        tuple(random.randint(0, 1) for _ in range(n))
        for _ in range(count)
    ])


def main():
    minimal_fitness = 7

    # Curly brackets also creates a set, if there isn't a colon to indicate a dictionary
    initial_population = {
        (1, 1, 0),
        (0, 0, 0),
        (0, 1, 0),
        (1, 0, 0)
    }
    #initial_population = get_initial_population(3, 4)

    fittest = genetic_algorithm(
        initial_population, fitness_function, minimal_fitness)
    print('Fittest Individual: ' + str(fittest))


if __name__ == '__main__':
    main()
