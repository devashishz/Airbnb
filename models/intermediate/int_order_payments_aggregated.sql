with payments as (
    select * from {{ ref('stg_olist__payments') }}
),

aggregated_payments as (
    select 
        order_id,
        
        -- Aggregate financial values
        sum(payment_value) as total_payment_value,
        
        -- Customer payment behavior
        count(payment_sequential) as total_payment_methods_used,
        max(payment_installments) as max_installments,
        
        -- Create a list of payment types used (requires DuckDB list_aggr or string_agg)
        string_agg(payment_type, ', ') as payment_types
        
    from payments
    group by 1
)

select * from aggregated_payments