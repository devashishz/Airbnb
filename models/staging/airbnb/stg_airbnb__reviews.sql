with source as (
    select * from read_csv_auto('s3://dbt-datasets/reviews.csv')
)

select
    listing_id,
    cast(date as timestamp) as review_date,
    reviewer_name,
    comments as review_text,
    sentiment as review_sentiment
from source