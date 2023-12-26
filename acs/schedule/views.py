from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from . forms import *
from .models import *
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import View

#===============================================================++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


POPULATION_SIZE = 9
NUMB_OF_ELITE_SCHEDULES = 1
TOURNAMENT_SELECTION_SIZE = 3
MUTATION_RATE = 0.05

class Data:
    def __init__(self):
        self._rooms = Room.objects.all()
        self._meetingTimes = MeetingTime.objects.all()
        self._instructors = Instructor.objects.all()
        self._courses = Course.objects.all()
        self._depts = Department.objects.all()

    def get_rooms(self): return self._rooms

    def get_instructors(self): return self._instructors

    def get_courses(self): return self._courses

    def get_depts(self): return self._depts

    def get_meetingTimes(self): return self._meetingTimes


class Schedule:
    def __init__(self):
        self._data = data
        self._classes = []
        self._numberOfConflicts = 0
        self._fitness = -1
        self._classNumb = 0
        self._isFitnessChanged = True

    def get_classes(self):
        self._isFitnessChanged = True
        return self._classes

    def get_numbOfConflicts(self): return self._numberOfConflicts

    def get_fitness(self):
        if self._isFitnessChanged:
            self._fitness = self.calculate_fitness()
            self._isFitnessChanged = False
        return self._fitness

    def initialize(self):
        sections = Section.objects.all()
        for section in sections:
            dept = section.department
            n = section.num_class_in_week
            if n <= len(MeetingTime.objects.all()):
                courses = dept.courses.all()
                for course in courses:
                    for i in range(n // len(courses)):
                        crs_inst = course.instructors.all()
                        newClass = Class(self._classNumb, dept, section.section_id, course)
                        self._classNumb += 1
                        newClass.set_meetingTime(data.get_meetingTimes()[rnd.randrange(0, len(MeetingTime.objects.all()))])
                        newClass.set_room(data.get_rooms()[rnd.randrange(0, len(data.get_rooms()))])
                        newClass.set_instructor(crs_inst[rnd.randrange(0, len(crs_inst))])
                        self._classes.append(newClass)
            else:
                n = len(MeetingTime.objects.all())
                courses = dept.courses.all()
                for course in courses:
                    for i in range(n // len(courses)):
                        crs_inst = course.instructors.all()
                        newClass = Class(self._classNumb, dept, section.section_id, course)
                        self._classNumb += 1
                        newClass.set_meetingTime(data.get_meetingTimes()[rnd.randrange(0, len(MeetingTime.objects.all()))])
                        newClass.set_room(data.get_rooms()[rnd.randrange(0, len(data.get_rooms()))])
                        newClass.set_instructor(crs_inst[rnd.randrange(0, len(crs_inst))])
                        self._classes.append(newClass)

        return self

    def calculate_fitness(self):
        self._numberOfConflicts = 0
        classes = self.get_classes()
        for i in range(len(classes)):
            if classes[i].room.seating_capacity < int(classes[i].course.max_numb_students):
                self._numberOfConflicts += 1
            for j in range(len(classes)):
                if j >= i:
                    if (classes[i].meeting_time == classes[j].meeting_time) and \
                            (classes[i].section_id != classes[j].section_id) and (classes[i].section == classes[j].section):
                        if classes[i].room == classes[j].room:
                            self._numberOfConflicts += 1
                        if classes[i].instructor == classes[j].instructor:
                            self._numberOfConflicts += 1
        return 1 / (1.0 * self._numberOfConflicts + 1)


class Population:
    def __init__(self, size):
        self._size = size
        self._data = data
        self._schedules = [Schedule().initialize() for i in range(size)]

    def get_schedules(self):
        return self._schedules


#class of genetic algorithm with its functions.

#===============================================================++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#===============================================================++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++




# Create your views here.
def index(request):
    return render(request, 'index.html')
    #return HttpResponse("This is home page")

def about(request):
    return render(request, 'about.html')
   #return HttpResponse("This is about page")

def product(request):
    return render(request, 'product.html')
    #return HttpResponse("This is product page")

def resource(request):
    return HttpResponse("This is resource page")

def pricing(request):
    return HttpResponse("This is pricing page")


def contact(request):
    if request.method == 'POST':
        message = request.POST['message']

        send_mail('TTGS Contact',
                  message,
                  settings.EMAIL_HOST_USER,
                  ['abdul.51347@iqra.edu.pk'],
                  fail_silently=False)
    return render(request, 'contact.html', {})

#################################################################################

@login_required
def admindash(request):
    return render(request, 'admindashboard.html', {})

#################################################################################

@login_required
def addCourses(request):
    form = CourseForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('addCourses')
        else:
            print('Invalid')
    context = {
        'form': form
    }
    return render(request, 'addCourses.html', context)

@login_required
def course_list_view(request):
    context = {
        'courses': Course.objects.all()
    }
    return render(request, 'courseslist.html', context)

@login_required
def delete_course(request, pk):
    crs = Course.objects.filter(pk=pk)
    if request.method == 'POST':
        crs.delete()
        return redirect('editcourse')

#################################################################################

@login_required
def addInstructor(request):
    form = InstructorForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('addInstructors')
    context = {
        'form': form
    }
    return render(request, 'addInstructors.html', context)

@login_required
def inst_list_view(request):
    context = {
        'instructors': Instructor.objects.all()
    }
    return render(request, 'inslist.html', context)

@login_required
def delete_instructor(request, pk):
    inst = Instructor.objects.filter(pk=pk)
    if request.method == 'POST':
        inst.delete()
        return redirect('editinstructor')

#################################################################################

@login_required
def addRooms(request):
    form = RoomForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('addRooms')
    context = {
        'form': form
    }
    return render(request, 'addRooms.html', context)

@login_required
def room_list(request):
    context = {
        'rooms': Room.objects.all()
    }
    return render(request, 'roomslist.html', context)

@login_required
def delete_room(request, pk):
    rm = Room.objects.filter(pk=pk)
    if request.method == 'POST':
        rm.delete()
        return redirect('editrooms')

#################################################################################

@login_required
def addTimings(request):
    form = MeetingTimeForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('addTimings')
        else:
            print('Invalid')
    context = {
        'form': form
    }
    return render(request, 'addTimings.html', context)

@login_required
def meeting_list_view(request):
    context = {
        'meeting_times': MeetingTime.objects.all()
    }
    return render(request, 'mtlist.html', context)

@login_required
def delete_meeting_time(request, pk):
    mt = MeetingTime.objects.filter(pk=pk)
    if request.method == 'POST':
        mt.delete()
        return redirect('editmeetingtime')

#################################################################################

@login_required
def addDepts(request):
    form = DepartmentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('addDepts')
    context = {
        'form': form
    }
    return render(request, 'addDepts.html', context)

@login_required
def department_list(request):
    context = {
        'departments': Department.objects.all()
    }
    return render(request, 'deptlist.html', context)

@login_required
def delete_department(request, pk):
    dept = Department.objects.filter(pk=pk)
    if request.method == 'POST':
        dept.delete()
        return redirect('editdepartment')

#################################################################################

@login_required
def addSections(request):
    form = SectionForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('addSections')
    context = {
        'form': form
    }
    return render(request, 'addSections.html', context)

@login_required
def section_list(request):
    context = {
        'sections': Section.objects.all()
    }
    return render(request, 'seclist.html', context)

@login_required
def delete_section(request, pk):
    sec = Section.objects.filter(pk=pk)
    if request.method == 'POST':
        sec.delete()
        return redirect('editsection')

#################################################################################
