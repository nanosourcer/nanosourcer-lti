# -*- coding: UTF-8 -*-
import json
import hashlib
from django.http import JsonResponse

from django.db import connection
import logging

from django.shortcuts import redirect
from django.template.context_processors import csrf

from m_common import *
from m_dao import *

__copyright__ = 'Copyright (c) 2016 The University of Texas at Austin'
__author__ = 'mccookpv'

def update_hash(request):

    list_o_files_to_hash = [

        settings.STATIC_ROOT + '/dist/nanosourcer.css',
        settings.STATIC_ROOT + '/dist/nanosourcer.min.js'

    ]

    hashes = ''.join([

        hashlib.sha1(open(x, 'rb').read()).hexdigest() for x in list_o_files_to_hash

    ])

    collective_hash = hashlib.sha1(hashes).hexdigest()


    return JsonResponse({"hash": collective_hash.decode('utf-8', errors='ignore')})

@verify_authorization_admin
@verify_course_user
def front_end_unit_tests(request):



    lti_session_key = request.session.get('lti_session_key', None)
    lti_session_data = request.session.get(lti_session_key)

    course_user_info = db_get_course_user_info(lti_session_data)

    course_info = course_user_info.get('course_info', {})

    course_id = course_info.get('course_id', None)

    context = {}

    return render_to_response('unit_test.html', context, context_instance=RequestContext(request))


@verify_authorization_admin
@verify_course_user
def nav_admin_view(request):

    p = "nav_admin_view"

    context_vars = {}

    update_message = request.session.get('update_message', None)

    context_vars['update_message'] = update_message
    request.session['update_message'] = None

    lti_session_key = request.session.get('lti_session_key', None)
    lti_session_data = request.session.get(lti_session_key)

    course_user_info = db_get_course_user_info(lti_session_data)

    user_info = course_user_info.get('user_info', {})
    course_info = course_user_info.get('course_info', {})

    # TODO temporary workaround =======================================
    # TODO - for now, hardcoding collection for everyone in this phase.
    #        Need to pull owner's collection PIDs from Fedora dynamically.
    collection_pid = 'islandora:battleimagecollection'
    collection_title = 'Battle Image Collection'
    collection_description = collection_title
    owner_id = course_user_info['user_info']['user_id']

    try:
        NsCollection.objects.get(collection_pid=collection_pid)
    except NsCollection.DoesNotExist:
        try:
            ns_collection = NsCollection()
            ns_collection.collection_pid = collection_pid
            ns_collection.title = collection_title
            ns_collection.description = collection_description
            ns_collection.owner_id = owner_id
            ns_collection.ts_create = timezone.now()
            ns_collection.ts_modify = timezone.now()
            ns_collection.save()
        except Exception as ex:
            logger_main.error(ex)

    course_id = course_info.get('course_id', None)
    user_id = user_info.get('user_id', None)

    user_first_name = user_info.get('user_first_name', 'unknown')
    user_last_name = user_info.get('user_last_name', 'unknown')
    user_full_name = "{0} {1}".format(user_first_name, user_last_name)

    context_vars['user_full_name'] = user_full_name
    context_vars['sis_user_id'] = user_info.get('sis_user_id', 'unknown-eid')

    # TODO get collections from Fedora, merged with course-collections already stored.
    # collection_pid_list = get_fedora_collection_list(user_id)
    collection_list = db_get_fedora_collection_list(collection_pid, course_id)

    course_metadata_list = db_get_course_metadata(course_id)

    course_search_types = db_get_or_create_course_search_types(course_id)

    init_admin_config = {'course_metadata_list': course_metadata_list}

    init_admin_config = json.dumps(init_admin_config)

    context_vars['lti_session_key'] = lti_session_key
    context_vars['course_info'] = course_info
    context_vars['collection_list'] = collection_list
    context_vars['course_metadata_list'] = course_metadata_list
    context_vars['course_search_types'] = course_search_types
    context_vars['approve_threshold_list'] = range(2, 6)

    context_vars['init_admin_config'] = init_admin_config

    # Get user and course IDs from LTI session vars.
    # TODO Django get current host url?
    context_vars['host_url'] = request.META['HTTP_HOST']

    return render_to_response('admin.html',
                              context_vars,
                              context_instance=RequestContext(request))

