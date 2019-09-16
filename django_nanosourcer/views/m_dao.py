# -*- coding: UTF-8 -*-
import logging
import re
from StringIO import StringIO
from random import randrange

import requests
from PIL import Image
from django.conf import settings
from django.utils import timezone

from django_nanosourcer.models import *

__copyright__ = 'Copyright (c) 2016 The University of Texas at Austin'
__author__ = 'mccookpv'

logger_main = logging.getLogger("main")


def construct_fedora_content_url(pid, obj_type):
    fedora_image_url = "{0}/objects/{1}/datastreams/{2}/content".format(settings.FEDORA_ROOT,
                                                                        pid,
                                                                        obj_type)
    return fedora_image_url


def get_fedora_image_dimensions(fedora_image_url):
    p = "get_fedora_image_dimensions"

    img_dims = {'top': 0,
                'left': 0,
                'sel_width': 0,
                'sel_height': 0,
                'image_width': 0,
                'image_height': 0,
                'is_entire_image': 1}

    response = requests.get(fedora_image_url)
    img_buf = StringIO(response.content)

    try:
        img_check = Image.open(img_buf)
        (img_w, img_h) = img_check.size
        img_dims['sel_width'] = img_w
        img_dims['sel_height'] = img_h
        img_dims['image_width'] = img_w
        img_dims['image_height'] = img_h

    except IOError as ioex:
        logger_main.error("{0}: {1}".format(p, ioex))
    except ImportError as ieex:
        logger_main.error("{0}: {1}".format(p, ieex))

    return img_dims


def db_admin_update_course_search_types(course_id,
                                        course_search_type_list):
    NsCourseGazetteer.objects.filter(course_id=course_id).delete()
    NsCourseSearch.objects.filter(course_id=course_id).delete()

    for type_id in course_search_type_list:
        ns_course_search = NsCourseSearch()
        ns_course_search.course_id = course_id
        ns_course_search.search_type_id = type_id
        ns_course_search.save()

        ns_gazetteer_list = NsGazetteer.objects.filter(search_type__id=type_id)
        for gaz in ns_gazetteer_list:
            ns_course_gazetteer = NsCourseGazetteer()
            ns_course_gazetteer.course_id = course_id
            ns_course_gazetteer.search_type_id = type_id
            ns_course_gazetteer.gazetteer_id = gaz.id
            ns_course_gazetteer.save()


def db_admin_update_course_metadata(course_id,
                                    course_metadata_list):
    NsCourseMetadataTerm.objects.filter(course_id=course_id).delete()

    for term_id in course_metadata_list:
        ns_course_metadata_term = NsCourseMetadataTerm()
        ns_course_metadata_term.course_id = course_id
        ns_course_metadata_term.metadata_term_id = term_id
        ns_course_metadata_term.save()


def db_admin_update_course_collection(course_id,
                                      collection_id=None):
    ns_course_collection_list = NsCourseCollection.objects.filter(course__id=course_id)

    for ncc in ns_course_collection_list:
        ncc.is_active = 0
        ncc.save()

    if collection_id:
        try:
            ns_course_collection = NsCourseCollection.objects.get(course__id=course_id)
            ns_course_collection.is_active = 1
            ns_course_collection.save()
        except NsCourseCollection.DoesNotExist:
            ns_course_collection = NsCourseCollection()
            ns_course_collection.course_id = course_id
            ns_course_collection.collection_id = collection_id
            ns_course_collection.is_active = 1
            ns_course_collection.ts_create = timezone.now()
            ns_course_collection.ts_modify = timezone.now()
            ns_course_collection.save()
            return ns_course_collection

    return None


def db_admin_update_course_round(course_id,
                                 title):
    ns_course_round_list = NsCourseRound.objects.filter(course__id=course_id)

    for ncr in ns_course_round_list:
        ncr.is_active = 0
        ncr.save()

    try:
        ns_course_round = NsCourseRound.objects.get(course__id=course_id)
        ns_course_round.is_active = 1
        ns_course_round.save()
    except NsCourseRound.DoesNotExist:
        ns_course_round = NsCourseRound()
        ns_course_round.course_id = course_id
        ns_course_round.title = title
        ns_course_round.is_active = 1
        ns_course_round.save()

    return ns_course_round


