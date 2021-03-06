# -*- coding: utf-8 -*-
__author__ = 'mengyuan'
__date__ = '2017/7/27 20:52'

import xadmin
from .models import CityDict, CourseOrg, Teacher


class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'click_nums', 'fav_num', 'image', 'address', 'city', 'add_time']
    search_fields = ['name', 'desc', 'click_nums', 'fav_num', 'image', 'address', 'city__name']
    list_filter = ['name', 'desc', 'click_nums', 'fav_num', 'image', 'address', 'city__name', 'add_time']


class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_years', 'work_company',
                    'work_position', 'points', 'click_nums', 'fav_num', 'add_time']
    search_fields = ['org', 'name', 'work_years', 'work_company',
                     'work_position', 'points', 'click_nums', 'fav_num', 'add_time']
    list_filter = ['org', 'name', 'work_years', 'work_company',
                   'work_position', 'points', 'click_nums', 'fav_num', 'add_time']

xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
