{{ config(materialized='incremental', unique_key='order_id') }}

with orders as (
    select * from {{ ref('stg_orders') }}
    {% if is_incremental() %}
    where order_date > (select max(order_date) from {{ this }})
    {% endif %}
),
lifecycle as (
    select
        order_id,
        customer_id,
        order_date,
        paid_at,
        shipped_at,
        delivered_at,
        status,
        -- Считаем время в днях между этапами
        extract(epoch from (paid_at - order_date))/86400 as days_to_pay,
        extract(epoch from (shipped_at - paid_at))/86400 as days_to_ship,
        extract(epoch from (delivered_at - shipped_at))/86400 as days_to_deliver,
        extract(epoch from (delivered_at - order_date))/86400 as total_delivery_days
    from orders
)
select * from lifecycle
