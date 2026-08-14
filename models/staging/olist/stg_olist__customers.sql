with source as (
    select * from {{ source('olist', 'olist_customers_dataset') }}
),

staged as (
    select
        cast(customer_id as varchar(50)) as customer_id,
        cast(customer_unique_id as varchar(50)) as customer_unique_id,
        cast(customer_zip_code_prefix as varchar(10)) as customer_zip_code_prefix,
        
        -- Standardize text formatting
        trim(lower(customer_city)) as customer_city,
        trim(upper(customer_state)) as customer_state
    from source
)

select * from staged