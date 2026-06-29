import random
import numpy
import matplotlib.pyplot as plt


def fitness(x):
    return -(x - 2) ** 2 + 10


def random_start():
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


def hill_climb():
    total_steps = 100

    current_x = random_start()
    current_fitness = fitness(current_x)

    trajectory = [(current_x, current_fitness)]

    for step_number in range(total_steps):
        candidate_x = mutate(current_x)
        candidate_fitness = fitness(candidate_x)

        candidate_is_better = candidate_fitness > current_fitness
        if candidate_is_better:
            current_x = candidate_x
            current_fitness = candidate_fitness
            trajectory.append((current_x, current_fitness))
        print(f"Step {step_number}")
    return current_x, current_fitness, trajectory


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


def plot_climb(best_x, best_fitness, trajectory):
    curve_xs, curve_ys = smooth_curve()
    plt.plot(curve_xs, curve_ys, color="black", label="fitness landscape")

    total_moves = len(trajectory)
    for move_number, (move_x, move_y) in enumerate(trajectory):
        progress = move_number / (total_moves - 1)
        size, opacity = point_size_and_opacity(progress)
        is_last_move = move_number == total_moves - 1
        label = "attempts (faint=early, bold=late)" if is_last_move else None
        plt.scatter([move_x], [move_y], s=size, color="green", alpha=opacity, label=label)

    plt.scatter([best_x], [best_fitness], s=80, color="red", label="best found")

    plt.xlabel("x")
    plt.ylabel("fitness")
    plt.title("Step 2 — Hill Climbing")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    random.seed(0)

    best_x, best_fitness, trajectory = hill_climb()

    print("best x:", best_x)
    print("best fitness:", best_fitness)
    print("accepted moves:", len(trajectory))

    plot_climb(best_x, best_fitness, trajectory)
