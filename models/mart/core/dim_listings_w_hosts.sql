{{
    config(
        materialized='table'
    )
}}

with listings as (
    select * from {{ ref('stg_airbnb__listings') }}
),

hosts as (
    select * from {{ ref('stg_airbnb__hosts') }}
)

select
    l.listing_id,
    l.listing_name,
    l.room_type,
    l.minimum_nights,
    l.price_per_night,
    
    -- Host details denormalized into the listing dimension
    h.host_id,
    h.host_name,
    h.is_superhost,
    
    -- Keeping track of when the record was created
    greatest(l.updated_at, h.updated_at) as last_updated_at

from listings as l
left join hosts as h
    on l.host_id = h.host_id
