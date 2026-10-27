{% test positive_values(model, column_name) %}
-- Этот тест проверяет, что значения в колонке больше нуля
select *
from {{ model }}
where {{ column_name }} <= 0
{% endtest %}
