{{ config(
    materialized='incremental',
    unique_key='order_id',
    indexes=[
      {'columns': ['order_date']},
      {'columns': ['customer_id']}
    ],
    on_schema_change='append_new_columns'
) }}

with orders as (
    select * from {{ ref('stg_orders') }}
    {% if is_incremental() %}
    where order_date > (select max(order_date) from {{ this }})
    {% endif %}
),
products as (
    select * from {{ ref('dim_products') }}
),
final as (
    select
        o.order_id,
        o.customer_id,
        o.product_id,
        o.order_date,
        o.status,
        o.quantity,
        p.price,
        (o.quantity * p.price) as order_total_amount
    from orders o
    left join products p on o.product_id = p.product_id
)
select * from final
