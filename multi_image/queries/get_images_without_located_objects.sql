SELECT *
FROM
    datascience._2_get_info_of_entity_images_with_located_objects(
        'tenant',
        6,
        'apparel'
    )
WHERE object_name = 'undetected'
ORDER BY product, image_id;