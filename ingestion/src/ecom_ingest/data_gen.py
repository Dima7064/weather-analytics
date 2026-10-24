import os
import random
from datetime import datetime, timedelta

import pandas as pd


def generate_csv_data(output_dir: str = "data") -> None:
    """Генерирует фейковые CSV-файлы для интернет-магазина."""
    os.makedirs(output_dir, exist_ok=True)

    # 1. Клиенты
    countries = ["Russia", "Germany", "USA", "Kazakhstan", "China", "Brazil"]
    customers = []
    for i in range(1, 101):  # 100 клиентов
        signup_date = datetime(2025, 1, 1) + timedelta(days=random.randint(0, 300))
        customers.append(
            {
                "customer_id": i,
                "name": f"User_{i}",
                "country": random.choice(countries),
                "signup_date": signup_date.strftime("%Y-%m-%d"),
            }
        )
    pd.DataFrame(customers).to_csv(f"{output_dir}/customers.csv", index=False)

    # 2. Товары
    categories = ["Electronics", "Books", "Clothing", "Home", "Sports"]
    products = []
    for i in range(1, 51):  # 50 товаров
        products.append(
            {
                "product_id": i,
                "name": f"Product_{i}",
                "category": random.choice(categories),
                "price": round(random.uniform(10.0, 500.0), 2),
            }
        )
    pd.DataFrame(products).to_csv(f"{output_dir}/products.csv", index=False)

    # 3. Заказы
    statuses = ["created", "paid", "shipped", "delivered", "cancelled"]
    orders = []
    start_date = datetime.now() - timedelta(days=180)

    for i in range(1, 1001):  # 1000 заказов
        order_date = start_date + timedelta(
            days=random.randint(0, 180), hours=random.randint(0, 23)
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
