import os
import random
from datetime import datetime, timedelta

import pandas as pd


def generate_csv_data(output_dir: str = "data") -> None:
    """Генерирует фейковые CSV-файлы для интернет-магазина."""
    os.makedirs(output_dir, exist_ok=True)

    # 1. Клиенты (100 клиентов)
    countries = ["Russia", "Germany", "USA", "Kazakhstan", "China", "Brazil"]
    customers = []
    for i in range(1, 101):
        signup_date = datetime(2023, 1, 1) + timedelta(days=random.randint(0, 700))
        customers.append(
            {
                "customer_id": i,
                "name": f"User_{i}",
                "country": random.choice(countries),
                "signup_date": signup_date.strftime("%Y-%m-%d"),
            }
        )
    pd.DataFrame(customers).to_csv(f"{output_dir}/customers.csv", index=False)

    # 2. Товары (50 товаров).
    # Делаем так, чтобы у некоторых товаров цена изменилась (для теста SCD2)
    categories = ["Electronics", "Books", "Clothing", "Home", "Sports"]
    products = []
    for i in range(1, 51):
        base_price = round(random.uniform(10.0, 500.0), 2)
        # Каждый 5-й товар "подешевел" или "подорожал" (симуляция изменения цены)
        current_price = base_price * random.choice([1.0, 1.1, 0.9])
        products.append(
            {
                "product_id": i,
                "name": f"Product_{i}",
                "category": random.choice(categories),
                "price": round(current_price, 2),
            }
        )
    pd.DataFrame(products).to_csv(f"{output_dir}/products.csv", index=False)

    # 3. Заказы (10 000 заказов за последние 2 года)
    statuses = ["created", "paid", "shipped", "delivered", "cancelled"]
    orders = []
    start_date = datetime.now() - timedelta(days=730)

    for i in range(1, 10001):
        order_date = start_date + timedelta(
            days=random.randint(0, 730), hours=random.randint(0, 23), minutes=random.randint(0, 59)
        )
        orders.append(
            {
                "order_id": i,
                "customer_id": random.randint(1, 100),
                "product_id": random.randint(1, 50),
                "quantity": random.randint(1, 5),
                "status": random.choice(statuses),
                "order_date": order_date.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )
    pd.DataFrame(orders).to_csv(f"{output_dir}/orders.csv", index=False)
