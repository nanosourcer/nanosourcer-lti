CREATE TABLE ns_course
(
  id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  sis_course_id VARCHAR(100),
  course_title VARCHAR(100),
  canvas_course_id INT(11),
  lti_course_id VARCHAR(100) NOT NULL,
  num_matching_selections INT(11) NOT NULL DEFAULT 2,
  start_lat VARCHAR(60) NULL,
  start_lng VARCHAR(60) NULL,
  start_zoom INT(11) NULL DEFAULT 4,
  year_min INT(11) NULL,
  year_max INT(11) NULL
);
CREATE UNIQUE INDEX ns_course_pk ON ns_course (id);
CREATE INDEX ns_course_idx1 ON ns_course (sis_course_id);
CREATE INDEX ns_course_idx2 ON ns_course (canvas_course_id);
CREATE INDEX ns_course_idx3 ON ns_course (lti_course_id);


CREATE TABLE ns_user
(
  id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  email VARCHAR(100),
  first_name VARCHAR(60) NOT NULL,
  last_name VARCHAR(60) NOT NULL,
  sis_user_id VARCHAR(40),
  canvas_user_id INT(11),
  lti_user_id VARCHAR(100) NOT NULL
);
CREATE UNIQUE INDEX ns_user_pk ON ns_user (id);
CREATE INDEX ns_user_idx1 ON ns_user (email);
CREATE INDEX ns_user_idx2 ON ns_user (sis_user_id);
CREATE INDEX ns_user_idx3 ON ns_user (canvas_user_id);
CREATE INDEX ns_user_idx4 ON ns_user (lti_user_id);


CREATE TABLE ns_collection
(
  id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  collection_pid VARCHAR(100) NOT NULL,
  title VARCHAR(100),
  description TEXT,
  owner_id INT(11) NOT NULL,
  ts_create TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  ts_modify TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  CONSTRAINT ns_collection_fk1 FOREIGN KEY (owner_id) REFERENCES ns_user (id)
);
CREATE UNIQUE INDEX ns_collection_pk ON ns_collection (id);
CREATE INDEX ns_collection_fk1 ON ns_collection (owner_id);
CREATE INDEX ns_collection_idx1 ON ns_collection (collection_pid);



CREATE TABLE ns_course_collection (
  id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  course_id INT(11) NOT NULL,
  collection_id INT(11) NOT NULL,
  is_active TINYINT(1) NOT NULL,
  ts_create TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  ts_modify TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  CONSTRAINT ns_course_collection_fk1 FOREIGN KEY (course_id) REFERENCES ns_course (id),
  CONSTRAINT ns_course_collection_fk2 FOREIGN KEY (collection_id) REFERENCES ns_collection (id)
);
CREATE UNIQUE INDEX ns_course_collection_pk ON ns_course_collection (id);
CREATE INDEX ns_course_collection_fk1 ON ns_course_collection (course_id);
CREATE INDEX ns_course_collection_fk2 ON ns_course_collection (collection_id);
CREATE UNIQUE INDEX ns_course_collection_comp1 ON ns_course_collection (course_id, collection_id);


CREATE TABLE ns_course_round
(
  id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  course_id INT(11) NOT NULL,
  is_active TINYINT(1) NOT NULL,
  title VARCHAR(100) NOT NULL,
  CONSTRAINT ns_course_round_fk1 FOREIGN KEY (course_id) REFERENCES ns_course (id)
);
CREATE UNIQUE INDEX ns_course_round_pk ON ns_course_round (id);
CREATE INDEX ns_course_round_fk1 ON ns_course_round (course_id);
CREATE INDEX ns_course_round_idx1 ON ns_course_round (title);


CREATE TABLE ns_course_user
(
  id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  user_id INT(11),
  course_id INT(11),
  CONSTRAINT ns_course_user_fk1 FOREIGN KEY (user_id) REFERENCES ns_user (id),
  CONSTRAINT ns_course_user_fk2 FOREIGN KEY (course_id) REFERENCES ns_course (id)
);
CREATE UNIQUE INDEX ns_course_user_pk ON ns_course_user (id);
CREATE INDEX ns_course_user_fk1 ON ns_course_user (user_id);
CREATE INDEX ns_course_user_fk2 ON ns_course_user (course_id);
CREATE UNIQUE INDEX ns_course_user_comp1 ON ns_course_user (user_id, course_id);




