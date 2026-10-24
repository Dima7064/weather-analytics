import os
from pathlib import Path

import pandas as pd

from ecom_ingest.data_gen import generate_csv_data


def test_generate_csv_data(tmp_path: Path) -> None:
    # tmp_path — это встроенная фикстура pytest, которая создает временную папку
    generate_csv_data(output_dir=str(tmp_path))

    assert os.path.exists(tmp_path / "customers.csv")
    assert os.path.exists(tmp_path / "products.csv")
    assert os.path.exists(tmp_path / "orders.csv")

    # Проверяем, что данных ровно столько, сколько мы задумали
    customers = pd.read_csv(tmp_path / "customers.csv")
    orders = pd.read_csv(tmp_path / "orders.csv")

    assert len(customers) == 100
    assert len(orders) == 1000
    assert "order_id" in orders.columns
