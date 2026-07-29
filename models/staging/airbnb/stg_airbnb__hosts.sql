with source as (
    select * from {{ source('raw_airbnb', 'hosts') }}
)

select
    host_id,
    
    -- Handle missing data at the source
    coalesce(host_name, 'Unknown') as host_name,
    
    is_superhost,
    created_at,
    updated_at

from source
