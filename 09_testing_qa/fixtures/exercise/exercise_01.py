"""Exercise: Fixtures.

Goal:
Create `my_solution/inventory_service.py` with a tiny inventory model.

Requirements:
- Create an `InventoryItem` dataclass with `sku`, `name`, and `stock`.
- Create `InventoryService` with `add_stock`, `reserve_stock`, and `low_stock_items`.
- `reserve_stock` must raise `LookupError` when the SKU is unknown.
- `reserve_stock` must raise `ValueError` when requested quantity exceeds stock.

Why this exercise matters:
The test suite is intentionally written around shared setup so you can practice recognizing when a fixture improves readability.
"""
