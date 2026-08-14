with orders as (
    select * from {{ ref('stg_olist__orders') }}
),

order_items as (
    select * from {{ ref('int_order_items_aggregated') }}
),

order_payments as (
    select * from {{ ref('int_order_payments_aggregated') }}
),

final as (
    select
        o.order_id,
        o.customer_id,
        o.order_status,
        
        -- Timestamps
        o.purchased_at,
        o.approved_at,
        o.shipped_at,
        o.delivered_at,
        o.estimated_delivery_at,
        
        -- Aggregated Item Metrics
        coalesce(i.total_items_in_order, 0) as total_items_in_order,
        coalesce(i.total_item_revenue, 0) as total_item_revenue,
        coalesce(i.total_freight_cost, 0) as total_freight_cost,
        
        -- Aggregated Payment Metrics
        coalesce(p.total_payment_value, 0) as total_payment_value,
        p.payment_types,
        
        -- Calculated Business Logic
        (coalesce(i.total_item_revenue, 0) + coalesce(i.total_freight_cost, 0)) as calculated_order_cost,
        
        -- SLA metric: Time to delivery in days (DuckDB syntax)
        date_diff('day', o.purchased_at, o.delivered_at) as days_to_delivery
        
    from orders o
    left join order_items i on o.order_id = i.order_id
    left join order_payments p on o.order_id = p.order_id
)

select * from final