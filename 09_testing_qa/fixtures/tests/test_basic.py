"""Tests for the Fixtures exercise."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).resolve().parents[1] / "my_solution" / "inventory_service.py"


def load_solution_module():
    if not MODULE_PATH.exists():
        pytest.skip("Create my_solution/inventory_service.py before running the exercise tests.")
    spec = importlib.util.spec_from_file_location("inventory_service", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


@pytest.fixture()
def service():
    module = load_solution_module()
    item = module.InventoryItem(sku="kb", name="Keyboard", stock=5)
    service = module.InventoryService(items={item.sku: item})
    return module, service


def test_add_stock(service) -> None:
    _module, inventory_service = service
    inventory_service.add_stock("kb", 3)
    assert inventory_service.items["kb"].stock == 8


def test_reserve_unknown_sku(service) -> None:
    _module, inventory_service = service
    with pytest.raises(LookupError):
        inventory_service.reserve_stock("missing", 1)


def test_low_stock_items(service) -> None:
    _module, inventory_service = service
    inventory_service.reserve_stock("kb", 3)
    low_stock = inventory_service.low_stock_items(threshold=2)
    assert [item.sku for item in low_stock] == ["kb"]
