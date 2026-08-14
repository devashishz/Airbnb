with source as (
    select * from {{ source('olist', 'olist_order_payments_dataset') }}
),

staged as (
    select
        cast(order_id as varchar(50)) as order_id,
        cast(payment_sequential as integer) as payment_sequential,
        
        -- Standardize payment type casing and spacing
        trim(lower(cast(payment_type as varchar(50)))) as payment_type,
        
        cast(payment_installments as integer) as payment_installments,
        cast(payment_value as decimal(10, 2)) as payment_value
    from source
)

select * from staged