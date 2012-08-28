# -*- coding:utf-8 -*-
from django.conf.urls.defaults import *

from django.views.generic import list_detail ,date_based,create_update
from django.views.generic.simple import redirect_to
from lesson.models import UserProfile, costs, student,Class,course
from django.conf import settings
from django.contrib.auth.models import User



urlpatterns = patterns('',
    # Example:
    # (r'^misj/', include('misj.foo.urls')),

    # Uncomment this for admin:
    (r'^admin/', include('django.contrib.admin.urls')),
    (r'^images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'F:/apache/htdocs/media'}),
    (r'^$',                 'misj.lesson.views.index',{'lang': 'cn'}),
    (r'^(?P<lang>\w{2})/$', 'misj.lesson.views.index'),

     #登陆
    (r'^accounts/login/$',  'django.contrib.auth.views.login',{'template_name': 'login.html'}),    
    (r'^accounts/logout/$', 'misj.lesson.views.logout'),    
    (r'^accounts/profile/$', redirect_to, {'url' : '/'}),    
    
    #教师
    (r'^teacher/$',          'misj.lesson.views.teacherindex'),    
    (r'^teacher/lesson/$',  'misj.lesson.views.lessonlist'),      #当前教师课程表列表
    (r'^teacher/lesson/comment/(?P<course_id>\d+)/$',  'misj.lesson.views.lessoncomment'),       #当天课程评价
    (r'^teacher/lesson/comment/(?P<course_id>\d+)/edit/$',  'misj.lesson.views.commentedit'),              #当天课程评价
    (r'^teacher/student/$',  'misj.lesson.views.studentlist'),                     #学生列表
    (r'^teacher/student/(?P<stu_id>\d+)/$',  'misj.lesson.views.studentabsentlist'),                     #学生列表
    (r'^teacher/student/absent/(?P<stu_id>\d+)/$',  'misj.lesson.views.studentabsent'),              #学生缺勤
    (r'^teacher/student/(?P<stu_id>\d+)/comment/$', 'misj.lesson.views.studentcomment'),     #添加学生评价 
    (r'^teacher/student/(?P<stu_id>\d+)/score/$',  'misj.lesson.views.studentscore'),                     #学生列表

    (r'^teacher/company/$',    'misj.lesson.views.requestlist'),             #公司发送需求报告列表
    (r'^teacher/blog/$',    'misj.lesson.views.blog'),
    (r'^teacher/blog/(?P<blog_id>\d+)/$',    'misj.lesson.views.blog_detail'),
    
    #岩琦
    (r'^iwasaki/$', 'misj.lesson.views.iwasaki_list'),       #列出最近老师的当前教学进度和教学报告。
    
    (r'^iwasaki/(?P<teacher_id>\d+)/$', 'misj.lesson.views.iwasaki_teach'), 
    (r'^iwasaki/comment/(?P<schedule_id>\d+)/$', 'misj.lesson.views.iwasaki_comment'), #回复教师的报告
    (r'^iwasaki/lesson/$', list_detail.object_list,{"queryset": course.objects.all(),'allow_empty':True}),
    (r'^iwasaki/lesson/add/$',  create_update.create_object,{'model' : course,
                                                           'post_save_redirect':'..'}), 
    (r'^iwasaki/lesson/edit/(?P<object_id>\d+)/$', create_update.update_object, {'model':course ,
                                                                                 'post_save_redirect':'../..'}  ),
    (r'^iwasaki/lesson/delete/(?P<object_id>\d+)/$', create_update.delete_object, {'model':course ,
                                                                                 'post_delete_redirect':'../..'}  ),

    #管理
    #教师管理
    (r'^manage/$',           'misj.lesson.views.manageindex'),  #各个链接，及老师的需求
    (r'^manage/reply/(?P<object_id>\d+)/$',     'misj.lesson.views.managereply'),  #各个链接，及老师的需求
    (r'^manage/teacher/$',   list_detail.object_list,{"queryset": UserProfile.objects.filter(rule_no__gt=3),'allow_empty':True}), 
    (r'^manage/teacher/edit/(?P<object_id>\d+)/$', create_update.update_object, {'model':UserProfile ,
                                                                                 'post_save_redirect':'../..'}  ),
    (r'^manage/teacher/assign/(?P<object_id>\d+)/$',   'misj.lesson.views.teacher_assign'), 

    (r'^manage/teacher/(?P<teacher_id>\d+)/$',  'misj.lesson.views.iwasaki_teach'),
    
    (r'^manage/teacher/regist/$', 'misj.lesson.views.regist'),
    #班级管理
    (r'^manage/class/$',   list_detail.object_list, {"queryset" :   Class.objects.all(),'allow_empty':True}), 
    (r'^manage/class/add/$',  create_update.create_object,{'model' : Class,
                                                           'post_save_redirect':'..'}), 
    (r'^manage/class/(?P<class_id>\d+)/$',   'misj.lesson.views.classstudent'),
    (r'^manage/class/edit/(?P<object_id>\d+)/$', create_update.update_object, {'model':Class ,
                                                                               'post_save_redirect':'../..'}  ),
    (r'^manage/class/delete/(?P<object_id>\d+)/$', create_update.delete_object, {'model':Class ,
                                                                                 'post_delete_redirect':'../..'}  ),
    
    #学生管理
    (r'^manage/student/$',   list_detail.object_list, {"queryset" :   student.objects.all(),'allow_empty':True}), 
    (r'^manage/student/(?P<stu_id>\d+)/$',  'misj.lesson.views.studentabsentlist'),  
    (r'^manage/student/(?P<stu_id>\d+)/score/$',  'misj.lesson.views.studentscore'),                     #学生列表

    (r'^manage/student/add/$',  create_update.create_object,{'model' : student,
                                                             'post_save_redirect':'..'}), 
    (r'^manage/student/edit/(?P<object_id>\d+)/$', create_update.update_object, {'model':student ,
                                                                                  'post_save_redirect':'../..'}  ),
    (r'^manage/student/delete/(?P<object_id>\d+)/$', create_update.delete_object, {'model':student ,
                                                                                   'post_delete_redirect':'../..'}  ),
    #成本管理
    (r'^manage/costs/$',     list_detail.object_list, {"queryset" :   costs.objects.all(),'allow_empty':True}), 
    (r'^manage/costs/add/$',  create_update.create_object,{'model' : costs,
                                                           'post_save_redirect':'..'}), 
    (r'^manage/costs/edit/(?P<object_id>\d+)/$', create_update.update_object, {'model':costs ,
                                                                               'post_save_redirect':'../..'}  ),
    (r'^manage/costs/delete/(?P<object_id>\d+)/$', create_update.delete_object, {'model':costs ,
                                                                                 'post_delete_redirect':'../..'}  ),

    (r'^manage/costs/all/$', 'misj.lesson.views.costlist'),

    
    (r'^comments/',include('django.contrib.comments.urls.comments')),

    #计划表
    
    (r'^schedule/$', 'misj.lesson.views.schedulelist'),    
    (r'^schedule/assign/$', 'misj.lesson.views.scheduleassign'),
    (r'^schedule/(?P<teacher_id>\d+)/$', 'misj.lesson.views.schedulelistbyteacher'),
    (r'^schedule/set/$', 'misj.lesson.views.scheduleset'),
    (r'^schedule/edit/(?P<schedule_id>\d+)/$', 'misj.lesson.views.scheduleedit'),
    (r'^schedule/delete/(?P<schedule_id>\d+)/$', 'misj.lesson.views.scheduledelete'),
    
)








