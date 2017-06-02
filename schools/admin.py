# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import *

# Register your models here.

admin.site.register(Institution_Category)
admin.site.register(Moi_Type)
admin.site.register(Institution_Management)
admin.site.register(Institution_address)
admin.site.register(Boundary_Category)
admin.site.register(Boundary_Type)
admin.site.register(Staff_Type)

admin.site.register(Staff_Qualifications)
admin.site.register(Boundary)

admin.site.register(Institution)
admin.site.register(Child)
admin.site.register(Relations)
admin.site.register(StudentGroup)

admin.site.register(Academic_Year)
admin.site.register(Staff)
admin.site.register(Student)
admin.site.register(Student_StudentGroupRelation)


admin.site.register(Staff_StudentGroupRelation)
admin.site.register(Programme)
admin.site.register(Assessment)
admin.site.register(Assessment_Lookup)



admin.site.register(Assessment_StudentGroup_Association)
admin.site.register(Assessment_Class_Association)
admin.site.register(Question)
admin.site.register(Answer)