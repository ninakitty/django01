from django.db import models

# Create your models here.
from organization.models import CourseOrg, Teacher


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name='机构名称', null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name='课程名')
    teacher = models.ForeignKey(Teacher, verbose_name='讲师', null=True, blank=True)
    desc = models.CharField(max_length=300, verbose_name='课程描述')
    needknow = models.CharField(max_length=300, verbose_name='课程须知', default='')
    teacher_tell = models.CharField(max_length=300, verbose_name='老师告诉你', default='')
    notice = models.CharField(max_length=50, verbose_name='课程公告', default='', null=True, blank=True)
    detail = models.TextField(verbose_name='课程详情')
    degree = models.CharField(verbose_name='等级', choices=(('cj', '初级'), ('zj', '中级'), ('gj', '高级')), max_length=2)
    learn_times = models.IntegerField(default=0, verbose_name='学习时长（分钟数）')
    students = models.IntegerField(default=0, verbose_name='学习人数')
    fav_num = models.IntegerField(default=0, verbose_name='收藏人数')
    image = models.ImageField(upload_to='courses/%Y/%m', verbose_name='封面图', max_length=100)
    click_num = models.IntegerField(default=0, verbose_name='点击数')
    category = models.CharField(default='后端开发', max_length=30, verbose_name='课程类别')
    tag = models.CharField(default='', max_length=10, verbose_name='课程标签')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程')
    name = models.CharField(max_length=100, verbose_name='章节名')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name='章节')
    name = models.CharField(max_length=100, verbose_name='视频名')
    url = models.CharField(max_length=200, verbose_name='视频链接', default='')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程')
    name = models.CharField(max_length=100, verbose_name='名称')
    download = models.FileField(upload_to='course/resource/%Y/%m', verbose_name='资源文件', max_length=100)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name
