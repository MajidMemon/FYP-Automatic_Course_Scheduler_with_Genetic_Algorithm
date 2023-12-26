from django.forms import ModelForm
from .models import *
from django import forms

class RoomForm(ModelForm):
    class Meta:
        model = Room
        labels = {
            "room_number": "Room ID",
            "seating_capacity": "Capacity"
        }
        fields = [
            'room_number',
            'seating_capacity'
        ]


class InstructorForm(ModelForm):
    class Meta:
        model = Instructor
        labels = {
            "ins_id": "Teacher UID",
            "ins_name": "Full Name"
        }
        fields = [
            'ins_id',
            'ins_name',
        ]


class MeetingTimeForm(ModelForm):
    class Meta:
        model = MeetingTime
        fields = [
            'meet_id',
            'meet_time',
            'day'
        ]
        widgets = {
            'meet_id': forms.TextInput(),
            'meet_time': forms.Select(),
            'day': forms.Select(),
        }
        labels = {
            "meet_id": "Meeting ID",
            "meet_time": "Time",
            "day": "Day of the Week"
        }


class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['course_number', 'course_name', 'max_numb_students', 'instructors']
        labels = {
            "course_number": "Course ID",
            "course_name": "Course Name",
            "max_numb_students": "Course Capacity",
            "instructors": "Course Teachers"
        }


class DepartmentForm(ModelForm):
    class Meta:
        model = Department
        fields = ['dept_name', 'courses']
        labels = {
            "dept_name": "Department Name",
            "courses": "Corresponding Courses"
        }


class SectionForm(ModelForm):
    class Meta:
        model = Section
        fields = ['section_id', 'department', 'num_class_in_week']
        labels = {
            "section_id": "Section ID",
            "department": "Corresponding Department",
            "num_class_in_week": "Classes Per Week"
        }
