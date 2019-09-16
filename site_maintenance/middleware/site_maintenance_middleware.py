# -*- coding: UTF-8 -*-
__copyright__ = 'Copyright (c) 2016 The University of Texas at Austin'
__author__ = 'mccookpv'

from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import redirect, render, render_to_response

class SiteMaintenanceMiddleware(object):

    def __init__(self,
                 *args,
                 **kwargs):
        pass

    def process_request(self,
                        request):


        err_data = {}

        res = render_to_response('site_maintenance.html',
                                 err_data,
                                 context_instance=RequestContext(request))

        # return HttpResponse("Site is undergoing maintenance.  Please check back in a couple of hours.")

        res.status_code = 500

        return res



