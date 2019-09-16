-- show student selection of gazetteers for each image
SELECT u.id as user_id, u.first_name as first_name, u.last_name as last_name,
  c.course_title as course_title, cround.id as round_id,
  cround.title as round_title, coll.title as collection_title,
  st.type_key as search_type, img.title as image_title,
  gu.url as gaz_url, pstat.status_key
FROM ns_user_select_gaz_url usgu
JOIN ns_user_select us ON us.id = usgu.user_select_id
JOIN ns_gaz_url gu ON gu.id = usgu.gaz_url_id
JOIN ns_search_type st ON st.id = usgu.search_type_id
JOIN ns_course_image_area cima ON cima.id = us.course_image_area_id
JOIN ns_image img ON img.id = cima.image_id
JOIN ns_course_round cround ON cround.id = us.course_round_id
JOIN ns_collection coll ON coll.id = us.collection_id
JOIN ns_user u ON u.id = us.user_id
JOIN ns_course c ON c.id = cround.course_id
JOIN ns_process_status pstat ON pstat.id = us.process_status_id
ORDER BY last_name, course_title, round_id, search_type, gaz_url

