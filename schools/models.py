# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.contrib.contenttypes.models import ContentType
#from django.contrib.contenttypes import generic
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User
#from object_permissions import register
#from fullhistory import register_model
#from assessments.models import *
from django.db import models

#register_model(User)

primary_field_type = [(0, 'Default'),(1, 'Integer'), (2, 'Char'), (3, 'Date'), (4,
                      'Lookup')]

active_status = [
    (0, 'Deleted'),
    (1, 'Inactive'),
    (2, 'Active'),
    (3, 'Promoted'),
    (4, 'Promotion Failed'),
    (5, 'Passed Out'),
    (6, 'Detained'),
    (7, 'Completed'),
    ]

Institution_Gender = [('boys', 'boys'), ('girls', 'girls'), ('co-ed',
                      'co-ed')]

Gender = [('male', 'male'), ('female', 'female')]

Group_Type = [('Class', 'Class'), ('Center', 'Center')]

QuestionType = [(1, 'Marks'), (2, 'Grade')]

Relation_Type = [('Mother', 'Mother'), ('Father', 'Father'), ('Siblings'
                 , 'Siblings')]



Alpha_list = [('', 'No Section')]
for typ in range(ord('a'), ord('z') + 1):
    alph = chr(typ).upper()
    typs = (alph, alph)
    Alpha_list.append(typs)


class Institution_Category(models.Model):

    '''This Class stores the Institution Category Information'''

    name = models.CharField(max_length=50)
    category_type = models.IntegerField()

    def __unicode__(self):
        return '%s' % self.name


#register_model(Institution_Category)


class Moi_Type(models.Model):

    '''This Class stores the Mother Toungue (Languages) Information'''

    name = models.CharField(max_length=50)

    def __unicode__(self):
        return '%s' % self.name


#register_model(Moi_Type)


class Institution_Management(models.Model):

    '''This Class stores the Institution Management Information'''


    name = models.CharField(max_length=50)

    def __unicode__(self):
        return '%s' % self.name


#register_model(Institution_Management)  # Register model for to store information in fullhistory


class Institution_address(models.Model):

    ''' This class stores information about institution address '''

    address = models.CharField(max_length=1000)
    area = models.CharField(max_length=200, blank=True, null=True)
    pincode = models.CharField(max_length=100, blank=True, null=True)
    landmark = models.CharField(max_length=1000, blank=True, null=True,
                                help_text='Can be comma separated')
    instidentification = models.CharField(max_length=1000, blank=True,
            null=True, help_text='Can be comma separated')
    instidentification2 = models.CharField(max_length=1000, blank=True,
            null=True, help_text='Can be comma separated')
    route_information = models.CharField(max_length=500, blank=True,
            null=True, help_text='Can be comma separated')


#register_model(Institution_address)  # Register model for to store information in fullhistory


class Boundary_Category(models.Model):

    '''This Class stores the Boundary Category Information'''

    boundary_category = models.CharField(max_length=100)

    def __unicode__(self):
        return '%s' % self.boundary_category


#register_model(Boundary_Category)  # Register model for to store information in fullhistory


class Boundary_Type(models.Model):

    '''This Class stores the Boundary Type Information'''

    boundary_type = models.CharField(max_length=100)

    def __unicode__(self):
        return '%s' % self.boundary_type


#register_model(Boundary_Type)  # Register model for to store information in fullhistory


class Staff_Type(models.Model):

    '''This Class stores information about Staff Type'''

    staff_type = models.CharField(max_length=100)
    category_type = models.IntegerField()

    def __unicode__(self):
        return '%s' % self.staff_type


#register_model(Staff_Type)  # Register model for to store information in fullhistory


class Staff_Qualifications(models.Model):

    ''' This Class Stores Information about staff qualification '''

    qualification = models.CharField(max_length=100)

    def __unicode__(self):
        return '%s' % self.qualification


#register_model(Staff_Qualifications)  # Register model for to store information in fullhistory


