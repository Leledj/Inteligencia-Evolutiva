import random

# Definindo a sequência alvo
target_sequence = [1, 2, 3, 4]

# Parâmetros do algoritmo genético
population_size = 100
mutation_rate = 0.01
number_of_generations = 100

# Gerar uma solução inicial aleatória
def generate_random_solution():
    return [random.randint(0, 9) for _ in range(len(target_sequence))]

# Calcular o 'fitness' de uma solução
def calculate_fitness(solution):
    return sum([1 for i, j in zip(solution, target_sequence) if i == j])

# Reprodução e mutação
def evolve(population):
    sorted_population = sorted(population, key=calculate_fitness, reverse=True)
    next_generation = sorted_population[:2]  # Mantém os dois melhores

    # Reprodução
    while len(next_generation) < population_size:
        parent1, parent2 = random.sample(sorted_population[:10], 2)  # Seleção aleatória
        child = parent1[:2] + parent2[2:]  # Crossover

        # Mutação
        if random.random() < mutation_rate:
            child[random.randint(0, len(child) - 1)] = random.randint(0, 9)

        next_generation.append(child)

    return next_generation

# Algoritmo genético
population = [generate_random_solution() for _ in range(population_size)]
for generation in range(number_of_generations):
    population = evolve(population)
    best_solution = max(population, key=calculate_fitness)
    print(f"Generation {generation}: Best Solution: {best_solution} Fitness: {calculate_fitness(best_solution)}")

    if calculate_fitness(best_solution) == len(target_sequence):
        print("Target sequence found!")
        break
