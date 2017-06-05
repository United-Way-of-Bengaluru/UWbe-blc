# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.db import models
from schools.models import *

# Create your models here.

Assessment_type = [(1, 'Institution'), (2, 'Student Group'), (3,
                   'Student')]


def default_end_date():
    ''' To select academic year end date'''

    now = datetime.date.today()
    currentYear = int(now.strftime('%Y'))
    currentMont = int(now.strftime('%m'))
    academicYear = current_academic().name
    academicYear = academicYear.split('-')
    if currentMont > 5 and int(academicYear[0]) == currentYear:
        academic_end_date = datetime.date(currentYear+1,12, 30)
    else:
        academic_end_date = datetime.date(currentYear, 5, 30)
    return academic_end_date


class Programme(models.Model):

    """ This class Stores information about Programme """

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, blank=True,
                                   null=True)
    start_date = models.DateField(max_length=20,
                                 default=datetime.date.today)
    end_date = models.DateField(max_length=20, default=default_end_date)
    programme_institution_category = models.ForeignKey(Boundary_Type,
            blank=True, null=True)
    active = models.IntegerField(blank=True, null=True, default=2)

    class Meta:

        ordering = ['-start_date', '-end_date', 'name']

    def __unicode__(self):
        return '%s (%s-%s)' % (self.name, self.start_date.strftime('%Y'
                               ), self.end_date.strftime('%Y'))

    def get_view_url(self):
        return '/programme/%s/view/' % self.id

    def get_edit_url(self):
        return '/programme/%s/update/' % self.id

    def getChild(self):
        if Assessment.objects.filter(programme__id=self.id,
                active__in=[1, 2]).count():
            return True
        else:
            return False

    def getModuleName(self):
        return 'programme'

    def getViewUrl(self):
        return '<a href="/programme/%s/view/" onclick="return KLP_View(this)" class="KLP_treetxt" title="%s (%s-%s)"> <img src="/static_media/tree-images/reicons/programme.gif" title="Programme" /> &nbsp; <span id="programme_%s_text">%s (%s-%s)</span> </a>' \
            % (
            self.id,
            self.name,
            self.start_date.strftime('%Y'),
            self.end_date.strftime('%Y'),
            self.id,
            self.name,
            self.start_date.strftime('%Y'),
            self.end_date.strftime('%Y'),
            )

    def CreateNewFolder(self):
        return '<span><a href="/programme/%s/view/" onclick="return KLP_View(this)" class="KLP_treetxt" title="%s (%s-%s)"> <img src="/static_media/tree-images/reicons/programme.gif" title="Programme" /> &nbsp; <span id="programme_%s_text">%s (%s-%s)</span></a></span>' \
            % (
            self.id,
            self.name,
            self.start_date.strftime('%Y'),
            self.end_date.strftime('%Y'),
            self.id,
            self.name,
            self.start_date.strftime('%Y'),
            self.end_date.strftime('%Y'),
            )





class Assessment(models.Model):

    """ This class stores information about Assessment """

    programme = models.ForeignKey(Programme)
    name = models.CharField(max_length=100)
    start_date = models.DateField(max_length=20,
                                 default=datetime.date.today)
    end_date = models.DateField(max_length=20, default=default_end_date)
    query = models.CharField(max_length=500, blank=True, null=True)
    active = models.IntegerField(blank=True, null=True, default=2)
    typ = models.IntegerField(choices=Assessment_type, default=3)
    double_entry = models.BooleanField('Requires double entry',
            default=True)
    flexi_assessment = \
        models.BooleanField('Allows multiple sets of answer per assessment'
                            , default=False)
    primary_field_name = models.CharField(max_length=500, blank=True,
            null=True)
    primary_field_type = \
        models.IntegerField(choices=primary_field_type, default=3,
                            null=True)

    class Meta:

        unique_together = (('programme', 'name'), )
        ordering = ['start_date']

    def __unicode__(self):
        return '%s' % self.name

    def get_view_url(self):
        return '/assessment/%s/view/' % self.id

    def get_edit_url(self):
        return '/assessment/%s/update/' % self.id

    def getChild(self):
        if Question.objects.filter(assessment__id=self.id,
                                   active=2).count():
            return True
        else:
            return False

    def getViewUrl(self):
        return '<a id="assessment_%s_view" href="/assessment/%s/view/" onclick="return KLP_View(this)" class="KLP_treetxt" title="%s"> <img src="/static_media/tree-images/reicons/assessment.gif" title="Assessment" /> &nbsp; <span id="assessment_%s_text">%s</span> </a>' \
            % (self.id, self.id, self.name, self.id, self.name)

    def getModuleName(self):
        return 'assessment'

    def getAssessmentStatus(self):
        QuesObj = Question.objects.filter(assessment__id=self.id,
                active=2)
        AnsObj = Answer.objects.filter(question__in=QuesObj)
        if AnsObj:
            return True
        else:
            return False

    def CreateNewFolder(self):
        return '<span><a id="assessment_%s_view" href="/assessment/%s/view/" onclick="return KLP_View(this)" class="KLP_treetxt" title="%s"> <img src="/static_media/tree-images/reicons/assessment.gif" title="Assessment" /> &nbsp; <span id="assessment_%s_text">%s</span></a></span>' \
            % (self.id, self.id, self.name, self.id, self.name)


#register_model(Assessment)  # Register model for to store information in fullhistory


class Assessment_Lookup(models.Model):

    """ This class stores information about Assessment """

    assessment = models.ForeignKey(Assessment)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    rank=models.IntegerField(blank=True, null=True, default=1)
    class Meta:

        ordering = ['name']
        unique_together = (('assessment', 'name'), )

    def __unicode__(self):
        return '%s' % self.name


