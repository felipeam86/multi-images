with last_sale as (
    select
        tp.product,
        min(oi.order_date) as first_sale,
        max(oi.order_date) as last_sale
    from
        public.tenant_products as tp
    inner join
            public.order_items as oi
            on
        tp.tenant_product_id = oi.tenant_product_id
    where
        tp.tenant_id = 6
    group by
        tp.product
    having
        min(oi.order_date) >= '2023-01-01'
    order by
        2
)

select
	ls.product,
	ri.image_id,
	replace(ri.image_uri, 'gs://', 'https://storage.googleapis.com/') as image_url,
	ri.angle,
	gt.name as image_type,
	ie.embedding,
	case
		when ls.first_sale >= '2023-06-01' then 'search'
		else 'match'
	end as group
from
	last_sale as ls
inner join
	public.raw_images ri 
	on
	ri.tenant_product = ls.product
inner join 
	datascience.image_embeddings ie 
	on
	ie.image_id = ri.image_id
inner join prediktia.global_types as gt on ri.image_type = gt.type_id
order by
    ls.product, ri.image_id
