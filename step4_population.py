import math
import random
import numpy
import matplotlib.pyplot as plt


def fitness(x):
    return math.cos(3 * x) - 0.1 * x ** 2


def random_individual():
    lower_bound = -10
    upper_bound = 10
    return random.uniform(lower_bound, upper_bound)


def clamp_to_bounds(x):
    lower_bound = -10
    upper_bound = 10
    if x < lower_bound:
        return lower_bound
    if x > upper_bound:
        return upper_bound
    return x


def mutate(x):
    step_size = 0.5
    nudged_x = x + random.gauss(0, step_size)
    return clamp_to_bounds(nudged_x)


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
    ranked_best_first = sorted(candidates, key=fitness, reverse=True)
    survivors = ranked_best_first[:population_size]
    return survivors


def evolve():
    total_generations = 30

    population = random_population()
    population_history = [population]

    for generation_number in range(total_generations):
        offspring = make_offspring(population)
        parents_and_offspring = population + offspring
        population = select_survivors(parents_and_offspring)
        population_history.append(population)

    best_individual = max(population, key=fitness)
    return best_individual, population_history


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


def plot_evolution(best_individual, population_history):
    curve_xs, curve_ys = smooth_curve()
    plt.plot(curve_xs, curve_ys, color="black", label="fitness landscape")

    total_generations = len(population_history)
    for generation_number, population in enumerate(population_history):
        progress = generation_number / (total_generations - 1)
        size, opacity = point_size_and_opacity(progress)
        is_last_generation = generation_number == total_generations - 1
        label = "population (faint=early, bold=late)" if is_last_generation else None
        for member in population:
            plt.scatter([member], [fitness(member)], s=size, color="green", alpha=opacity, label=label)
            label = None

    plt.scatter([best_individual], [fitness(best_individual)], s=80, color="red", label="best found")
    plt.xlabel("x")
    plt.ylabel("fitness")
    plt.title("Step 4 — Population")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    random.seed(0)

    best_individual, population_history = evolve()

    print("best x:", best_individual)
    print("best fitness:", fitness(best_individual))

    plot_evolution(best_individual, population_history)
