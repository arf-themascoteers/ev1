import random
import numpy
import matplotlib.pyplot as plt


def fitness(x):
    return -(x - 2) ** 2 + 10


def random_candidate():
    lower_bound = -10
    upper_bound = 10
    return random.uniform(lower_bound, upper_bound)


def random_search():
    total_guesses = 1000

    best_x = random_candidate()
    best_fitness = fitness(best_x)

    all_guesses = []

    for guess_number in range(total_guesses):
        candidate_x = random_candidate()
        candidate_fitness = fitness(candidate_x)
        all_guesses.append((candidate_x, candidate_fitness))

        candidate_is_better = candidate_fitness > best_fitness
        if candidate_is_better:
            best_x = candidate_x
            best_fitness = candidate_fitness

    return best_x, best_fitness, all_guesses


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


def plot_search(best_x, best_fitness, all_guesses):
    curve_xs, curve_ys = smooth_curve()
    plt.plot(curve_xs, curve_ys, color="black", label="fitness landscape")

    total_guesses = len(all_guesses)
    for guess_number, (guess_x, guess_y) in enumerate(all_guesses):
        progress = guess_number / (total_guesses - 1)
        size, opacity = point_size_and_opacity(progress)
        is_last_guess = guess_number == total_guesses - 1
        label = "attempts (faint=early, bold=late)" if is_last_guess else None
        plt.scatter([guess_x], [guess_y], s=size, color="green", alpha=opacity, label=label)

    plt.scatter([best_x], [best_fitness], s=80, color="red", label="best found")

    plt.xlabel("x")
    plt.ylabel("fitness")
    plt.title("Step 1 — Random Search")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    random.seed(0)

    best_x, best_fitness, all_guesses = random_search()

    print("best x:", best_x)
    print("best fitness:", best_fitness)

    plot_search(best_x, best_fitness, all_guesses)
