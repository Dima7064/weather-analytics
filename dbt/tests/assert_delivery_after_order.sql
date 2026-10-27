-- Этот тест ищет заказы, где доставка произошла РАНЬШЕ, чем заказ был создан.
-- Если такие есть, тест упадет с ошибкой.

select
    order_id,
    order_date,
    delivered_at
from {{ ref('fct_order_lifecycle') }}
where delivered_at < order_date
