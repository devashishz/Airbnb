with source as (
    select * from read_csv_auto('s3://dbt-datasets/listings.csv')
)

select
    id as listing_id,
    host_id,
    trim(name) as listing_name,
    listing_url,
    room_type,
    cast(replace(price, '$', '') as numeric(10, 2)) as price_per_night,
    minimum_nights,
    created_at,
    updated_at
from source
