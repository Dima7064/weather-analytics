select
    order_id,
    order_total_amount,
    quantity,
    price,
    (quantity * price) as expected_amount
from {{ ref('fct_orders') }}
where abs(order_total_amount - (quantity * price)) > 0.01
