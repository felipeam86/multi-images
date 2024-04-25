with families as (
	select distinct
		LEFT(tp.product, 20) as product,
		-- ri.source_url,
		tc."name" as category,
		case
			when tp.name like '%BRASIER%' then 'BRASIER'
			when tp.name like '%BRALETTE%' then 'BRALETTE'
			when tp.name like '%PAREO%' then 'PAREO'
			when tp.name like '%BRASILERA HILO%' then 'BRASILERA HILO'
			when tp.name like '%STRING%' then 'BRASILERA HILO'
			when tp.name like '%BRASILERA%' then 'BRASILERA'
			when tp.name like '%BRAZILIAN%' then 'BRASILERA'
			when tp.name like '%CULOTTE%' then 'CULOTTE'
			when tp.name like '%CUOTTE%' then 'CULOTTE'
			when tp.name like '%PANTY ZERO%' then 'CULOTTE'
			when tp.name like '%PANTY ALTO%' then 'PANTY ALTO'
			when tp.name like '%BUSTIER%' then 'BUSTIER'
		end as family,
		tp.name

	from
		public.tenant_products tp
	join public.tenant_categories tc
		on tc.tenant_category_id = tp.tenant_category_id
	inner join public.raw_images ri
		on ri.tenant_product = tp.product
		where tp.tenant_id = 6
		and tc."name" = 'Panty'
	order by
		family
)

select * from families;