class Boundary(models.Model):

    '''This class specifies the longitude and latitute of the area'''

    parent = models.ForeignKey('self', blank=True, null=True)
    name = models.CharField(max_length=300)
    boundary_category = models.ForeignKey(Boundary_Category,
            blank=True, null=True)
    boundary_type = models.ForeignKey(Boundary_Type, blank=True,
            null=True)
    active = models.IntegerField(blank=True, null=True, default=2)

    class Meta:

        """ Used For ordering """

        ordering = ['name']

    def __unicode__(self):
        return '%s' % self.name

    def getChild(self, boundaryType):
        if Boundary.objects.filter(parent__id=self.id, active=2,
                                   boundary_type=boundaryType).count():
            return True
        elif Institution.objects.filter(boundary__id=self.id,
                active=2).count():
            return True
        else:
            return False

    def getModuleName(self):
        return 'boundary'

    def getViewUrl(self, boundaryType):
        return '<a href="/boundary/%s/%s/view/" onclick="return KLP_View(this)" class="KLP_treetxt" title="%s"> <img src="/static_media/tree-images/reicons/boundary.gif" title="Boundary" /> &nbsp; <span id="boundary_%s_text">%s</span> </a>' \
            % (self.id, boundaryType, self.name, self.id, self.name)

    def CreateNewFolder(self, boundaryType):
        return '<span><a href="/boundary/%s/%s/view/" onclick="return KLP_View(this)" class="KLP_treetxt" title="%s"> <img src="/static_media/tree-images/reicons/boundary.gif" title="Boundary" /> &nbsp; <span id="boundary_%s_text">%s</span> </a></span>' \
            % (self.id, boundaryType, self.name, self.id, self.name)

    def get_view_url(self, boundaryType):
        return '/boundary/%s/%s/view/' % (self.id, boundaryType)

    def get_edit_url(self):
        return '/boundary/%s/update/' % self.id

    def get_update_url(self):
        return '/boundary/%d/update/' % self.id

    def getPermissionChild(self, boundaryType):
        if Boundary.objects.filter(parent__id=self.id, active=2,
                                   boundary_type=boundaryType):
            return True
        else:
            return False

    def getPermissionViewUrl(self):
        return '<a href="/boundary/%s/permissions/" onclick="return KLP_View(this)" class="KLP_treetxt" title="%s"> <img src="/static_media/tree-images/reicons/boundary.gif" title="boundary" />  %s </a>' \
            % (self.id, self.name, self.name)

    def getAssessmentPermissionViewUrl(self, assessment_id):
        return '<a href="/boundary/%s/assessmentpermissions/%s/" onclick="return KLP_View(this)" class="KLP_treetxt" title="%s"> <img src="/static_media/tree-images/reicons/boundary.gif" title="boundary" />  %s </a>' \
            % (self.id, assessment_id, self.name, self.name)

    def showPermissionViewUrl(self, userSel):
        if self.boundary_category.id in [9, 10, 13, 14]:
            return '<a href="/show/%s/user/%s/permissions/" onclick="return KLP_View(this)" class="KLP_treetxt" title="%s"> <img src="/static_media/tree-images/reicons/boundary.gif" title="boundary" />  %s </a>' \
                % (self.id, userSel, self.name, self.name)
        else:
            return '<a href="/list/%s/user/%s/permissions/" onclick="return KLP_View(this)" class="KLP_treetxt" title="%s"> <img src="/static_media/tree-images/reicons/boundary.gif" title="boundary" />  %s </a>' \
                % (self.id, userSel, self.name, self.name)


#register_model(Boundary)


