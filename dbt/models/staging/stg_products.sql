with source as (
    select * from {{ source('raw', 'products') }}
),
renamed as (
    select
        product_id::int as product_id,
        name::varchar as product_name,
        category::varchar as category,
        price::numeric(10,2) as price
    from source
)
select * from renamed
