.from django.db import models
import random as rnd
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save, post_delete
from datetime import timedelta, date

time_slots = (
    ('8:30 - 11:30', '8:30 - 11:30'),
    ('11:45 - 2:45', '11:45 - 2:45'),
    ('3:00 - 6:00', '3:00 - 6:00'),
    ('6:30 - 9:30', '6:30 - 9:30'),

)

DAYS_OF_WEEK = (
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday'),
)



class Room(models.Model):
    room_number = models.CharField(max_length=6)
    seating_capacity = models.IntegerField(default=0)
    room_type = models.CharField(max_length=10)

    def __str__(self):
        return self.room_number


class Instructor(models.Model):
    ins_id = models.CharField(max_length=6, primary_key=True)
    ins_name = models.CharField(max_length=25)
    

    def __str__(self):
        return f'{self.ins_id} {self.ins_name}'


class MeetingTime(models.Model):
    meet_id = models.CharField(max_length=4, primary_key=True)
    meet_time = models.CharField(max_length=50, choices=time_slots)
    day = models.CharField(max_length=15, choices=DAYS_OF_WEEK)

    def __str__(self):
        return f'{self.meet_id} {self.day} {self.meet_time}'


class Course(models.Model):
    course_number = models.CharField(max_length=25, primary_key=True)
    course_name = models.CharField(max_length=40)
    max_numb_students = models.CharField(max_length=65)
    instructors = models.ManyToManyField(Instructor)

    def __str__(self):
        return f'{self.course_number} {self.course_name}'


class Department(models.Model):
    dept_name = models.CharField(max_length=50)
    courses = models.ManyToManyField(Course)

    @property
    def get_courses(self):
        return self.courses

    def __str__(self):
        return self.dept_name
