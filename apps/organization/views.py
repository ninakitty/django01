import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from organization.forms import UserAskForm
from .models import CourseOrg, City


# Create your views here.
class OrgView(View):
    '''
    课程机柜列表
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
    def post(self, request):
        resp = {}
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            userask = userask_form.save(commit=True)
            resp['status'] = 'success'
        else:
            resp['status'] = 'fail'
            resp['msg']=userask_form.errors
        return HttpResponse(json.dumps(resp), content_type="application/json")