def db_admin_update_course_config(course_id,
                                  num_matching_selections,
                                  start_lat,
                                  start_lng,
                                  start_zoom,
                                  year_min,
                                  year_max):
    p = 'db_admin_update_course_config'

    try:
        ns_course = NsCourse.objects.get(id=course_id)
        ns_course.num_matching_selections = num_matching_selections
        ns_course.start_lat = start_lat
        ns_course.start_lng = start_lng
        ns_course.start_zoom = start_zoom
        ns_course.year_min = year_min
        ns_course.year_max = year_max
        ns_course.save()
        return ns_course
    except NsCourse.DoesNotExist:
        return None
    except Exception as ex:
        logger_main.error('{0}: {1}'.format(p, ex))
        return None


def db_get_collection_pid(collection_id):
    try:
        ns_collection = NsCollection.objects.get(id=collection_id)
        return ns_collection.collection_pid
    except NsCollection.DoesNotExist:
        return None


def build_gaz_config():
    gaz_config = {}

    sql = "SELECT sg.id, sg.display_order, sg.is_sortable, " + \
          "sg.is_visible, sg.is_default_sort, " + \
          "st.type_key, gz.gaz_name, gz.url, " \
          "gz.gaz_key, gb.label_key, gb.default_label, gb.align " \
          "FROM ns_search_gaz_label sg " \
          "JOIN ns_gazetteer gz ON gz.search_type_id = sg.search_type_id " \
          "JOIN ns_search_type st ON st.id = sg.search_type_id " \
          "JOIN ns_gaz_label gb ON gb.id = sg.gaz_label_id " \
          "WHERE gz.is_active = 1 "

    ns_search_gaz_label_list = NsSearchGazLabel.objects.raw(sql)

    for sg in ns_search_gaz_label_list:

        display_order = "{0:03}".format(sg.display_order)
        is_sortable = sg.is_sortable
        is_visible = sg.is_visible
        is_default_sort = sg.is_default_sort
        type_key = sg.type_key
        gaz_key = sg.gaz_key
        gaz_name = sg.gaz_name
        gaz_url = sg.url
        label_key = sg.label_key
        align = sg.align
        default_label = sg.default_label

        if type_key not in gaz_config:
            gaz_config[type_key] = {'gaz_dict': {},
                                    'columns': {}}

        gaz_dict = gaz_config[type_key]['gaz_dict']

        if gaz_key not in gaz_dict:
            gaz_config[type_key]['gaz_dict'][gaz_key] = {'gaz_name': gaz_name,
                                                         'gaz_url': gaz_url
                                                         }

        if is_default_sort:
            gaz_config[type_key]['default_sort'] = label_key

        gaz_config[type_key]['columns'][display_order] = {'label_key': label_key,
                                                          'default_label': default_label,
                                                          'is_sortable': is_sortable,
                                                          'is_visible': is_visible,
                                                          'align': align}

    return gaz_config


def db_get_processed_image_list(user_id,
                                course_round_id):
    image_pid_list = []

    ns_user_select = NsUserSelect.objects.filter(user__id=user_id,
                                                 course_round__id=course_round_id,
                                                 process_status_id=2)
    for nus in ns_user_select:
        image_pid = nus.course_image_area.image.image_pid
        image_pid_list.append(image_pid)

    return image_pid_list


def get_random_image_pid(collection_pid,
                         user_id,
                         course_round_id,
                         last_image_pid=None,
                         limit=None):

    fedora_image_list = get_fedora_image_list(collection_pid)

    # fedora_image_list = mock_get_fedora_image_pid_list(limit=limit)

    if limit:
        fedora_image_list = fedora_image_list[0:limit]

    processed_image_list = db_get_processed_image_list(user_id,
                                                       course_round_id)

    out_list = [pid for pid in fedora_image_list if pid not in processed_image_list]

    if not out_list:
        return None

    if last_image_pid and len(out_list) > 1:
        if last_image_pid in out_list:
            out_list.remove(last_image_pid)

    if len(out_list) < 1:
        return None

    img_idx = randrange(0, len(out_list))
    image_pid = out_list[img_idx]

    return image_pid


def get_db_course_user_info(lti_course_id,
                            lti_user_id):
    try:
        ns_user = NsUser.objects.get(lti_user_id=lti_user_id)
    except NsUser.DoesNotExist:
        return None

    try:
        ns_course = NsCourse.objects.get(lti_course_id=lti_course_id)
    except NsCourse.DoesNotExist:
        return None

    try:
        ns_course_user = NsCourseUser.objects.get(user=ns_user,
                                                  course=ns_course)

        course_user_info = {'id': ns_course_user.id,
                            'course_id': ns_course_user.course.id,
                            'user_id': ns_course_user.user.id}
    except NsCourseUser.DoesNotExist:
        ns_course_user = NsCourseUser()
        ns_course_user.user = ns_user
        ns_course_user.course = ns_course
        ns_course_user.save()
        course_user_info = {'id': ns_course_user.id,
                            'course_id': ns_course_user.course.id,
                            'user_id': ns_course_user.user.id}

    return course_user_info


