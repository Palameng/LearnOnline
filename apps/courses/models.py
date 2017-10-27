# _*_ encoding:utf-8 _*_
from datetime import datetime
from django.db import models
from organization.models import CourseOrg, Teacher

# Create your models here.


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name=u"课程机构", null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name=u"课程名")
    desc = models.CharField(max_length=300, verbose_name=u"课程描述")
    detail = models.TextField(verbose_name=u"课程详情")
    is_banner = models.BooleanField(verbose_name=u"是否轮播", default=False)
    degree = models.CharField(choices=(("cj", "初级"), ("zj", "中级"), ("gj", "高级")), max_length=2)
    teacher = models.ForeignKey(Teacher, verbose_name=u"课程老师", null=True, blank=True)
    learn_time = models.IntegerField(default=0, verbose_name=u"学习时长")
    students = models.IntegerField(default=0, verbose_name=u"学习人数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏")
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name=u"封面", max_length=100)
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    category = models.CharField(default="后端开发", max_length=20, verbose_name=u"课程类别")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    tag = models.CharField(default="", verbose_name=u"课程标签", max_length=10)
    needknow = models.CharField(default="", max_length=300, verbose_name=u"课程须知")
    tip = models.CharField(default="", max_length=300, verbose_name=u"老师提示")

    class Meta:
        verbose_name = u"课程"
        verbose_name_plural = verbose_name

    def getChapter(self):
        # 获取课程章节数
        return self.lesson_set.all().count()

    def getLearnUser(self):
        # 获取学习了该课程的学生
        return self.usercourse_set.all()[:5]

    def getLesson(self):
        #获取所有章节
        return self.lesson_set.all()

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"课程")  # 设置外键为Course
    name = models.CharField(max_length=100, verbose_name=u"章节名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    learn_time = models.IntegerField(default=0, verbose_name=u"课程学习时长")

    class Meta:
        verbose_name = u"章节"
        verbose_name_plural = verbose_name

    def getLessonVideo(self):
        return self.video_set.all()

    def __str__(self):
        return self.name


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u"章节")  # 设置外键为Course
    name = models.CharField(max_length=100, verbose_name=u"视频名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    url = models.CharField(max_length=200, verbose_name=u"访问地址", default='')
    learn_time = models.IntegerField(default=0, verbose_name=u"课程学习时长")

    class Meta:
        verbose_name = u"视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"课程")  # 设置外键为Course
    name = models.CharField(max_length=100, verbose_name=u"名称")
    download = models.FileField(upload_to="course/resource/%Y/%m", verbose_name=u"资源文件", max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程资源"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
