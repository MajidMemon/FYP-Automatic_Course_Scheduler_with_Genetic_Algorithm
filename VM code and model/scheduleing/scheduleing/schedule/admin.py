from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Department)
admin.site.register(Instructor)
admin.site.register(Classroom)
#admin.site.register(time_slots)
#admin.site.register(DAYS_OF_WEEK)
admin.site.register(Course)
admin.site.register(CourseSession)
admin.site.register(InstructorPreference)

admin.site.register(MeetingTime)