CREATE TABLE ns_image
(
  id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  collection_id INT(11) NOT NULL,
  image_pid VARCHAR(100) NOT NULL,
  title VARCHAR(200) NULL,
  CONSTRAINT ns_image_fk1 FOREIGN KEY (collection_id) REFERENCES ns_collection (id)
);
CREATE UNIQUE INDEX ns_image_pk ON ns_image (id);
CREATE INDEX ns_image_fk1 ON ns_image (collection_id);
CREATE UNIQUE INDEX ns_image_comp1 ON ns_image (collection_id, image_pid);


CREATE TABLE ns_course_image_area
(
  id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  course_id INT(11),
  image_id INT(11),
  pos_top INT(11),
  pos_left INT(11),
  sel_width INT(11),
  sel_height INT(11),
  image_width INT(11),
  image_height INT(11),
  is_entire_image TINYINT(1),
  CONSTRAINT ns_course_image_area_fk1 FOREIGN KEY (course_id) REFERENCES ns_course (id),
  CONSTRAINT ns_course_image_area_fk2 FOREIGN KEY (image_id) REFERENCES ns_image (id)
);
CREATE UNIQUE INDEX ns_course_image_area_pk ON ns_course_image_area (id);
CREATE INDEX ns_course_image_area_fk1 ON ns_course_image_area (course_id);
CREATE INDEX ns_course_image_area_fk2 ON ns_course_image_area (image_id);
CREATE UNIQUE INDEX ns_course_image_area_comp1 ON ns_course_image_area (course_id,
                                                                        image_id,
                                                                        pos_top,
                                                                        pos_left,
                                                                        sel_width,
                                                                        sel_height,
                                                                        image_width,
                                                                        image_height);


CREATE TABLE ns_search_type
(
  id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  type_key VARCHAR(20),
  type_name VARCHAR(20),
  description VARCHAR(100),
  display_order INT(11)
);
CREATE UNIQUE INDEX ns_search_type_pk ON ns_search_type (id);
CREATE INDEX ns_search_type_idx1 ON ns_search_type (type_key);



CREATE TABLE ns_course_search
(
  id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  course_id INT(11),
  search_type_id INT(11),
  CONSTRAINT ns_course_search_fk1 FOREIGN KEY (course_id) REFERENCES ns_course (id),
  CONSTRAINT ns_course_search_fk2 FOREIGN KEY (search_type_id) REFERENCES ns_search_type (id)
);
CREATE UNIQUE INDEX ns_course_search_pk ON ns_course_search (id);
CREATE INDEX ns_course_search_fk1 ON ns_course_search (course_id);
CREATE INDEX ns_course_search_fk2 ON ns_course_search (search_type_id);
CREATE UNIQUE INDEX ns_course_search_comp1 ON ns_course_search (course_id, search_type_id);




CREATE TABLE ns_gazetteer
(
  id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  gaz_key VARCHAR(20) NOT NULL,
  gaz_name VARCHAR(20) NOT NULL,
  search_type_id INT(11) NOT NULL,
  url VARCHAR(100) NOT NULL,
  is_active TINYINT(1) DEFAULT 1,
  CONSTRAINT ns_gazetteer_fk1 FOREIGN KEY (search_type_id) REFERENCES ns_search_type (id)
);
CREATE UNIQUE INDEX ns_gazetteer_pk ON ns_gazetteer (id);
CREATE INDEX ns_gazetteer_fk1 ON ns_gazetteer (search_type_id);
CREATE UNIQUE INDEX ns_gazetteer_idx1 ON ns_gazetteer (gaz_key);


CREATE TABLE ns_course_gazetteer
(
  id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  course_id INT(11),
  search_type_id INT(11),
  gazetteer_id INT(11),
  CONSTRAINT ns_course_gazetteer_fk1 FOREIGN KEY (course_id) REFERENCES ns_course (id),
  CONSTRAINT ns_course_gazetteer_fk2 FOREIGN KEY (search_type_id) REFERENCES ns_search_type (id),
  CONSTRAINT ns_course_gazetteer_fk3 FOREIGN KEY (gazetteer_id) REFERENCES ns_gazetteer (id)
);
CREATE UNIQUE INDEX ns_course_gazetteer_pk ON ns_course_gazetteer (id);
CREATE INDEX ns_course_gazetteer_fk1 ON ns_course_gazetteer (course_id);
CREATE INDEX ns_course_gazetteer_fk2 ON ns_course_gazetteer (search_type_id);
CREATE INDEX ns_course_gazetteer_fk3 ON ns_course_gazetteer (gazetteer_id);
CREATE UNIQUE INDEX ns_course_gazetteer_comp1 ON ns_course_gazetteer (course_id, search_type_id, gazetteer_id);



