INSERT INTO ns_metadata_term (id, dcterm, type_key, dcterm_uri)
VALUES
  (1, 'title', 'Title', 'http://purl.org/dc/terms/title '),
  (2, 'date', 'Date (Scanned)', 'http://purl.org/dc/terms/date'),
  (3, 'description', 'Basic Image Description', 'http://purl.org/dc/terms/description'),
  (4, 'creator', 'Creator of Image', 'http://purl.org/dc/terms/creator'),
  (5, 'spatial', 'Spatial Coverage (Location)', 'http://purl.org/dc/terms/spatial'),
  (6, 'description', 'Additional Image Description', 'http://purl.org/dc/terms/description'),
  (7, 'date', 'Image Subject Date', 'http://purl.org/dc/terms/date'),
  (8, 'date', 'Image as an Object Date', 'http://purl.org/dc/terms/date'),
  (9, 'date', 'Copyright Date', 'http://purl.org/dc/terms/date'),
  (10, 'publisher', 'Publisher', 'http://purl.org/dc/terms/publisher'),
  (11, 'format', 'Resource Format', 'http://purl.org/dc/terms/format'),
  (12, 'creator', 'Creator (Scan)', 'http://purl.org/dc/terms/creator'),
  (13, 'description', 'Note from Image Processing', 'http://purl.org/dc/terms/description');


INSERT INTO ns_search_type (id, type_key, type_name, description, display_order)
VALUES
  (1, 'place', 'Place', 'Place description', 1),
  (2, 'period', 'Period', 'Period description', 2);


INSERT INTO ns_gazetteer (id, gaz_key, gaz_name, search_type_id, url, is_active)
VALUES
  (1, 'pleiades', 'Pleiades', 1, 'http://pleiades.stoa.org/', 1),
  (2, 'periodo', 'Periodo', 2, 'http://perio.do/', 1);


INSERT INTO ns_gaz_label (id, label_key, default_label, align)
VALUES
  (1, 'label', 'Title', 'left'),
  (2, 'secondaryLabel', 'Description', 'left'),
  (3, 'spatialLabel', 'Spatial Label', 'left'),
  (4, 'lat', 'Lat', 'left'),
  (5, 'long', 'Long', 'left'),
  (6, 'dateMin', 'Date Min', 'right'),
  (7, 'dateMax', 'Date Max', 'right'),
  (8, 'gazetteerURI', 'URI', 'left');


INSERT INTO ns_search_gaz_label (id, search_type_id, gaz_label_id, display_order, is_sortable, is_visible, is_default_sort)
VALUES
  (1,  1, 1, 1, 1, 1, 1),
  (2,  1, 2, 2, 0, 1, 0),
  (3,  1, 3, 3, 1, 1, 0),
  (4,  1, 4, 4, 0, 0, 0),
  (5,  1, 5, 5, 0, 0, 0),
  (6,  1, 6, 6, 0, 0, 0),
  (7,  1, 7, 7, 0, 0, 0),
  (8,  1, 8, 8, 0, 0, 0),

  (9,  2, 1, 1, 1, 1, 1),
  (10, 2, 2, 2, 0, 0, 0),
  (11, 2, 3, 3, 0, 1, 0),
  (12, 2, 4, 4, 0, 0, 0),
  (13, 2, 5, 5, 0, 0, 0),
  (14, 2, 6, 6, 0, 1, 0),
  (15, 2, 7, 7, 0, 1, 0),
  (16, 2, 8, 8, 0, 0, 0);


INSERT INTO ns_review_image_status (id, status_key, status_title)
    VALUES
      (0, 'pending', 'Pending'),
      (1, 'incomplete', 'Incomplete'),
      (2, 'complete', 'Complete');

INSERT INTO ns_review_gaz_status (id, status_key, status_title)
VALUES
  (0, 'pending', 'Pending'),
  (1, 'rejected', 'Rejected'),
  (2, 'accepted', 'Accepted');


INSERT INTO ns_process_status (id, status_key, status_title)
VALUES
  (0, 'pending', 'Pending'),
  (1, 'abandoned', 'Abandoned'),
  (2, 'processed', 'Processed');

