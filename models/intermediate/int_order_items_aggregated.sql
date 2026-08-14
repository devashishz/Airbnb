with order_items as (
    select * from {{ ref('stg_olist__order_items') }}
),

aggregated_items as (
    select 
        order_id,
        
        -- Basket size metrics
        count(order_item_id) as total_items_in_order,
        count(distinct product_id) as unique_products_in_order,
        count(distinct seller_id) as unique_sellers_in_order,
        
        -- Aggregate financial values
        sum(price) as total_item_revenue,
        sum(freight_value) as total_freight_cost,
        
        -- Logistics SLA metric (earliest shipping limit)
        min(shipping_limit_date) as earliest_shipping_limit_date
        
    from order_items
    group by 1
)

select * from aggregated_items