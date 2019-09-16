# -*- coding: UTF-8 -*-
import logging
import re

from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext

from m_dao import db_get_course_user_info

__copyright__ = 'Copyright (c) 2016 The University of Texas at Austin'
__author__ = 'mccookpv'

logger_main = logging.getLogger("main")


class NanosourcerException(Exception):
    def __init__(self,
                 error_code=None,
                 error_message=None):
        self.error_code = error_code
        self.error_message = error_message

    def __str__(self):
        return repr("{0}: {1}".format(self.error_code,
                                      self.error_message))


def verify_authorization_admin(func):
    """
    Decorator to verify user has 'admin' authorization.
    """

    def decorator(request, *args, **kwargs):

        lti_session_key = request.session.get('lti_session_key', None)
        lti_session_data = request.session.get(lti_session_key)

        roles = lti_session_data.get('roles', None)
        user_role_list = get_user_role_list(roles)

        context_vars = {}

        if not is_valid_role(lti_session_data,
                             user_role_list,
                             ['admin', 'instructor', 'ta']):
            context_vars['err_title'] = 'Access denied.'
            context_vars['err_message'] = 'You do not have authorization for this view.'
            response = render_to_response('lobby/lti_error.html',
                                          context_vars,
                                          context_instance=RequestContext(request))
            set_response_meta_nocache(response)
            return response

        return func(request, *args, **kwargs)

    return decorator


def verify_course_user(func):
    """
    Decorator to verify course and user association exist.
    """

    def decorator(request, *args, **kwargs):

        lti_session_key = request.session.get('lti_session_key', None)
        lti_session_data = request.session.get(lti_session_key)

        course_user_info = db_get_course_user_info(lti_session_data)

        context_vars = {}

        if not course_user_info:
            context_vars['err_title'] = 'Unable to find course information.'
            context_vars['err_message'] = 'No course information found. Please relaunch application from Canvas.'
            response = render_to_response('lobby/lti_error.html',
                                          context_vars,
                                          context_instance=RequestContext(request))
            set_response_meta_nocache(response)
            return response

        return func(request, *args, **kwargs)

    return decorator


def get_user_role_list(roles):

    role_list = str(roles).split(',')

    service_role_mappings_dict = settings.SERVICE_ROLE_MAPPINGS

    user_role_list = []

    for service_key, service_value in service_role_mappings_dict.items():
        for param_role in role_list:
            if re.search(service_key, param_role):
                user_role_list.append(service_value)

    return user_role_list


def is_valid_role(lti_session_data,
                  user_role_list=(),
                  role_verify_list=()):

    if not user_role_list:
        roles = lti_session_data.get('roles', None)
        user_role_list = get_user_role_list(roles)

    is_valid = False

    for role in role_verify_list:
        if role in user_role_list:
            is_valid = True
            break

    return is_valid


def set_response_meta_nocache(response):
    response['Pragma'] = 'no-cache'
    response['Cache-Control'] = 'must-revalidate'
    response['Cache-Control'] = 'no-cache'
    response['Cache-Control'] = 'no-store'
    response['Expires'] = 'Mon, 8 Aug 2006 10:00:00 GMT'
    return response