def db_get_course_user_info(lti_session_data):
    lti_course_id = lti_session_data.get('context_id', None)
    lti_user_id = lti_session_data.get('user_id', None)

    if not lti_course_id or not lti_user_id:
        return None

    try:
        ns_course_user = NsCourseUser.objects.get(user__lti_user_id=lti_user_id,
                                                  course__lti_course_id=lti_course_id)
    except NsCourseUser.DoesNotExist:

        try:
            ns_course = NsCourse.objects.get(lti_course_id=lti_course_id)
        except NsCourse.DoesNotExist:
            ns_course = NsCourse()
            ns_course.lti_course_id = lti_course_id
            ns_course.course_title = lti_session_data.get('context_title', 'unknown course ')
            ns_course.sis_course_id = lti_session_data.get('lis_course_offering_sourcedid', 'unknown')
            ns_course.canvas_course_id = lti_session_data.get('custom_canvas_course_id', 'unknown')
            ns_course.num_matching_selections = 2
            ns_course.start_lat = '0'
            ns_course.start_lng = '0'
            ns_course.start_zoom = 4
            ns_course.year_min = -5000
            ns_course.year_max = 2000

            ns_course.save()
        except Exception as ex:
            logger_main.info(ex)
            return None

        try:
            ns_user = NsUser.objects.get(lti_user_id=lti_user_id)
        except NsUser.DoesNotExist:
            ns_user = NsUser()
            ns_user.lti_user_id = lti_user_id
            ns_user.first_name = lti_session_data.get('lis_person_name_given', 'unknown')
            ns_user.last_name = lti_session_data.get('lis_person_name_family', 'unknown')
            ns_user.email = lti_session_data.get('lis_person_contact_email_primary', 'unknown')
            ns_user.sis_user_id = lti_session_data.get('lis_person_sourcedid', 'unknown')
            ns_user.canvas_user_id = lti_session_data.get('custom_canvas_user_id', 'unknown')
            ns_user.save()
        except Exception as ex:
            logger_main.info(ex)
            return None

        user_id = ns_user.id
        course_id = ns_course.id

        ns_course_user = NsCourseUser()
        ns_course_user.user_id = user_id
        ns_course_user.course_id = course_id
        ns_course_user.save()

    course_user_id = ns_course_user.id

    sql = "SELECT uc.*, " + \
          "c.id as course_id, c.sis_course_id, c.course_title, " \
          "c.canvas_course_id, c.lti_course_id, " \
          "c.num_matching_selections, " \
          "u.id as user_id, u.sis_user_id, u.email, u.first_name, " \
          "u.last_name, u.canvas_user_id, u.lti_user_id " \
          "FROM ns_course_user uc " \
          "LEFT JOIN ns_user u ON u.id = uc.user_id " \
          "LEFT JOIN ns_course c ON c.id = uc.course_id " \
          "WHERE uc.id = {0} ".format(course_user_id)

    uc_list = NsCourseUser.objects.raw(sql)

    course_user_info = {}

    for uc in uc_list:
        course_user_info = {'course_user_id': uc.id,
                            'user_info': {'user_id': uc.user_id,
                                          'user_email': uc.email,
                                          'user_first_name': uc.first_name,
                                          'user_last_name': uc.last_name,
                                          'sis_user_id': uc.sis_user_id,
                                          'canvas_user_id': uc.canvas_user_id,
                                          'lti_user_id': uc.lti_user_id,
                                          },
                            'course_info': {'course_id': uc.course_id,
                                            'sis_course_id': uc.sis_course_id,
                                            'course_title': uc.course_title,
                                            'canvas_course_id': uc.canvas_course_id,
                                            'lti_course_id': uc.lti_course_id,
                                            'num_matching_selections': uc.num_matching_selections
                                            }
                            }

    return course_user_info