class Institution(models.Model):

    ''' It stores the all data regarding Institutions'''

    boundary = models.ForeignKey(Boundary)
    dise_code = models.CharField(max_length=14, blank=True, null=True)
    name = models.CharField(max_length=300)
    cat = models.ForeignKey(Institution_Category, blank=True, null=True)
    institution_gender = models.CharField(max_length=10,
            choices=Institution_Gender, default='co-ed')
    languages = models.ManyToManyField(Moi_Type)
    mgmt = models.ForeignKey(Institution_Management, null=True)
    inst_address = models.ForeignKey(Institution_address, blank=True,
            null=True)
    active = models.IntegerField(blank=True, null=True, default=2)

    class Meta:

        ordering = ['name']

    def __unicode__(self):
        return '%s' % self.name

    def get_all_cat(self, category_type):
        return Institution_Category.objects.all(category_type=category_type)

    def getChild(self):
        if StudentGroup.objects.filter(institution__id=self.id,
                active=2).count():
            return True
        else:
            return False

    def get_all_mgmt(self):
        return institution_Management.objects.all()

    def get_all_languages(self):
        return Moi_Type.objects.all()

    def getModuleName(self):
        return 'institution'

    def get_update_url(self):
        return '/institution/%d/update/' % self.id

    def getViewUrl(self):
        return '<a href="/institution/%s/view/" onclick="return KLP_View(this)" class="KLP_treetxt" title="%s"> <img src="/static_media/tree-images/reicons/institution.gif" title="institution" /> &nbsp; <span id="institution_%s_text">%s</span> </a>' \
            % (self.id, self.name + ' (' + str(self.id) + ')', self.id,
               self.name + ' (' + str(self.id) + ')')

    def get_view_url(self):
        return '/institution/%s/view/' % self.id

    def get_edit_url(self):
        return '/institution/%s/update/' % self.id

    def CreateNewFolder(self):
        retStr = \
            '<span><a href="/institution/%s/view/" onclick="return KLP_View(this)" class="KLP_treetxt" title="%s"> <img src="/static_media/tree-images/reicons/institution.gif" title="institution" /> &nbsp; <span id="institution_%s_text">%s</span></a> </span>' \
            % (self.id, self.name + ' (' + str(self.id) + ')', self.id,
               self.name + ' (' + str(self.id) + ')')
        groupObjects = \
            StudentGroup.objects.filter(institution__id=self.id,
                active=2)
        if groupObjects:
            retStr = \
                "<div class='hitarea hasChildren-hitarea collapsable-hitarea'></div>" \
                + retStr + '<ul>'
            for groupObj in groupObjects:
                groupName = groupObj.name

                if groupName == '0':
                    groupName = 'Anganwadi Class'
                retStr = retStr \
                    + """<li id="%s"><span><a class="KLP_treetxt" onclick="return KLP_View(this)" href="/studentgroup/%s/view/" title="%s"> <img title="Class" src="/static_media/tree-images/reicons/studentgroup_%s.gif"> <span id="studentgroup_%s_text">%s</span>  </a></span></li>""" \
                    % (
                    groupObj.id,
                    groupObj.id,
                    groupName,
                    groupObj.group_type,
                    groupObj.id,
                    groupName,
                    )
            retStr = retStr + '</ul>'
        return retStr

    def getStudentProgrammeUrl(self, filter_id, secfilter_id):
        assname = \
            Assessment.objects.filter(id=secfilter_id).values_list('name'
                , flat=True)[0]
        InstName = self.name

        return '<a href="/studentgroup/%s/programme/%s/assessment/%s/view" onclick="return KLP_View(this)" class="KLP_treetxt" title="%s"> <img src="/static_media/tree-images/reicons/institution.gif" title="%s" /> &nbsp; <span id="institution_%s_text">%s </span> <span style="color:green;font-size:12px">%s</span></a>' \
            % (
            self.id,
            filter_id,
            secfilter_id,
            InstName,
            InstName,
            self.id,
            InstName,
            assname,
            )

    def save(self, *args, **kwargs):
        # custom save method
        #pdb.set_trace()
        from django.db import connection
        connection.features.can_return_id_from_insert = False
        #print "save"

        #print "name is",self.name, "=================== active is", self.active
        self.full_clean()
        super(Institution, self).save(*args, **kwargs)

#register(['Acess'], Institution)  # Register model for Object permissions
#register_model(Institution)  # Register model for to store information in fullhistory

