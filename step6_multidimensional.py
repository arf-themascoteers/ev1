import math
import random
import numpy
import matplotlib.pyplot as plt


def rastrigin(vector):
    total = 10 * len(vector)
    for component in vector:
        total += component ** 2 - 10 * math.cos(2 * math.pi * component)
    return total


def fitness(vector):
    return -rastrigin(vector)


def make_individual(vector, step_size):
    individual = {"vector": vector, "step_size": step_size}
    return individual


def individual_fitness(individual):
    return fitness(individual["vector"])


def clamp_to_bounds(component):
    lower_bound = -5.12
    upper_bound = 5.12
    if component < lower_bound:
        return lower_bound
    if component > upper_bound:
        return upper_bound
    return component


def random_individual():
    dimensions = 2
    lower_bound = -5.12
    upper_bound = 5.12
    starting_step_size = 2.0

    vector = []
    for axis_number in range(dimensions):
        vector.append(random.uniform(lower_bound, upper_bound))

    return make_individual(vector, starting_step_size)


def mutate(individual):
    learning_rate = 0.3

    old_step_size = individual["step_size"]
    grown_or_shrunk = math.exp(learning_rate * random.gauss(0, 1))
    new_step_size = old_step_size * grown_or_shrunk

    old_vector = individual["vector"]
    new_vector = []
    for component in old_vector:
        nudged_component = component + new_step_size * random.gauss(0, 1)
        new_vector.append(clamp_to_bounds(nudged_component))

    return make_individual(new_vector, new_step_size)


def random_population():
    population_size = 12
    population = []
    for member_number in range(population_size):
        population.append(random_individual())
    return population


def make_offspring(population):
    offspring = []
    for parent in population:
        child = mutate(parent)
        offspring.append(child)
    return offspring


def select_survivors(candidates):
    population_size = 12
    ranked_best_first = sorted(candidates, key=individual_fitness, reverse=True)
    survivors = ranked_best_first[:population_size]
    return survivors


def evolve():
    total_generations = 40

    population = random_population()
    population_history = [population]

    for generation_number in range(total_generations):
        print(f"Generation {generation_number}")
        offspring = make_offspring(population)
        parents_and_offspring = population + offspring
        population = select_survivors(parents_and_offspring)
        population_history.append(population)

    best_individual = max(population, key=individual_fitness)
    return best_individual, population_history


def landscape_grid():
    axis_values = numpy.linspace(-5.12, 5.12, 200)
    grid_x, grid_y = numpy.meshgrid(axis_values, axis_values)

    grid_fitness = numpy.empty_like(grid_x)
    for row in range(grid_x.shape[0]):
        for column in range(grid_x.shape[1]):
            point = [grid_x[row, column], grid_y[row, column]]
            grid_fitness[row, column] = fitness(point)

    return grid_x, grid_y, grid_fitness


def point_size_and_opacity(progress):
    smallest_size = 5
    largest_size = 70
    size = smallest_size + progress * (largest_size - smallest_size)

    faintest = 0.15
    boldest = 1.0
    opacity = faintest + progress * (boldest - faintest)

    return size, opacity


def plot_evolution(best_individual, population_history):
    grid_x, grid_y, grid_fitness = landscape_grid()
    plt.contourf(grid_x, grid_y, grid_fitness, levels=40, cmap="viridis")
    plt.colorbar(label="fitness")

    total_generations = len(population_history)
    for generation_number, population in enumerate(population_history):
        progress = generation_number / (total_generations - 1)
        size, opacity = point_size_and_opacity(progress)
        is_last_generation = generation_number == total_generations - 1
        label = "population (faint=early, bold=late)" if is_last_generation else None
        for individual in population:
            x_value = individual["vector"][0]
            y_value = individual["vector"][1]
            plt.scatter([x_value], [y_value], s=size, color="white", edgecolor="black", alpha=opacity, label=label)
            label = None

    best_vector = best_individual["vector"]
    plt.scatter([best_vector[0]], [best_vector[1]], s=120, color="red", label="best found")
    plt.xlabel("x1")
    plt.ylabel("x2")
    plt.title("Step 6 — Multi-Dimensional (2D Rastrigin)")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    random.seed(0)

    best_individual, population_history = evolve()

    print("best vector:", best_individual["vector"])
    print("best fitness:", individual_fitness(best_individual))

    plot_evolution(best_individual, population_history)
