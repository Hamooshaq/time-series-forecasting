from __future__ import annotations

import sys
import unittest
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from restaurant_forecasting.config import ProjectPaths
from restaurant_forecasting.data_loader import prepare_recipe_mapping, prepare_sales_data, prepare_supplier_contacts
from restaurant_forecasting.inventory import build_historical_ingredient_usage
from restaurant_forecasting.pipeline import run_pipeline


class PipelineSmokeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.paths = ProjectPaths.from_root(PROJECT_ROOT)
        cls.result = run_pipeline(cls.paths, horizon_days=7)

    def test_recipe_mapping_loader_accepts_proposal_schema(self) -> None:
        self.assertEqual(
            set(self.result.recipe_mapping.columns),
            {"menu_item_name", "ingredient_name", "quantity_per_order", "unit"},
        )

    def test_case_insensitive_recipe_join(self) -> None:
        sales = pd.DataFrame(
            [
                {
                    "date": "2025-01-01",
                    "restaurant_id": 1,
                    "restaurant_type": "food stall",
                    "menu_item_name": "laksa",
                    "meal_type": "lunch",
                    "key_ingredients_tags": "rice noodles, fish broth",
                    "typical_ingredient_cost": 4.5,
                    "observed_market_price": 10.0,
                    "actual_selling_price": 12.0,
                    "quantity_sold": 100,
                    "has_promotion": False,
                    "special_event": False,
                    "weather_condition": "sunny",
                }
            ]
        )
        recipe = pd.DataFrame(
            [
                {"menu_item_name": "LAKSA", "ingredient_name": "rice noodles", "quantity_per_order": 0.15, "unit": "kg"},
            ]
        )
        prepared_sales = prepare_sales_data(sales)
        prepared_recipe = prepare_recipe_mapping(recipe)
        historical_usage = build_historical_ingredient_usage(prepared_sales, prepared_recipe)
        self.assertFalse(historical_usage.empty)
        self.assertAlmostEqual(historical_usage.iloc[0]["historical_ingredient_usage"], 15.0)

    def test_supplier_contacts_cover_entire_recipe_catalog(self) -> None:
        required_columns = {
            "supplier_name",
            "ingredient_name",
            "email",
            "contact_person",
            "phone",
            "lead_time_days",
            "notes",
        }
        self.assertEqual(set(self.result.supplier_contacts.columns), required_columns)
        recipe_ingredients = set(self.result.recipe_mapping["ingredient_name"].unique())
        supplier_ingredients = set(self.result.supplier_contacts["ingredient_name"].unique())
        self.assertEqual(recipe_ingredients, supplier_ingredients)

    def test_historical_ingredient_usage_known_slice(self) -> None:
        target_date = pd.Timestamp("2024-01-01")
        laksa_sales = self.result.sales[
            (self.result.sales["date"] == target_date) & (self.result.sales["menu_item_name"] == "Laksa")
        ]["quantity_sold"].sum()
        tamarind_usage = self.result.historical_ingredient_usage[
            (self.result.historical_ingredient_usage["date"] == target_date)
            & (self.result.historical_ingredient_usage["ingredient_name"] == "Tamarind")
        ]["historical_ingredient_usage"].sum()
        self.assertAlmostEqual(tamarind_usage, laksa_sales * 0.01, places=4)

    def test_chain_total_forecast_is_not_per_restaurant_average(self) -> None:
        multi_restaurant_rows = self.result.menu_forecast[self.result.menu_forecast["active_restaurant_count"] > 1]
        self.assertFalse(multi_restaurant_rows.empty)
        self.assertTrue(
            (multi_restaurant_rows["predicted_quantity_sold"] > multi_restaurant_rows["average_per_active_restaurant"]).all()
        )

    def test_augmented_inventory_covers_all_recipe_ingredients(self) -> None:
        latest_snapshot = self.result.inventory[self.result.inventory["Date"] == self.result.inventory["Date"].max()]
        latest_raw_snapshot = self.result.raw_inventory[self.result.raw_inventory["Date"] == self.result.raw_inventory["Date"].max()]
        inventory_items = set(latest_snapshot["Item_Name"].unique())
        raw_inventory_items = set(latest_raw_snapshot["Item_Name"].unique())
        recipe_ingredients = set(self.result.recipe_mapping["ingredient_name"].unique())
        self.assertTrue(recipe_ingredients.issubset(inventory_items))
        self.assertTrue(raw_inventory_items.issubset(inventory_items))
        self.assertGreaterEqual(len(latest_snapshot), len(latest_raw_snapshot))

    def test_reorder_quantities_are_not_negative(self) -> None:
        self.assertTrue((self.result.inventory_alerts["recommended_reorder_qty"] >= 0).all())

    def test_mapping_coverage_is_complete(self) -> None:
        self.assertAlmostEqual(self.result.mapping_coverage["coverage_ratio"], 1.0, places=6)


if __name__ == "__main__":
    unittest.main()
