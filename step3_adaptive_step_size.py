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


def mutate(x, step_size):
    nudged_x = x + random.gauss(0, step_size)
    return clamp_to_bounds(nudged_x)


def grow_step(step_size):
    return step_size * 1.22


def shrink_step(step_size):
    return step_size * 0.82


def evolution_strategy():
    total_steps = 200
    check_interval = 20
    target_success_rate = 1 / 5

    current_x = random_start()
    current_fitness = fitness(current_x)
    step_size = 2.0

    successes_in_block = 0
    trajectory = [(current_x, current_fitness)]
    step_size_history = [step_size]

    for step_number in range(total_steps):
        print(f"Step {step_number}")
        candidate_x = mutate(current_x, step_size)
        candidate_fitness = fitness(candidate_x)

        candidate_is_better = candidate_fitness > current_fitness
        if candidate_is_better:
            current_x = candidate_x
            current_fitness = candidate_fitness
            successes_in_block += 1
            trajectory.append((current_x, current_fitness))

        block_finished = (step_number + 1) % check_interval == 0
        if block_finished:
            success_rate = successes_in_block / check_interval
            if success_rate > target_success_rate:
                step_size = grow_step(step_size)
            else:
                step_size = shrink_step(step_size)
            successes_in_block = 0

        step_size_history.append(step_size)

    return current_x, current_fitness, trajectory, step_size_history


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


def plot_strategy(best_x, best_fitness, trajectory, step_size_history):
    figure, (landscape_axis, step_axis) = plt.subplots(1, 2, figsize=(12, 5))

    curve_xs, curve_ys = smooth_curve()
    landscape_axis.plot(curve_xs, curve_ys, color="black", label="fitness landscape")

    total_moves = len(trajectory)
    for move_number, (move_x, move_y) in enumerate(trajectory):
        progress = move_number / (total_moves - 1)
        size, opacity = point_size_and_opacity(progress)
        is_last_move = move_number == total_moves - 1
        label = "attempts (faint=early, bold=late)" if is_last_move else None
        landscape_axis.scatter([move_x], [move_y], s=size, color="green", alpha=opacity, label=label)

    landscape_axis.scatter([best_x], [best_fitness], s=80, color="red", label="best found")
    landscape_axis.set_xlabel("x")
    landscape_axis.set_ylabel("fitness")
    landscape_axis.set_title("Step 3 — Adaptive Step Size")
    landscape_axis.legend()

    step_axis.plot(step_size_history, color="purple")
    step_axis.set_xlabel("iteration")
    step_axis.set_ylabel("step size")
    step_axis.set_title("Step size over time")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    random.seed(0)

    best_x, best_fitness, trajectory, step_size_history = evolution_strategy()

    print("best x:", best_x)
    print("best fitness:", best_fitness)
    print("final step size:", step_size_history[-1])

    plot_strategy(best_x, best_fitness, trajectory, step_size_history)
