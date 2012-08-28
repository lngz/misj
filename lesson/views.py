# -*- coding:utf-8 -*-
from django.template import Context, loader
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.newforms import form_for_model
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import list_detail ,date_based,create_update
from django.db import connection


import datetime
import HTMLCalendar

from  siteforms import *


from models import UserProfile,schedule,course,student,absent,teacher_blog,teacher_request,costs,scores


#权限decorator
def admin_required(f):
    def wrapper(request, *args, **kwargs):
        user_profile = request.user.get_profile()
        rule_no = user_profile.rule_no
        if rule_no == '0' :
            return f(request, *args, **kwargs)
        else :
            return HttpResponseRedirect('/')
    return wrapper

def company_required(f):
    def wrapper(request, *args, **kwargs):
        user_profile = request.user.get_profile()
        rule_no = user_profile.rule_no
        if rule_no == '1' or rule_no == '2' :
            return f(request, *args, **kwargs)
        else :
            return HttpResponseRedirect('/')
    return wrapper


def iwasaki_required(f):
    def wrapper(request, *args, **kwargs):
        user_profile = request.user.get_profile()
        rule_no = user_profile.rule_no
        if rule_no == '3':
            return f(request, *args, **kwargs)
        else :
            return HttpResponseRedirect('/')
    return wrapper


def teacher_required(f):
    def wrapper(request, *args, **kwargs):
        user_profile = request.user.get_profile()
        rule_no = user_profile.rule_no
        if rule_no == '4' or rule_no == '5':
            return f(request, *args, **kwargs)
        else :
            return HttpResponseRedirect('/')
    return wrapper

def notteacher_required(f):
    def wrapper(request, *args, **kwargs):
        user_profile = request.user.get_profile()
        rule_no = user_profile.rule_no
        if rule_no < '4':
            return f(request, *args, **kwargs)
        else :
            return HttpResponseRedirect('/')
    return wrapper

@login_required
def index(request, lang = 'cn'):

    c = Context({
        
    })

    #user_profile = request.user.get_profile()
    user_profile = request.user.get_profile()
    rule_no = user_profile.rule_no
    if rule_no == '0' or rule_no == '1' or rule_no == '2' :
        return HttpResponseRedirect('/manage')
    elif rule_no == '3':
        return HttpResponseRedirect('/iwasaki')
    elif rule_no == '4' or rule_no == '5':
        return HttpResponseRedirect('/teacher')
    

    '''
    中日文切换的例子
    templatefile = 'index.html'
    if lang.startswith('jp'):
        templatefile = 'jp/' + templatefile
       
    else:
        templatefile = 'cn/' + templatefile
    
    t = loader.get_template(templatefile)
    return HttpResponse(t.render(c))
    '''
    
@login_required
def regist(request):
    
    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():

            loginname = form.clean_data['loginname']
            username = form.clean_data['username']
            password = form.clean_data['password']
            rule_no =  form.clean_data['rule_no']
            intro =  form.clean_data['intro']
            contact =  form.clean_data['contact']
            email =  form.clean_data['email']
            
            userid = User.objects.create_user(username=loginname,email=email,password=password)
            new_usr_profile = UserProfile(user = userid,
                                          loginname =loginname,
                                          username = username ,
                                          password = password ,
                                          rule_no =  rule_no  ,
                                          intro =    intro    ,
                                          contact =  contact  ,
                                          email =    email    ,
                                          )
            new_usr_profile.save()
            
            return HttpResponseRedirect('/')
    else:
        form = UserForm()
    
    return render_to_response('register.html',{'form':form})

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")

def black(request) :
    return HttpResponse("空白")
    

@login_required
def lessonlist(request) :      #当前教师课程表列表

    user_profile = request.user.get_profile()

    user_profile.Class
    sch_list = schedule.objects.filter(teacher=request.user)
    caldict = {}
    for sch in sch_list :
        if not caldict.has_key(sch.Teach_time.year):
          #  print sch.Teach_time.year
            caldict[sch.Teach_time.year] = {}
        if not caldict[sch.Teach_time.year].has_key(sch.Teach_time.month):
            caldict[sch.Teach_time.year][sch.Teach_time.month] = {}
        caldict[sch.Teach_time.year][sch.Teach_time.month][sch.Teach_time.day] = 'comment/'+str(sch.id) + '/edit'

       # print caldict
    
    cal = HTMLCalendar.MonthCal()
    caltext = ''
    for y in caldict.keys():
        for m in caldict[y]:
            caltext = caltext + cal.render(y,m,caldict[y][m]) 


    c = Context({
        'classname':user_profile.Class,
        'schedule' :sch_list,
        'caltext'  :caltext,
    })
    templatefile = 'lessonlist.html'
    t = loader.get_template(templatefile)
    return HttpResponse(t.render(c))    

