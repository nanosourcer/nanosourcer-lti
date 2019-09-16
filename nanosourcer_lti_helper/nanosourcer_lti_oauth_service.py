# -*- coding: UTF-8 -*-
__copyright__ = 'Copyright (c) 2016 The University of Texas at Austin'
__author__ = 'mccookpv'

import django_nanosourcer.my_oauth.oauth as oauth

import cgi
import urllib
import time
import random
import urlparse
import hmac
import binascii
import logging

# logger_main = logging.getLogger("main")

class NanoSourcerSimpleOauthVerification(object):
    """
    Ripped in part from my_oauth package, for purposes of verifying the POST data signature
    directly without other processing concerns.
    Also using a kludge where an embedded URL must have '%' symbols additionally escaped as
    %25 tokens prior to usual urlencoding.
    This builds on the provided my_oauth package installed externally.
    """
    def __init__(self,
                 request,
                 consumer_key,
                 consumer_secret):
        """
        Initializes the items needed to create an my_oauth.OAuthRequest, which
        will provide the data for creating signature to match the 'oauth_signature'
        parameter sent by the LMS when application is first launched.
        The 'consumer_key' and 'consumer_secret' values are retrieved from the
        centrally stored LTI application XML config file.  The lti_config_service
        with the host information should have been built elsewhere and passed to
        this object.  The 'consumer_key' and 'consumer_secret' values were also
        entered into the LMS by the site admin when the app was first installed.
        """

        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret

        self.consumer = oauth.OAuthConsumer(self.consumer_key,
                                            self.consumer_secret)

        request_path = request.build_absolute_uri(request.get_full_path())

        # Double-escaping needed in some cases so that whole POST packet
        # creates a valid matching signature.

        self.request_param_string = self.double_escape_values(request.POST)

        # Use above method to only double-escape % in values, not keys.
        # If that doesn't work, try this to brute-force escape the entire POST body:
        # request_params = request.body.replace("%", "%25")

        # Construct the my_oauth request from the request parameters
        # self.oauth_request = my_oauth.OAuthRequest.from_request(request.method,
        #                                                      request_path,
        #                                                      headers=request.environ,
        #                                                      query_string=self.request_param_string)

        self.oauth_request = self.from_request(request.method,
                                               request_path,
                                               headers=request.environ,
                                               query_string=self.request_param_string)




    def from_request(http_method,
                     http_url,
                     headers=None,
                     parameters=None,
                     query_string=None):
        """Combines multiple parameter sources.
           Kludge copy of method from OauthRequest class.
           That class method uses a _split_header method call that removes any parameters with blank values.
           Since the LMS preserves empty params when constructing the oauth_signature, it's necessary
           to keep these in the app parameters as well.
        """
        if parameters is None:
            parameters = {}

        # Headers
        if headers and 'Authorization' in headers:
            auth_header = headers['Authorization']
            # Check that the authorization header is OAuth.
            if auth_header[:6] == 'OAuth ':
                auth_header = auth_header[6:]
                try:
                    # Get the parameters from the header.
                    header_params = oauth.OAuthRequest._split_header(auth_header)
                    parameters.update(header_params)
                except:
                    raise oauth.OAuthError('Unable to parse OAuth parameters from '
                        'Authorization header.')

        # GET or POST query string.
        if query_string:
            query_params = NanoSourcerSimpleOauthVerification._split_url_string(query_string)
            parameters.update(query_params)

        # URL parameters.
        param_str = urlparse.urlparse(http_url)[4] # query
        url_params = oauth.OAuthRequest._split_url_string(param_str)
        parameters.update(url_params)

        if parameters:
            return oauth.OAuthRequest(http_method, http_url, parameters)

        return None
    from_request = staticmethod(from_request)

    def _split_url_string(param_str):
        """Turn URL string into parameters.
           Kludge -- overriding OauthRequest library method which hard-codes
           'keep_blank_values=False'.
        """
        parameters = cgi.parse_qs(param_str, keep_blank_values=True)
        for k, v in parameters.iteritems():
            parameters[k] = urllib.unquote(v[0])
        return parameters
    _split_url_string = staticmethod(_split_url_string)

    @staticmethod
    def double_escape_values(params):
        """
        Additional kludge to double-escape values in embedded values containing escaping.
        Necessary to match signature calculation of POST data. Probably a saner way to handle
        this, but may take comparison with how the LMS is constructing its own POST data.
        """
        key_values = {}
        for k, v in params.items():
            if v:
                v = oauth.escape(oauth.escape(oauth._utf8_str(v)))
            key_values[k] = v

        return '&'.join(['%s=%s' % (k, v) for k, v in key_values.items()])

    @staticmethod
    def single_escape_values(params):
        """
        Single escaping POST values, necessary for calculation of oauth_signature.
        """
        key_values = {}
        for k, v in params.items():
            if v:
                v = oauth.escape(oauth._utf8_str(v))
            key_values[k] = v

        return '&'.join(['%s=%s' % (k, v) for k, v in key_values.items()])

    def verify_consumer_key(self):
        """
        Ensure the oauth_consumer_key parameter sent by the LMS on application launch
        matches the 'consumer_key' value stored in the application's LTI XML file.
        """
        oauth_consumer_key = self.oauth_request.get_parameter('oauth_consumer_key')
        if oauth_consumer_key != self.consumer_key:
            return False
        else:
            return True

    def verify_signature(self):
        """
        More focused oauth_signature verification built on top of my_oauth package code.
        Returns True or False based on signature matching the value the LMS provides in
        the 'oauth_signature' parameter.

        """

        try:
            oauth_signature = self.oauth_request.get_parameter('oauth_signature')
        except:
            raise Exception("No oauth_signature found")

        try:
            oauth_signature_method = self.oauth_request.get_parameter('oauth_signature_method')
        except Exception:
            raise Exception("No oauth_signature_method found")

        try:
            oauth_token = self.oauth_request.get_parameter('oauth_token')
        except oauth.OAuthError:
            oauth_token = None

        if oauth_signature_method == 'HMAC-SHA1':
            signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()
        else:
            signature_method = oauth.OAuthSignatureMethod_PLAINTEXT()

        # Validate the signature.
        # logger_main.info("check_signature oauth_token     {0}".format(oauth_token))
        # logger_main.info("check_signature oauth_signature {0}".format(oauth_signature))
        valid_sig = signature_method.check_signature(self.oauth_request,
                                                     self.consumer,
                                                     oauth_token,
                                                     oauth_signature)

        return valid_sig

    def verify_oauth_timestamp(self,
                               session_timestamp,
                               timeout=300):
        """
        Checks the LMS-provided 'oauth_timestamp' against a stored session value,
        for possible timeout setting. Default is 300 seconds, or 5 minutes.
        TODO Unimplemented.
        """
        try:
            oauth_timestamp = self.oauth_request.get_parameter("oauth_timestamp")
        except:
            oauth_timestamp = None

    def verify_oauth_nonce(self, session_nonce):
        """
        Checks oauth_nonce value against a stored session nonce.
        """
        try:
            oauth_nonce = self.oauth_request.get_parameter("oauth_nonce")
        except:
            raise Exception("No oauth_nonce found")
        return oauth_nonce == session_nonce

