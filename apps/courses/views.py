from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from courses.models import Course

# 课程列表
from operation.models import UserCourse, UserFavorite


class CourseListView(View):
    def get(self, request):
        allcourse = Course.objects.all().order_by('-add_time')
        hotcourse = Course.objects.all().order_by('-click_num')[:3]
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                allcourse = allcourse.order_by('-students')
            elif sort == 'hot':
                allcourse = allcourse.order_by('-click_num')
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(allcourse, request=request, per_page=9)
        newcourses = p.page(page)
        return render(request, 'course-list.html', {
            'allcourse': newcourses,
            'hotcourse': hotcourse,
            'sort': sort,
        })


# 课程详情
class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        category = course.lesson_set.count()
        userlist = course.usercourse_set.all()[:3]
        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True
        tag = course.tag
        if tag:
            related_course = Course.objects.filter(~Q(id=course_id), tag=tag).order_by('-click_num')[:1]
        else:
            related_course = []
        # 添加课程点击量
        course.click_num += 1
        course.save()
        return render(request, 'course-detail.html', {
            'cur_course': course,
            'category': category,
            'userlist': userlist,
            'related_course': related_course,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org
        })
