with source as (
    select * from {{ source('raw_airbnb', 'reviews') }}
)

select
    -- IDs (Standardizing foreign keys)
    listing_id,
    
    -- Timestamps (Casting to ensure proper date formatting in Snowflake)
    cast(date as timestamp) as review_date,
    
    -- Dimensions
    reviewer_name,
    comments as review_text,
    sentiment as review_sentiment

from source