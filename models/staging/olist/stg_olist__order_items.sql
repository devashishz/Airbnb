with source as (
    select * from {{ source('olist', 'olist_order_items_dataset') }}
),

staged as (
    select
        cast(order_id as varchar(50)) as order_id,
        cast(order_item_id as integer) as order_item_id,
        cast(product_id as varchar(50)) as product_id,
        cast(seller_id as varchar(50)) as seller_id,
        
        -- Handle timestamps
        cast(shipping_limit_date as timestamp) as shipping_limit_date,
        
        -- Cast financials to decimals
        cast(price as decimal(10, 2)) as price,
        cast(freight_value as decimal(10, 2)) as freight_value
    from source
)

select * from staged