def db_get_course_search_types(course_id):
    search_type_list = []

    sql = "SELECT st.*, " + \
          "cs.course_id as course_id " \
          "FROM ns_search_type st " \
          "LEFT JOIN ns_course_search cs ON cs.search_type_id = st.id " \
          "                              AND cs.course_id = {0} " \
          "ORDER BY st.display_order ".format(course_id)

    st_list = NsSearchType.objects.raw(sql)

    for st in st_list:
        if not st.course_id:
            is_selected = 0
        else:
            is_selected = 1
        item = {'search_type_id': st.id,
                'type_key': st.type_key,
                'type_name': st.type_name,
                'description': st.description,
                'is_selected': is_selected
                }
        search_type_list.append(item)

    return search_type_list


def db_get_or_create_course_search_types(course_id):
    search_type_list = db_get_course_search_types(course_id)

    is_add_default_course_search = True

    for item in search_type_list:

        is_selected = item.get('is_selected', None)
        if is_selected:
            is_add_default_course_search = False

    if is_add_default_course_search:
        try:
            result_list = NsSearchType.objects.all()[:1]
            if result_list:
                ns_search_type = result_list[0]
                ns_course_search = NsCourseSearch()
                ns_course_search.course_id = course_id
                ns_course_search.search_type = ns_search_type
                ns_course_search.save()
                search_type_list = db_get_course_search_types(course_id)
        except NsSearchType.DoesNotExist:
            return search_type_list

    return search_type_list


def db_get_course_metadata(course_id):
    metadata_list = []

    sql = "SELECT m.*, " + \
          "cm.course_id as course_id " \
          "FROM ns_metadata_term m " \
          "LEFT JOIN ns_course_metadata_term cm ON cm.metadata_term_id = m.id " \
          "                                     AND cm.course_id = {0} " \
          "ORDER BY m.dcterm, m.type_key ".format(course_id)

    ns_metadata_list = NsMetadataTerm.objects.raw(sql)

    for nsm in ns_metadata_list:
        if not nsm.course_id:
            is_selected = 0
        else:
            is_selected = 1
        item = {'metadata_term_id': nsm.id,
                'dcterm': nsm.dcterm,
                'type_key': nsm.type_key,
                'dcterm_uri': nsm.dcterm_uri,
                'is_selected': is_selected
                }
        metadata_list.append(item)

    return metadata_list


def db_get_course_metadata_tuples(course_id):
    metadata_tuples = []

    sql = "SELECT m.*, " + \
          "cm.course_id as course_id " \
          "FROM ns_metadata_term m " \
          "LEFT JOIN ns_course_metadata_term cm ON cm.metadata_term_id = m.id " \
          "WHERE cm.course_id = {0} " \
          "ORDER BY m.dcterm, m.type_key ".format(course_id)

    ns_metadata_list = NsMetadataTerm.objects.raw(sql)

    for nsm in ns_metadata_list:
        item = (nsm.dcterm, nsm.type_key)
        metadata_tuples.append(item)

    return metadata_tuples


# TODO -- temporary parameter of hard-coded collection pid.
def db_get_fedora_collection_list(collection_pid,
                                  course_id):
    collection_list = []

    sql = "SELECT coll.*, " + \
          "cc.is_active as is_active " \
          "FROM ns_collection coll " \
          "LEFT JOIN ns_course_collection cc ON cc.collection_id = coll.id " \
          "                                  AND cc.course_id = '{1}' " \
          "WHERE coll.collection_pid = '{0}' " \
          "ORDER BY coll.collection_pid ".format(collection_pid, course_id)

    ns_collection_list = NsCollection.objects.raw(sql)

    for nsc in ns_collection_list:
        is_active = nsc.is_active
        if not is_active:
            is_active = 0
        info = {'collection_id': nsc.id,
                'collection_pid': nsc.collection_pid,
                'title': nsc.title,
                'description': nsc.description,
                'is_active': is_active
                }

        collection_list.append(info)

    return collection_list


def get_active_collection(course_id):
    try:
        ns_course_collection = NsCourseCollection.objects.get(course_id=course_id,
                                                              is_active=1)
        return ns_course_collection
    except NsCourseCollection.DoesNotExist:
        return None


def get_course_round(course_id):
    try:
        ns_course_round = NsCourseRound.objects.get(course=course_id)
        return ns_course_round
    except NsCourseRound.DoesNotExist:
        return None