from django.db.models.signals import post_save, pre_save
from schools.receivers import KLP_NewInst_Permission

# Call KLP_NewInst_Permission method on Institution save

post_save.connect(KLP_NewInst_Permission, sender=Institution)


class TaggedItem(models.Model):

    tag = models.SlugField()
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type',
            'object_id')

    def __unicode__(self):
        return self.tag


class Child(models.Model):

    ''' This class stores the personnel information of the childrens'''

    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    uid = models.CharField(max_length=100, blank=True, null=True)
    dob = models.DateField(max_length=20)
    gender = models.CharField(max_length=10, choices=Gender,
                              default='male')
    mt = models.ForeignKey(Moi_Type, null=True)

    class Meta:

        ordering = ['first_name', 'middle_name', 'last_name']
    
    def __unicode__(self):
        return '%s' % self.first_name

    def getRelations(self):
        return Relations.objects.filter(child__id=self.id)

    def getFather(self):
        return Relations.objects.get(relation_type='Father',
                child__id=self.id)

    def getMother(self):
        return Relations.objects.get(relation_type='Mother',
                child__id=self.id)

    def getStudent(self):
        return Student.objects.get(child__id=self.id)

    def get_view_url(self):
        return '/child/%s/view/' % self.id

    def get_update_url(self):
        return '/child/%d/update/' % self.id


    def save(self, *args, **kwargs):
        # custom save method
        #pdb.set_trace()
        from django.db import connection
        connection.features.can_return_id_from_insert = False
        #print "save"

        #print "first name is", self.first_name
        self.full_clean()
        super(Child, self).save(*args, **kwargs)

#register_model(Child)  # Register model for to store information in fullhistory


class Relations(models.Model):

    ''' This class stores relation information of the childrens'''

    relation_type = models.CharField(max_length=10,
            choices=Relation_Type, default='Mother')
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    child = models.ForeignKey(Child)

    def __unicode__(self):
        return '%s' % self.first_name

    def get_view_url(self):
        return ''


#register_model(Relations)  # Register model for to store information in fullhistory


class StudentGroup(models.Model):

    ''' Here it holds the informaion of the class and section of the Institutions'''

    institution = models.ForeignKey(Institution)
    name = models.CharField(max_length=50)
    section = models.CharField(max_length=10, choices=Alpha_list,
                               blank=True, default='')
    active = models.IntegerField(blank=True, null=True, default=2)
    group_type = models.CharField(max_length=10, choices=Group_Type,
                                  default='Class')

    class Meta:

        unique_together = (('institution', 'name', 'section'), )
        ordering = ['name', 'section']

    def __unicode__(self):
        return '%s' % self.name

    def getChild(self):
        return False

    def getSchoolIdentity(self):
        return '%s: %s' % (self.institution__id, self.institution__name)

    def getModuleName(self):
        return 'studentgroup'

    def get_update_url(self):
        return '/studentgroup/%d/update/' % self.id

    def getViewUrl(self):
        sec = self.section
        if sec == None:
            sec = ''
        groupName = self.name
        if groupName == '0':
            groupName = 'Anganwadi Class'
        return '<a href="/studentgroup/%s/view/" onclick="return KLP_View(this)" class="KLP_treetxt" title="%s %s"> <img src="/static_media/tree-images/reicons/studentgroup_%s.gif" title="%s" /> <span id="studentgroup_%s_text">%s %s</span> </a>' \
            % (
            self.id,
            groupName,
            sec,
            self.group_type,
            self.group_type,
            self.id,
            groupName,
            sec,
            )

    def getStudentProgrammeUrl(self, filter_id, secfilter_id):
        assname1 = Assessment.objects.filter(id=secfilter_id)
        assname = assname1.values_list('name', flat=True)[0]
        groupName = self.name
        if groupName == '0':
            groupName = 'Anganwadi Class'
        sec = self.section
        if sec == None:
            sec = ''
        if assname1[0].typ in [2, 3]:
            objid = self.id
            assicon = 'studentgroup_%s' % self.group_type
            displayname = groupName + ' ' + sec
        else:
            objid = self.institution.id
            assicon = 'institution'
            displayname = self.institution.name
        return '<a href="/studentgroup/%s/programme/%s/assessment/%s/view" onclick="return KLP_View(this)" class="KLP_treetxt" title="%s %s"> <img src="/static_media/tree-images/reicons/%s.gif" title="%s" /> &nbsp; <span id="studentgroup_%s_%s_text">%s </span> <span style="color:green;font-size:12px">%s</span></a>' \
            % (
            objid,
            filter_id,
            secfilter_id,
            groupName,
            sec,
            assicon,
            self.group_type,
            secfilter_id,
            objid,
            displayname,
            assname,
            )

    def get_view_url(self):
        return '/studentgroup/%s/view/' % self.id

    def CreateNewFolder(self):
        sec = self.section
        if sec == None:
            sec = ''
        groupName = self.name
        if groupName == '0':
            groupName = 'Anganwadi Class'
        return '<span><a href="/studentgroup/%s/view/" onclick="return KLP_View(this)" class="KLP_treetxt" title="%s %s"> <img src="/static_media/tree-images/reicons/studentgroup_%s.gif" title="%s" /> &nbsp; <span id="studentgroup_%s_text">%s %s</span> </a></span>' \
            % (
            self.id,
            groupName,
            sec,
            self.group_type,
            self.group_type,
            self.id,
            groupName,
            sec,
            )

    def save(self, *args, **kwargs):
        # custom save method
        #pdb.set_trace()
        from django.db import connection
        connection.features.can_return_id_from_insert = False
        #print "save"

        #print "name is",self.name, "=================== active is", self.active
        self.full_clean()
        super(StudentGroup, self).save(*args, **kwargs)

