# -*- coding:utf-8 -*-
from django import newforms as forms
from models import Class,course,UserProfile

class UserForm(forms.Form):

    loginname = forms.CharField()
    username = forms.CharField()
    password = forms.CharField()
    rule_no = forms.ChoiceField(choices=(('0', '管理员'), 
                                         ('1', '公司领导'), 
                                         ('2', '公司职员'), 
                                         ('3', '岩琦校长'), 
                                         ('4', '教师组长'), 
                                         ('5', '教师')),)
    intro = forms.CharField()
    contact = forms.CharField()
    email = forms.EmailField()
    
    

class CommentForm(forms.Form):
    teach_memo = forms.CharField ( widget=forms.widgets.Textarea() )



class AbsentForm(forms.Form):
    absent_course = forms.ModelChoiceField(queryset=course.objects.all())
    reason = forms.CharField ()
    absentdate = forms.DateField()
    am_or_pm  = forms.ChoiceField (
                                 choices=(('AM', '上午'), 
                                          ('PM', '下午'),
                                          ))

class BlogForm(forms.Form):
    title =  forms.CharField ()
    contents = forms.CharField ( widget=forms.widgets.Textarea() )

class RequestForm(forms.Form):
    
    contents = forms.CharField ( widget=forms.widgets.Textarea() )
    
    
class classForm(forms.Form):

    classname = forms.ModelChoiceField(queryset=Class.objects.all())
    
    
class scheduleForm(forms.Form):
    classname = forms.ModelChoiceField(queryset=Class.objects.all())
    teacher = forms.ModelChoiceField(queryset=UserProfile.objects.filter(rule_no__gt=3))
    
    startdate = forms.DateField (  )
    enddate = forms.DateField (  )
    

    
class schedulesetForm(forms.Form):
    course = forms.ModelChoiceField(queryset=course.objects.all())
    classname = forms.ModelChoiceField(queryset=Class.objects.all())
    teacher = forms.ModelChoiceField(queryset=UserProfile.objects.filter(rule_no__gt=3))
    
    startdate = forms.DateField (  )
    
class scoreForm(forms.Form):
    type = forms.ChoiceField ( choices=(('Test', '测试'), ('Interview', '面试')))
    Description =  forms.CharField ( widget=forms.widgets.Textarea() )
    score = forms.IntegerField()
    
    