def get_fedora_image_list(collection_pid):
    s = requests.Session()

    s.auth = (settings.FEDORA_USER, settings.FEDORA_PASSWORD)

    qpref = 'SELECT ?s '
    sparql = qpref + 'FROM <#ri> where ' + \
             '{ ?s<info:fedora/fedora-system:def/relations-external#isMemberOfCollection> <info:fedora/' + \
             collection_pid + "> }"

    post_data = {'query': sparql,
                 'type': 'tuples',
                 'lang': 'sparql',
                 'format': 'json',
                 'dt': 'on'
                 }

    url = "{0}/risearch".format(settings.FEDORA_ROOT)

    response = s.post(url, data=post_data)

    item_list = response.json().get('results', [])

    pid_list = []

    for item in item_list:

        val = item.get('s', None)
        if not val or 'info:fedora/' not in val:
            continue
        val = re.sub('info:fedora/', '', val)
        pid_list.append(val)

    return pid_list


def get_image_metadata(image_pid,
                       course_id):
    p = "get_image_metadata"

    fedora_metadata_json_url = construct_fedora_content_url(image_pid, 'JSON')
    response = requests.get(fedora_metadata_json_url)

    if response.status_code != 200:
        logger_main.error('{0}: Unable to find JSON for this image URL {1}'.format(p,
                                                                                   fedora_metadata_json_url))
        return []

    course_metadata_tuples = db_get_course_metadata_tuples(course_id)

    chunk = response.json()

    metadata_list = []

    image_title = chunk.get('title', '')
    metadata = chunk.get('metadata', [])

    for item in metadata:

        dc_term = item.get('dcTerm', None)
        type_key = item.get('type', None)

        if (dc_term, type_key) in course_metadata_tuples:
            metadata_list.append(item)

    return image_title, metadata_list


def db_get_active_course_round_info(course_id):
    course_round_info = None

    ns_course_round = NsCourseRound.objects.filter(course__id=course_id,
                                                   is_active=1)[:1]

    if ns_course_round:
        ncr = ns_course_round[0]

        course_round_info = {'course_id': course_id,
                             'course_round_id': ncr.id,
                             'title': ncr.title
                             }

    return course_round_info


def db_get_active_course_collection_info(course_id,
                                         collection_pid,
                                         owner_id):
    course_collection_info = None

    ns_course_collection = NsCourseCollection.objects.filter(course__id=course_id,
                                                             collection__collection_pid=collection_pid,
                                                             is_active=1)[:1]
    if ns_course_collection:
        ncc = ns_course_collection[0]

        course_collection_info = {'course_id': course_id,
                                  'collection_id': ncc.collection.id,
                                  'collection_pid': ncc.collection.collection_pid,
                                  'title': ncc.collection.title,
                                  'description': ncc.collection.description,
                                  'owner_id': ncc.collection.owner_id
                                  }

    return course_collection_info


