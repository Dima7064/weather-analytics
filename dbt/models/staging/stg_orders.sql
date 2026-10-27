with source as (
    select * from {{ source('raw', 'orders') }}
),
renamed as (
    select
        order_id::int as order_id,
        customer_id::int as customer_id,
        product_id::int as product_id,
        quantity::int as quantity,
        status::varchar as status,
        order_date::timestamp as order_date,
        paid_at::timestamp as paid_at,
        shipped_at::timestamp as shipped_at,
        delivered_at::timestamp as delivered_at
    from source
)
select * from renamed
