# -*- coding: UTF-8 -*-
__copyright__ = 'Copyright (c) 2016 The University of Texas at Austin'
__author__ = 'mccookpv'

from django.http import HttpResponse
from django.http import Http404
from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.conf import settings
import logging
import json

logger_main = logging.getLogger("main")

class NanoSourcerLtiHandshakeMiddleware(object):

    def __init__(self,
                 *args,
                 **kwargs):

        self.lti_app_config = settings.LTI_APP_CONFIG

    def get_lti_session_key(self, request):

        if request.method == 'POST':

            lti_session_key = request.POST.get('lti_session_key', None)
            if not lti_session_key:
                lti_session_key = request.POST.get('lk', None)

        elif request.method == 'GET':
            lti_session_key = request.GET.get('lk', None)
            if not lti_session_key:
                lti_session_key = request.GET.get('lti_session_key', None)
        else:
            if request.body:
                request_body_dict = json.loads(request.body)
                lti_session_key = request_body_dict.get('lk', None)
                if not lti_session_key:
                    lti_session_key = request_body_dict.get('lti_session_key', None)
            else:
                lti_session_key = None

        return lti_session_key

    def bypass_exclude_paths(self,
                             request):

        lti_middleware_exclude_path_list = self.lti_app_config.get_lti_middleware_exclude_paths()

        for ex_regex in lti_middleware_exclude_path_list:
            # if request.path.startswith(regex):
            if ex_regex.match(request.path):
                return True

        return False

    def process_request(self,
                        request):

        p = "process_request"

        if self.bypass_exclude_paths(request):
            return None

        logger_main.info("=" * 64)
        logger_main.info("{0} {1}".format(p, request.path))

        lti_session_key = self.get_lti_session_key(request)

        request.session['lti_session_key'] = lti_session_key

        # logger_main.info('{0} lti_session_key {1}'.format(p, lti_session_key))

        # for k, v in request.POST.items():
        #     logger_main.info("POST {0}:{1}".format(k, v))

        # for k, v in request.GET.items():
        #     logger_main.info("GET {0}:{1}".format(k, v))

        if not self.lti_app_config:
            return HttpResponse(content="LTI app configuration not found.",
                                content_type=None,
                                status=500,
                                reason='LTI app configuration not found.')

        if self.bypass_exclude_paths(request):
            return None

        lti_session_data, message_dict = self.lti_app_config.get_valid_lti_session(request,
                                                                                   lti_session_key=lti_session_key,
                                                                                   default_session_expiry=3600,
                                                                                   lti_session_data=None,
                                                                                   load_full_handshake=False,
                                                                                   load_convenience_vars=True,
                                                                                   print_lti_handshake=False,
                                                                                   include_param_keys=[],
                                                                                   include_header_keys=[])

        if not lti_session_data:
            return HttpResponse(content="Session has expired. Please re-launch application from menu.",
                                content_type=None,
                                status=401,
                                reason='Session has expired. Please re-launch application from menu.')

        return None


    def process_view(self,
                     request,
                     view_func,
                     view_args,
                     view_kwargs):
        return None

    def process_template_response(self,
                                  request,
                                  response):
        return None

    def process_response(self,
                         request,
                         response):
        return response

    def process_exception(self,
                          request,
                          exception):

        if hasattr(exception, 'error_code') and hasattr(exception, 'error_message'):
            return HttpResponse(content=exception.error_message,
                                content_type=None,
                                status=exception.error_code,
                                reason=exception.error_message)
        else:

            if isinstance(exception, PermissionDenied):
                return HttpResponse(content="Access denied.",
                                    content_type=None,
                                    status=403,
                                    reason='Access denied.')
            elif isinstance(exception, SuspiciousOperation):
                return HttpResponse(content="Access denied.",
                                    content_type=None,
                                    status=403,
                                    reason='Access denied.')
            elif isinstance(exception, Http404):
                return HttpResponse(content="Resource not found.",
                                    content_type=None,
                                    status=404,
                                    reason='Resource not found.')
            else:
                if str(exception):
                    return HttpResponse(content="Error: {0}".format(str(exception)),
                                        content_type=None,
                                        status=500,
                                        reason=exception)
                else:
                    return HttpResponse(content="Access denied.",
                                        content_type=None,
                                        status=403,
                                        reason='Access denied.')

    def get_timedelta_seconds(self,
                              td):
        return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10 ** 6) / 10 ** 6


