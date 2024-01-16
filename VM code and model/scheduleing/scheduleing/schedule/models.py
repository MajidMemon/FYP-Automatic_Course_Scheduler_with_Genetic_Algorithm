from django.db import models
import math
import random as rnd
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save, post_delete
from datetime import timedelta, date
# Create your models here.


time_slots = (
    ('8:30 - 11:30', '8:30 - 11:30'),
    ('11:45 - 2:45', '11:45 - 2:45'),
    ('3:00 - 6:00', '3:0 - 6:00'),
    ('6:30 - 9:30', '6:30 - 9:30'),
)

DAYS_OF_WEEK = (
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
)

POPULATION_SIZE = 100
MAX_GENERATIONS = 50
CROSSOVER_RATE = 0.8
MUTATION_RATE = 0.2

class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} (ID: {self.id})"

class Instructor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} (ID: {self.id})"

class Classroom(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} (ID: {self.id})"

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    max_sessions = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.name} (ID: {self.id})"


class MeetingTime(models.Model):
    id = models.AutoField(primary_key=True)
    time = models.CharField(max_length=35, choices=time_slots)
    day = models.CharField(max_length=15, choices=DAYS_OF_WEEK)

    def __str__(self):
        return f"{self.day} {self.get_time_display()} (ID: {self.id})"
    

class InstructorPreference(models.Model):
    id = models.AutoField(primary_key=True)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    preferred_courses = models.ManyToManyField(Course)
    preferred_days = models.CharField(max_length=255,null=True)
    max_classes_per_day = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.instructor.name}'s Preferences (ID: {self.id})"

class CourseSession(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    instructors = models.ManyToManyField(Instructor)
    classrooms = models.ManyToManyField(Classroom)
    meeting_times = models.ManyToManyField(MeetingTime)
    
    def is_instructor_available(self):
        try:
            instructor_preference = InstructorPreference.objects.get(instructor=self.instructor)
            # Check if the session's meeting time day and course match instructor's preferences
            return (
                self.meeting_time.day in instructor_preference.preferred_days and
                self.course in instructor_preference.preferred_courses
            )
        except InstructorPreference.DoesNotExist:
            return False

    def __str__(self):
        return f"{self.course.name} Session (ID: {self.id})"