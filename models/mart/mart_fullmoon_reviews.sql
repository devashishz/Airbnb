{{
    config(
        materialized='table'
    )
}}

with fct_reviews as (
    select * from {{ ref('fct_reviews') }}
),

full_moon_dates as (
    select * from {{ ref('seed_full_moon_dates') }}
)

select
    r.review_id,
    r.listing_id,
    r.review_date,
    r.reviewer_name,
    r.review_text,
    r.review_sentiment,
    
    -- The Fix: Safely evaluating the presence of a full moon match
    case 
        when fm.full_moon_date is null then 'not full moon'
        else 'full moon'
    end as is_full_moon

from fct_reviews as r
left join full_moon_dates as fm
    -- Senior Move: Explicitly casting both sides to DATE ensures 
    -- time components don't break the join condition.
    on date(r.review_date) = date(fm.full_moon_date)
