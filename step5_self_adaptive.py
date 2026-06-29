import math
import random
import numpy
import matplotlib.pyplot as plt


def fitness(x):
    return math.cos(3 * x) - 0.1 * x ** 2


def make_individual(x, step_size):
    individual = {"x": x, "step_size": step_size}
    return individual


def individual_fitness(individual):
    return fitness(individual["x"])


def random_individual():
    lower_bound = -10
    upper_bound = 10
    starting_step_size = 2.0
    x = random.uniform(lower_bound, upper_bound)
    return make_individual(x, starting_step_size)


def clamp_to_bounds(x):
    lower_bound = -10
    upper_bound = 10
    if x < lower_bound:
        return lower_bound
    if x > upper_bound:
        return upper_bound
    return x


def mutate(individual):
    learning_rate = 0.3

    old_step_size = individual["step_size"]
    grown_or_shrunk = math.exp(learning_rate * random.gauss(0, 1))
    new_step_size = old_step_size * grown_or_shrunk

    old_x = individual["x"]
    nudged_x = old_x + new_step_size * random.gauss(0, 1)
    new_x = clamp_to_bounds(nudged_x)

    return make_individual(new_x, new_step_size)


def random_population():
    population_size = 8
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
    population_size = 8
    ranked_best_first = sorted(candidates, key=individual_fitness, reverse=True)
    survivors = ranked_best_first[:population_size]
    return survivors


def average_step_size(population):
    total = 0
    for individual in population:
        total += individual["step_size"]
    return total / len(population)


def evolve():
    total_generations = 30

    population = random_population()
    population_history = [population]
    average_step_size_history = [average_step_size(population)]

    for generation_number in range(total_generations):
        print(f"Generation {generation_number}")
        offspring = make_offspring(population)
        parents_and_offspring = population + offspring
        population = select_survivors(parents_and_offspring)
        population_history.append(population)
        average_step_size_history.append(average_step_size(population))

    best_individual = max(population, key=individual_fitness)
    return best_individual, population_history, average_step_size_history


def smooth_curve():
    xs = numpy.linspace(-10, 10, 400)
    ys = [fitness(x) for x in xs]
    return xs, ys


def point_size_and_opacity(progress):
    smallest_size = 5
    largest_size = 60
    size = smallest_size + progress * (largest_size - smallest_size)

    faintest = 0.1
    boldest = 1.0
    opacity = faintest + progress * (boldest - faintest)

    return size, opacity


def plot_evolution(best_individual, population_history, average_step_size_history):
    figure, (landscape_axis, step_axis) = plt.subplots(1, 2, figsize=(12, 5))

    curve_xs, curve_ys = smooth_curve()
    landscape_axis.plot(curve_xs, curve_ys, color="black", label="fitness landscape")

    total_generations = len(population_history)
    for generation_number, population in enumerate(population_history):
        progress = generation_number / (total_generations - 1)
        size, opacity = point_size_and_opacity(progress)
        is_last_generation = generation_number == total_generations - 1
        label = "population (faint=early, bold=late)" if is_last_generation else None
        for individual in population:
            landscape_axis.scatter([individual["x"]], [individual_fitness(individual)], s=size, color="green", alpha=opacity, label=label)
            label = None

    landscape_axis.scatter([best_individual["x"]], [individual_fitness(best_individual)], s=80, color="red", label="best found")
    landscape_axis.set_xlabel("x")
    landscape_axis.set_ylabel("fitness")
    landscape_axis.set_title("Step 5 — Self-Adaptive Mutation")
    landscape_axis.legend()

    step_axis.plot(average_step_size_history, color="purple")
    step_axis.set_xlabel("generation")
    step_axis.set_ylabel("average step size")
    step_axis.set_title("Step size evolving on its own")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    random.seed(0)

    best_individual, population_history, average_step_size_history = evolve()

    print("best x:", best_individual["x"])
    print("best fitness:", individual_fitness(best_individual))
    print("best individual's step size:", best_individual["step_size"])

    plot_evolution(best_individual, population_history, average_step_size_history)