CREATE TABLE ns_metadata_term
(
  id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  dcterm VARCHAR(100) NOT NULL,
  type_key VARCHAR(100) NOT NULL,
  dcterm_uri VARCHAR(200) NULL
);
CREATE UNIQUE INDEX ns_metadata_term_pk ON ns_metadata_term (id);
CREATE UNIQUE INDEX ns_metadata_term_comp1 ON ns_metadata_term (dcterm, type_key);




CREATE TABLE ns_course_metadata_term
(
    id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    course_id INT(11) NOT NULL,
    metadata_term_id INT(11) NOT NULL,
    CONSTRAINT ns_course_metadata_term_fk1 FOREIGN KEY (course_id) REFERENCES ns_course (id),
    CONSTRAINT ns_course_metadata_term_fk2 FOREIGN KEY (metadata_term_id) REFERENCES ns_metadata_term (id)
);
CREATE UNIQUE INDEX ns_course_metadata_term_pk ON ns_course_metadata_term (id);
CREATE INDEX ns_course_metadata_term_fk1 ON ns_course_metadata_term (course_id);
CREATE INDEX ns_course_metadata_term_fk2 ON ns_course_metadata_term (metadata_term_id);
CREATE UNIQUE INDEX ns_course_metadata_term_comp1 ON ns_course_metadata_term (course_id, metadata_term_id);





CREATE TABLE ns_gaz_url
(
  id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  url VARCHAR(760) NOT NULL
);
CREATE UNIQUE INDEX ns_gaz_url_pk ON ns_gaz_url (id);
-- CREATE UNIQUE INDEX ns_gaz_url_idx1 ON ns_gaz_url (url);


CREATE TABLE ns_gaz_label
(
    id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    label_key VARCHAR(100) NOT NULL,
    default_label VARCHAR(100) NOT NULL,
    align VARCHAR(10) NOT NULL DEFAULT 'left'
);
CREATE UNIQUE INDEX ns_gaz_label_pk ON ns_gaz_label (id);
CREATE UNIQUE INDEX ns_gaz_label_key_idx1 ON ns_gaz_label (label_key);



CREATE TABLE ns_search_gaz_label
(
  id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  search_type_id INT(11) NOT NULL,
  gaz_label_id INT(11) NOT NULL,
  display_order INT(11) NOT NULL,
  is_sortable TINYINT(1) DEFAULT 0,
  is_visible TINYINT(1) DEFAULT 0,
  is_default_sort TINYINT(11) DEFAULT 0,
  CONSTRAINT ns_search_gaz_label_fk1 FOREIGN KEY (search_type_id) REFERENCES ns_search_type (id),
  CONSTRAINT ns_course_gaz_label_fk2 FOREIGN KEY (gaz_label_id) REFERENCES ns_gaz_label (id)
);
CREATE UNIQUE INDEX ns_search_gaz_label_pk ON ns_search_gaz_label (id);
CREATE UNIQUE INDEX ns_search_gaz_label_comp1 ON ns_search_gaz_label (search_type_id, gaz_label_id);

CREATE TABLE ns_review_image_status
(
  id INT(11) PRIMARY KEY NOT NULL,
  status_key VARCHAR(10) NOT NULL,
  status_title VARCHAR(50) NOT NULL
);
CREATE UNIQUE INDEX ns_review_image_status_pk ON ns_review_image_status (id);
CREATE UNIQUE INDEX ns_review_image_status_idx ON ns_review_image_status (status_key);


CREATE TABLE ns_review_gaz_status
(
  id INT(11) PRIMARY KEY NOT NULL,
  status_key VARCHAR(10) NOT NULL,
  status_title VARCHAR(50) NOT NULL
);
CREATE UNIQUE INDEX ns_review_gaz_status_pk ON ns_review_gaz_status (id);
CREATE UNIQUE INDEX ns_review_gaz_status_idx ON ns_review_gaz_status (status_key);


CREATE TABLE ns_process_status
(
  id INT(11) PRIMARY KEY NOT NULL,
  status_key VARCHAR(10) NOT NULL,
  status_title VARCHAR(50) NOT NULL
);
CREATE UNIQUE INDEX ns_process_status_pk ON ns_process_status (id);
CREATE UNIQUE INDEX ns_process_status_idx ON ns_process_status (status_key);


