# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models




class NsCollection(models.Model):
    collection_pid = models.CharField(max_length=100)
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey('NsUser', models.DO_NOTHING)
    ts_create = models.DateTimeField()
    ts_modify = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ns_collection'


class NsCourse(models.Model):
    sis_course_id = models.CharField(max_length=100, blank=True, null=True)
    course_title = models.CharField(max_length=100, blank=True, null=True)
    canvas_course_id = models.IntegerField(blank=True, null=True)
    lti_course_id = models.CharField(max_length=100)
    num_matching_selections = models.IntegerField()
    start_lat = models.CharField(max_length=60, blank=True, null=True)
    start_lng = models.CharField(max_length=60, blank=True, null=True)
    start_zoom = models.IntegerField(blank=True, null=True)
    year_min = models.IntegerField(blank=True, null=True)
    year_max = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ns_course'


class NsCourseCollection(models.Model):
    course = models.ForeignKey(NsCourse, models.DO_NOTHING)
    collection = models.ForeignKey(NsCollection, models.DO_NOTHING)
    is_active = models.IntegerField()
    ts_create = models.DateTimeField()
    ts_modify = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ns_course_collection'
        unique_together = (('course', 'collection'),)


class NsCourseGazetteer(models.Model):
    course = models.ForeignKey(NsCourse, models.DO_NOTHING, blank=True, null=True)
    search_type = models.ForeignKey('NsSearchType', models.DO_NOTHING, blank=True, null=True)
    gazetteer = models.ForeignKey('NsGazetteer', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ns_course_gazetteer'
        unique_together = (('course', 'search_type', 'gazetteer'),)


class NsCourseImageArea(models.Model):
    course = models.ForeignKey(NsCourse, models.DO_NOTHING, blank=True, null=True)
    image = models.ForeignKey('NsImage', models.DO_NOTHING, blank=True, null=True)
    pos_top = models.IntegerField(blank=True, null=True)
    pos_left = models.IntegerField(blank=True, null=True)
    sel_width = models.IntegerField(blank=True, null=True)
    sel_height = models.IntegerField(blank=True, null=True)
    image_width = models.IntegerField(blank=True, null=True)
    image_height = models.IntegerField(blank=True, null=True)
    is_entire_image = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ns_course_image_area'
        unique_together = (('course', 'image', 'pos_top', 'pos_left', 'sel_width', 'sel_height', 'image_width', 'image_height'),)


class NsCourseMetadataTerm(models.Model):
    course = models.ForeignKey(NsCourse, models.DO_NOTHING)
    metadata_term = models.ForeignKey('NsMetadataTerm', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'ns_course_metadata_term'
        unique_together = (('course', 'metadata_term'),)


class NsCourseRound(models.Model):
    course = models.ForeignKey(NsCourse, models.DO_NOTHING)
    is_active = models.IntegerField()
    title = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'ns_course_round'


class NsCourseSearch(models.Model):
    course = models.ForeignKey(NsCourse, models.DO_NOTHING, blank=True, null=True)
    search_type = models.ForeignKey('NsSearchType', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ns_course_search'
        unique_together = (('course', 'search_type'),)


class NsCourseUser(models.Model):
    user = models.ForeignKey('NsUser', models.DO_NOTHING, blank=True, null=True)
    course = models.ForeignKey(NsCourse, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ns_course_user'
        unique_together = (('user', 'course'),)


class NsGazLabel(models.Model):
    label_key = models.CharField(unique=True, max_length=100)
    default_label = models.CharField(max_length=100)
    align = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'ns_gaz_label'


class NsGazUrl(models.Model):
    url = models.CharField(max_length=760)

    class Meta:
        managed = False
        db_table = 'ns_gaz_url'


class NsGazetteer(models.Model):
    gaz_key = models.CharField(unique=True, max_length=20)
    gaz_name = models.CharField(max_length=20)
    search_type = models.ForeignKey('NsSearchType', models.DO_NOTHING)
    url = models.CharField(max_length=100)
    is_active = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ns_gazetteer'


class NsImage(models.Model):
    collection = models.ForeignKey(NsCollection, models.DO_NOTHING)
    image_pid = models.CharField(max_length=100)
    title = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'ns_image'
        unique_together = (('collection', 'image_pid'),)


class NsMetadataTerm(models.Model):
    dcterm = models.CharField(max_length=100)
    type_key = models.CharField(max_length=100)
    dcterm_uri = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ns_metadata_term'
        unique_together = (('dcterm', 'type_key'),)


class NsProcessStatus(models.Model):
    id = models.IntegerField(primary_key=True)
    status_key = models.CharField(unique=True, max_length=10)
    status_title = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'ns_process_status'


class NsReviewGazStatus(models.Model):
    id = models.IntegerField(primary_key=True)
    status_key = models.CharField(unique=True, max_length=10)
    status_title = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'ns_review_gaz_status'


class NsReviewImageStatus(models.Model):
    id = models.IntegerField(primary_key=True)
    status_key = models.CharField(unique=True, max_length=10)
    status_title = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'ns_review_image_status'


class NsSearchGazLabel(models.Model):
    search_type = models.ForeignKey('NsSearchType', models.DO_NOTHING)
    gaz_label = models.ForeignKey(NsGazLabel, models.DO_NOTHING)
    display_order = models.IntegerField()
    is_sortable = models.IntegerField(blank=True, null=True)
    is_visible = models.IntegerField(blank=True, null=True)
    is_default_sort = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ns_search_gaz_label'
        unique_together = (('search_type', 'gaz_label'),)


class NsSearchType(models.Model):
    type_key = models.CharField(max_length=20, blank=True, null=True)
    type_name = models.CharField(max_length=20, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    display_order = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ns_search_type'


class NsUser(models.Model):
    email = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    sis_user_id = models.CharField(max_length=40, blank=True, null=True)
    canvas_user_id = models.IntegerField(blank=True, null=True)
    lti_user_id = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'ns_user'


class NsUserHistory(models.Model):
    user_select = models.ForeignKey('NsUserSelect', models.DO_NOTHING)
    bbox_geo_nw_lat = models.CharField(max_length=30, blank=True, null=True)
    bbox_geo_nw_long = models.CharField(max_length=30, blank=True, null=True)
    bbox_geo_se_lat = models.CharField(max_length=30, blank=True, null=True)
    bbox_geo_se_long = models.CharField(max_length=30, blank=True, null=True)
    year_begin = models.IntegerField(blank=True, null=True)
    year_end = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ns_user_history'


class NsUserHistoryGazetteer(models.Model):
    user_select = models.ForeignKey('NsUserSelect', models.DO_NOTHING, blank=True, null=True)
    gazetteer = models.ForeignKey(NsGazetteer, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ns_user_history_gazetteer'
        unique_together = (('user_select', 'gazetteer'),)


class NsUserHistoryKeywordClause(models.Model):
    user_select = models.ForeignKey('NsUserSelect', models.DO_NOTHING, blank=True, null=True)
    search_type = models.ForeignKey(NsSearchType, models.DO_NOTHING, blank=True, null=True)
    keyword_clause = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'ns_user_history_keyword_clause'
        unique_together = (('user_select', 'search_type'),)


class NsUserHistoryMetadataTerm(models.Model):
    user_select = models.ForeignKey('NsUserSelect', models.DO_NOTHING)
    metadata_term = models.ForeignKey(NsMetadataTerm, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'ns_user_history_metadata_term'
        unique_together = (('user_select', 'metadata_term'),)


class NsUserSelect(models.Model):
    user = models.ForeignKey(NsUser, models.DO_NOTHING, blank=True, null=True)
    course_image_area = models.ForeignKey(NsCourseImageArea, models.DO_NOTHING)
    collection = models.ForeignKey(NsCollection, models.DO_NOTHING)
    course_round = models.ForeignKey(NsCourseRound, models.DO_NOTHING)
    process_status = models.ForeignKey(NsProcessStatus, models.DO_NOTHING, blank=True, null=True)
    review_image_status = models.ForeignKey(NsReviewImageStatus, models.DO_NOTHING, blank=True, null=True)
    review_user_id = models.IntegerField(blank=True, null=True)
    ts_review = models.DateTimeField(blank=True, null=True)
    ts_submit = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ns_user_select'
        unique_together = (('user', 'course_image_area', 'collection', 'course_round'),)


class NsUserSelectGazLabel(models.Model):
    user_select_gaz_url = models.ForeignKey('NsUserSelectGazUrl', models.DO_NOTHING)
    gaz_label = models.ForeignKey(NsGazLabel, models.DO_NOTHING)
    gaz_label_value = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ns_user_select_gaz_label'
        unique_together = (('user_select_gaz_url', 'gaz_label'),)


class NsUserSelectGazUrl(models.Model):
    gaz_url = models.ForeignKey(NsGazUrl, models.DO_NOTHING)
    user_select = models.ForeignKey(NsUserSelect, models.DO_NOTHING)
    search_type = models.ForeignKey(NsSearchType, models.DO_NOTHING)
    course_image_area = models.ForeignKey(NsCourseImageArea, models.DO_NOTHING)
    review_gaz_status = models.ForeignKey(NsReviewGazStatus, models.DO_NOTHING, blank=True, null=True)
    review_user = models.ForeignKey(NsUser, models.DO_NOTHING, blank=True, null=True)
    ts_review = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ns_user_select_gaz_url'

