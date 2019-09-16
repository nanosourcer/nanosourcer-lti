# -*- coding: UTF-8 -*-

import os

from django.http import Http404
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from wsgiref.util import FileWrapper

from m_common import *

__copyright__ = 'Copyright (c) 2016 The University of Texas at Austin'
__author__ = 'mccookpv'


def download_adhoc_zip(request):
    """
    Download the Nanosourcer ad-hoc query results as a zip compressed file.
    """

    logger_main.info('download_adhoc_zip check 001')

    zipfile = "{0}/db/ddl/queries/nanosourcer_csv.zip".format(settings.BASE_DIR)
    logger_main.info('download_adhoc_zip check 002')

    context_vars = {}

    if not os.path.exists(zipfile):
        context_vars['err_title'] = 'No zip file exists.'
        context_vars['err_message'] = 'No zip file was found.'
        response = render_to_response('lobby/lti_error.html',
                                      context_vars,
                                      context_instance=RequestContext(request),
                                      )
        set_response_meta_nocache(response)
        return response

    logger_main.info('zipfile {0}'.format(zipfile))

    zf = open(zipfile, "rb")

    response = HttpResponse(FileWrapper(zf), content_type='application/zip')
    logger_main.info('download_adhoc_zip check 003')
    response['Content-Disposition'] = 'attachment; filename=nanosourcer_csv.zip'
    logger_main.info('download_adhoc_zip check 004')
    return response

def queryzip(request,
             config_key=None):

    context_vars = {'lti_session_key'}

    response = render_to_response('temp_query_zip_download.html',
                                  context_vars,
                                  context_instance=RequestContext(request),
                                  )
    set_response_meta_nocache(response)
    return response

@csrf_exempt
def assignment_lti_config(request, config_key=None):

    response = render_to_response("config/assignment.xml",
                                  context_vars,
                                  content_type="application/xml; charset=utf-8",
                                  context_instance=RequestContext(request))


    set_response_meta_nocache(response)

    return response

@csrf_exempt
def nav_lti_config(request,
                   config_key=None):
    """
    Returns a prepared LTI XML configuration file to the LMS LTI app installation.

    https://<host>/<config_key>
    https://<host>/config/main
    """

    if not config_key:
        config_key = "main"

    config_root = "{0}/templates/config".format(settings.PROJECT_ROOT)

    path = "{0}/{1}.xml".format(config_root,
                                config_key)

    if not os.path.exists(path):
        raise Http404()

    app_url = request.build_absolute_uri('/')

    context_vars = dict()
    context_vars['entry_root_url'] = app_url
    context_vars['server_env'] = settings.SERVER_ENV

    response = render_to_response("config/{0}.xml".format(config_key),
                                  context_vars,
                                  content_type="application/xml; charset=utf-8",
                                  context_instance=RequestContext(request))

    set_response_meta_nocache(response)

    return response


@csrf_exempt
def nav_main(request):

    p = "nav_main"

    context_vars = {}

    lti_session_key = request.session.get('lti_session_key', None)

    # is_launch = request.session.get('is_launch')
    #
    # if is_launch:
    #     request.session['is_launch'] = 0
    #
    #     context_vars['is_lti_launch'] = 1
    #     context_vars['lti_session_key'] = lti_session_key
    #
    #     # response = render_to_response('launcher.html',
    #     #                               context_vars,
    #     #                               context_instance=RequestContext(request),
    #     #                               )
    #     # set_response_meta_nocache(response)
    #
    #     return redirect("/main/?lk=" + lti_session_key)

    if not lti_session_key:
        context_vars['err_title'] = 'Invalid session.'
        context_vars['err_message'] = 'No session data found. Please relaunch application from Canvas.'
        response = render_to_response('lobby/lti_error.html',
                                      context_vars,
                                      context_instance=RequestContext(request),
                                      )
        set_response_meta_nocache(response)
        return response

    lti_session_data = request.session.get(lti_session_key)

    roles = lti_session_data.get('roles', None)
    user_role_list = get_user_role_list(roles)

    if is_valid_role(lti_session_data,
                     user_role_list,
                     ['admin', 'instructor', 'ta']):

        entry_url = "/admin/?lk={0}".format(lti_session_key)

        rr = redirect(entry_url)
        return rr

    elif is_valid_role(lti_session_data,
                       user_role_list=user_role_list,
                       role_verify_list=['student']):

        entry_url = "/view/?lk={0}".format(lti_session_key)

        rr = redirect(entry_url)
        return rr

    else:

        context_vars['err_title'] = 'Unauthorized.'
        context_vars['err_message'] = 'You are not authorized to access this application.'

        response = render_to_response('lobby/lti_error.html',
                                      context_vars,
                                      context_instance=RequestContext(request))
        set_response_meta_nocache(response)
        return response

def logout(request):

    context_vars = {}

    lti_session_key = request.session['lti_session_key']

    request.session['lti_session_key'] = None
    request.session[lti_session_key] = None

    response = render_to_response('lobby/lti_session_end.html',
                                  context_vars,
                                  context_instance=RequestContext(request),
                                  )
    set_response_meta_nocache(response)
    return response

