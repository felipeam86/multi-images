WITH image_type AS (
    SELECT gt.type_id, gt.name
    FROM prediktia.global_types AS gt
    WHERE parent_type_id = 96
)

SELECT *
FROM
    datascience._2_get_entity_products_with_their_images(
        'tenant',
        6,
        'apparel'
    );
