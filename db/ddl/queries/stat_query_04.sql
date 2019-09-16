-- show users, image and gazetteer selections, including users with no activity
SELECT
  u.first_name as first_name, u.last_name as last_name,
  c.course_title AS course_title,
  cround.id      AS round_id,
  cround.title   AS round_title,
  coll.title     AS collection_title,
  st.type_key    AS search_type,
  img.title as image_title,
  gu.url as gazetteer_url
FROM ns_user u
LEFT JOIN ns_user_select us ON us.user_id = u.id
LEFT JOIN ns_course_round cround ON cround.id = us.course_round_id
LEFT JOIN ns_collection coll ON coll.id = us.collection_id
LEFT JOIN ns_course c ON c.id = cround.course_id
LEFT JOIN ns_user_select_gaz_url usgu ON usgu.user_select_id = us.id
LEFT JOIN ns_gaz_url gu ON gu.id = usgu.gaz_url_id
LEFT JOIN ns_search_type st ON st.id = usgu.search_type_id
LEFT JOIN ns_course_image_area cima ON cima.id = us.course_image_area_id
LEFT JOIN ns_image img ON img.id = cima.image_id
ORDER BY last_name, course_title, round_title, collection_title, search_type, image_title, gazetteer_url