#register_model(StudentGroup)  # Register model for to store information in fullhistory


class Academic_Year(models.Model):

    ''' Its stores the academic years information'''

    name = models.CharField(max_length=20, unique=True)
    active = models.IntegerField(blank=True, null=True, default=0)
    def __unicode__(self):
        return self.name


#register_model(Academic_Year)  # Register model for to store information in fullhistory


def current_academic():
    ''' To select current academic year'''
    try:
        academicObj = Academic_Year.objects.get(active=1)
        return academicObj
    except Academic_Year.DoesNotExist:
        return 1





class Staff(models.Model):

    '''This Class stores the Institution Worker(Staff) Information'''

    institution = models.ForeignKey(Institution, blank=True, null=True)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    uid = models.CharField(max_length=100, blank=True, null=True)
    doj = models.DateField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=Gender,
                              default='female')
    mt = models.ForeignKey(Moi_Type, default='kannada')

    # qualification = models.ForeignKey(Staff_Qualifications,blank=True,null=True, default=1)

    qualification = models.ManyToManyField(Staff_Qualifications,
            blank=True, null=True)
    staff_type = models.ForeignKey(Staff_Type, default=1)
    active = models.IntegerField(blank=True, null=True, default=2)

    class Meta:

        ordering = ['first_name', 'middle_name', 'last_name']

    def __unicode__(self):
        return '%s %s %s' % (self.first_name, self.middle_name,
                             self.last_name)

    def getAssigendClasses(self):
        return StudentGroup.objects.filter(staff_studentgrouprelation__staff__id=self.id,
                staff_studentgrouprelation__active=2)


#register_model(Staff)  # Register model for to store information in fullhistory


