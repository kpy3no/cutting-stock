import numpy
import sys


def cal_pop_fitness(pop, rectangles_sum=0):
    # Calculating the fitness value of each solution in the current population.
    # The fitness function calulates the sum of products between each input and its corresponding weight.
    fitness = list(map(lambda points: sum_routes(points) + rectangles_sum, pop))
    return numpy.array(fitness)


# def select_mating_pool(pop, fitness, num_parents):
#     # Selecting the best individuals in the current generation as parents for producing the offspring of the next generation.
#     parents = []
#     for parent_num in range(num_parents):
#         min_fitness_idx = numpy.argmin(fitness)
#         parents.append(pop[min_fitness_idx])
#         fitness[min_fitness_idx] = sys.float_info.max
#     return parents

def select_mating_pool(pop, fitness, num_parents):
    # Selecting the best individuals in the current generation as parents for producing the offspring of the next generation.
    parents = numpy.empty((num_parents, pop.shape[1]), dtype=object)
    for parent_num in range(num_parents):
        min_fitness_idx = numpy.where(fitness == numpy.min(fitness))
        min_fitness_idx = min_fitness_idx[0][0]
        parents[parent_num, :] = pop[min_fitness_idx, :]
        fitness[min_fitness_idx] = sys.float_info.max
    return parents


# def crossover(parents, offspring_size):
#     offspring = []
#
#     # The point at which crossover takes place between two parents. Usually, it is at the center.
#     crossover_point = len(parents[0])/2
#
#     for k in range(offspring_size):
#         # Index of the first parent to mate.
#         parent1_idx = k%len(parents)
#         # Index of the second parent to mate.
#         parent2_idx = (k+1)%len(parents)
#         # The new offspring will have its first half of its genes taken from the first parent.
#         offspring[k, 0:crossover_point] = parents[parent1_idx, 0:crossover_point]
#         # The new offspring will have its second half of its genes taken from the second parent.
#         offspring[k, crossover_point:] = parents[parent2_idx, crossover_point:]
#     return offspring

def crossover(parents, offspring_size, num_gen_twist):
    offspring = numpy.empty(offspring_size, dtype=object)
    # The point at which crossover takes place between two parents. Usually, it is at the center.
    crossover_point = numpy.uint8(offspring_size[1]/2)
    twist_left_point = crossover_point - int(num_gen_twist / 2)
    twist_right_point = crossover_point + int((num_gen_twist / 2) + num_gen_twist % 2)

    for k in range(offspring_size[0]):
        # Index of the first parent to mate.
        parent_idx = k%parents.shape[0]
        # The new offspring will have its first half of its genes taken from the one parent.
        offspring[k, 0:twist_left_point] = parents[parent_idx, 0:twist_left_point]
        # The new offspring will have gen twisted from one parent (count = num_gen_twist)
        # offspring[k, twist_left_point:twist_right_point] = parents[parent_idx, twist_right_point:twist_left_point]
        parent_reverse = parents[parent_idx, ::-1]
        offspring[k, twist_left_point:twist_right_point] = parent_reverse[twist_left_point:twist_right_point]
        # The new offspring will have its second half of its genes taken from the parent.
        offspring[k, twist_right_point:] = parents[parent_idx, twist_right_point:]
    return offspring


def mutation(offspring_crossover, num_mutations=1):
    # Mutation changes a number of genes as defined by the num_mutations argument. The changes are random.
    mutations_counter = numpy.uint8(offspring_crossover.shape[1] / num_mutations)

    for idx in range(1, offspring_crossover.shape[0]):
        gene_idx = mutations_counter - 1
        for mutation_num in range(num_mutations):
            # The random index to swap
            random_index = numpy.random.randint(1, offspring_crossover.shape[1])
            temp = offspring_crossover[idx, gene_idx]
            offspring_crossover[idx, gene_idx] = offspring_crossover[idx, random_index]
            offspring_crossover[idx, random_index] = temp
    return offspring_crossover


def sum_rectangles(figures):
    sum_distance = 0

    for rectangle in figures:
        sum_distance += rectangle.perimeter()

    return sum_distance


def sum_routes(routes):
    sum_distance = 0

    for i in range(len(routes) - 1):
        sum_distance += routes[i].distance_to(routes[i+1])
    return sum_distance


def value_function(figures, routes):
    return sum_rectangles(figures) + sum_routes(routes)