# Capstone Scope Alignment

## Final Project Framing
**Title:** AI-Driven Restaurant Inventory Forecasting and Supplier Decision Support System for a Central Warehouse

**Research question:** How can historical multi-restaurant sales data and warehouse inventory snapshots be used to forecast short-term demand, estimate ingredient consumption, monitor stock risk, and generate supplier reorder requests?

## What The Current System Now Covers
- Historical sales analytics at chain level.
- Central-warehouse inventory monitoring using current stock, reorder thresholds, lead times, and supplier assignments.
- Historical ingredient deduction from sales using the provided recipe mapping.
- Future ingredient requirement forecasting from predicted menu demand.
- Low-stock alerts and stockout-risk indicators.
- Reorder quantity recommendations using lead-time demand plus reorder-level logic.
- Supplier-level draft order requests and email text generation.
- Streamlit dataset upload workflow for sales, inventory, recipe mapping, and supplier master data.

## Data Model Notes
- `restaurant_sales_data.csv` remains the historical demand source.
- `restaurant_inventory_2024_by_ingredients.csv` is now the default base warehouse inventory source, covering January 1, 2024 through December 31, 2024.
- `recipe_mapping.csv` is now the authoritative recipe master.
- `supplier_contacts.csv` is a dummy but fully structured supplier dataset with ingredient-level assignment, contact details, and lead times.

## Central Warehouse Assumption
The confirmed operating model is one large warehouse serving multiple restaurants. Because of that:
- historical demand is analyzed across all restaurants together
- forecast demand is aggregated as chain-total demand
- ingredient requirements are translated into warehouse-level stock planning
- reorder decisions are produced for the shared warehouse, not for individual outlets

## Demo Story
1. Load default or uploaded datasets.
2. Show historical sales and forward demand on the same scale.
3. Forecast future menu demand.
4. Convert the forecast into ingredient requirements.
5. Compare predicted needs against the warehouse inventory catalog.
6. Surface critical stock alerts and reorder quantities.
7. Generate supplier-level order drafts with contact-ready email text.

## Expected Deliverables
- Streamlit prototype
- Forecast and reorder CSV exports
- Historical ingredient usage export
- Supplier order draft export
- Final report describing forecasting, inventory intelligence, and supplier decision support
