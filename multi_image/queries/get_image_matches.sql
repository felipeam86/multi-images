WITH thumbnail_imgs AS (
    SELECT
        pi.image_id,
        pi.processed_image_uri,
        gt.name
    FROM public.processed_images AS pi
    INNER JOIN public.raw_images AS ri ON pi.image_id = ri.image_id
    INNER JOIN prediktia.global_types AS gt ON ri.image_type = gt.type_id
    WHERE
        pi.type = 'thumbnail_img'
        AND pi.width = 600 AND pi.format_id = 90
)

SELECT
    im.image_id AS search_image_id,
    im.product AS search_product,
    im.match_image_id,
    im.match_product,
    ti1.processed_image_uri AS search_thumb,
    ti2.processed_image_uri AS match_thumb,
    im.angle AS search_angle,
    im.match_angle,
    ti1.name AS search_image_type,
    ti2.name AS match_image_type,
    im.score AS image_score
FROM
    datascience._2_get_info_of_entity_products_with_img_matches(
        'tenant',
        6,
        'tenant',
        6,
        'apparel',
        array['back','front'],
        'google_vision'
    ) AS im
INNER JOIN thumbnail_imgs AS ti1
    ON im.image_id = ti1.image_id
INNER JOIN thumbnail_imgs AS ti2
    ON im.match_image_id = ti2.image_id;
