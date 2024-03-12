# -*- coding: utf-8 -*-
'''
    Genetic Algorithm for the Flow-Shop Scheduling Problem
      Based off the article "Adaptive genetic algorithm for 
      two-stage hybrid flow-shop scheduling with sequence-
      independent setup time and no-interruption requirement" 
      by Yan Qiao, NaiQi Wu, YunFang He, ZhiWu Li, Tao Chen
'''
import random
import math

# Define parameters
NUM_JOBS = 20
NUM_MACHINES = 8
POPULATION_SIZE = 10
NUM_GENERATIONS = 100
CROSSOVER_RATE = 0.8
MUTATION_RATE_1 = 0.03
MUTATION_RATE_2 = 1.0
DIVERSITY_THRESHOLD = 0.8
STABILITY_THRESHOLD = 0.8
MIN_TIME = 1
MAX_TIME = 10

def generate_processing_times():
    return [random.randint(MIN_TIME, MAX_TIME) for _ in range(NUM_MACHINES)]

# Generate random initial population
def generate_initial_population():
    population = []
    for _ in range(POPULATION_SIZE):
        chromosome = []
        for _ in range(NUM_JOBS):
            # Generate random processing times for each job on each machine
            processing_times = generate_processing_times()
            chromosome.append(processing_times)
        population.append(chromosome)
    return population

# Calculate fitness of a chromosome
def calculate_fitness(chromosome):
    total_processing_time = 0
    machine_times = [0] * NUM_MACHINES
    
    for job in chromosome:
        for machine, processing_time in enumerate(job):
            machine_times[machine] += processing_time
        total_processing_time += max(machine_times)
    
    return total_processing_time

# Perform crossover between two chromosomes
def crossover(parent1, parent2, probability=CROSSOVER_RATE):
    if probability > random.random():
        return parent1, parent2

    crossover_point = random.randint(1, NUM_JOBS - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

# Perform mutation on a chromosome
def mutate(chromosome , probability=MUTATION_RATE_1):
    for i in range(len(chromosome)):
        if probability > random.random():
            chromosome[i] = generate_processing_times()
    return chromosome

# Calculate the distance between two chromosomes
def calculate_distance(chromosome1, chromosome2):
    return sum([1 for i in range(NUM_JOBS) if chromosome1[i] != chromosome2[i]])

# Calculate the diversity of the population
def calculate_diversity(population):
    diversity = 0
    for i in range(len(population) - 1):
        for j in range(i + 1, len(population)):
            diversity += calculate_distance(population[i], population[j])
    diversity /= (NUM_JOBS * POPULATION_SIZE * (POPULATION_SIZE - 1) / 2)
    return diversity

# Genetic Algorithm
def genetic_algorithm():
    # Generate initial population
    population = generate_initial_population()
    diversity_scores = []
    fitness_scores = []
    
    # Evolution loop
    for generation in range(NUM_GENERATIONS):
        # Evaluate fitness of each individual
        fitness_scores = [calculate_fitness(chromosome) for chromosome in population]
        
        # Evaluate diversity of the population
        diversity = calculate_diversity(population)
        diversity_avg = sum(diversity_scores) / len(diversity_scores) if diversity_scores else 0
        diversity_scores.append(diversity)
        diversity_stability = sum([1 for score in diversity_scores if abs(score - diversity_avg) <= 0.05]) / len(diversity_scores)

        # Print statistics
        if math.log10(generation+1) % 1 == 0:
            print("Generation ", generation+1, ":", fitness_scores)
            print("Best Fitness: ", min(fitness_scores))
            print("Diversity: ", diversity)
            print("Diversity Average: ", diversity_avg)
            print("Diversity Stability: ", diversity_stability)
            print()
        
        # Select parents for crossover
        parents = random.choices(population, weights=[1 / (fitness + 1) for fitness in fitness_scores], k=2)

        # Set up the probability of crossover and mutation
        cross_prob = CROSSOVER_RATE
        muta_prob = MUTATION_RATE_1
        div_thresh = DIVERSITY_THRESHOLD
        
        # Perform crossover and mutation to create new generation
        offspring = []
        for _ in range(POPULATION_SIZE // 2):
            # Based off the rules given in 4.4 of the article
            if muta_prob == MUTATION_RATE_1 and diversity < div_thresh and diversity_stability >= STABILITY_THRESHOLD:
                div_thresh = diversity_avg
            if diversity >= div_thresh:
                muta_prob = MUTATION_RATE_2
            if muta_prob == MUTATION_RATE_2:
                cross_prob = diversity
            child1, child2 = crossover(parents[0], parents[1], cross_prob)

            if diversity <= CROSSOVER_RATE:
                muta_prob = MUTATION_RATE_1
            offspring.extend([mutate(child1, muta_prob), mutate(child2, muta_prob)])
        
        # Replace old population with new generation
        population = offspring
    
    # Select best solution from final population
    best_solution = min(population, key=calculate_fitness)
    best_fitness = calculate_fitness(best_solution)
    
    return best_solution, best_fitness

print("Number of Jobs:", NUM_JOBS)
print("Number of Machines:", NUM_MACHINES)
best_solution, best_fitness = genetic_algorithm()
print("Best solution:", best_solution)
print("Best fitness:", best_fitness)