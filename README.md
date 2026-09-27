# Restaurant Inventory Forecasting Capstone

## Background
This project started from a common issue in restaurant operations: inventory is often managed reactively. Sometimes ingredients run out unexpectedly, and other times there is too much overstock.

The goal here is to explore a more data-driven approach by connecting sales data, recipe mapping, and inventory into one flow. This is not meant to be a perfect system, but rather a working prototype that shows how demand can be translated into ingredient planning and reorder decisions.

---

## Project Overview
This project focuses on inventory planning for a central warehouse that supplies multiple restaurant branches.

The main idea is:
- Forecast menu demand from historical sales
- Convert that demand into ingredient requirements
- Compare projected usage with warehouse stock
- Generate alerts and reorder suggestions

This is built as a **capstone prototype**, not a production-ready system.

---

## Business Assumptions
The project uses a simplified business setup:

- Multiple restaurant branches exist
- All branches are supplied by a single central warehouse

Because of this:
- Demand is analyzed at the chain level
- Ingredient requirements are aggregated
- Reorder planning is done at the warehouse level, not per branch

---

## Main Datasets
The project uses four main datasets:

- `restaurant_sales_data.csv`  
  Historical menu-level sales data

- `restaurant_inventory_2024_by_ingredients.csv`  
  Ingredient-level warehouse inventory data for one year

- `recipe_mapping.csv`  
  Mapping between menu items and ingredients with quantity per serving

- `supplier_contacts.csv`  
  Dummy supplier dataset used for grouping and draft orders

The local raw/reference CSV files are intentionally excluded from this public repository. They may contain course or project data that is not licensed for redistribution. Supply files with the same schemas locally before running the pipeline.

---

## How It Works
The pipeline follows this general flow:

1. Load and clean all datasets: sales, inventory, recipe, and supplier
2. Normalize names and units so they can be joined properly
3. Forecast future menu demand from historical sales
4. Convert menu demand into ingredient requirements using recipe mapping
5. Calculate historical ingredient usage
6. Compare projected demand with the latest warehouse stock
7. Classify stock status as healthy, warning, or critical
8. Calculate reorder quantity recommendations
9. Group reorder items by supplier
10. Generate supplier order summaries and draft messages
11. Display everything in a Streamlit dashboard

---

## Machine Learning (Forecasting)

### Role Of Machine Learning
Machine learning in this project is used specifically for **sales forecasting**.

It predicts future menu demand based on historical sales data. That prediction becomes the main input for the rest of the system:

- ingredient requirement estimation
- stock monitoring
- reorder recommendation

So ML is used in the **forecasting stage**, and the rest of the pipeline depends on its output.

---

### Model Used
The model used is a **ridge-style regression model**, implemented using `pandas` and `numpy`.

---

### Why This Model Was Chosen
This model was chosen for practical reasons:

- The project is a capstone prototype, so the model needs to be simple and explainable
- Ridge regression helps reduce overfitting compared to basic linear regression
- It is easier to debug and interpret than more complex models
- It works well for structured tabular sales data
- It fits the goal of building an end-to-end system, not only focusing on prediction accuracy

---

### Why Not More Complex Models
More advanced models such as LSTM, XGBoost, or Prophet were not used because:

- They increase complexity and are harder to explain
- The project is not purely about machine learning
- The main goal is to build a complete workflow from forecast to inventory to reorder
- A simpler model is more practical and easier to justify for a prototype

---

### Features Used Conceptually
The model learns from historical patterns such as:

- menu item sales trends over time
- date-related patterns
- aggregated demand across branches
- optional scenario inputs such as promotion, events, and weather

---

### Evaluation
The forecasting model is evaluated using:

- MAE
- RMSE
- WAPE

This helps show that the model is not only implemented, but also checked for performance.
No benchmark scores are claimed in this repository. Run the pipeline against an appropriate local dataset to generate and review MAE, RMSE, and WAPE for that data.

---

### Important Note
Machine learning is **not used for the entire system**.

- ML is only used for predicting demand
- The rest of the pipeline, such as ingredient conversion, stock alerts, and reorder logic, uses rule-based business logic

