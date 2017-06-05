# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import *

# Register your models here.

admin.site.register(Programme)
admin.site.register(Assessment)
admin.site.register(Assessment_Lookup)



admin.site.register(Assessment_StudentGroup_Association)
admin.site.register(Assessment_Class_Association)
admin.site.register(Question)
admin.site.register(Answer)