def db_get_threshold_image_info(course_id,
                                collection_id,
                                course_round_id,
                                owner_id):
    """
    Qualifying images having associated gazetteers meeting the selection threshold.
    """

    threshold_image_info = {}

    # result = NsUserSelect.objects.raw(sql)

    sql = "SELECT DISTINCT cima.id, img.image_pid, a.gaz_url_count " + \
          "FROM (SELECT st.id as search_type_id, " \
          "             st.type_key as search_type_key, " \
          "             st.type_name as search_type_name, " \
          "             cima.id as cima_id, " \
          "             gaz_url.id as gaz_url_id, " \
          "             gaz_url.url as gaz_url, " \
          "      COUNT(*) as gaz_url_count " \
          "      FROM ns_user_select us " \
          "          JOIN ns_user_select_gaz_url ugu ON ugu.user_select_id = us.id " \
          "          JOIN ns_search_type st ON st.id = ugu.search_type_id " \
          "          JOIN ns_gaz_url gaz_url ON gaz_url.id = ugu.gaz_url_id " \
          "          JOIN ns_collection coll ON coll.id = us.collection_id " \
          "          JOIN ns_course_image_area cima ON cima.id = ugu.course_image_area_id" \
          "          JOIN ns_course_collection crs_coll ON crs_coll.id = us.collection_id " \
          "          JOIN ns_course_round crs_round ON crs_round.id = us.course_round_id " \
          "          JOIN ns_course c ON c.id = crs_round.course_id " \
          "          WHERE (us.process_status_id = 0 or us.process_status_id IS NULL) " \
          "          AND c.id = {0} " \
          "          AND us.collection_id = {1} " \
          "          AND crs_coll.id = {1} " \
          "          AND crs_coll.is_active = 1 " \
          "          AND crs_round.id = {2} " \
          "          AND crs_round.is_active = 1 " \
          "          AND (us.review_image_status_id IS NULL OR us.review_image_status_id != 1) " \
          "          GROUP BY st.id, cima.id, gaz_url.id, c.num_matching_selections " \
          "          HAVING COUNT(*) >= c.num_matching_selections) a " \
          "JOIN ns_search_type st ON st.id = a.search_type_id " \
          "JOIN ns_user_select_gaz_url ugu ON ugu.gaz_url_id = a.gaz_url_id AND ugu.search_type_id = st.id " \
          "JOIN ns_user_select us ON us.id = ugu.user_select_id " \
          "JOIN ns_course_image_area cima ON cima.id = ugu.course_image_area_id " \
          "JOIN ns_image img ON img.id = cima.image_id " \
          "JOIN ns_course_collection crs_coll ON crs_coll.id = us.collection_id " \
          "JOIN ns_course_round crs_round ON crs_round.id = us.course_round_id " \
          "JOIN ns_course c ON c.id = crs_round.course_id " \
          "WHERE us.collection_id = {1} " \
          "AND (us.process_status_id = 0 or us.process_status_id IS NULL) " \
          "AND c.id = {0} " \
          "AND crs_coll.id = {1} " \
          "AND crs_coll.is_active = 1 " \
          "AND crs_round.id = {2} " \
          "AND crs_round.is_active = 1 " \
          "AND (us.review_image_status_id IS NULL OR us.review_image_status_id != 1) " \
          "AND cima.is_entire_image = 1 " \
          "AND cima.image_width = cima.sel_width " \
          "AND cima.image_height = cima.sel_height " \
          "AND cima.pos_top = 0 " \
          "AND cima.pos_left = 0 " \
          "ORDER BY cima.id; ".format(course_id,
                                      collection_id,
                                      course_round_id)

    # logger_main.info(sql)

    ns_course_image_area_list = NsCourseImageArea.objects.raw(sql)

    for cima in ns_course_image_area_list:
        course_image_area_id = cima.id
        image_pid = cima.image_pid
        gaz_url_count = cima.gaz_url_count

        image_info = threshold_image_info.get(course_image_area_id, {})

        image_info['image_pid'] = image_pid
        image_info['gaz_url_count'] = gaz_url_count

        threshold_image_info[course_image_area_id] = image_info

    # logger_main.info(json.dumps(threshold_image_info))

    return threshold_image_info


