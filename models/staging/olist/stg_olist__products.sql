with source as (
    select * from {{ source('olist', 'olist_products_dataset') }}
),

staged as (
    select
        cast(product_id as varchar(50)) as product_id,
        
        -- Rename category and fix original dataset typos
        cast(product_category_name as varchar(100)) as product_category_name_pt,
        cast(product_name_lenght as integer) as product_name_length,
        cast(product_description_lenght as integer) as product_description_length,
        cast(product_photos_qty as integer) as product_photos_qty,
        
        -- Handle missing dimensional data by defaulting to 0
        coalesce(cast(product_weight_g as integer), 0) as product_weight_g,
        coalesce(cast(product_length_cm as integer), 0) as product_length_cm,
        coalesce(cast(product_height_cm as integer), 0) as product_height_cm,
        coalesce(cast(product_width_cm as integer), 0) as product_width_cm
    from source
)

select * from staged