@login_required
def lessoncomment(request, course_id) :
    
    if request.method == 'POST':
        
        form = CommentForm(request.POST)
        if form.is_valid():

            #Teach_content =  form.clean_data['id_Teach_content']
            teach_memo =  form.clean_data['teach_memo']
        
            user = request.user
            teach_date=datetime.datetime.now()
            user_profile = request.user.get_profile()
            
            new_schedule = schedule( Teach_content = course.objects.get(id=course_id),
                                 Teach_time    = teach_date,
                                 teacher       = user ,
                                 Class         = user_profile.Class,
                                 teach_memo    = teach_memo
                               )
            new_schedule.save()
        
         
            return HttpResponseRedirect('../..')
    else:
        
        form = CommentForm()
    return render_to_response('add_schedule.html', {'form': form,
                                                    'course': course.objects.get(id=course_id),
                                                    })

    
    
@login_required  
def commentedit(request, course_id) :
    #thecourse = course.objects.get(id=course_id),
    
    if request.method == 'POST':
        
        form = CommentForm(request.POST)
        if form.is_valid():

            #Teach_content =  form.clean_data['id_Teach_content']
            teach_memo =  form.clean_data['teach_memo']
        
            user = request.user
            teach_date=datetime.datetime.now()

            theschedule = schedule.objects.get(id=course_id)
            theschedule.teach_memo = teach_memo
            theschedule.save()
        
         
            return HttpResponseRedirect('../../..')
    else:
        theschedule=schedule.objects.get(id=course_id)
        data = {'teach_memo':theschedule.teach_memo}

        form = CommentForm(data)
    return render_to_response('add_schedule.html', {'form': form,
                                                    'course': schedule.objects.get(id=course_id),
                                                    })
@login_required
def studentlist(request):
    user_profile = request.user.get_profile()
    c = user_profile.Class
    stu = student.objects.filter(classname=c)
    

    c = Context({
        'stu' :stu
    })
    templatefile = 'studentlist.html'
    t = loader.get_template(templatefile)
    return HttpResponse(t.render(c))    
    
@login_required
def studentabsentlist(request,stu_id) :

    stu = student.objects.get(id=stu_id)
    scorelist = scores.objects.filter(student=stu_id)
    absentlist = absent.objects.filter(student=stu_id)

    c = Context({
        'stu' :stu,
        'scorelist' : scorelist,
        'absentlist':absentlist,
        
    })
    templatefile = 'studentabsentlist.html'
    t = loader.get_template(templatefile)
    return HttpResponse(t.render(c))    
    
    



@login_required
def studentabsent(request,stu_id) :
    
    if request.method == 'POST':
        form = AbsentForm(request.POST)
        if form.is_valid():
            absent_course =  form.clean_data['absent_course']
            reason =  form.clean_data['reason']
            absentdate =  form.clean_data['absentdate']
            am_or_pm =  form.clean_data['am_or_pm']
            new_absent = absent( student=student.objects.get(id=stu_id),
                                 absent_course=absent_course,
                                 absentdate=absentdate,
                                 reason=reason,                      
                                 am_or_pm=am_or_pm,
                                 )
            new_absent.save()        
                     
            
            return HttpResponseRedirect('../..')
    else:
        form = AbsentForm()
    return render_to_response('studentabsent.html', {'form': form})



def studentscore(request,stu_id) :
    
  
    if request.method == 'POST':
        form = scoreForm(request.POST)
        if form.is_valid():
            type =  form.clean_data['type']
            Description =  form.clean_data['Description']
            score =  form.clean_data['score']
           
            new_scores = scores( student=student.objects.get(id=stu_id),
                                 type = type,
                                 Description = Description,
                                 score = score,
                                 )
            new_scores.save()        
                     
            
            return HttpResponseRedirect('../..')
    else:
        form = scoreForm()
    return render_to_response('studentscore.html', {'form': form})



def studentcomment(request,stu_id) :
    
    pass

#向公司发送需求
@login_required
def requestlist(request):

    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            contents =  form.clean_data['contents']
            new_request = teacher_request( teacher=request.user,
                                     contents = contents,
                                     time = datetime.datetime.now(),
                                     )
            new_request.save()        
         
         
    
    requestlist = teacher_request.objects.filter(teacher=request.user)
    form = RequestForm()
    return render_to_response('teacher_request.html', {'form': form,
                                                    'requestlist' : requestlist,
                                                    })



