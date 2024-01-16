# scheduling_algorithm.py

from random import * 
from random import shuffle, randint, choice, choices
from django.db import transaction
from .models import *

class GeneticAlgorithm:
    def __init__(self, population_size=100, max_generations=50, crossover_rate=0.8, mutation_rate=0.2):
        self.population_size = population_size
        self.max_generations = max_generations
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate

    def run(self):
        population = self._generate_initial_population()

        for generation in range(self.max_generations):
            fitness_scores = [self._calculate_fitness(schedule) for schedule in population]

            # Select parents for crossover based on roulette wheel selection
            total_fitness = sum(fitness_scores)
            probabilities = [score / total_fitness for score in fitness_scores]

            parents = self._select_parents(population, probabilities, self.population_size)

            # Create next generation using crossover and mutation
            next_generation = []
            for i in range(0, self.population_size, 2):
                parent1, parent2 = parents[i], parents[i + 1]

                if random() < self.crossover_rate:
                    child1, child2 = self._crossover(parent1, parent2)
                else:
                    child1, child2 = parent1, parent2

                if random() < self.mutation_rate:
                    child1 = self._mutate(child1)
                if random() < self.mutation_rate:
                    child2 = self._mutate(child2)

                next_generation.extend([child1, child2])

            population = next_generation

        # Select the best schedule from the final population
        best_schedule = max(population, key=self._calculate_fitness)
        return best_schedule

    def _generate_initial_population(self):
        population = []
        for _ in range(self.population_size):
            schedule = self._generate_random_schedule()
            population.append(schedule)
        return population

    def _generate_random_schedule(self):
        courses = Course.objects.all()
        instructors = Instructor.objects.all()
        classrooms = Classroom.objects.all()
        meeting_times = MeetingTime.objects.all()

        schedule = []

        for course in courses:
            instructors_list = list(instructors.filter(department=course.department))
            classrooms_list = list(classrooms)
            meeting_times_list = list(meeting_times)

            shuffle(instructors_list)
            shuffle(classrooms_list)
            shuffle(meeting_times_list)
            

        # Randomly select one course for the schedule
            selected_course = choice(courses)

            for instructor, classroom, meeting_time in zip(instructors_list, classrooms_list, meeting_times_list):
            # Use the selected_course in the CourseSession
                schedule.append(CourseSession(course=selected_course, instructor=instructor, classroom=classroom, meeting_time=meeting_time))

        return schedule
    
    def _calculate_fitness(self, schedule):
        conflicts = 0

        # Check conflicts based on constraints
        for session in schedule:
            # Check if instructor is teaching in another classroom at the same time
            if CourseSession.objects.filter(instructor=session.instructor, meeting_time=session.meeting_time).exclude(id=session.id).exists():
                conflicts += 1

            # Check if classroom is occupied by another course session at the same time
            if CourseSession.objects.filter(classroom=session.classroom, meeting_time=session.meeting_time).exclude(id=session.id).exists():
                conflicts += 1

            # Check if the course matches the instructor's preferences
            try:
                instructor_preference = InstructorPreference.objects.get(instructor=session.instructor)
                if (
                    any(mt.day in instructor_preference.preferred_days for mt in [session.meeting_time]) and
                    session.course in instructor_preference.preferred_courses
                ):
                    conflicts += 1
            except InstructorPreference.DoesNotExist:
                pass

        return 1 / (1 + conflicts)  # Higher fitness for fewer conflicts

    def _crossover(self, parent1, parent2):
        crossover_point = randint(1, len(parent1) - 1)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        return child1, child2

    def _mutate(self, schedule):
        mutated_schedule = schedule.copy()
        idx1, idx2 = sample(range(len(mutated_schedule)), 2)
        mutated_schedule[idx1], mutated_schedule[idx2] = mutated_schedule[idx2], mutated_schedule[idx1]
        return mutated_schedule

    def _select_parents(self, population, probabilities, size):
        parents = choices(population, weights=probabilities, k=size)
        return parents