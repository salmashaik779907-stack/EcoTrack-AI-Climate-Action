# EcoTrack AI – Sustainable Inventory & Waste Reduction System

**An AI-powered inventory monitoring and decision-support system supporting Climate Action (UN Sustainable Development Goal 13).**

## 1. Project Overview

EcoTrack AI is a sustainable inventory management project that uses demand forecasting and inventory analysis to identify potential excess stock and support better inventory decisions.

Businesses may order or store more products than required. This can lead to excess inventory, unnecessary storage and avoidable resource consumption.

EcoTrack AI analyzes inventory and demand data to identify stock risks and provide recommendations that can help reduce potential surplus.

## 2. Problem Statement

Traditional inventory management may result in:
- Excess stock due to inaccurate demand planning.
- Unnecessary inventory holding and storage.
- Poor visibility of overstock and stock shortage risks.
- Inefficient replenishment decisions.

EcoTrack AI aims to address these problems through data analysis, demand forecasting and inventory recommendations.

## 3. Project Objectives

- Analyze historical inventory and sales data.
- Use demand forecasting to support inventory planning.
- Identify potential surplus and stock shortage risks.
- Provide smart inventory recommendations.
- Demonstrate how better inventory planning can support sustainability.
- Contribute to SDG 13 – Climate Action.

## 4. Key Features

### Overview Dashboard
Displays inventory information, summary metrics, charts and inventory details.

### Risk Analysis
Identifies inventory risk levels using stock coverage and estimated target stock.

### Smart Recommendations
Provides suggestions such as reviewing high stock, monitoring moderate surplus and considering replenishment for low stock.

### What-If Simulation
Allows users to explore hypothetical surplus-reduction scenarios and view illustrative inventory-value estimates.

## 5. Sustainability Contribution

EcoTrack AI supports sustainable inventory planning by helping identify potential excess stock and encouraging more informed replenishment decisions.

**Climate Action connection:**
- Encourages efficient resource utilization.
- Helps businesses review unnecessary inventory accumulation.
- Supports data-driven and responsible inventory planning.
- Demonstrates a technology-based approach to sustainability.

*Note: Potential surplus is an estimate, not confirmed waste. Simulation results are illustrative and do not represent measured waste prevention or carbon-emission reductions.*

## 6. Technology Stack

- Python
- Pandas
- Scikit-learn
- XGBoost
- Streamlit
- Plotly
- Joblib

## 7. Project Structure

```text
EcoTrack-AI/
│
├── app/
│   ├── dashboard.py
│   └── ecotrack.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── models/
│
├── outputs/
│
├── src/
│   ├── train_model.py
│   ├── evaluate_model.py
│   ├── future_forecast.py
│   ├── inventory_optimization.py
│   ├── inventory_risk.py
│   └── other analysis scripts
│
├── requirements.txt
└── README.md
```

## 8. Installation and Execution

### Step 1: Clone the repository

```bash
git clone https://github.com/salmashaik779907-stack/EcoTrack-AI-Climate-Action.git
```

### Step 2: Open the project folder

```bash
cd EcoTrack-AI-Climate-Action
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the EcoTrack AI dashboard

```bash
python -m streamlit run app/ecotrack.py
```

The dashboard will open in your browser.

## 9. Dataset

The project uses supply-chain inventory data containing fields such as:
- Date
- SKU ID
- Warehouse ID
- Units Sold
- Inventory Level
- Reorder Point
- Order Quantity
- Unit Cost
- Demand Forecast

## 10. Expected Benefits

- Better inventory visibility.
- Early identification of potential surplus.
- Improved demand-based planning.
- More informed replenishment decisions.
- Greater awareness of sustainable inventory practices.

## 11. Team Members

**Project Type:** Group Project

**Team Members:**
1. [Member 1 – Name]
2. [Member 2 – Name]
3. [Member 3 – Name]
4. [Member 4 – Name]

*Replace the placeholders with the names and contributions of all team members.*

## 12. Future Enhancements

- Integration of real-time inventory data.
- Product expiry and perishability monitoring.
- More advanced demand forecasting.
- Estimation of environmental impact using verified emissions factors.
- Notifications for potential surplus and stock shortages.

## 13. Repository

GitHub: https://github.com/salmashaik779907-stack/EcoTrack-AI-Climate-Action

---

**EcoTrack AI – Smarter Inventory, Less Surplus, More Sustainable Decisions.**