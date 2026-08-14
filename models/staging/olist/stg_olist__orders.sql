with source as (
    select * from {{ source('olist', 'olist_orders_dataset') }}
),

renamed as (
    select
        -- Primary & Foreign Keys
        cast(order_id as text) as order_id,
        cast(customer_id as text) as customer_id,

        -- Status & Timestamps
        cast(order_status as text) as order_status,
        cast(order_purchase_timestamp as timestamp) as purchased_at,
        cast(order_approved_at as timestamp) as approved_at,
        cast(order_delivered_carrier_date as timestamp) as shipped_at,
        cast(order_delivered_customer_date as timestamp) as delivered_at,
        cast(order_estimated_delivery_date as timestamp) as estimated_delivery_at

    from source
)

select * from renamed