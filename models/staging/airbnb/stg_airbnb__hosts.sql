with source as (
    select * from read_csv_auto('s3://dbt-datasets/hosts.csv')
)

select
    id as host_id,
    coalesce(name, 'Unknown') as host_name,
    is_superhost,
    created_at,
    updated_at
from source
