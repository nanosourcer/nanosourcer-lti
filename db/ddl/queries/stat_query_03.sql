-- show gazetteers having at least two or more matches per image
SELECT
  c.course_title AS course_title,
  cround.id      AS round_id,
  cround.title   AS round_title,
  coll.title     AS collection_title,
  st.type_key    AS search_type,
  img.image_pid  AS image_pid,
  img.title      AS image_title,
  gu.url         AS gazetteer_url,
  count(*)       AS gazetteer_count
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
GROUP BY course_title, round_id, round_title, collection_title, search_type, image_pid, image_title, gazetteer_url
HAVING count(*) >= 2
ORDER BY course_title, round_id, round_title, collection_title, search_type, image_pid, image_title, gazetteer_url,
  gazetteer_count DESC;