#register_model(Assessment_Lookup)


class Assessment_StudentGroup_Association(models.Model):

    '''This Class stores the Assessment and Student Group Association Information'''

    assessment = models.ForeignKey(Assessment)
    student_group = models.ForeignKey(StudentGroup)
    active = models.IntegerField(blank=True, null=True, default=2)


    def save(self, *args, **kwargs):
        # custom save method
        #pdb.set_trace()
        from django.db import connection
        connection.features.can_return_id_from_insert = False
        #print "save"

        #print "Access", self.active
        self.full_clean()
        super(Assessment_StudentGroup_Association, self).save(*args, **kwargs)

    class Meta:

        unique_together = (('assessment', 'student_group'), )


#register_model(Assessment_StudentGroup_Association)  # Register model for to store information in fullhistory


class Assessment_Class_Association(models.Model):

    '''This Class stores the Assessment and Student Group Association Information'''

    assessment = models.ForeignKey(Assessment)
    student_group = models.ForeignKey(StudentGroup)
    active = models.IntegerField(blank=True, null=True, default=2)

    class Meta:

        unique_together = (('assessment', 'student_group'), )


#register_model(Assessment_Class_Association)  # Register model for to store information in fullhistory


class Assessment_Institution_Association(models.Model):

    '''This Class stores the Assessment and Student Group Association Information'''

    assessment = models.ForeignKey(Assessment)
    institution = models.ForeignKey(Institution)
    active = models.IntegerField(blank=True, null=True, default=2)

    class Meta:

        unique_together = (('assessment', 'institution'), )


class Question(models.Model):

    """ This class stores Assessment detail information """

    assessment = models.ForeignKey(Assessment)
    name = models.CharField(max_length=200)
    question_type = models.IntegerField(choices=QuestionType, default=1)
    score_min = models.DecimalField(max_digits=10, decimal_places=2,
                                   blank=True, null=True)
    score_max = models.DecimalField(max_digits=10, decimal_places=2,
                                   blank=True, null=True)
    grade = models.CharField(max_length=100, blank=True, null=True)
    order = models.IntegerField()
    double_entry = models.BooleanField(default=True)
    active = models.IntegerField(blank=True, null=True, default=2)

    class Meta:

        unique_together = (('assessment', 'name'), )
        ordering = ['order']

    def __unicode__(self):
        return self.name

    def getAllGrades(self):
        return gradeList

    def getSelectedGrades(self):
        if self.grade:
            return self.grade.split(',')
        else:
            return ''

    def getChild(self):
        return False

    def getViewUrl(self):
        return '<a href="/question/%s/view/" onclick="return KLP_View(this)" class="KLP_treetxt" title="%s"> <img src="/static_media/tree-images/reicons/question.gif" title="Question" /> &nbsp; <span id="question_%s_text">%s</span> </a>' \
            % (self.id, self.name, self.id, self.name)

    def getModuleName(self):
        return 'question'

    def get_view_url(self):
        return '/question/%s/view/' % self.id

    def get_edit_url(self):
        return '/question/%s/update/' % self.id

    def CreateNewFolder(self):
        return '<span><a href="/question/%s/view/" onclick="return KLP_View(this)" class="KLP_treetxt" title="%s"> <img src="/static_media/tree-images/reicons/question.gif" title="Question" /> &nbsp; <span id="question_%s_text">%s</span></a></span>' \
            % (self.id, self.name, self.id, self.name)


#register_model(Question)  # Register model for to store information in fullhistory


class Answer(models.Model):

    """ This class stores information about student marks and grade """
    
    question = models.ForeignKey(Question)

    # student = models.IntegerField(blank = True, null = True,default=0) # models.ForeignKey(Student)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type',
            'object_id')
    answer_score = models.DecimalField(max_digits=10, decimal_places=2,
            blank=True, null=True)
    answer_grade = models.CharField(max_length=30, blank=True, null=True)
    double_entry = models.IntegerField(blank=True, null=True, default=0)
    status = models.IntegerField(blank=True, null=True)
    user1 = models.ForeignKey(User, blank=True, null=True,
                              related_name='user1')
    user2 = models.ForeignKey(User, blank=True, null=True,
                              related_name='user2')
    creation_date = models.DateField(auto_now_add=True,
                                    blank=True, null=True)
    last_modified_date = models.DateField(auto_now=True,
            blank=True, null=True)
    last_modified_by = models.ForeignKey(User, blank=True, null=True,
            related_name='last_modified_by')
    flexi_data = models.CharField(max_length=30, blank=True, null=True)

    class Meta:

        unique_together = (('question', 'object_id', 'flexi_data'), )


    def save(self, *args, **kwargs):
        # custom save method
        #pdb.set_trace()
        from django.db import connection
        connection.features.can_return_id_from_insert = False
        #print "save"

        #print "=================== status is", self.status
        self.full_clean()
        super(Answer, self).save(*args, **kwargs)

#register_model(Answer)  # Register model for to store information in fullhistory


class UserAssessmentPermissions(models.Model):

    """ This class stores information about user, instituion and assessment permissions"""

    user = models.ForeignKey(User)
    instituion = models.ForeignKey(Institution)
    assessment = models.ForeignKey(Assessment)
    access = models.BooleanField(default=True)

    class Meta:

        unique_together = (('user', 'instituion', 'assessment'), )


    def save(self, *args, **kwargs):
        # custom save method
        #pdb.set_trace()
        from django.db import connection
        connection.features.can_return_id_from_insert = False
        #print "save"

        #print "Access", self.access
        self.full_clean()
        super(UserAssessmentPermissions, self).save(*args, **kwargs)

