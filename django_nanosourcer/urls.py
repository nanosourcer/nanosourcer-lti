# -*- coding: UTF-8 -*-

from django.conf.urls import url

from django_nanosourcer.views import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin

__copyright__ = 'Copyright (c) 2016 The University of Texas at Austin'
__author__ = 'mccookpv'

admin.autodiscover()

urlpatterns = [
    url(r'^(?P<config_key>\w{0,50})$', v_main.nav_lti_config),
    url('r^assignment/', v_main.assignment_lti_config),
    url(r'^config/(?P<config_key>\w{0,50})$', v_main.nav_lti_config),
    url(r'^main/$', v_main.nav_main),
    url(r'^logout/$', v_main.logout),
    url(r'^view/$', v_student.nav_student_view),
    url(r'^admin/$', v_admin.nav_admin_view),
    url(r'^admin-data/$', v_admin.admin_data),
    url(r'^admin-update/$', v_admin.admin_update),
    url(r'^admin-accept/$', v_admin.nav_admin_acceptance),
    url(r'^admin-accept-update/$', v_admin.admin_accept_update),
    url(r'^admin-data/$', v_admin.admin_data),
    url(r'^student-selections/$', v_api.SaveStudentSelection.as_view()),
    url(r'^queryzip/$', v_main.queryzip),
    url(r'^download-adhoc-zip/$', v_main.download_adhoc_zip)
]