def db_get_threshold_gaz_info(course_id,
                              collection_id,
                              course_round_id,
                              course_image_area_id,
                              owner_id):
    """
    Search type gaz_urls with label values
    """

    threshold_gaz_info = {}

    sql = "SELECT DISTINCT st.id, " + \
          "      st.type_key as search_type_key, " \
          "      st.type_name as search_type_name, " \
          "      gaz_url.id as gaz_url_id, " \
          "      gaz_url.url as gaz_url, " \
          "      sgl.display_order as label_display_order, " \
          "      gl.label_key, " \
          "      gl.default_label, " \
          "      usgl.gaz_label_value, " \
          "      a.gaz_url_count " \
          "FROM (SELECT st.id as search_type_id, " \
          "             st.type_key as search_type_key, " \
          "             st.type_name as search_type_name, " \
          "             gaz_url.id as gaz_url_id, " \
          "             gaz_url.url as gaz_url, " \
          "             COUNT(*) as gaz_url_count " \
          "      FROM ns_user_select us " \
          "      JOIN ns_user_select_gaz_url ugu ON ugu.user_select_id = us.id " \
          "      JOIN ns_search_type st ON st.id = ugu.search_type_id " \
          "      JOIN ns_gaz_url gaz_url ON gaz_url.id = ugu.gaz_url_id " \
          "      JOIN ns_course_image_area cima ON cima.id = us.course_image_area_id " \
          "      JOIN ns_image img ON img.id = cima.image_id " \
          "      JOIN ns_course c ON c.id = cima.course_id " \
          "      JOIN ns_course_collection crs_coll ON crs_coll.id = us.collection_id " \
          "      JOIN ns_collection coll ON coll.id = img.collection_id " \
          "      JOIN ns_course_round crs_round ON crs_round.id = us.course_round_id AND crs_round.course_id = c.id " \
          "      WHERE cima.is_entire_image = 1 " \
          "      AND   cima.id = {3} " \
          "      AND   us.process_status_id = 0 " \
          "      AND   c.id = {0} " \
          "      AND   coll.id = {1} " \
          "      AND   us.collection_id = {1} " \
          "      AND   crs_coll.collection_id = {1} " \
          "      AND   crs_coll.is_active = 1 " \
          "      AND   crs_round.id = {2} " \
          "      AND   crs_round.is_active = 1 " \
          "      AND (us.review_image_status_id IS NULL OR us.review_image_status_id != 2) " \
          "      GROUP BY st.id, gaz_url.id, c.num_matching_selections " \
          "      HAVING COUNT(*) >= c.num_matching_selections) a " \
          "JOIN ns_search_type st ON st.id = a.search_type_id " \
          "JOIN ns_user_select_gaz_url usgu ON usgu.gaz_url_id = a.gaz_url_id AND usgu.search_type_id = st.id " \
          "JOIN ns_user_select us ON us.id = usgu.user_select_id " \
          "JOIN ns_user_select_gaz_label usgl ON usgl.user_select_gaz_url_id = usgu.id " \
          "JOIN ns_gaz_label gl ON gl.id = usgl.gaz_label_id " \
          "JOIN ns_search_gaz_label sgl ON sgl.gaz_label_id = gl.id " \
          "JOIN ns_gaz_url gaz_url ON gaz_url.id = a.gaz_url_id " \
          "WHERE sgl.is_visible = 1 " \
          "AND   (us.review_image_status_id IS NULL OR us.review_image_status_id != 2) " \
          "ORDER BY st.id, gaz_url_id, sgl.display_order ".format(course_id,
                                                                  collection_id,
                                                                  course_round_id,
                                                                  course_image_area_id)

    # logger_main.info(sql)

    visible_label_info = db_get_visible_gaz_label_list()

    visible_default_label_info = db_get_visible_gaz_default_label_info()

    ns_search_type_list = NsSearchType.objects.raw(sql)

    for st_rec in ns_search_type_list:

        gaz_url_id = st_rec.gaz_url_id
        search_type_id = st_rec.id
        search_type_key = st_rec.search_type_key
        search_type_name = st_rec.search_type_name
        gaz_url = st_rec.gaz_url
        label_key = st_rec.label_key
        default_label = st_rec.default_label
        gaz_label_value = st_rec.gaz_label_value

        vis_label_info = visible_label_info.get(search_type_key, {})
        vis_default_label_info = visible_default_label_info.get(search_type_key, {})

        if label_key not in vis_label_info:
            continue

        vis_label_do = vis_label_info[label_key]

        st_info = threshold_gaz_info.get(search_type_key, {})

        gaz_url_list = st_info.get('gaz_url_list', {})

        gaz_info = gaz_url_list.get(gaz_url_id, {})

        gaz_label_info = gaz_info.get('gaz_label_info', {})

        gaz_info['gaz_url'] = gaz_url

        gaz_label_info[vis_label_do] = {'label_key': label_key,
                                        'default_label': default_label,
                                        'label_value': gaz_label_value
                                        }

        gaz_url_list[gaz_url_id] = gaz_info

        gaz_info['gaz_label_info'] = gaz_label_info

        st_info['gaz_url_list'] = gaz_url_list

        st_info['search_type_id'] = search_type_id
        st_info['search_type_name'] = search_type_name
        st_info['vis_label_list'] = [a[0] for a in sorted(vis_default_label_info.items(), key=lambda (k, v): (v, k))]

        threshold_gaz_info[search_type_key] = st_info

    return threshold_gaz_info


def db_get_visible_gaz_label_list():
    visible_label_info = {}

    gaz_label_list = NsSearchGazLabel.objects.filter(is_visible=1)

    for gl in gaz_label_list:
        search_type_key = gl.search_type.type_key
        gaz_label_key = gl.gaz_label.label_key
        display_order = gl.display_order

        gaz_label_info = visible_label_info.get(search_type_key, {})

        gaz_label_info[gaz_label_key] = "{0:09}".format(display_order)

        visible_label_info[search_type_key] = gaz_label_info

    return visible_label_info


def db_get_visible_gaz_default_label_info():
    visible_label_info = {}

    gaz_label_list = NsSearchGazLabel.objects.filter(is_visible=1)

    for gl in gaz_label_list:
        search_type_key = gl.search_type.type_key
        gaz_label_key = gl.gaz_label.label_key
        gaz_default_label = gl.gaz_label.default_label
        display_order = gl.display_order

        gaz_label_info = visible_label_info.get(search_type_key, {})

        gaz_label_info[gaz_default_label] = "{0:09}".format(display_order)

        visible_label_info[search_type_key] = gaz_label_info

    return visible_label_info


