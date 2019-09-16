# -*- coding: UTF-8 -*-
__copyright__ = 'Copyright (c) 2016 The University of Texas at Austin'
__author__ = 'mccookpv'

import json
from uuid import uuid4
from random import randrange
import logging
import yaml
import re
from django.conf import settings
from nanosourcer_lti_oauth_service import NanoSourcerSimpleOauthVerification

from Crypto.Cipher import DES
from django.utils.http import urlencode
from base64 import b64encode
from django.utils.encoding import smart_str, smart_unicode

logger_main = logging.getLogger("main")

class NanoSourcerLtiSessionException(object):

    def __init__(self,
                 error_title='',
                 error_message=''):

        self.error_context_vars = {}
        self.error_title = error_title
        self.error_message = error_message

    @property
    def error_title(self):
        return self.error_context_vars['err_title']

    @error_title.setter
    def error_title(self, value):
        self._error_context_vars['err_title'] = value

    @property
    def error_message(self):
        return self.error_context_vars['err_message']

    @error_message.setter
    def error_message(self, value):
        self._error_context_vars['err_message'] = value

    @property
    def error_context_vars(self):
        return self._error_context_vars

    @error_context_vars.setter
    def error_context_vars(self, value):
        self._error_context_vars = value



class NanoSourcerLtiAppConfig(object):

    def __init__(self,
                 config_dict,
                 debug=False,
                 headers=None):

        if not headers:
            headers = {}

        self.config_dict = config_dict
        self._debug = debug
        self._headers = headers

        self.key_trans_table = dict(zip((ord(char) for char in "+/="),
                                        (ord(char) for char in u'-@_')))

        self.service_role_mappings = {'TeacherEnrollment': 'instructor',
                                      'Instructor': 'instructor',
                                      'TeachingAssistant': 'ta',
                                      'TaEnrollment': 'ta',
                                      'Administrator': 'admin',
                                      'StudentEnrollment': 'student',
                                      'Learner': 'student'}

        self.key_trans_table = dict(zip((ord(char) for char in "+/="),
                                        (ord(char) for char in u'-@_')))

    @property
    def is_allow_any_host(self):
        return self._is_allow_any_host

    @is_allow_any_host.setter
    def is_allow_any_host(self, value):
        self._is_allow_any_host = value

    @property
    def fixed_lms_host_url(self):
        return self._fixed_lms_host_url

    @fixed_lms_host_url.setter
    def fixed_lms_host_url(self, value):
        self._fixed_lms_host_url = value

    @property
    def prefer_fixed_lms_host_url(self):
        return self._prefer_fixed_lms_host_url

    @prefer_fixed_lms_host_url.setter
    def prefer_fixed_lms_host_url(self, value):
        self._prefer_fixed_lms_host_url = value

    @property
    def negotiate_dynamic_oauth_token(self):
        return self._negotiate_dynamic_oauth_token

    @negotiate_dynamic_oauth_token.setter
    def negotiate_dynamic_oauth_token(self, value):
        self._negotiate_dynamic_oauth_token = value

    @property
    def api_rows_per_page(self):
        return self._api_rows_per_page

    @api_rows_per_page.setter
    def api_rows_per_page(self, value):
        self._api_rows_per_page = value

    @property
    def api_request_limit(self):
        return self._api_request_limit

    @api_request_limit.setter
    def api_request_limit(self, value):
        self._api_request_limit = value

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, value):
        self._debug = value

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, value):
        self._headers = value

    def init_headers(self):

        if self._prefer_fixed_lms_host_url is True and \
                self._fixed_lms_host_url:
            access_token = self.get_api_oauth_token_header(self._fixed_lms_host_url)
            self._headers['Authorization'] = access_token

    def get_app_name(self):
        return self.config_dict.get('app_name', None)

    def get_lti_host_key(self):
        return self.config_dict.get('lti_host_key', None)

    def get_lti_consumer_key(self):
        return self.config_dict.get('lti_consumer_key', None)

    def get_lti_consumer_secret(self):
        return self.config_dict.get('lti_consumer_secret', None)

    def get_lti_encryption_pass_key(self):
        return self.config_dict.get('lti_encryption_pass_key', None)

    def get_lti_middleware_exclude_paths(self):
        return self.config_dict.get('lti_middleware_exclude_paths', [])

    def get_host_app_key_set(self):
        return self.config_dict.get('host_app_keys', {})

    def get_host_app_key_info(self,
                              host_app_key):
        host_app_key_set = self.get_host_app_key_set()
        return host_app_key_set.get(host_app_key, {})

    def is_host_allowed(self,
                        host_url):
        host_info = self.get_host_info(host_url)
        return host_info.get('allow', False)

    def get_global_api_oauth_token(self,
                                   host_app_key):
        host_app_key_info = self.get_host_app_key_info(host_app_key)
        return host_app_key_info.get('global_api_oauth_token', None)

    def get_host_set(self):
        return self.config_dict.get('hosts', {})

    def get_host_info(self,
                      host_url):
        host_set = self.get_host_set()
        return host_set.get(host_url, {})

    def get_host_app_key(self,
                         host_url):

        host_info = self.get_host_info(host_url)
        return host_info.get('host_app_key', None)

    def get_api_oauth_token_header(self,
                                  host_url):

        host_info = self.get_host_info(host_url)
        api_key = host_info.get('api_oauth_token', None)
        if not api_key:
            host_app_key = self.get_host_app_key(host_url)
            api_key = self.get_global_api_oauth_token(host_app_key)
            if not api_key:
                return None

        return "Bearer {0}".format(api_key)

    def construct_api_oauth_token_header(self,
                                         api_key):
        return "Bearer {0}".format(api_key)

    def get_origin_host_url(self, request):

        origin_host_url = None

        custom_lms_api_domain = request.POST.get('custom_canvas_api_domain', None)

        if custom_lms_api_domain:
            origin_host_url = "https://{0}".format(custom_lms_api_domain)
            return origin_host_url

            # if not origin_host_url:

            # launch_presentation_return_url = request.POST.get('launch_presentation_return_url', None)
            #
            # if launch_presentation_return_url:
            #
            #     pattern = re.compile("^(\w+://[\w+\.]*)/.*$")
            #
            #     m = pattern.match(launch_presentation_return_url)
            #
            #     if m:
            #         return m.group(1)

        if not origin_host_url:
            origin_host_url = request.META.get('origin', None)

        if not origin_host_url:
            origin_host_url = request.META.get('HTTP_ORIGIN', None)

        return origin_host_url

    def encrypt_lti_key(self,
                        lti_key):

        lti_encryption_pass_key = self.get_lti_encryption_pass_key()

        if not lti_encryption_pass_key:
            return lti_key

        des_obj = DES.new(lti_encryption_pass_key, DES.MODE_ECB)

        diff = len(lti_key) % 8

        if diff:
            padlen = 8 - diff
            lti_key += (chr(0) * padlen)

        encrypted_key = des_obj.encrypt(lti_key)

        return encrypted_key

    def create_lti_session_key(self,
                               request):

        p = "create_lti_session_key"

        canvas_user_id = request.POST.get('custom_canvas_user_id', None)
        canvas_course_id = request.POST.get('custom_canvas_course_id', None)
        nonce = request.POST.get('oauth_nonce', randrange(0, 1000000))

        if not canvas_user_id or not canvas_course_id:
            return None

        # lti_session_key = "{0}@@{1}@@{2}".format(canvas_user_id,
        #                                          canvas_course_id,
        #                                          nonce)

        lti_session_key = "{0}@@{1}".format(canvas_user_id,
                                            canvas_course_id)

        lti_session_key = self.encrypt_lti_key(lti_session_key)

        key_encoded = b64encode(lti_session_key)

        # logger_main.info(self.key_trans_table)
        # lti_session_key = unicode(lti_session_key).translate(self.key_trans_table)
        key_encoded = key_encoded.replace('+', '_').replace('/', '-').replace('=', '~')

        return key_encoded

    def template_lti_session_data(self,
                                  lti_session_data=None):

        if not lti_session_data:
            lti_session_data = {}

        new_lti_session_data = {
            'lti_session_key': None,
            'header_http_origin': None,
            'header_http_user_agent': None,
            'header_http_referer': None,
            'header_remote_addr': None,
            'context_id': None,
            'user_id': None,
            'context_label': None,
            'context_title': None,
            'custom_canvas_course_id': None,
            'custom_canvas_enrollment_state': None,
            'lis_course_offering_sourcedid': None,
            'lis_person_name_given': None,
            'lis_person_name_family': None,
            'lis_person_contact_email_primary': None,
            'ext_roles': None,
            'roles': None,
            'lis_person_sourcedid': None,
            'user_image': None,
            'custom_canvas_user_id': None,
            'custom_canvas_user_login_id': None,
            'custom_canvas_api_domain': None,
            'lti_message_type': None,
            'lti_version': None,
            'oauth_callback': None,
            'oauth_consumer_key': None,
            'oauth_nonce': None,
            'oauth_signature': None,
            'oauth_signature_method': None,
            'oauth_timestamp': None,
            'oauth_version': None,
            'resource_link_id': None,
            'resource_link_title': None,
            'launch_presentation_return_url': None,
            'launch_presentation_document_target': None
        }

        new_lti_session_data.update(lti_session_data)

        return new_lti_session_data

    def convenience_lti_session_data(self,
                                     lti_session_data):

        course_id = lti_session_data.get('custom_canvas_course_id', None)
        login_id = lti_session_data.get('custom_canvas_login_id', None)
        sis_user_id = lti_session_data.get('lis_person_sourcedid', None)
        sis_course_id = lti_session_data.get('lis_course_offering_sourcedid', None)
        user_name = lti_session_data.get('lis_person_name_full', None)
        user_email = lti_session_data.get('lis_person_contact_email_primary', None)

        if not sis_user_id and login_id:
            sis_user_id = login_id
        elif not login_id and sis_user_id:
            login_id = sis_user_id

        new_lti_session_data = {'course_id': course_id,
                                'login_id': login_id,
                                'sis_user_id': sis_user_id,
                                'sis_course_id': sis_course_id,
                                'user_name': user_name,
                                'user_email': user_email}

        lti_session_data.update(new_lti_session_data)

        return lti_session_data

    @staticmethod
    def extract_host_url(full_url):

        if not full_url:
            return None

        m = re.match(r"^(https?://[^/]*)/?.*$", full_url)

        if m and m.group(1):
            return m.group(1)

        return None

    def print_lti_handshake_vars(self,
                                 request):

        logger_main.info("=" * 64)
        logger_main.info("LTI Parameters")
        logger_main.info("-" * 64)

        for k, v in request.POST.items():
            logger_main.info("param : {0}: {1}".format(k, v))

        logger_main.info("=" * 64)
        logger_main.info("LTI Headers")
        logger_main.info("-" * 64)

        for k, v in request.META.items():
            logger_main.info("header : {0}: {1}".format(k, v))

        logger_main.info("=" * 64)

    def get_user_role_list(self,
                           roles):

        role_list = str(roles).split(',')

        service_role_mappings_dict = self.service_role_mappings

        user_role_list = []

        for service_key, service_value in service_role_mappings_dict.items():
            for param_role in role_list:
                if re.search(service_key, param_role):
                    user_role_list.append(service_value)

        return user_role_list

    def launch_lti_session_data(self,
                                request,
                                default_session_expiry=3600,
                                lti_session_data=None,
                                load_full_handshake=False,
                                load_convenience_vars=True,
                                print_lti_handshake=False,
                                include_param_keys=None,
                                include_header_keys=None,
                                service_role_mappings_dict=None):

        p = "launch_lti_session_data"

        message_dict = {}

        if request.method != 'POST':
            return None, {'post_method': 'Invalid request method not POST'}

        if not request.POST:
            return None, {'post_empty': 'No data in request'}

        lti_course_id = request.POST.get('context_id')
        lti_user_id = request.POST.get('user_id')

        if not lti_course_id:
            return None, {'lti_course_id_empty': 'No course_id found in request'}

        if not lti_user_id:
            return None, {'lti_user_id_empty': 'No user_id found in request'}

        if lti_session_data:
            lti_session_data = self.template_lti_session_data(lti_session_data)
        else:
            lti_session_data = self.template_lti_session_data()

        if print_lti_handshake:
            self.print_lti_handshake_vars(request)

        for k, v in request.META.items():
            k = k.lower()
            if isinstance(v, unicode):
                kval = v.encode("utf-8")
            else:
                kval = str(v)

            if load_full_handshake == True:
                lti_session_data["header_{0}".format(k)] = kval
            else:
                kheader = "header_{0}".format(k)
                if include_header_keys and kheader in include_header_keys:
                    lti_session_data[kheader] = kval

        for k, v in request.POST.items():
            if isinstance(v, unicode):
                kval = v.encode("utf-8")
            else:
                kval = str(v)
            if load_full_handshake == True:
                lti_session_data[k] = kval
            else:
                if k in lti_session_data:
                    lti_session_data[k] = kval
                if include_param_keys and k in include_param_keys:
                    lti_session_data[k] = kval

        # TODO : validate origin_host_url ?

        # Always store the 'origin_host_url' convenience key.
        # Most applications will rely on this to identify the calling host.
        origin_host_url = self.get_origin_host_url(request)
        lti_session_data['origin_host_url'] = origin_host_url

        # TODO - necessary? redundant?
        lti_session_data['host_url'] = origin_host_url

        if load_convenience_vars:
            lti_session_data = self.convenience_lti_session_data(lti_session_data)

        oauth_nonce = lti_session_data.get('oauth_nonce', None)
        if not oauth_nonce:
            oauth_nonce = str(uuid4())
        origin_host_url = lti_session_data.get('origin_host_url', None)
        oauth_signature = lti_session_data.get('oauth_signature', None)

        if not oauth_nonce:
            return None, {'oauth_nonce': 'No oauth_nonce value'}

        if not origin_host_url:
            return None, {'origin_host_url': 'No origin_host_url in request'}

        if not oauth_signature:
            return None, {'oauth_signature': 'No oauth_signature in request'}

        if not lti_session_data:
            return None, {'lti_session_data_empty': 'No lti_session_data'}

        consumer_key = self.get_lti_consumer_key()
        consumer_secret = self.get_lti_consumer_secret()

        # Verify oauth_signature against LTI key and secret.
        oauth_verification = NanoSourcerSimpleOauthVerification(request,
                                                                consumer_key,
                                                                consumer_secret)

        if not oauth_verification.verify_consumer_key():
            return None, {'verify_consumer_key': 'Verify of consumer key failed'}

        if not oauth_verification.verify_signature():
            # TODO -- fix this!
            # return None, {'verify_signature': 'Verify of signature failed'}
            pass

        lti_session_key = self.create_lti_session_key(request)

        request.session['lti_session_key'] = lti_session_key
        lti_session_data['is_lti_launch'] = 1

        if service_role_mappings_dict:
            roles = lti_session_data.get('roles', None)
            if roles:
                role_list = self.get_user_role_list(roles)
                if 'instructor' in role_list:
                    lti_session_data['instructor_session_token'] = str(uuid4())
                if 'admin' in role_list:
                    lti_session_data['instructor_session_token'] = str(uuid4())
                if 'ta' in role_list:
                    lti_session_data['instructor_session_token'] = str(uuid4())

        request.session[lti_session_key] = lti_session_data

        request.session['is_launch'] = 1

        request.session['keepalive'] = True
        request.session.set_expiry(default_session_expiry)
        request.session.modified = True
        request.session.save()

        return lti_session_data, message_dict

    def establish_existing_canvas_session(self,
                                          request,
                                          default_session_expiry=3600):

        lti_session_key = request.session.get('lti_session_key')
        lti_session_data = request.session.get(lti_session_key, None)

        if not lti_session_data:
            raise NanoSourcerLtiSessionException('User session has expired. (1)',
                                         'Please re-launch application from sidebar menu.')

        origin_host_url = lti_session_data.get('origin_host_url', None)

        if not origin_host_url:
            raise NanoSourcerLtiSessionException('Invalid access attempt.',
                                         'Please re-launch application from sidebar menu.')

        # TODO FIX!!
        # if not self.is_host_allowed(origin_host_url):
        #     raise NanoSourcerLtiSessionException('Access denied.',
        #                                  'LTI host may not access this application.')

        request.session['keepalive'] = True
        request.session.set_expiry(default_session_expiry)

        return lti_session_data

    def get_valid_lti_session(self,
                              request,
                              lti_session_key=None,
                              default_session_expiry=3600,
                              lti_session_data=None,
                              load_full_handshake=False,
                              load_convenience_vars=True,
                              print_lti_handshake=False,
                              include_param_keys=None,
                              include_header_keys=None,
                              user_roles=None,
                              service_role_mappings_dict=None):

        p = "get_valid_lti_session"

        message_dict = {}
        is_launch = False

        if not lti_session_data:
            if lti_session_key:
                lti_session_data = request.session.get(lti_session_key, None)

        if request.method == 'POST':

            oauth_nonce = request.POST.get('oauth_nonce', None)
            lti_course_id = request.POST.get('context_id', None)
            lti_user_id = request.POST.get('user_id', None)
            host_url = self.get_origin_host_url(request)

            if oauth_nonce and host_url:
                is_launch = True
            else:
                is_launch = False
                if not lti_session_data or not lti_session_data.get('oauth_nonce', None):
                    is_launch = True

            if is_launch:
                (lti_session_data, message_dict) = \
                    self.launch_lti_session_data(request,
                                                 default_session_expiry=default_session_expiry,
                                                 lti_session_data=lti_session_data,
                                                 load_full_handshake=load_full_handshake,
                                                 load_convenience_vars=load_convenience_vars,
                                                 print_lti_handshake=print_lti_handshake,
                                                 include_param_keys=include_param_keys,
                                                 include_header_keys=include_header_keys,
                                                 service_role_mappings_dict=service_role_mappings_dict)

                if message_dict:
                    logger_main.error(message_dict)

        if not lti_session_data:
            if is_launch:
                message_dict['launch_session'] = 'Unable to create new session'
            else:
                message_dict['current_session'] = 'Unable to find existing session'

        lti_session_key = request.session.get('lti_session_key')

        return lti_session_data, message_dict


