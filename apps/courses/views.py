from django.shortcuts import render

# Create your views here.
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

# 课程列表
from courses.models import Course


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
            'sort':sort,
        })
