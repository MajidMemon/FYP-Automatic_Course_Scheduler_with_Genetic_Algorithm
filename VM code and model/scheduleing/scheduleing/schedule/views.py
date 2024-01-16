# views.py

#from django.shortcuts import render
#from .scheduling_algorithm import GeneticAlgorithm
#
#def GeneticAlgorithm(request):
#    best_schedule = GeneticAlgorithm()
#
 #   # Output the best schedule (you may want to log this information)
 #   for session in best_schedule:
 #       print(f"{session.course.name} | {session.instructor.name} | {session.classroom.name} | {session.meeting_time}")
#
 #   # Pass the best schedule to the template for rendering
 #   context = {'best_schedule': best_schedule}
 #   return render(request, 'results.html', context)

# views.py
# views.py

from django.shortcuts import render
from .scheduling_algorithm import GeneticAlgorithm

def run_genetic_algorithm(request):
    # Create an instance of the GeneticAlgorithm class
    genetic_algorithm = GeneticAlgorithm()

    # Run the genetic algorithm
    best_schedule = genetic_algorithm.run()

    # Output the best schedule (you may want to log this information)
    for session in best_schedule:
        print(f"{session.course.name} | {session.instructor.name} | {session.classroom.name} | {session.meeting_time}")

    # Pass the best schedule to the template for rendering
    context = {'best_schedule': best_schedule}
    return render(request, 'results.html', context)