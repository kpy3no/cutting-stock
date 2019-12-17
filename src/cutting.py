#!/usr/bin/python
# encoding=utf8

import time
import numpy as np
import src.utils as utils
import src.genethic as gen
from src.entities import Point


class RandomAlgorithm:

    def __init__(self, start_point, figures):
        self.start_point = start_point
        self.figures = figures
        self.name = 'Случайный'

    def generate_routes(self):
        routes = []
        left_figures = self.figures.copy()
        point_routes = [self.start_point]
        currentPoint = self.start_point

        np.random.shuffle(left_figures)
        for figure in left_figures:
            currentPoint = utils.closest_border_rectangle_point(currentPoint, figure)
            point_routes.append(currentPoint)
            routes.append(figure)
        return point_routes


class GreedyAlgorithm:

    def __init__(self, start_point, figures):
        self.start_point = start_point
        self.figures = figures
        self.name = 'Жадный'

    def generate_routes(self):
        currentPoint = self.start_point
        left_figures = self.figures.copy()
        point_routes = [self.start_point]
        routes = []

        left_figures = left_figures
        while len(left_figures) > 1:
            closest_point = utils.closest_border_rectangle_point(currentPoint, left_figures[0])
            closest_distance = currentPoint.distance_to(closest_point)
            closest_figure = left_figures[0]
            for figure in left_figures:
                point_to_figure = utils.closest_border_rectangle_point(currentPoint, figure)
                distance = currentPoint.distance_to(point_to_figure)

                if distance < closest_distance:
                    closest_distance = distance
                    closest_figure = figure
                    closest_point = point_to_figure

            point_routes.append(closest_point)
            routes.append(closest_figure)
            left_figures.remove(closest_figure)

        return point_routes


def percentage(part, whole):
    return float(whole) * float(part)/ 100.0


class GeneticAlgorithm:

    def __init__(self, start_point, figures, population_size=8, num_generations=1000, num_parents_mating=4, num_mutations=None, num_gen_twist=None):
        self.start_point = start_point
        self.figures = figures
        self.population_size = population_size
        self.num_generations = num_generations
        self.num_parents_mating = num_parents_mating
        self.num_points = len(self.figures) + 1
        self.pop_size = (self.population_size, self.num_points)
        self.name = 'Генетический'
        if num_mutations is None:
            num_mutations = int(percentage(5, self.num_points))

        self.num_mutations = num_mutations
        # count of gene taking participant in crossover
        if num_gen_twist is None:
            num_gen_twist = int(percentage(20, self.num_points))

        self.num_gen_twist = num_gen_twist

    def generate_routes(self):
        point_routes = [self.start_point]
        random_alg = RandomAlgorithm(self.start_point, self.figures)
        new_population = []
        figures_value = sum_rectangles(self.figures)

        # generate first random populations
        for iteration in range(self.population_size):
            new_population.append(random_alg.generate_routes())

        new_population = np.array(new_population)

        best_outputs = []
        for generation in range(self.num_generations):
            print("Generation : ", generation)
            # Measuring the fitness of each chromosome in the population.
            fitness = gen.cal_pop_fitness(new_population)
            print("Fitness")
            print(fitness)

            index_min = np.argmin(fitness)
            best_outputs.append(new_population[index_min])

            # Selecting the best parents in the population for mating.
            parents = gen.select_mating_pool(new_population, fitness, self.num_parents_mating)
            print("Parents")
            print(parents)

            # Generating next generation using crossover.
            offspring_crossover = gen.crossover(parents, offspring_size=(self.pop_size[0]-parents.shape[0], self.num_points), num_gen_twist=self.num_gen_twist)
            print("Crossover")
            print(offspring_crossover)

            # Adding some variations to the offspring using mutation.
            offspring_mutation = gen.mutation(offspring_crossover, self.num_mutations)
            print("Mutation")
            print(offspring_mutation)

            # Creating the new population based on the parents and offspring.
            new_population[0:parents.shape[0], :] = parents
            new_population[parents.shape[0]:, :] = offspring_mutation

        # Getting the best solution after iterating finishing all generations.
        # At first, the fitness is calculated for each solution in the final generation.
        fitness = gen.cal_pop_fitness(new_population)
        # Then return the index of that solution corresponding to the best fitness.
        best_match_idx = np.where(fitness == np.max(fitness))

        print("Best solution : ", new_population[best_match_idx, :])
        print("Best solution fitness : ", fitness[best_match_idx])

        # utils.draw_figures(self.figures, list(new_population[int(best_match_idx[0][0])]))
        return list(new_population[int(best_match_idx[0][0])])


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


def run_algorithm(algorithm, label=None):
    start_time = time.time()
    points = algorithm.generate_routes()
    passed_time = time.time() - start_time

    overall_value = value_function(rectangles, points)
    points_value = overall_value - rectangles_value

    lbl_str = 'Описание'
    lbl_str += '\n' + 'начальная точка={0},{1}'.format(points[0].x, points[0].y)
    lbl_str += '\n' + 'кол-во фигур={0}'.format(len(rectangles))
    lbl_str += '\n' + 'алгоритм={0}'.format(algorithm.name)
    lbl_str += '\n' + 'требуемое время={:2.3f}'.format(passed_time)
    lbl_str += '\n' + 'общая стоимость={:2.3f}'.format(overall_value)
    lbl_str += '\n' + 'стоимость фигур={:2.3f}'.format(rectangles_value)
    lbl_str += '\n' + 'стоимость маршрута={:2.3f}'.format(points_value)

    if label is not None:
        lbl_str += '\n' + label

    utils.draw_figures(rectangles, points, 100, lbl_str)


def run_genetic():
    genetic_algorithm = GeneticAlgorithm(startPoint, rectangles)
    label = 'размер популяции={0}'
    label += '\n' + 'кол-во поколений={0}'.format(genetic_algorithm.num_generations)
    label += '\n' + 'кол-во родителей={0}'.format(genetic_algorithm.num_parents_mating)
    label += '\n' + 'кол-во мутаций в хромосоме={0}'.format(genetic_algorithm.num_parents_mating)
    label += '\n' + 'кол-во смешивающихся ген={0}'.format(genetic_algorithm.num_gen_twist)
    run_algorithm(genetic_algorithm, label)

if __name__ == "__main__":
    rectangles = utils.read_rectangles('../data/rectangles_file.csv')
    startPoint = Point(0, 0)
    rectangles_value = sum_rectangles(rectangles)

    # greedy_algorithm = GreedyAlgorithm(startPoint, rectangles)
    # run_algorithm(greedy_algorithm)

    # random_algorithm = RandomAlgorithm(startPoint, rectangles)
    # run_algorithm(random_algorithm)

    run_genetic()
    # run_algorithm(genetic_algorithm)