@verify_authorization_admin
@verify_course_user
def admin_update(request):

    c = {}
    c.update(csrf(request))

    p = "admin_update"

    lti_session_key = request.session.get('lti_session_key', None)
    lti_session_data = request.session.get(lti_session_key)

    course_user_info = db_get_course_user_info(lti_session_data)

    course_info = course_user_info.get('course_info', {})

    course_id = course_info.get('course_id', None)

    if request.method == "POST":

        update_message = "Changes saved."

        num_matching_selections = request.POST.get('course_approve_threshold', 2)
        start_lat = request.POST.get('start_lng', 35)
        start_lng = request.POST.get('start_lng', 18)
        start_zoom = request.POST.get('start_zoom', 4)
        year_min = request.POST.get('year_min', None)
        year_max = request.POST.get('year_max', None)

        collection_id = request.POST.get('course_collection_select')
        course_metadata_list = request.POST.getlist('course_metadata_select')
        course_search_type_list = request.POST.getlist('course_search_type_select')

        if not course_search_type_list:
            update_message = "{0}<br>Note: You must select at least one search type.  ".format(update_message) + \
                             "One type has been defaulted."
            db_get_or_create_course_search_types(course_id)

        ns_course = db_admin_update_course_config(course_id,
                                                  num_matching_selections,
                                                  start_lat,
                                                  start_lng,
                                                  start_zoom,
                                                  year_min,
                                                  year_max)

        ns_course_collection = db_admin_update_course_collection(course_id,
                                                                 collection_id)

        ns_course_round = db_admin_update_course_round(course_id, 'Round 1')

        db_admin_update_course_search_types(course_id,
                                            course_search_type_list)

        db_admin_update_course_metadata(course_id,
                                        course_metadata_list)

        request.session['update_message'] = update_message

    entry_url = "/admin/?lk={0}".format(lti_session_key)

    rr = redirect(entry_url)
    return rr

@verify_authorization_admin
@verify_course_user
def admin_data(request):

    logger_main = logging.getLogger('main')

    lti_session_key = request.session.get('lti_session_key', None)
    lti_session_data = request.session.get(lti_session_key)

    course_user_info = db_get_course_user_info(lti_session_data)

    course_info = course_user_info.get('course_info', {})

    course_id = course_info.get('course_id', None)

    context = {}

    db_conneciton = connection.cursor()

    sql = "".join([

        "SELECT ",
            "ns_user.first_name, ",
            "ns_user.last_name, ",
            "ns_user.sis_user_id, ",
            "ns_user.email, ",
            "ns_image.image_pid, ",
            "ns_gaz_url.url, ",
            "ns_user_select_gaz_label.gaz_label_value ",
        "FROM ns_user_select ",
            "JOIN ns_course_image_area ON ns_user_select.course_image_area_id = ns_course_image_area.id ",
            "JOIN ns_image ON ns_course_image_area.image_id = ns_image.id ",
            "JOIN ns_user ON ns_user_select.user_id = ns_user.id ",
            "JOIN ns_user_select_gaz_url ON ns_user_select.id = ns_user_select_gaz_url.user_select_id ",
            "JOIN ns_gaz_url ON ns_user_select_gaz_url.gaz_url_id = ns_gaz_url.id ",
            "JOIN ns_user_select_gaz_label ON ns_user_select_gaz_url.gaz_url_id = ns_user_select_gaz_label.gaz_label_id ",
        "WHERE ns_user.first_name <> 'Test';"

    ])

    db_conneciton.execute(sql)
    context['query_main'] = db_conneciton.fetchall()
    db_conneciton.close()

    return render_to_response('admin-data.html', context, context_instance=RequestContext(request))