CREATE TABLE ns_user_select
(
  id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  user_id INT(11),
  course_image_area_id INT(11) NOT NULL,
  collection_id INT(11) NOT NULL,
  course_round_id INT(11) NOT NULL,
  process_status_id INT(11) DEFAULT 0,
  review_image_status_id INT(11) DEFAULT '0',
  review_user_id INT(11) NULL,
  ts_review TIMESTAMP NULL,
  ts_submit TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  CONSTRAINT ns_user_select_fk1 FOREIGN KEY (user_id) REFERENCES ns_user (id),
  CONSTRAINT ns_user_select_fk2 FOREIGN KEY (course_image_area_id) REFERENCES ns_course_image_area (id),
  CONSTRAINT ns_user_select_fk3 FOREIGN KEY (collection_id) REFERENCES ns_collection (id),
  CONSTRAINT ns_user_select_fk4 FOREIGN KEY (course_round_id) REFERENCES ns_course_round (id),
  CONSTRAINT ns_user_select_fk5 FOREIGN KEY (review_image_status_id) REFERENCES ns_review_image_status (id),
  CONSTRAINT ns_user_select_fk6 FOREIGN KEY (process_status_id) REFERENCES ns_process_status (id)
);
CREATE UNIQUE INDEX ns_user_select_pk ON ns_user_select (id);
CREATE INDEX ns_user_select_fk1 ON ns_user_select (user_id);
CREATE INDEX ns_user_select_fk2 ON ns_user_select (course_image_area_id);
CREATE INDEX ns_user_select_fk3 ON ns_user_select (collection_id);
CREATE INDEX ns_user_select_fk4 ON ns_user_select (course_round_id);
CREATE INDEX ns_user_select_fk5 ON ns_user_select (review_image_status_id);
CREATE INDEX ns_user_select_fk6 ON ns_user_select (process_status_id);
CREATE UNIQUE INDEX ns_user_select_comp1 ON ns_user_select (user_id, course_image_area_id, collection_id, course_round_id);



CREATE TABLE ns_user_select_gaz_url
(
  id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  gaz_url_id INT(11) NOT NULL,
  user_select_id INT(11) NOT NULL,
  search_type_id INT(11) NOT NULL,
  course_image_area_id INT(11) NOT NULL,
  review_gaz_status_id INT(11) DEFAULT '0',
  review_user_id INT(11) NULL,
  ts_review TIMESTAMP NULL,
  CONSTRAINT ns_user_select_gaz_url_fk1 FOREIGN KEY (gaz_url_id)     REFERENCES ns_gaz_url (id),
  CONSTRAINT ns_user_select_gaz_url_fk2 FOREIGN KEY (user_select_id) REFERENCES ns_user_select (id),
  CONSTRAINT ns_user_select_gaz_url_fk3 FOREIGN KEY (search_type_id) REFERENCES ns_search_type (id),
  CONSTRAINT ns_user_select_gaz_url_fk4 FOREIGN KEY (review_user_id) REFERENCES ns_user (id),
  CONSTRAINT ns_user_select_gaz_url_fk5 FOREIGN KEY (course_image_area_id) REFERENCES ns_course_image_area (id),
  CONSTRAINT ns_user_select_gaz_url_fk6 FOREIGN KEY (review_gaz_status_id) REFERENCES ns_review_gaz_status (id)
);
CREATE UNIQUE INDEX ns_user_select_gaz_url_pk ON ns_user_select_gaz_url (id);
CREATE INDEX ns_user_select_gaz_url_fk1 ON ns_user_select_gaz_url (gaz_url_id);
CREATE INDEX ns_user_select_gaz_url_fk2 ON ns_user_select_gaz_url (user_select_id);
CREATE INDEX ns_user_select_gaz_url_fk3 ON ns_user_select_gaz_url (search_type_id);
CREATE INDEX ns_user_select_gaz_url_fk4 ON ns_user_select_gaz_url (review_user_id);
CREATE INDEX ns_user_select_gaz_url_fk5 ON ns_user_select_gaz_url (course_image_area_id);
CREATE INDEX ns_user_select_gaz_url_fk6 ON ns_user_select_gaz_url (review_gaz_status_id);


