# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import User

# 班级
class Class(models.Model):
    classname = models.CharField('班级名称',max_length=255)
    description  = models.TextField('课程内容',blank=True)
    student_amount = models.IntegerField('学员数量')
    teach_time = models.CharField('课时总数',max_length=255)
    class_place = models.CharField('班级地点',max_length=20)
    begin_time = models.CharField('开课时间',max_length=255)
    end_time = models.CharField('结课时间',max_length=255)
    operator_company = models.CharField('合作方',max_length=255)
    operator_name = models.CharField('合作方联系人',max_length=255)
    operator_contact = models.CharField('合作方联系方式',max_length=255)
    communicater = models.CharField('管理对接人',max_length=255)

    class Admin:
        pass

    def __str__(self):
        return self.classname
    
    def __unicode__(self):
        return self.classname
    

# 教师类
class UserProfile(models.Model):
    user = models.ForeignKey(User,unique=True)
    loginname = models.CharField('登陆名',max_length=20)
    username = models.CharField('用户姓名',max_length=20)
    password = models.CharField('用户登陆密码',max_length=20)
    rule_no = models.CharField('角色',\
                            choices=(('0', '管理员'), 
                                     ('1', '公司领导'), 
                                     ('2', '公司职员'), 
                                     ('3', '岩琦校长'), 
                                     ('4', '教师组长'), 
                                     ('5', '教师')),
                            max_length=1,blank=False)
    intro = models.TextField('用户简介',blank=True)
    Class = models.ForeignKey(Class,blank=True,null=True)
    contact = models.CharField('用户联系方式',max_length=50)
    email = models.EmailField('用户email')
    
    class Admin:
        pass

    def __str__(self):
        return self.username
    
    def __unicode__(self):
        return self.username
    

# 学员类
class student(models.Model):
    name = models.CharField('学员姓名',max_length=255)
    age = models.IntegerField('年龄')
    colledge = models.CharField('学员毕业学校',max_length=255)
    majar = models.CharField('专业',max_length=255)
    hometown = models.CharField('籍贯',max_length=255)
    cellphone = models.CharField('联系电话(手机)',max_length=255)
    sitephone = models.CharField('联系电话(固定)',max_length=255)
    email = models.EmailField('学员email')
    classname  = models.ForeignKey(Class)
    inro = models.TextField('学员简介',blank=True)                        
    jp_level = models.CharField('角色',\
                            choices=(('1', '一级'), 
                                     ('2', '二级'), 
                                     ('3', '三级'),
                                     ('4', '四级'),
                                     ('5', '无日语基础')),
                            max_length=1, blank=False)
    Servicecharges  = models.IntegerField('服务费总额',)#服务费
    trainingcharge  = models.IntegerField('培训费',)#培训费
    Margin  = models.IntegerField('保证金总额')#保证金
    amount1 = models.IntegerField('交款1金额')#交款项目1
    item1 = models.CharField('交款1项目',max_length=255)
    Receipts1 = models.CharField('交款1收据',max_length=255)
    recepter1 = models.CharField('交款1收款人',max_length=255)
    amount2 = models.IntegerField('交款2金额')#交款项目2
    item2  = models.CharField('交款2项目',max_length=255)
    Receipts2 = models.CharField('交款2收据',max_length=255)
    recepter2 = models.CharField('交款2收款人',max_length=255)



    class Admin:
        pass

    def __str__(self):
        return self.name
    
    def __unicode__(self):
        return self.name

    
# 学员成绩

class scores(models.Model) :
    student  = models.ForeignKey(student)
    type = models.CharField('测试类型',\
                            choices=(('Test', '测试'), ('Interview', '面试')),
                            max_length=8, blank=False)
    Description = models.TextField('测试内容说明',blank=True)
    score = models.IntegerField('成绩')

    class Admin:
        pass


    
# 课程
class course(models.Model):
    courcename = models.TextField('课程内容')
    course_no = models.IntegerField("课程序号",max_length=8)
    course_type = models.CharField('课程类型',\
                            choices=(('Welcome Program', 'Welcome Program'), 
                                     ('Level I', 'Level I'),
                                     ('Level II', 'Level II'),
                                     ('Level III', 'Level III'),
                                     ('Level IV', 'Level IV'),
                                     ), max_length=20,
                             blank=False)
    #cource_time  = models.IntegerField("课程所需时间")
    

    class Admin:
        pass
    def __str__(self):
        return self.courcename
    
    def __unicode__(self):
        return self.courcename

    
# 日程表
class schedule(models.Model):
    Teach_content  = models.ForeignKey(course)
    Teach_time = models.DateField('授课时间',)
    teacher = models.ForeignKey(User)
    Class = models.ForeignKey(Class)
    teach_memo = models.TextField('授课备注',max_length=2000 ,blank=True,null=True )
    iwasaki_memo = models.TextField('岩琦老师备注',max_length=2000 ,blank=True,null=True )

    class Admin:
        pass
    def __str__(self):
        return '%s %s' % (self.teacher, self.Teach_content)

    
    def __unicode__(self):
        return '%s %s' % (self.teacher, self.Teach_content)


    
    

# 缺勤情况
class absent(models.Model):
    student = models.ForeignKey(student)
    absent_course = models.ForeignKey(course)   
    reason = models.CharField('缺勤原因',max_length=255)
    absentdate = models.DateField()
    am_or_pm  = models.CharField('缺勤上下午',
                                 choices=(('AM', '上午'), 
                                          ('PM', '下午'),
                                          ),
                                 max_length=255)

    class Admin:
        pass

# 知识点
class knowledge(models.Model):
    knowledge_point  = models.CharField('知识点',max_length=255)
    knowledge_content = models.TextField('授课内容',max_length=255)
    plan_schedule = models.CharField('计划日程',max_length=255)
    actual_program = models.CharField('实际日程',max_length=255)

    class Admin:
        pass

#学生掌握程度
    
class masterdegree(models.Model):
    knowledge_point = models.CharField('知识点',max_length=255)
    student = models.CharField('学员',max_length=255)
    marks = models.CharField('评分',max_length=255)
    memo = models.TextField('备注',max_length=255)                           
                                         
    class Admin:                         
        pass                             


    
# 成本
class costs(models.Model):
    item = models.CharField('名目',max_length=255)
    detail= models.CharField('明细',max_length=255)
    amount = models.FloatField('数额')
    time = models.CharField('日期',max_length=255)
    relate = models.CharField('所属关系',max_length=255)
    relater = models.CharField('经手人',max_length=255)
    fapiao = models.CharField('发票号',max_length=255)
    is_receive_fapiao=models.CharField('财务收到发票',max_length=255)
    shouju = models.CharField('收据',max_length=255)
    is_receive_shouju=models.CharField('财务收到收据',max_length=255)
                               
    class Admin:               
        pass                   
    
class teacher_request(models.Model) :
    teacher = models.ForeignKey(UserProfile)
    contents = models.TextField('内容' )
    time = models.DateTimeField('时间',blank=True)
    comments = models.CharField('comments',max_length=255,blank=True)

    class Admin:
        pass


#教师交流
class teacher_blog(models.Model) :
    teacher = models.ForeignKey(UserProfile)
    title = models.CharField("标题",max_length=255)
    contents = models.TextField('内容' )
    time = models.DateTimeField('时间',blank=True)
    comments = models.CharField('comments',max_length=255,blank=True)
    #enable_comments = models.BooleanField(default=True)
    class Admin:
        pass
    
    
    