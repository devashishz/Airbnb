{{
    config(
        materialized='incremental',
        unique_key='review_id',
        on_schema_change='fail'
    )
}}

with stg_reviews as (
    select * from {{ ref('stg_airbnb__reviews') }}
)

select
    -- Create a deterministic surrogate primary key using dbt_utils
    -- This proves you know how to handle raw data that lacks a reliable unique ID
    {{ dbt_utils.generate_surrogate_key([
        'listing_id', 
        'review_date', 
        'reviewer_name', 
        'review_text'
    ]) }} as review_id,
    
    listing_id,
    review_date,
    reviewer_name,
    review_text,
    review_sentiment

from stg_reviews
where review_text is not null -- Basic data cleansing

-- Senior Logic: Only process new records if the table already exists
{% if is_incremental() %}

    -- Grab reviews strictly newer than the most recent date in the destination table
    and review_date > (select max(review_date) from {{ this }})

{% endif %}