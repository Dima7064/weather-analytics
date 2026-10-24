with source as (
    select * from {{ source('raw', 'customers') }}
),
renamed as (
    select
        customer_id::int as customer_id,
        name::varchar as customer_name,
        country::varchar as country,
        signup_date::date as signup_date
    from source
)
select * from renamed
