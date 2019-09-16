# -*- coding: UTF-8 -*
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from pprint import pprint, pformat
from m_common import *
from m_dao import *

__copyright__ = 'Copyright (c) 2016 The University of Texas at Austin'
__vcs_id__ = '$Id: v_main.py 33 2015-02-13 20:46:12Z mccookpv $'
__author__ = 'mccookpv'


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class SaveStudentSelection(APIView):
    @csrf_exempt
    def post(self, request):

        p = "SaveStudentSelection.post"

        refresh_msg = "Please refresh your browser page to load a new image."

        indata = request.data
        user_data = json.loads(indata.get('userData'))

        bbox_nw_lat = user_data.get('bbox_nw_lat', None)
        bbox_nw_lng = user_data.get('bbox_nw_lng', None)
        bbox_se_lat = user_data.get('bbox_se_lat', None)
        bbox_se_lng = user_data.get('bbox_se_lng', None)
        year_min = user_data.get('year_min', None)
        year_max = user_data.get('year_max', None)
        course_search_types = user_data.get('course_search_types', {})
        search_results = user_data.get('search_results', {})
        image_dimensions = user_data.get('image_dimensions', {})
        image_title = user_data.get('image_title', '')
        # metadata_list = user_data.get('metadata_list', {})
        collection_pid = user_data.get('collection_pid', None)
        image_pid = user_data.get('image_pid', None)
        course_round_id = user_data.get('course_round_id', None)
        lti_user_id = user_data.get('lti_user_id', None)
        lti_course_id = user_data.get('lti_course_id', None)
        process_status_id = user_data.get('process_status_id', 0)
        is_gaz_selected = user_data.get('is_gaz_selected', 0)

        logger_main.info("{0}: lti_user_id              {1}".format(p, lti_user_id))
        logger_main.info("{0}: lti_course_id            {1}".format(p, lti_course_id))
        logger_main.info("{0}: course_round_id          {1}".format(p, course_round_id))
        logger_main.info("{0}: collection_pid           {1}".format(p, collection_pid))
        logger_main.info("{0}: image_pid                {1}".format(p, image_pid))
        logger_main.info("{0}: bbox_nw_lat              {1}".format(p, bbox_nw_lat))
        logger_main.info("{0}: bbox_nw_lng              {1}".format(p, bbox_nw_lng))
        logger_main.info("{0}: bbox_se_lat              {1}".format(p, bbox_se_lat))
        logger_main.info("{0}: bbox_se_lng              {1}".format(p, bbox_se_lng))
        logger_main.info("{0}: year_min                 {1}".format(p, year_min))
        logger_main.info("{0}: year_max                 {1}".format(p, year_max))
        logger_main.info("{0}: course_search_types         ".format(p))
        logger_main.info(pformat(course_search_types))
        logger_main.info("{0}: search_results              ".format(p))
        logger_main.info(pformat(search_results))
        logger_main.info("{0}: image_dimensions            ".format(p))
        logger_main.info(pformat(image_dimensions))
        logger_main.info("{0}: process_status_id        {1}".format(p, process_status_id))
        logger_main.info("{0}: is_gaz_selected          {1}".format(p, is_gaz_selected))

        try:

            if not is_gaz_selected and process_status_id != 1:
                raise NanosourcerException(error_code=400,
                                           error_message="No gazetteer URL was selected. (00001)")

            try:
                ns_course_user = NsCourseUser.objects.get(course__lti_course_id=lti_course_id,
                                                          user__lti_user_id=lti_user_id)
                ns_course = ns_course_user.course
                ns_user = ns_course_user.user
            except NsCourseUser.DoesNotExist:
                raise NanosourcerException(error_code=404,
                                           error_message="User for this Course not found. (00002)")

            try:
                ns_collection = NsCollection.objects.get(collection_pid=collection_pid)
            except NsCollection.DoesNotExist:
                raise NanosourcerException(error_code=404,
                                           error_message="Collection not found. (00003)")

            course_id = ns_course.id

            gaz_label_key_id_dict = {}

            for stkey, stinfo in search_results.items():

                course_search_info = course_search_types.get(stkey, {})
                search_type_id = course_search_info.get('search_type_id', None)
                is_search_type_selected = course_search_info.get('is_selected', 0)

                if not search_type_id or not is_search_type_selected:
                    continue

                gaz_label_key_id_dict[stkey] = {}

                try:
                    NsSearchType.objects.get(id=search_type_id)
                except NsSearchType.DoesNotExist:
                    raise NanosourcerException(error_code=404,
                                               error_message="Search type not found for {0}. (00004)".format(stkey))

                stinfo['search_type_id'] = search_type_id

                columns = stinfo.get('columns', {})
                for colkey, colinfo in columns.items():
                    label_key = colinfo.get('label_key', None)
                    is_visible = colinfo.get('is_visible', 0)
                    if is_visible == 1:
                        try:
                            ns_gaz_label = NsGazLabel.objects.get(label_key=label_key)
                            gaz_label_key_id_dict[stkey][label_key] = ns_gaz_label.id
                        except NsGazLabel.DoesNotExist:
                            logger_main.error("{0}: ns_gaz_label.label_key not found {1}".format(p, label_key))
                            continue

            try:
                ns_image = NsImage.objects.get(image_pid=image_pid)
            except NsImage.DoesNotExist:
                try:
                    ns_image = NsImage()
                    ns_image.collection = ns_collection
                    ns_image.image_pid = image_pid
                    ns_image.title = image_title
                    ns_image.save()
                except Exception as savex:
                    logger_main.error("{0}: {1}".format(p, savex))
                    raise NanosourcerException(error_code=404,
                                               error_message="Unable to save image data. (00005)")

            pos_top = image_dimensions.get('top', None)
            pos_left = image_dimensions.get('left', None)
            sel_width = image_dimensions.get('sel_width', None)
            sel_height = image_dimensions.get('sel_height', None)
            image_width = image_dimensions.get('image_width', None)
            image_height = image_dimensions.get('image_height', None)
            is_entire_image = image_dimensions.get('is_entire_image', 0)

            if pos_top is None or pos_left is None or sel_width is None or sel_height is None:
                raise NanosourcerException(error_code=404,
                                           error_message="Image information is missing: {0}. (00006)".format(image_pid))

            try:
                ns_course_image_area = NsCourseImageArea.objects.get(image__id=ns_image.id,
                                                                     course__id=ns_course.id,
                                                                     pos_top=pos_top,
                                                                     pos_left=pos_left,
                                                                     sel_width=sel_width,
                                                                     sel_height=sel_height,
                                                                     image_width=image_width,
                                                                     image_height=image_height)
            except NsCourseImageArea.DoesNotExist:
                try:
                    ns_course_image_area = NsCourseImageArea()
                    ns_course_image_area.course = ns_course
                    ns_course_image_area.image = ns_image
                    ns_course_image_area.pos_top = pos_top
                    ns_course_image_area.pos_left = pos_left
                    ns_course_image_area.sel_width = sel_width
                    ns_course_image_area.sel_height = sel_height
                    ns_course_image_area.image_width = image_width
                    ns_course_image_area.image_height = image_height
                    ns_course_image_area.is_entire_image = is_entire_image
                    ns_course_image_area.save()
                except Exception as savex:
                    logger_main.error("{0}: {1}".format(p, savex))
                    raise NanosourcerException(error_code=404,
                                               error_message="Unable to save image selection. " +
                                                             "{0}. (00007)".format(refresh_msg))

            try:
                ns_user_select = NsUserSelect.objects.get(user=ns_user,
                                                          course_image_area=ns_course_image_area,
                                                          collection=ns_collection,
                                                          course_round__id=course_round_id)
                if ns_user_select.process_status_id == 2:
                    raise NanosourcerException(error_code=404,
                                               error_message="You have already processed this image. " +
                                                             "It cannot be updated. (00008)")
            except NsUserSelect.DoesNotExist:
                try:
                    ns_user_select = NsUserSelect()
                    ns_user_select.user = ns_user
                    ns_user_select.course_image_area = ns_course_image_area
                    ns_user_select.collection = ns_collection
                    ns_user_select.course_round_id = course_round_id
                    ns_user_select.review_image_status_id = 0
                    ns_user_select.review_user = None
                    ns_user_select.ts_review = None
                    ns_user_select.process_status_id = 0
                    ns_user_select.ts_submit = timezone.now()
                    ns_user_select.save()
                except Exception as savex:
                    logger_main.error("{0}: {1}".format(p, savex))
                    raise NanosourcerException(error_code=404,
                                               error_message="Unable to save user selections. " +
                                                             "{0}. (00009)".format(refresh_msg))

            try:
                NsUserHistory.objects.get(user_select__id=ns_user_select.id)
            except NsUserHistory.DoesNotExist:
                try:
                    ns_user_history = NsUserHistory()
                    ns_user_history.user_select_id = ns_user_select.id
                    ns_user_history.bbox_geo_nw_lat = bbox_nw_lat
                    ns_user_history.bbox_geo_nw_long = bbox_nw_lng
                    ns_user_history.bbox_geo_se_lat = bbox_se_lat
                    ns_user_history.bbox_geo_se_long = bbox_se_lng
                    if year_min:
                        ns_user_history.year_begin = year_min
                    if year_max:
                        ns_user_history.year_end = year_max
                    ns_user_history.save()
                except Exception as savex:
                    logger_main.error("{0}: {1}".format(p, savex))
                    raise NanosourcerException(error_code=404,
                                               error_message="Unable to save user selections. " +
                                                             "{0} (00010)".format(refresh_msg))

            NsUserHistoryMetadataTerm.objects.filter(user_select__id=ns_user_select.id).delete()

            ns_course_metadata_term_list = NsCourseMetadataTerm.objects.filter(course__id=ns_course.id)

            for cmt in ns_course_metadata_term_list:
                try:
                    ns_user_history_metadata_term = NsUserHistoryMetadataTerm()
                    ns_user_history_metadata_term.user_select_id = ns_user_select.id
                    ns_user_history_metadata_term.metadata_term_id = cmt.metadata_term_id
                    ns_user_history_metadata_term.save()
                except Exception as savex:
                    logger_main.error("{0}: {1}".format(p, savex))
                    raise NanosourcerException(error_code=404,
                                               error_message="Unable to save user selections. {0} " +
                                                             "(00011)".format(refresh_msg))

            for stkey, stinfo in search_results.items():

                search_type_id = stinfo.get('search_type_id', None)
                if not search_type_id:
                    continue

                keyword_str = stinfo.get('keyword_str', None)
                user_selections = stinfo.get('user_selections', {})

                if not user_selections:
                    # logger_main.error('{0}: {1}".format(No user selections for {1}'.format(stkey))
                    continue

                # label and gazetteerURI are always required.
                label = user_selections.get('label', None)
                gaz_url = user_selections.get('gazetteerURI', None)
                if not label:
                    logger_main.error('{0}: label not found in result'.format(p))
                    continue
                if not gaz_url:
                    logger_main.error('{0}: gazetteerURI not found in result'.format(p))
                    continue

                try:
                    ns_gaz_url = NsGazUrl.objects.get(url=gaz_url)
                except NsGazUrl.DoesNotExist:
                    ns_gaz_url = NsGazUrl()
                    ns_gaz_url.url = gaz_url
                    ns_gaz_url.save()

                try:
                    nug = NsUserSelectGazUrl.objects.get(gaz_url=ns_gaz_url,
                                                         user_select=ns_user_select)
                except NsUserSelectGazUrl.DoesNotExist:
                    try:
                        nug = NsUserSelectGazUrl()
                        nug.gaz_url_id = ns_gaz_url.id
                        nug.user_select_id = ns_user_select.id
                        nug.course_image_area = ns_course_image_area
                        nug.search_type_id = search_type_id
                        nug.review_gaz_status_id = 0
                        nug.review_user_id = None
                        nug.ts_review = None
                        nug.save()
                    except Exception as savex:
                        logger_main.error("{0}: {1}".format(p, savex))
                        raise NanosourcerException(error_code=404,
                                                   error_message="Unable to save user selections. " +
                                                                 "{0} (00012)".format(refresh_msg))
                except Exception as ex:
                    logger_main.error("{0}: {1}".format(p, ex))
                    raise NanosourcerException(error_code=404,
                                               error_message="Unable to save user selections. " +
                                                             "{0} (00013)".format(refresh_msg))

                for label_key, label_id in gaz_label_key_id_dict[stkey].items():

                    if user_selections.get(label_key, ''):
                        try:
                            if type(user_selections.get(label_key, '') == 'unicode'):
                                user_value = user_selections.get(label_key, ' ')
                            else:
                                user_value = user_selections[label_key].encode('UTF-8')
                        except Exception as uex:
                            logger_main.error("{0}: {1}".format(p, uex))
                            user_value = ''
                    else:
                        user_value = ''

                    if not label_id:
                        logger_main.error("NsGazLabel not found for label ID {0}".format(label_id))
                        continue

                    if not user_value:
                        user_value = ''

                    try:
                        NsUserSelectGazLabel.objects.get(user_select_gaz_url_id=nug.id,
                                                         gaz_label_id=label_id)

                    except NsUserSelectGazLabel.DoesNotExist:
                        try:
                            nusgl = NsUserSelectGazLabel()
                            nusgl.user_select_gaz_url = nug
                            nusgl.gaz_label_id = label_id
                            if user_value:
                                if isinstance(user_value, str):
                                    nusgl.gaz_label_value = user_value.decode('UTF-8')
                                elif isinstance(user_value, unicode):
                                    nusgl.gaz_label_value = user_value
                                elif isinstance(user_value, int):
                                    nusgl.gaz_label_value = user_value
                                else:
                                    logger_main.error(type(user_value))
                                    logger_main.error(user_value)
                                    nusgl.gaz_label_value = user_value
                            else:
                                nusgl.gaz_label_value = user_value
                            nusgl.save()
                        except Exception as savex:
                            logger_main.error("{0}: {1}".format(p, savex))
                            raise NanosourcerException(error_code=404,
                                                       error_message="Unable to save user selections. " +
                                                                     "{0} (00014)".format(refresh_msg))

                ns_course_gazetter_list = NsCourseGazetteer.objects.filter(course__id=course_id,
                                                                           search_type__id=search_type_id)

                NsUserHistoryGazetteer.objects.filter(user_select__id=ns_user_select.id).delete()

                for cg in ns_course_gazetter_list:
                    try:
                        ns_user_history_gazetteer = NsUserHistoryGazetteer()
                        ns_user_history_gazetteer.user_select_id = ns_user_select.id
                        ns_user_history_gazetteer.gazetteer_id = cg.gazetteer.id
                        ns_user_history_gazetteer.save()
                    except Exception as savex:
                        logger_main.error("{0}: {1}".format(p, savex))
                        raise NanosourcerException(error_code=404,
                                                   error_message="Unable to save user selections. " +
                                                                 "{0} (00015)".format(refresh_msg))

                if keyword_str:
                    try:
                        NsUserHistoryKeywordClause.objects.get(user_select__id=ns_user_select.id,
                                                               search_type__id=search_type_id)
                    except NsUserHistoryKeywordClause.DoesNotExist:
                        try:
                            ns_user_history_keyword_clause = NsUserHistoryKeywordClause()
                            ns_user_history_keyword_clause.user_select_id = ns_user_select.id
                            ns_user_history_keyword_clause.search_type_id = search_type_id
                            ns_user_history_keyword_clause.keyword_clause = keyword_str
                            ns_user_history_keyword_clause.save()
                        except Exception as savex:
                            logger_main.error("{0}: {1}".format(p, savex))
                            raise NanosourcerException(error_code=404,
                                                       error_message="Unable to save user selections. " +
                                                                     "{0} (00016)".format(refresh_msg))
                    except Exception as ex:
                        logger_main.error("{0}: {1}".format(p, ex))
                        raise NanosourcerException(error_code=404,
                                                   error_message="Unable to save user selections. " +
                                                                 "{0} (00017)".format(refresh_msg))

            try:
                ns_user_select = NsUserSelect.objects.get(user=ns_user,
                                                          course_image_area=ns_course_image_area,
                                                          collection=ns_collection,
                                                          course_round__id=course_round_id)
                if process_status_id == 1:
                    ns_user_select.process_status_id = 1
                else:
                    ns_user_select.process_status_id = 2
                ns_user_select.save()
            except NsUserSelect.DoesNotExist as dnex:
                logger_main.error("{0}: {1}".format(p, dnex))
                raise NanosourcerException(error_code=400,
                                           error_message="Unable to mark this image as processed. (00018)")
            except Exception as savex:
                logger_main.error("{0}: {1}".format(p, savex))
                raise NanosourcerException(error_code=404,
                                           error_message="Unable to save user selections. " +
                                                         "{0} (00019)".format(refresh_msg))

            response = JSONResponse({'info': 'success'},
                                    status=200)
            set_response_meta_nocache(response)
            return response

        except NanosourcerException as ne:

            response = JSONResponse({'info': ne.error_message},
                                    status=ne.error_code)
            set_response_meta_nocache(response)
            return response
