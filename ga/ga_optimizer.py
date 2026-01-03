# ga/ga_optimizer.py

import pygad
import numpy as np
from ga.fitness import fitness_function

def run_ga(X_train, X_test, y_train, y_test):

    num_features = X_train.shape[1]

    def fitness_wrapper(ga_instance, solution, solution_idx):
        return fitness_function(
            ga_instance,
            solution,
            solution_idx,
            X_train,
            X_test,
            y_train,
            y_test
        )

    gene_space = (
        [{"low": 0, "high": 1}] * num_features +  # feature mask
        [
            {"low": 30, "high": 80},   # n_estimators
            {"low": 5, "high": 15}     # max_depth
        ]
    )

    ga = pygad.GA(
        num_generations=10,        # reduced
        sol_per_pop=8,             # reduced
        num_parents_mating=4,
        num_genes=num_features + 2,
        fitness_func=fitness_wrapper,
        gene_space=gene_space,
        mutation_percent_genes=8,
        parent_selection_type="tournament",
        keep_parents=2,
        random_seed=42,
        parallel_processing=None   # <<<<<< disable multiprocessing
    )

    ga.run()

    solution, fitness, _ = ga.best_solution()
    print(f"🧬 Best GA Fitness Score: {fitness:.4f}")

    return solution
