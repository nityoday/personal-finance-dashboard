# personal-finance-dashboard
Best used with app "Money Manager" by Realbyte, Inc. This project provides a Streamlit-based dashboard for analyzing your personal expenses, using data exported from the **Money Manager Expense & Budget** app by Realbyte Inc. The dashboard allows you to visualize and explore your spending habits, helping you make better financial decisions.

---

## Features

### 1. **Data Import**

- Export data from the Money Manager Expense & Budget app as `.xls`. (or convert suitably to xls or xlsx)
- Import the exported `.xls` or `.xlsx` file directly into the dashboard.
- The dashboard processes the data to focus solely on **expenses**, ignoring all income entries.

### 2. **Tabs for Analysis**

- **Overall Analysis**: View high-level metrics, monthly trends, category breakdowns, and insights.
- **Monthly Deep Dive**: Analyze spending within a selected month, including detailed breakdowns and visualizations.
- **Comparison Overview**: Compare expenses across the last three months, with grouped data by category and subcategory. (Work in progress)

### 3. **Interactive Visualizations**

- Bar charts, line charts, stacked bar charts, and treemaps.
- Filters for categories, subcategories, and date ranges.
- Detailed tables summarizing expenses.

### 4. **Key Metrics**

- Total expenses.
- Average monthly spending.
- Highest monthly spending.
- Transaction counts and daily averages.

---

## How to Use

### Prerequisites

- Install Python 3.7 or later.
- Install required dependencies:
  ```bash
  pip install streamlit pandas plotly openpyxl xlrd
  ```

### Running the Application

1. Clone this repository.
2. Navigate to the project directory.
3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
   or use
   ```bash
   python -m streamlit run app.py
   ```
4. Upload your `.xls` or `.xlsx` file exported from the Money Manager Expense & Budget app.

---

## Dashboard Insights

### Overall Analysis

- Visualize spending trends over time.
- Analyze category-wise and subcategory-wise expenses.
- Gain insights into top spending categories and patterns.

### Monthly Deep Dive

- Focus on specific months for detailed spending insights.
- View daily spending trends.
- Analyze the breakdown of categories and subcategories.

### Comparison Overview (Work in progress)

- Compare spending across the last three months.
- Grouped tables showing category and subcategory totals.

---

## Notes

- The app is designed for personal use and does not store any uploaded data.

---

## License

This project is licensed under the MIT License.

---

## Support

For questions or issues, kindly open an issue in the repository.

