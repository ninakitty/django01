import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from operation.models import UserFavorite
from organization.forms import UserAskForm
from .models import CourseOrg, City


# Create your views here.
class OrgView(View):
    '''
    课程机构列表
    '''

    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        hot_orgs = CourseOrg.objects.order_by('-click_num')[:5]
        all_city = City.objects.all()

        city_id = request.GET.get('city', '')
        ct = request.GET.get('ct', '')
        sort = request.GET.get('sort', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=city_id)
        if ct:
            all_orgs = all_orgs.filter(category=ct)
        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by('students')
            elif sort == 'courses':
                all_orgs = all_orgs.order_by('course_num')

        orgs_num = all_orgs.count()
        # 分页

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, request=request, per_page=5)
        orgs = p.page(page)

        return render(request, 'org-list.html',
                      {'all_orgs': orgs, 'all_city': all_city, 'orgs_num': orgs_num, 'city_id': city_id,
                       'category': ct, 'hot_orgs': hot_orgs, 'sort': sort})


class AddUserAskView(View):
    '''
    添加用户咨询
    '''

    def post(self, request):
        resp = {}
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            userask_form.save(commit=True)
            resp['status'] = 'success'
        else:
            resp['status'] = 'fail'
            resp['msg'] = userask_form.errors
        return HttpResponse(json.dumps(resp), content_type="application/json")


class OrgHomeView(View):
    '''
    机构首页
    '''

    def get(self, request, org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=org_id)
        user = request.user
        # 判断是否已收藏，2代表机构
        if request.user.is_authenticated():
            has_fav = UserFavorite.objects.filter(user=user, fav_id=course_org.id, fav_type=2)
        else:
            has_fav = False
        allcourses = course_org.course_set.all()
        print(allcourses.count())
        allteachers = course_org.teacher_set.all()
        return render(request, 'org-detail-homepage.html',
                      {'course_org': course_org, 'allcourses': allcourses, 'allteachers': allteachers,
                       'current_page': current_page, 'has_fav': has_fav})


class OrgCourseView(View):
    '''
    机构课程
    '''

    def get(self, request, org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=org_id)
        # 判断是否已收藏，2代表机构
        user = request.user
        if request.user.is_authenticated():
            has_fav = UserFavorite.objects.filter(user=user, fav_id=course_org.id, fav_type=2)
        else:
            has_fav = False
        allcourses = course_org.course_set.all()
        return render(request, 'org-detail-course.html',
                      {'course_org': course_org, 'allcourses': allcourses, 'current_page': current_page,
                       'has_fav': has_fav})


class OrgDescView(View):
    '''
    机构详情
    '''

    def get(self, request, org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=org_id)
        # 判断是否已收藏，2代表机构
        user=request.user
        if request.user.is_authenticated():
            has_fav = UserFavorite.objects.filter(user=user, fav_id=course_org.id, fav_type=2)
        else:
            has_fav = False
        return render(request, 'org-detail-desc.html',
                      {'course_org': course_org, 'current_page': current_page, 'has_fav': has_fav})


class OrgTeacherView(View):
    '''
    机构老师
    '''

    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=org_id)
        # 判断是否已收藏，2代表机构
        user = request.user
        if request.user.is_authenticated():
            has_fav = UserFavorite.objects.filter(user=user, fav_id=course_org.id, fav_type=2)
        else:
            has_fav = False
        allteachers = course_org.teacher_set.all()
        return render(request, 'org-detail-teachers.html',
                      {'course_org': course_org, 'current_page': current_page, 'allteacher': allteachers,
                       'has_fav': has_fav})


class AddFavView(View):
    '''
    机构收藏
    '''

    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)
        user = request.user
        resp = {}
        # 判断是否登录
        if not request.user.is_authenticated():
            resp['status'] = 'fail'
            resp['msg'] = '用户未登录'
            return HttpResponse(json.dumps(resp), content_type="application/json")
        else:
            exist_fav = UserFavorite.objects.filter(user=user, fav_id=fav_id, fav_type=fav_type)
            # 判断是否收藏
            if exist_fav:
                # 取消收藏
                resp['status'] = 'success'
                resp['msg'] = '收藏'
                exist_fav.delete()
                return HttpResponse(json.dumps(resp), content_type="application/json")
            else:
                # 收藏
                user_fav = UserFavorite()
                user_fav.user = user
                user_fav.fav_id = fav_id
                user_fav.fav_type = fav_type
                user_fav.save()
                resp['status'] = 'success'
                resp['msg'] = '已收藏'
                return HttpResponse(json.dumps(resp), content_type="application/json")