@verify_authorization_admin
@verify_course_user
def nav_admin_acceptance(request):

    context_vars = {}

    lti_session_key = request.session.get('lti_session_key', None)
    lti_session_data = request.session.get(lti_session_key)

    course_user_info = db_get_course_user_info(lti_session_data)

    context_vars['host_url'] = request.META['HTTP_HOST']

    user_info = course_user_info.get('user_info', {})
    course_info = course_user_info.get('course_info', {})

    course_id = course_info.get('course_id', None)
    owner_id = course_user_info['user_info']['user_id']

    user_first_name = user_info.get('user_first_name', 'unknown')
    user_last_name = user_info.get('user_last_name', 'unknown')
    user_full_name = "{0} {1}".format(user_first_name, user_last_name)

    context_vars['user_full_name'] = user_full_name
    context_vars['sis_user_id'] = user_info.get('sis_user_id', 'unknown-eid')
    context_vars['lti_session_key'] = lti_session_key

    # TODO temporary workaround
    # TODO - for now, hardcoding collection for everyone in this phase.
    #        Need to pull owner's collection PIDs from Fedora dynamically.
    collection_pid = 'islandora:battleimagecollection'

    course_round_info = db_get_active_course_round_info(course_id)

    course_collection_info = db_get_active_course_collection_info(course_id,
                                                                  collection_pid,
                                                                  owner_id)

    if not course_collection_info or not course_round_info:
        context_vars['err_title'] = 'Collection not found.'
        context_vars['err_message'] = 'Collection was not found for PID: {0}'.format(collection_pid)
        response = render_to_response('lobby/admin_lti_error.html',
                                      context_vars,
                                      context_instance=RequestContext(request))
        set_response_meta_nocache(response)
        return response

    collection_id = course_collection_info.get('collection_id', None)
    course_round_id = course_round_info.get('course_round_id', None)

    threshold_image_info = db_get_threshold_image_info(course_id,
                                                       collection_id,
                                                       course_round_id,
                                                       owner_id)
    if not threshold_image_info:
        context_vars['err_title'] = 'No qualifying images found.'
        context_vars['err_message'] = 'No qualifying images are available for review.'
        response = render_to_response('lobby/admin_lti_error.html',
                                      context_vars,
                                      context_instance=RequestContext(request))
        set_response_meta_nocache(response)
        return response

    last_cima_id = request.session.get('last_cima_id', -1)


    sorted_cima_id_list = sorted(k for k in threshold_image_info.keys())

    course_image_area_id = sorted_cima_id_list[0]

    next_found = False

    for idx, cima_id in enumerate(sorted_cima_id_list):

        if cima_id > last_cima_id:
            last_cima_id = cima_id
            course_image_area_id = cima_id
            next_found = True

    if not next_found:
        last_cima_id = -1

    request.session['last_cima_id'] = last_cima_id

    image_pid = threshold_image_info[course_image_area_id]['image_pid']

    total_threshold_images = len(threshold_image_info)

    fedora_image_url = construct_fedora_content_url(image_pid, 'JPG')

    context_vars['fedora_image_url'] = fedora_image_url

    threshold_gaz_info = db_get_threshold_gaz_info(course_id,
                                                   collection_id,
                                                   course_round_id,
                                                   course_image_area_id,
                                                   owner_id)

    (image_title, metadata_list) = get_image_metadata(image_pid,
                                                      course_id)

    vis_label_headers = db_get_visible_gaz_label_list()

    context_vars['threshold_gaz_info'] = threshold_gaz_info
    context_vars['threshold_image_info'] = threshold_image_info
    context_vars['total_threshold_images'] = total_threshold_images
    context_vars['vis_label_headers'] = vis_label_headers
    context_vars['image_title'] = image_title
    context_vars['metadata_list'] = metadata_list
    context_vars['course_image_area_id'] = course_image_area_id
    context_vars['course_round_id'] = course_round_id
    context_vars['collection_id'] = collection_id
    context_vars['owner_id'] = owner_id

    return render_to_response('admin_accept.html',
                              context_vars,
                              context_instance=RequestContext(request))

@verify_authorization_admin
@verify_course_user
def admin_accept_update(request):

    c = {}
    c.update(csrf(request))

    p = "admin_accept_update"

    lti_session_key = request.session.get('lti_session_key', None)
    # lti_session_data = request.session.get(lti_session_key)

    if request.method == "POST":

        btn_cancel = request.POST.get('btn_cancel', None)

        if btn_cancel:
            last_cima_id = request.session.get('last_cima_id', 1)
            request.session['last_cima_id'] = last_cima_id
            entry_url = "/admin-accept/?lk={0}".format(lti_session_key)

            rr = redirect(entry_url)
            return rr

        update_message = "Changes saved."

        course_round_id = request.POST.get('course_round_id')
        collection_id = request.POST.get('collection_id')
        course_image_area_id = request.POST.get('course_image_area_id')
        owner_id = request.POST.get('owner_id')

        gaz_selection_list = request.POST.getlist('gaz_selection')

        if not gaz_selection_list:
            update_message = "Changes not saved.  No gazetteer URLs were selected for approval.  "
        else:
            for gaz_item in gaz_selection_list:

                m = re.match("^(\d+)_(\d+)$", gaz_item)

                if m:
                    search_type_id = m.group(1)
                    gaz_id = m.group(2)

                    logger_main.info('search_type_id {0}'.format(search_type_id))
                    logger_main.info('gaz_id         {0}'.format(gaz_id))

                    db_admin_approve_update(course_round_id,
                                            collection_id,
                                            course_image_area_id,
                                            owner_id,
                                            search_type_id,
                                            gaz_id)

        request.session['update_message'] = update_message

    entry_url = "/admin-accept/?lk={0}".format(lti_session_key)

    rr = redirect(entry_url)
    return rr



