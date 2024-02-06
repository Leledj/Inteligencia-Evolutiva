import random
import pickle
import os


# Definindo a sequência alvo mais complexa
target_sequence = [7,9,8,5,4,6,7,2,1]

# Parâmetros do algoritmo genético
population_size = 200
mutation_rate = 0.05
number_of_generations = 1000
tournament_size = 5


# Gerar uma solução inicial aleatória
def generate_random_solution():
    return [random.randint(0, 9) for _ in range(len(target_sequence))]

# Calcular o 'fitness' de uma solução
def calculate_fitness(solution):
    return sum([1 for i, j in zip(solution, target_sequence) if i == j])

# Funções básicas (geração inicial e fitness) permanecem as mesmas

# Função de torneio para seleção
def tournament_selection(population):
    winners = []
    for _ in range(tournament_size):
        participants = random.sample(population, tournament_size)
        winner = max(participants, key=calculate_fitness)
        winners.append(winner)
    return winners

# Crossover mais complexo
def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(target_sequence) - 1)
    return parent1[:crossover_point] + parent2[crossover_point:]

# Evolução
def evolve(population):
    new_generation = []

    # Seleção por torneio
    selected_for_reproduction = tournament_selection(population)

    # Crossover e mutação
    while len(new_generation) < population_size:
        parent1, parent2 = random.sample(selected_for_reproduction, 2)
        child = crossover(parent1, parent2)

        # Mutação
        if random.random() < mutation_rate:
            child[random.randint(0, len(child) - 1)] = random.randint(0, 9)

        new_generation.append(child)

    return new_generation

# Tentar carregar a população do arquivo, se disponível
if os.path.exists('evolutionary_algorithm_state.pkl'):
    with open('evolutionary_algorithm_state.pkl', 'rb') as input_file:
        population = pickle.load(input_file)
else:
    # Criar uma nova população se o arquivo não existir
    population = [generate_random_solution() for _ in range(population_size)]

# Algoritmo genético
for generation in range(number_of_generations):
    population = evolve(population)
    best_solution = max(population, key=calculate_fitness)
    print(f"Generation {generation}: Best Solution: {best_solution} Fitness: {calculate_fitness(best_solution)}")

    if calculate_fitness(best_solution) == len(target_sequence):
        print("Target sequence found!")
        break

# Salvando a população em um arquivo
try:
    with open('evolutionary_algorithm_state.pkl', 'wb') as output_file:
        pickle.dump(population, output_file)
    print("Estado do algoritmo salvo com sucesso.")
except IOError as e:
    print(f"Erro ao salvar o estado do algoritmo: {e}")