@iwasaki_required
@login_required
def iwasaki_list(request) :

    teachers = UserProfile.objects.filter(rule_no__gt=3)
 
    c = Context({
        'teacherlist': teachers,
    })
    templatefile = 'teacherlist.html'
    t = loader.get_template(templatefile)
    return HttpResponse(t.render(c))    
    

@notteacher_required
@login_required    
def iwasaki_teach(request,teacher_id):
    
    u = User.objects.get(id=teacher_id)
    user_profile = u.get_profile()

    user_profile.Class
    sch_list = schedule.objects.filter(teacher=teacher_id)
    caldict = {}
    for sch in sch_list :
        if not caldict.has_key(sch.Teach_time.year):
          #  print sch.Teach_time.year
            caldict[sch.Teach_time.year] = {}
        if not caldict[sch.Teach_time.year].has_key(sch.Teach_time.month):
            caldict[sch.Teach_time.year][sch.Teach_time.month] = {}
        caldict[sch.Teach_time.year][sch.Teach_time.month][sch.Teach_time.day] = '/schedule/edit/'+str(sch.id) 

       # print caldict
    
    cal = HTMLCalendar.MonthCal()
    caltext = ''
    for y in caldict.keys():
        for m in caldict[y]:
            caltext = caltext + cal.render(y,m,caldict[y][m]) 


    c = Context({
        'user_profile':user_profile.Class,
        'schedule' :sch_list,
        'caltext' : caltext
    })
    templatefile = 'iwasakilookteacher.html'
    t = loader.get_template(templatefile)
    return HttpResponse(t.render(c))    

@iwasaki_required
@login_required
def iwasaki_comment(request,schedule_id):
    #thecourse = course.objects.get(id=course_id),
    
    if request.method == 'POST':
        
        form = CommentForm(request.POST)
        
        if form.is_valid():

            #Teach_content =  form.clean_data['id_Teach_content']
            iwasaki_memo =  form.clean_data['teach_memo']
            theschedule = schedule.objects.get(id=schedule_id)
            theschedule.iwasaki_memo = iwasaki_memo
            theschedule.save()
        
         
            return HttpResponseRedirect('../..')
            
    else:
        theschedule = schedule.objects.get(id=schedule_id)
        data = {'teach_memo':theschedule.iwasaki_memo}

        form = CommentForm(data)
    return render_to_response('iwasaki_comment.html', {'form': form,
                                                       'schedule': theschedule,
                                                       'username' :'岩琦老师'
                                                    })


@login_required
def blog(request) :
    if request.method == 'POST':
       
        form = BlogForm(request.POST)
        
        if form.is_valid():

            #Teach_content =  form.clean_data['id_Teach_content']
            title =  form.clean_data['title']
            contents =  form.clean_data['contents']
            new_blog = teacher_blog( teacher=request.user,
                                     title = title,
                                     contents = contents,
                                     time = datetime.datetime.now(),
                                     )
            new_blog.save()        
         
         
    
    bloglist = teacher_blog.objects.all()
    form = BlogForm()
    return render_to_response('teacher_blog.html', {'form': form,
                                                    'bloglist' : bloglist,
                                                    })

@login_required
def blog_detail(request,blog_id) :
    user_profile = request.user.get_profile()
    username = user_profile.username
    url = request.get_full_path()
    blog = teacher_blog.objects.get(id = blog_id)
    
    return render_to_response('teacher_blog_detail.html', {
                                                    'blog' : blog,
                                                    'username' : username,
                                                    'url' :url,
                                                    })
@admin_required
@login_required
def manageindex(request):

    requestlist = teacher_request.objects.all()    
    return render_to_response('manageindex.html', { 'requestlist' : requestlist,
                                                    })
@notteacher_required
@login_required
def managereply(request,object_id):

    teacher_req = teacher_request.objects.get(id=object_id)    
    return render_to_response('managereply.html', {
                                                    'teacher_req' : teacher_req,
                                                    'username' : '公司',
                                                    })


@teacher_required
@login_required
def teacherindex(request):
    c = Context({
    })
    templatefile = 'teacherindex.html'
    t = loader.get_template(templatefile)
    return HttpResponse(t.render(c))  

@notteacher_required
@login_required
def teacher_assign(request,object_id):
    if request.method == 'POST':
        
        form = classForm(request.POST)
        
        if form.is_valid():

            #Teach_content =  form.clean_data['id_Teach_content']
            classname =  form.clean_data['classname']
            #print classname
            theteacher = UserProfile.objects.get(id=object_id)
            theteacher.Class = classname
            theteacher.save()
        
         
            return HttpResponseRedirect('../..')
            
    else:
        theteacher = UserProfile.objects.get(id=object_id)
        form = classForm()
    return render_to_response('teacher_assign.html', {'form': form,
                                                      'teacher' :theteacher
                             })
