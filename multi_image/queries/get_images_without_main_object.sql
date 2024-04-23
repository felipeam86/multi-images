SELECT
    product,
    image_id,
    array_agg(object_name) AS located_objects_names,
    image_uri,
    replace(
        image_uri, 'gs://', 'https://storage.googleapis.com/'
    ) AS image_url,
    filename,
    angle,
    image_type_name,
    category,
    gender,
    brand
FROM
    datascience._2_get_info_of_entity_images_with_located_objects(
        'tenant',
        6,
        'apparel'
    )
WHERE
    NOT object_name = 'undetected'
    AND
    image_id NOT IN (
        SELECT iwmo.image_id
        FROM
            datascience._2_get_entity_images_with_main_object(
                'tenant',
                6,
                'apparel'
            ) AS iwmo
    )
GROUP BY
    product,
    image_id,
    image_uri,
    filename,
    angle,
    image_type_name,
    category,
    gender,
    brand
ORDER BY product, image_id;
