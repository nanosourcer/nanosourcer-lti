# -*- coding: UTF-8 -*-
import json
from datetime import datetime
import os

from m_common import *
from m_dao import *

__copyright__ = 'Copyright (c) 2016 The University of Texas at Austin'
__author__ = 'mccookpv'

@verify_course_user
def nav_student_view(request):

    lti_session_key = request.session.get('lti_session_key', None)
    lti_session_data = request.session.get(lti_session_key)

    course_user_info = db_get_course_user_info(lti_session_data)

    context_vars = {}

    user_info = course_user_info.get('user_info', {})
    course_info = course_user_info.get('course_info', {})

    lti_user_id = user_info.get('lti_user_id', None)
    lti_course_id = course_info.get('lti_course_id', None)

    user_id = user_info.get('user_id', None)
    course_id = course_info.get('course_id', None)

    user_first_name = user_info.get('user_first_name', 'unknown')
    user_last_name = user_info.get('user_last_name', 'unknown')
    user_full_name = "{0} {1}".format(user_first_name, user_last_name)

    context_vars['lti_session_key'] = lti_session_key
    context_vars['lti_user_id'] = lti_user_id
    context_vars['lti_course_id'] = lti_course_id
    context_vars['course_user_info'] = course_user_info
    context_vars['user_full_name'] = user_full_name
    context_vars['sis_user_id'] = user_info.get('sis_user_id', 'unknown-eid')

    # Set defaults of begin and year values.
    now = datetime.now()
    year_min = -5000
    year_max = now.year

    ns_collection = get_active_collection(course_id)

    if not ns_collection:
        context_vars['err_title'] = 'No active collection.'
        context_vars['err_message'] = 'No image collection has been established for this round.'
        response = render_to_response('lobby/lti_error.html',
                                      context_vars,
                                      context_instance=RequestContext(request))
        set_response_meta_nocache(response)
        return response

    collection_pid = ns_collection.collection.collection_pid

    ns_course_round = get_course_round(course_id)
    course_round_id = ns_course_round.id

    logger_main.error(course_round_id)

    last_image_pid = request.session.get('last_image_pid', None)

    image_pid = get_random_image_pid(collection_pid,
                                     user_id,
                                     course_round_id,
                                     last_image_pid=last_image_pid)

    request.session['last_image_pid'] = image_pid

    if not image_pid:
        context_vars['err_title'] = 'No images found.'
        context_vars['err_message'] = 'No more images found for review.'
        response = render_to_response('lobby/lti_error.html',
                                      context_vars,
                                      context_instance=RequestContext(request))
        set_response_meta_nocache(response)
        return response

    fedora_image_url = construct_fedora_content_url(image_pid, 'JPG')

    # Get image dimensions of selected image.
    img_dims = get_fedora_image_dimensions(fedora_image_url)

    course_search_types = db_get_course_search_types(course_id)

    course_search_type_list = {}
    for st in course_search_types:
        course_search_type_list[st['type_key']] = {'type_name': st['type_name'],
                                                   'search_type_id': st['search_type_id'],
                                                   'description': st['description'],
                                                   'is_selected': st['is_selected']
                                                   }

    (image_title, metadata_list) = get_image_metadata(image_pid,
                                                      course_id)

    gaz_config = build_gaz_config()


    init_course_config = {'start_lat': 35,
                          'start_lng': 18,
                          'start_zoom': 4,
                          'pagination_limit': 100,
                          'year_min': year_min,
                          'year_max': year_max,
                          'course_search_types': course_search_type_list,
                          'gazetteer_base_url': settings.GAZETTEER_BASE_URL,
                          'gazetteer_api_key': settings.GAZETTEER_API_KEY,
                          'course_user_info': course_user_info,
                          'image_title': image_title,
                          'metadata_list': metadata_list,
                          'gaz_config': gaz_config,
                          'collection_pid': collection_pid,
                          'image_pid': image_pid,
                          'course_round_id': course_round_id,
                          'fedora_image_url': fedora_image_url,
                          'image_dimensions': img_dims,
                          'lti_session_key': lti_session_key,
                          'lti_user_id': lti_user_id,
                          'lti_course_id': lti_course_id,
                          'mapbox_url' : settings.MAPBOX_URL,
                          'mapbox_token' : settings.MAPBOX_TOKEN,
                          'mapbox_leaflet_url' : settings.MAPBOX_LEAFLET_URL
                          }

    init_course_config = json.dumps(init_course_config)

    context_vars['host_url'] = request.META['HTTP_HOST']
    context_vars['init_course_config'] = init_course_config
    context_vars['year_min'] = year_min
    context_vars['year_max'] = year_max
    context_vars['user_full_name'] = user_full_name
    context_vars['fedora_image_url'] = fedora_image_url
    context_vars['image_title'] = image_title
    context_vars['metadata_list'] = metadata_list
    context_vars['course_search_types'] = course_search_types

    response = render_to_response('student_index.html',
                                  context_vars,
                                  context_instance=RequestContext(request))

    set_response_meta_nocache(response)

    return response