CREATE TABLE ns_user_select_gaz_label
(
  id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  user_select_gaz_url_id INT(11) NOT NULL,
  gaz_label_id INT(11) NOT NULL,
  gaz_label_value VARCHAR(2000),
  CONSTRAINT ns_user_select_gaz_label_fk1 FOREIGN KEY (user_select_gaz_url_id) REFERENCES ns_user_select_gaz_url (id),
  CONSTRAINT ns_user_select_gaz_label_fk2 FOREIGN KEY (gaz_label_id) REFERENCES ns_gaz_label (id)
);
CREATE UNIQUE INDEX ns_user_select_gaz_label_pk ON ns_user_select_gaz_label (id);
CREATE INDEX ns_user_select_gaz_label_fk1 ON ns_user_select_gaz_label (user_select_gaz_url_id);
CREATE INDEX ns_user_select_gaz_label_fk2 ON ns_user_select_gaz_label (gaz_label_id);
CREATE UNIQUE INDEX ns_user_select_gaz_label_comp1 ON ns_user_select_gaz_label (user_select_gaz_url_id, gaz_label_id);





CREATE TABLE ns_user_history
(
    id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    user_select_id INT(11) NOT NULL,
    bbox_geo_nw_lat VARCHAR(30),
    bbox_geo_nw_long VARCHAR(30),
    bbox_geo_se_lat VARCHAR(30),
    bbox_geo_se_long VARCHAR(30),
    year_begin INT(11),
    year_end INT(11),
    CONSTRAINT ns_user_history_fk1 FOREIGN KEY (user_select_id) REFERENCES ns_user_select (id)
);
CREATE UNIQUE INDEX ns_user_history_pk ON ns_user_history (id);
CREATE INDEX ns_user_history_fk1 ON ns_user_history (user_select_id);


CREATE TABLE ns_user_history_gazetteer
(
    id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    user_select_id INT(11),
    gazetteer_id INT(11),
    CONSTRAINT ns_user_history_gazetteer_fk1 FOREIGN KEY (user_select_id) REFERENCES ns_user_select (id),
    CONSTRAINT ns_user_history_gazetteer_fk2 FOREIGN KEY (gazetteer_id) REFERENCES ns_gazetteer (id)
);
CREATE UNIQUE INDEX ns_user_history_gazetteer_pk ON ns_user_history_gazetteer (id);
CREATE INDEX ns_user_history_gazetteer_fk1 ON ns_user_history_gazetteer (user_select_id);
CREATE INDEX ns_user_history_gazetteer_fk2 ON ns_user_history_gazetteer (gazetteer_id);
CREATE UNIQUE INDEX ns_user_history_gazetteer_comp1 ON ns_user_history_gazetteer (user_select_id, gazetteer_id);


CREATE TABLE ns_user_history_keyword_clause
(
    id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    user_select_id INT(11),
    search_type_id INT(11),
    keyword_clause VARCHAR(200) NOT NULL,
    CONSTRAINT ns_user_history_keyword_clause_fk1 FOREIGN KEY (user_select_id) REFERENCES ns_user_select (id),
    CONSTRAINT ns_user_history_keyword_clause_fk2 FOREIGN KEY (search_type_id) REFERENCES ns_search_type (id)
);
CREATE UNIQUE INDEX ns_user_history_keyword_clause_pk ON ns_user_history_keyword_clause (id);
CREATE INDEX ns_user_history_keyword_clause_fk1 ON ns_user_history_keyword_clause (user_select_id);
CREATE INDEX ns_user_history_keyword_clause_fk2 ON ns_user_history_keyword_clause (search_type_id);
CREATE UNIQUE INDEX ns_user_history_keyword_clause ON ns_user_history_keyword_clause (user_select_id, search_type_id);



CREATE TABLE ns_user_history_metadata_term
(
  id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
  user_select_id INT(11) NOT NULL,
  metadata_term_id INT(11) NOT NULL,
  CONSTRAINT ns_user_history_metadata_term_fk1 FOREIGN KEY (user_select_id) REFERENCES ns_user_select (id),
  CONSTRAINT ns_user_history_metadata_term_fk2 FOREIGN KEY (metadata_term_id) REFERENCES ns_metadata_term (id)
);
CREATE UNIQUE INDEX ns_user_history_metadata_term_pk ON ns_user_history_metadata_term (id);
CREATE INDEX ns_user_history_metadata_term_fk1 ON ns_user_history_metadata_term (user_select_id);
CREATE INDEX ns_user_history_metadata_term_fk2 ON ns_user_history_metadata_term (metadata_term_id);
CREATE UNIQUE INDEX ns_user_history_metadata_term_comp1 ON ns_user_history_metadata_term (user_select_id, metadata_term_id);


