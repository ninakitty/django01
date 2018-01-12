from django.db import models


# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=50, verbose_name='城市名称')
    desc = models.CharField(max_length=200, verbose_name='城市描述')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '城市'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name='机构名称')
    desc = models.TextField(verbose_name='机构详情')
    category = models.CharField(max_length=6, verbose_name='机构分类', default='pxjg',
                                choices=(('pxjg', '培训机构'), ('gx', '高校'), ('gr', '个人')))
    click_num = models.IntegerField(default=0, verbose_name='点击数')
    fav_num = models.IntegerField(default=0, verbose_name='收藏数')
    image = models.ImageField(upload_to='org/%Y/%m', verbose_name='封面图', max_length=100)
    address = models.CharField(max_length=150, verbose_name='机构地址')
    city = models.ForeignKey(City, verbose_name='所在城市')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    students = models.IntegerField(default=0, verbose_name='学习人数')
    course_num = models.IntegerField(default=0, verbose_name='课程数')

    class Meta:
        verbose_name = '课程机构'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg, verbose_name='所属机构')
    name = models.CharField(max_length=50, verbose_name='教师名称')
    work_years = models.IntegerField(default=0, verbose_name='工作年限')
    work_company = models.CharField(max_length=50, verbose_name='就职公司')
    work_position = models.CharField(max_length=50, verbose_name='就职职位')
    points = models.CharField(max_length=50, verbose_name='教学特点')
    click_num = models.IntegerField(default=0, verbose_name='点击数')
    fav_num = models.IntegerField(default=0, verbose_name='收藏数')
    image = models.ImageField(upload_to='org/teacher/%Y/%m', verbose_name='封面图', max_length=100, null=True, blank=True)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '教师'
        verbose_name_plural = verbose_name