@notteacher_required
@login_required
def scheduleassign(request):
    if request.method == 'POST':
        
        form = scheduleForm(request.POST)
        
        if form.is_valid():

            classname =  form.clean_data['classname']
            startdate =  form.clean_data['startdate']
            enddate =  form.clean_data['enddate']
            teacher =  form.clean_data['teacher']

            thecourse = course.objects.all().order_by('course_no')
            #print thecourse
            for acourse in thecourse :
                #print acourse
                if startdate > enddate :
                    break
                
                #周末不排课
                while startdate.weekday() >= 5 :
                    startdate =  startdate + datetime.timedelta(1)
                new_schedule = schedule( Teach_content = acourse,
                                 Teach_time    = startdate,
                                 teacher       = teacher.user ,
                                 Class         = classname,
                               )
                new_schedule.save()
                startdate =  startdate + datetime.timedelta(1)
         
            return HttpResponseRedirect('..')
            
    else:
        
        form = scheduleForm()
    return render_to_response('schedule.html', {'form': form,
                                                })
@notteacher_required
@login_required
def scheduleset(request):
    if request.method == 'POST':
        
        form = schedulesetForm(request.POST)
        
        if form.is_valid():
            courseid = form.clean_data['course']
            classname =  form.clean_data['classname']
            startdate =  form.clean_data['startdate']
            teacher =  form.clean_data['teacher']


            new_schedule = schedule( Teach_content = courseid,
                                 Teach_time    = startdate,
                                 teacher       = teacher.user ,
                                 Class         = classname,
                               )
            new_schedule.save()

         
            return HttpResponseRedirect('..')
            
    else:
        
        form = schedulesetForm()
    return render_to_response('scheduleset.html', {'form': form,
                                                })
    
@notteacher_required
@login_required
def schedulelist(request) :
    
    
    
    return render_to_response('schedulelist.html', {  'schedules' :schedule.objects.all(),

                             })
    

@notteacher_required
@login_required
def schedulelistbyteacher(request,teacher_id) :

    sch_list = schedule.objects.filter(teacher=teacher_id)
    caldict = {}
    for sch in sch_list :
        if not caldict.has_key(sch.Teach_time.year):
           # print sch.Teach_time.year
            caldict[sch.Teach_time.year] = {}
        if not caldict[sch.Teach_time.year].has_key(sch.Teach_time.month):
            caldict[sch.Teach_time.year][sch.Teach_time.month] = {}
        caldict[sch.Teach_time.year][sch.Teach_time.month][sch.Teach_time.day] = '/schedule/edit/'+str(sch.id) 

       # print caldict
    
    cal = HTMLCalendar.MonthCal()
    caltext = ''
    for y in caldict.keys():
        for m in caldict[y]:
            caltext = caltext + cal.render(y,m,caldict[y][m]) 


    
    
    return render_to_response('schedulelistbyteacher.html', 
                              {  'schedules' :sch_list,
                                 'caltext' : caltext,
                                 })
                             

@notteacher_required
@login_required
def scheduleedit(request,schedule_id) :
    
    return create_update.update_object(
        request,
        object_id = schedule_id,
        model = schedule ,
        post_save_redirect = "../..",
        template_name = "scheduleedit.html",
    )
@notteacher_required
@login_required
def scheduledelete(request,schedule_id) :
    schedule.objects.get(id=schedule_id).delete()
    return HttpResponseRedirect('../..')
    
    
@notteacher_required 
@login_required
def costlist(request) :
    
    stu_list = student.objects.all()
    
    
    cursor = connection.cursor()
    cursor.execute(""" SELECT sum(amount)  FROM lesson_costs """)

    costall =  cursor.fetchone()[0]
    
    cursor.execute(""" SELECT sum(Servicecharges)  FROM lesson_student """)

    Servicecharges =  cursor.fetchone()[0]
    
    
    cursor.execute(""" SELECT sum(trainingcharge)  FROM lesson_student """)

    trainingcharge =  cursor.fetchone()[0]
    
    
      
    cursor.execute(""" SELECT sum(Margin)  FROM lesson_student """)

    Margin =  cursor.fetchone()[0]
  
    return render_to_response('costlist.html', 
                              {  'stu_list':stu_list,
                                 'costall' : costall,
                                 'Servicecharges':Servicecharges,
                                 'trainingcharge' :trainingcharge,
                                 'Margin': Margin,
                                 })
                             
        
@notteacher_required 
@login_required
def classstudent(request,class_id) :
    
    stu_list = student.objects.filter(classname=class_id)
    
    
  
    return render_to_response('classstudent.html', 
                              {  'stu_list':stu_list,
                                 
                                 })