def db_admin_approve_update(course_round_id,
                            collection_id,
                            course_image_area_id,
                            owner_id,
                            search_type_id,
                            gaz_id):
    ns_user_select_gaz_url_list = NsUserSelectGazUrl.objects.filter(gaz_url__id=gaz_id,
                                                                    search_type__id=search_type_id,
                                                                    user_select__collection__id=collection_id,
                                                                    user_select__course_round__id=course_round_id,
                                                                    user_select__course_image_area__id=course_image_area_id
                                                                    )

    for usgu in ns_user_select_gaz_url_list:
        usgu.review_user_id = owner_id
        usgu.review_gaz_status_id = 2
        usgu.ts_review = timezone.now()
        usgu.save()

    ns_user_select_list = NsUserSelect.objects.filter(course_round__id=course_round_id,
                                                      collection__id=collection_id,
                                                      course_image_area__id=course_image_area_id)
    for us in ns_user_select_list:
        us.review_user_id = owner_id
        us.review_image_status_id = 2
        us.ts_review = timezone.now()
        us.save()


def mock_get_fedora_image_pid_list(limit=None):

    pid_list = ["islandora:1853",
                "islandora:1843",
                "islandora:1774",
                "islandora:1825",
                "islandora:1860",
                "islandora:1828",
                "islandora:1844",
                "islandora:1839",
                "islandora:1812",
                "islandora:1857",
                "islandora:1721",
                "islandora:1870",
                "islandora:1785",
                "islandora:1868",
                "islandora:1745",
                "islandora:1776",
                "islandora:1849",
                "islandora:1761",
                "islandora:1855",
                "islandora:1852",
                "islandora:1879",
                "islandora:1773",
                "islandora:1763",
                "islandora:1796",
                "islandora:1838",
                "islandora:1799",
                "islandora:1821",
                "islandora:1804",
                "islandora:1748",
                "islandora:1808",
                "islandora:1807",
                "islandora:1779",
                "islandora:1833",
                "islandora:1861"
                ]

    end_range = limit if limit else len(pid_list)

    return [pid_list[idx] for idx in range(0, end_range)]

def get_fedora_collection_list(lti_session_data):

    id_key = 'facultyCollection'

    s = requests.Session()

    s.auth = (settings.FEDORA_USER, settings.FEDORA_PASSWORD)

    qstr = "objects/?pid=true&identifier=true&label=true" + \
             "&query=identifier~*{0}*+ownerId={1}".format(id_key, owner_id)

    url = "{0}/{1}".format(settings.FEDORA_ROOT, qstr)

    params = {u'resultFormat': u'xml'}

    response = s.get(url, params=params)
    print(response.content)

    return []

# def get_db_user_info(lti_user_id,
#                      userInfo=None):
#     try:
#         ns_user = NsUser.objects.get(lti_user_id=lti_user_id)
#         userInfo = {'id': ns_user.id,
#                     'lti_user_id': lti_user_id,
#                     'last_name': ns_user.last_name,
#                     'first_name': ns_user.first_name,
#                     'email': ns_user.email,
#                     'eid': ns_user.eid,
#                     'canvas_user_id': ns_user.canvas_user_id}
#     except NsUser.DoesNotExist:
#         if userInfo:
#             ns_user = NsUser()
#             ns_user.lti_user_id = lti_user_id
#             ns_user.email = userInfo.get('email', None)
#             ns_user.first_name = userInfo.get('first_name', None)
#             ns_user.last_name = userInfo.get('last_name', None)
#             ns_user.eid = userInfo.get('eid', None)
#             ns_user.canvas_user_id = userInfo.get('canvas_user_id', None)
#             ns_user.save()
#             userInfo['id'] = ns_user.id
#
#     return userInfo
#
#
# def get_db_course_info(lti_course_id,
#                        courseInfo=None):
#     courseInfo = {'id': 1,
#                   'lti_course_id': 'lti_dev_02',
#                   'canvas_course_id': None,
#                   'sis_course_id': None}
#
#     try:
#         ns_course = NsCourse.objects.get(lti_course_id=lti_course_id)
#         courseInfo = {'id': ns_course.id,
#                       'lti_course_id': lti_course_id,
#                       'sis_course_id': ns_course.sis_course_id,
#                       'canvas_course_id': ns_course.canvas_course_id}
#     except NsCourse.DoesNotExist:
#         if courseInfo:
#             ns_course = NsCourse()
#             ns_course.lti_course_id = lti_course_id
#             ns_course.sis_course_id = courseInfo.get('sis_course_id', None)
#             ns_course.canvas_course_id = courseInfo.get('canvas_course_id', None)
#             ns_course.save()
#             courseInfo['id'] = ns_course.id
#
#     return courseInfo
