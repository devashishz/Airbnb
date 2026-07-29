with source as (
    select * from {{ source('raw_airbnb', 'listings') }}
)

select
    listing_id,
    host_id,
    
    -- Text cleanup
    trim(listing_name) as listing_name,
    listing_url,
    room_type,
    
    -- Senior move: Handling dirty numeric data and casting properly
    -- Assuming price might come in with a '$' or as a string
    cast(replace(price, '$', '') as numeric(10, 2)) as price_per_night,
    
    minimum_nights,
    
    -- Standardization
    created_at,
    updated_at

from source
