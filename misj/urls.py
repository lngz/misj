# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

from django.views.generic import list_detail ,date_based,create_update
from django.views.generic.simple import redirect_to
from lesson.models import UserProfile, costs, student,Class,course
from django.conf import settings
from django.contrib.auth.models import User



# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'misj.views.home', name='home'),
    # url(r'^misj/', include('misj.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Uncomment this for admin:

    (r'^images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'F:/apache/htdocs/media'}),
    url(r'^$',                 'lesson.views.index',{'lang': 'cn'}),
    #url(r'^$',                 'lesson.views.test'),

    url(r'^(?P<lang>\w{2})/$', 'lesson.views.index'),

     #登陆
    url(r'^accounts/login/$',  'django.contrib.auth.views.login',{'template_name': 'login.html'}),    
    url(r'^accounts/logout/$', 'lesson.views.logout'),    
    url(r'^accounts/profile/$', redirect_to, {'url' : '/'}),    
    
    #教师
    url(r'^teacher/$',          'lesson.views.teacherindex'),    
    url(r'^teacher/lesson/$',  'lesson.views.lessonlist'),      #当前教师课程表列表
    url(r'^teacher/lesson/comment/(?P<course_id>\d+)/$',  'lesson.views.lessoncomment'),       #当天课程评价
    url(r'^teacher/lesson/comment/(?P<course_id>\d+)/edit/$',  'lesson.views.commentedit'),              #当天课程评价
    url(r'^teacher/student/$',  'lesson.views.studentlist'),                     #学生列表
    url(r'^teacher/student/(?P<stu_id>\d+)/$',  'lesson.views.studentabsentlist'),                     #学生列表
    url(r'^teacher/student/absent/(?P<stu_id>\d+)/$',  'lesson.views.studentabsent'),              #学生缺勤
    url(r'^teacher/student/(?P<stu_id>\d+)/comment/$', 'lesson.views.studentcomment'),     #添加学生评价 
    url(r'^teacher/student/(?P<stu_id>\d+)/score/$',  'lesson.views.studentscore'),                     #学生列表

    url(r'^teacher/company/$',    'lesson.views.requestlist'),             #公司发送需求报告列表
    url(r'^teacher/blog/$',    'lesson.views.blog'),
    url(r'^teacher/blog/(?P<blog_id>\d+)/$',    'lesson.views.blog_detail'),
    
    #岩琦
    url(r'^iwasaki/$', 'lesson.views.iwasaki_list'),       #列出最近老师的当前教学进度和教学报告。
    
    url(r'^iwasaki/(?P<teacher_id>\d+)/$', 'lesson.views.iwasaki_teach'), 
    url(r'^iwasaki/comment/(?P<schedule_id>\d+)/$', 'lesson.views.iwasaki_comment'), #回复教师的报告
    url(r'^iwasaki/lesson/$', list_detail.object_list,{"queryset": course.objects.all(),'allow_empty':True}),
    url(r'^iwasaki/lesson/add/$',  create_update.create_object,{'model' : course,
                                                           'post_save_redirect':'..'}), 
    url(r'^iwasaki/lesson/edit/(?P<object_id>\d+)/$', create_update.update_object, {'model':course ,
                                                                                 'post_save_redirect':'../..'}  ),
    url(r'^iwasaki/lesson/delete/(?P<object_id>\d+)/$', create_update.delete_object, {'model':course ,
                                                                                 'post_delete_redirect':'../..'}  ),

    #管理
    #教师管理
    url(r'^manage/$',           'lesson.views.manageindex'),  #各个链接，及老师的需求
    url(r'^manage/reply/(?P<object_id>\d+)/$',     'lesson.views.managereply'),  #各个链接，及老师的需求
    url(r'^manage/teacher/$',   list_detail.object_list,{"queryset": UserProfile.objects.filter(rule_no__gt=3),'allow_empty':True}), 
    url(r'^manage/teacher/edit/(?P<object_id>\d+)/$', create_update.update_object, {'model':UserProfile ,
                                                                                 'post_save_redirect':'../..'}  ),
    url(r'^manage/teacher/assign/(?P<object_id>\d+)/$',   'lesson.views.teacher_assign'), 

    url(r'^manage/teacher/(?P<teacher_id>\d+)/$',  'lesson.views.iwasaki_teach'),
    
    url(r'^manage/teacher/regist/$', 'lesson.views.regist'),
    #班级管理
    url(r'^manage/class/$',   list_detail.object_list, {"queryset" :   Class.objects.all(),'allow_empty':True}), 
    url(r'^manage/class/add/$',  create_update.create_object,{'model' : Class,
                                                           'post_save_redirect':'..'}), 
    url(r'^manage/class/(?P<class_id>\d+)/$',   'lesson.views.classstudent'),
    url(r'^manage/class/edit/(?P<object_id>\d+)/$', create_update.update_object, {'model':Class ,
                                                                               'post_save_redirect':'../..'}  ),
    url(r'^manage/class/delete/(?P<object_id>\d+)/$', create_update.delete_object, {'model':Class ,
                                                                                 'post_delete_redirect':'../..'}  ),
    
    #学生管理
    url(r'^manage/student/$',   list_detail.object_list, {"queryset" :   student.objects.all(),'allow_empty':True}), 
    url(r'^manage/student/(?P<stu_id>\d+)/$',  'lesson.views.studentabsentlist'),  
    url(r'^manage/student/(?P<stu_id>\d+)/score/$',  'lesson.views.studentscore'),                     #学生列表

    url(r'^manage/student/add/$',  create_update.create_object,{'model' : student,
                                                             'post_save_redirect':'..'}), 
    url(r'^manage/student/edit/(?P<object_id>\d+)/$', create_update.update_object, {'model':student ,
                                                                                  'post_save_redirect':'../..'}  ),
    url(r'^manage/student/delete/(?P<object_id>\d+)/$', create_update.delete_object, {'model':student ,
                                                                                   'post_delete_redirect':'../..'}  ),
    #成本管理
    url(r'^manage/costs/$',     list_detail.object_list, {"queryset" :   costs.objects.all(),'allow_empty':True}), 
    url(r'^manage/costs/add/$',  create_update.create_object,{'model' : costs,
                                                           'post_save_redirect':'..'}), 
    url(r'^manage/costs/edit/(?P<object_id>\d+)/$', create_update.update_object, {'model':costs ,
                                                                               'post_save_redirect':'../..'}  ),
    url(r'^manage/costs/delete/(?P<object_id>\d+)/$', create_update.delete_object, {'model':costs ,
                                                                                 'post_delete_redirect':'../..'}  ),

    url(r'^manage/costs/all/$', 'lesson.views.costlist'),

    
   (r'^comments/',include('django.contrib.comments.urls')),

    #计划表
    
    url(r'^schedule/$', 'lesson.views.schedulelist'),    
    url(r'^schedule/assign/$', 'lesson.views.scheduleassign'),
    url(r'^schedule/(?P<teacher_id>\d+)/$', 'lesson.views.schedulelistbyteacher'),
    url(r'^schedule/set/$', 'lesson.views.scheduleset'),
    url(r'^schedule/edit/(?P<schedule_id>\d+)/$', 'lesson.views.scheduleedit'),
    url(r'^schedule/delete/(?P<schedule_id>\d+)/$', 'lesson.views.scheduledelete'),
 
)
