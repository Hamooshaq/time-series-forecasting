from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from restaurant_forecasting.config import ProjectPaths
from restaurant_forecasting.pipeline import run_pipeline


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the restaurant forecasting capstone pipeline.")
    parser.add_argument("--horizon-days", type=int, default=14, help="Forecast horizon in days.")
    parser.add_argument(
        "--weather",
        type=str,
        choices=["Sunny", "Cloudy", "Rainy"],
        default=None,
        help="Optional weather override for all forecast dates.",
    )
    parser.add_argument("--promotion", action="store_true", help="Simulate a promotion for the forecast horizon.")
    parser.add_argument("--special-event", action="store_true", help="Simulate a special event for the forecast horizon.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = ProjectPaths.from_root(PROJECT_ROOT)
    paths.output_dir.mkdir(parents=True, exist_ok=True)

    result = run_pipeline(
        paths=paths,
        horizon_days=args.horizon_days,
        weather_condition=args.weather,
        has_promotion=args.promotion,
        special_event=args.special_event,
    )

    result.menu_forecast.to_csv(paths.output_dir / "menu_item_forecast.csv", index=False)
    result.ingredient_forecast.to_csv(paths.output_dir / "ingredient_forecast.csv", index=False)
    result.historical_ingredient_usage.to_csv(paths.output_dir / "historical_ingredient_usage.csv", index=False)
    result.inventory_alerts.to_csv(paths.output_dir / "inventory_alerts.csv", index=False)
    result.supplier_reorders.to_csv(paths.output_dir / "supplier_reorders.csv", index=False)
    result.supplier_order_drafts.to_csv(paths.output_dir / "supplier_order_drafts.csv", index=False)

    print("Forecast pipeline completed successfully.")
    print(f"Backtest MAE: {result.metrics.mae:.2f}")
    print(f"Backtest RMSE: {result.metrics.rmse:.2f}")
    print(f"Backtest WAPE: {result.metrics.wape:.2f}%")
    print(f"Mapping coverage: {result.mapping_coverage['coverage_ratio'] * 100:.2f}% of forecasted menu volume")
    print(f"Warehouse ingredients in latest snapshot: {result.inventory_alerts['Item_Name'].nunique()}")
    print(f"Output directory: {paths.output_dir}")


if __name__ == "__main__":
    main()