This separation keeps the system simpler and easier to control.
For this project, keeping the forecasting step separate from the inventory rules also made the overall pipeline easier to explain and debug.

---

## Recipe Mapping (Core Component)
Recipe mapping is a key part of this project.

Without it, the system would only know what menu items were sold, but not what ingredients were used.

Basic idea:
- Each menu item uses a certain quantity of ingredients
- Forecasted menu demand is translated into ingredient demand

This is what allows the system to move from sales forecasting to actual inventory planning.

---

## Inventory Logic
The system uses the latest warehouse inventory snapshot for monitoring.

It compares:
- current stock
- reorder level
- lead time
- estimated usage

Reorder quantity is calculated using:

```text
recommended_reorder_qty = max(lead_time_demand + reorder_level - current_stock, 0)
```

This is a simplified approach, but it works well enough for a prototype.
The logic is still relatively simple, but it is sufficient for the current scope and makes the reorder calculations easier to justify.

---

## Supplier Logic
Supplier data in this project is still a structured dummy dataset using Supplier A, Supplier B, and Supplier C.

It is used to:
- group reorder items by supplier
- display supplier contact information
- generate draft order messages

This part is mainly for demonstration purposes.

---

## Dashboard (Streamlit)
The project includes a Streamlit dashboard with:

- demand summary
- sales outlook
- ingredient planning
- stock health monitoring
- supplier reorder summary
- dataset setup view

Features:
- CSV upload support for all datasets
- Quick Stock Update feature
  This allows partial stock updates without replacing the entire dataset

---

## Project Structure

```text
forecasting/
├── app/
│   └── streamlit_app.py
├── data/
├── scripts/
│   └── run_capstone_pipeline.py
├── src/
│   └── restaurant_forecasting/
│       ├── config.py
│       ├── data_loader.py
│       ├── forecasting.py
│       ├── inventory.py
│       └── pipeline.py
├── tests/
│   └── test_pipeline.py
└── README.md
```

---

## How To Run

### 1. Install dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 2. Run the pipeline
```bash
python3 scripts/run_capstone_pipeline.py --horizon-days 14
```

### 3. Run the dashboard
```bash
streamlit run app/streamlit_app.py
```

### 4. Run tests
```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

---

## Outputs
Running the pipeline will generate:

- `menu_item_forecast.csv`
- `ingredient_forecast.csv`
- `historical_ingredient_usage.csv`

Generated outputs are written under `output/` and are intentionally ignored by Git.

## Project Status and Limitations

This is a capstone prototype, not a production inventory system. It uses simplified assumptions, a ridge-style regression implemented with NumPy/Pandas, and rule-based reorder logic. It does not model all operational factors such as supplier reliability, spoilage, transfers, promotions, uncertainty intervals, or branch-level constraints. Supplier contacts in the local demo data are synthetic placeholders.
- `inventory_alerts.csv`
- `supplier_reorders.csv`
- `supplier_order_drafts.csv`

One practical takeaway from this project is that even a relatively simple forecasting model becomes much more useful when it is connected to recipe mapping, stock monitoring, and reorder planning.

---

## Implementation Notes
Some practical decisions made during development:

- The inventory dataset was upgraded to a full one-year dataset to improve analysis
- Recipe mapping is used as the main bridge between sales and inventory
- The dashboard was adjusted to be more readable and interactive
- Cost values are shown as estimated values without assuming a specific currency
- Supplier routing had to be fixed to ensure correct grouping
- A Quick Stock Update feature was added to make stock updates more realistic

---

## Limitations
This project still has several limitations:

- It is a prototype, not a production system
- Supplier data is dummy and not connected to a real supplier system
- It is not connected to a live POS, database, or email service
- Forecast accuracy depends heavily on the quality of the historical sales data and recipe mapping
- External factors such as promotions and seasonality are still limited to the available dataset and scenario settings
- Reorder suggestions are intended for planning, not as final purchasing decisions

---

## Closing Note
This project is an attempt to connect sales forecasting with inventory planning in a more structured way. There is still a lot that can be improved, but the core pipeline from sales to forecast to ingredient planning to reorder recommendation is already in place.