class Student(models.Model):

    ''' This class gives information regarding the students class , academic year and personnel details'''

    child = models.ForeignKey(Child)
    other_student_id = models.CharField(max_length=100, blank=True,
            null=True)
    active = models.IntegerField(blank=True, null=True, default=2)

    class Meta:

        ordering = ['child__first_name']

    def GetName(self):
        return self.child.first_name

    def __unicode__(self):
        return '%s' % self.child

    def getChild(self):
        return False

    def get_all_academic_years(self):
        return Academic_Year.objects.all()

    def get_all_languages(self):
        return Moi_Type.objects.all()

    def getModuleName(self):
        return 'student'

    def get_update_url(self):
        return '/student/%d/update/' % self.id

    def getViewUrl(self):
        return '<a href="/student/%s/view/" onclick="return KLP_View(this)" class="KLP_treetxt" title="%s"> %s </a>' \
            % (self.id, self.child, self.child)

    def get_view_url(self):
        return '/student/%s/view/' % self.id

    def CreateNewFolder(self):
        return '<span><img src="/static_media/tree-images/reicons/student.gif" title="student" /> &nbsp;<a href="/boundary/%s/institution/%s/classes/%s/sections/%s/students/%s/view/" onclick="return KLP_View(this)" class="KLP_treetxt"> %s </a><a href="/boundary/%s/institution/%s/classes/%s/sections/%s/students/%s/edit/" onclick="return KLP_View(this)"> <img src="/static_media/images/pagebuilder_edit.gif" title="Edit"/></a><span class="delConf" onclick="deleteSchool(\'%s\', \'student\', \'%s\')"><img width="11" title="Delete" src="/static_media/images/PageRow_delete.gif" title="Delete"></span></span>' \
            % (
            self.class_section.classname.sid.boundary.id,
            self.class_section.classname.sid.id,
            self.class_section.classname.id,
            self.class_section.id,
            self.id,
            self.name,
            self.class_section.classname.sid.boundary.id,
            self.class_section.classname.sid.id,
            self.class_section.classname.id,
            self.class_section.id,
            self.id,
            self.id,
            self.name,
            )


    def save(self, *args, **kwargs):
        # custom save method
        #pdb.set_trace()
        from django.db import connection
        connection.features.can_return_id_from_insert = False
        #print "save"

        #print "active is", self.active
        self.full_clean()
        super(Student, self).save(*args, **kwargs)

#register_model(Student)  # Register model for to store information in fullhistory


class Student_StudentGroupRelation(models.Model):

    '''This Class stores the Student and Student Group Realation Information'''

    student = models.ForeignKey(Student)
    student_group = models.ForeignKey(StudentGroup)
    academic = models.ForeignKey(Academic_Year,
                                 default=current_academic)
    active = models.IntegerField(blank=True, null=True, default=2)

    class Meta:

        unique_together = (('student', 'student_group', 'academic'), )

    def save(self, *args, **kwargs):
        # custom save method
        #pdb.set_trace()
        from django.db import connection
        connection.features.can_return_id_from_insert = False
        #print "save"

        #print "active is", self.active
        self.full_clean()
        super(Student_StudentGroupRelation, self).save(*args, **kwargs)

#register_model(Student_StudentGroupRelation)  # Register model for to store information in fullhistory


class Staff_StudentGroupRelation(models.Model):

    '''This Class stores the Staff and Student Group Realation Information'''

    staff = models.ForeignKey(Staff)
    student_group = models.ForeignKey(StudentGroup)
    academic = models.ForeignKey(Academic_Year,
                                 default=current_academic)
    active = models.IntegerField(blank=True, null=True, default=2)

    class Meta:

        unique_together = (('staff', 'student_group', 'academic'), )


#register_model(Staff_StudentGroupRelation)  # Register model for to store information in fullhistory





#register_model(Programme)  # Register model for to store information in fullhistory




def call(sender, method, instance):
    func = getattr(sender, method, None)
    if callable(func):
        func(instance)

def post_save_hook(sender, **kwargs):
    if kwargs['created']:
        call(sender, 'after_create', kwargs['instance'])
        if kwargs['instance'].boundary_type.id == 2:
            a=Boundary_Category.objects.get(id=13)
            obj = Boundary.objects.get(id=kwargs['instance'].id)
            if obj.parent.id == 1:
                obj.boundary_category = a
                obj.save()
    else:
        call(sender, 'after_update', kwargs['instance'])
    call(sender, 'after_save', kwargs['instance'])

post_save.connect(post_save_hook, sender=Boundary)
# Create your models here.
