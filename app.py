import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import calendar
import numpy as np

# Set page config
st.set_page_config(
    page_title="Personal Expense Tracker",
    page_icon="\U0001F4B0",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        padding-right: 4px;
        padding-left: 4px;
    }
    </style>
    """, unsafe_allow_html=True)

# Function to load and process data
@st.cache_data
def load_data(uploaded_file):
    try:
        # Determine file type and use appropriate engine
        if uploaded_file.name.endswith('.xls'):
            df = pd.read_excel(uploaded_file, engine='xlrd')
        else:
            df = pd.read_excel(uploaded_file, engine='openpyxl')
        
        # Convert Date column to datetime
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Extract various date components
        df['Year'] = df['Date'].dt.year
        df['Month'] = df['Date'].dt.month
        df['MonthName'] = df['Date'].dt.strftime('%b-%y')
        df['YearMonth'] = df['Date'].dt.strftime('%Y-%m')
        
        # Fill empty subcategories with "Other"
        df['Subcategory'] = df['Subcategory'].fillna('Other')

        # Filter out Income entries
        df = df[df['Income/Expense'] != 'Income']
        
        return df
    except Exception as e:
        if 'xlrd' in str(e):
            st.error("Please install xlrd for .xls file support: pip install xlrd>=2.0.1")
        else:
            st.error(f"Error loading file: {str(e)}")
        return None

def main():
    # Header
    st.title("\U0001F4B0 Personal Expense Analytics Dashboard")
    
    # File uploader
    uploaded_file = st.file_uploader("Upload your expense Excel file", type=['xlsx', 'xls'])
    
    if uploaded_file is not None:
        df = load_data(uploaded_file)
        
        if df is not None:
            # Filters
            min_date, max_date = df['Date'].min(), df['Date'].max()
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("Start Date", min_date, min_value=min_date, max_value=max_date)
            with col2:
                end_date = st.date_input("End Date", max_date, min_value=min_date, max_value=max_date)
            
            # Convert start_date and end_date to datetime64 for comparison
            df = df[(df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))]

            # Main tabs
            tab1, tab2, tab3 = st.tabs(["\U0001F4CA Overall Analysis", "\U0001F4C5 Monthly Deep Dive", "\U0001F4B8 Comparison Overview"])
            
            # Tab 1: Overall Analysis
            with tab1:
                # Top metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    total_expense = df['INR'].sum()
                    st.metric("Total Expenses", f"\u20B9{total_expense:,.2f}")
                with col2:
                    avg_monthly = df.groupby('YearMonth')['INR'].sum().mean()
                    st.metric("Average Monthly", f"\u20B9{avg_monthly:,.2f}")
                with col3:
                    max_monthly = df.groupby('YearMonth')['INR'].sum().max()
                    st.metric("Highest Monthly", f"\u20B9{max_monthly:,.2f}")
                with col4:
                    num_transactions = len(df)
                    st.metric("Total Transactions", num_transactions)
                
                # Additional Filters
                category_filter = st.multiselect("Filter by Category", df['Category'].unique())
                if category_filter:
                    df = df[df['Category'].isin(category_filter)]
                
                # Graphs
                col1, col2 = st.columns(2)
                
                with col1:
                    # Monthly trend
                    monthly_expenses = df.groupby('YearMonth')['INR'].sum().reset_index()
                    fig = px.bar(monthly_expenses, x='YearMonth', y='INR',
                                 title='Monthly Expense Trend',
                                 labels={'INR': 'Expenses (₹)', 'YearMonth': 'Month'},
                                 text_auto=True)
                    fig.update_layout(height=400, xaxis_title='Month', yaxis_title='Expenses (₹)')
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Category breakdown
                    category_expenses = df.groupby('Category')['INR'].sum().reset_index()
                    category_expenses.sort_values(by='INR', ascending=False, inplace=True)
                    fig = px.bar(category_expenses, x='Category', y='INR',
                                 title='Expenses by Category',
                                 labels={'INR': 'Expenses (₹)', 'Category': 'Category'},
                                 text_auto=True)
                    fig.update_layout(height=400, xaxis_title='Category', yaxis_title='Expenses (₹)')
                    st.plotly_chart(fig, use_container_width=True)

                # Category-wise Trends with Filters
                selected_categories = st.multiselect("Select Categories for Trend Analysis", category_expenses['Category'].tolist(), default=category_expenses['Category'].tolist())
                category_monthly = df.pivot_table(
                    index='YearMonth',
                    columns='Category',
                    values='INR',
                    aggfunc='sum'
                ).fillna(0)
                category_monthly = category_monthly[selected_categories]
                fig = px.line(category_monthly,
                              title='Category-wise Expense Trends',
                              labels={'value': 'Expenses (₹)', 'YearMonth': 'Month'})
                fig.update_layout(height=500)
                st.plotly_chart(fig, use_container_width=True)

                # Subcategory-wise Trends
                st.subheader("Subcategory-wise Expense Trends")
                selected_category = st.selectbox("Select a Category for Subcategory Trends", df['Category'].unique(), index=0)
                filtered_subcategory_data = df[df['Category'] == selected_category]
                subcategory_monthly = filtered_subcategory_data.pivot_table(
                    index='YearMonth',
                    columns='Subcategory',
                    values='INR',
                    aggfunc='sum'
                ).fillna(0)
                fig = px.line(subcategory_monthly,
                              title=f'Subcategory Trends in {selected_category}',
                              labels={'value': 'Expenses (₹)', 'YearMonth': 'Month'})
                fig.update_layout(height=500)
                st.plotly_chart(fig, use_container_width=True)

                # Additional Graphs
                st.subheader("Additional Insights")
                top_categories = df.groupby(['Category', 'Subcategory'])['INR'].sum().reset_index()
                fig = px.treemap(top_categories, path=['Category', 'Subcategory'], values='INR',
                                  title='Top Expense Categories',
                                  labels={'INR': 'Total Expenses (₹)'})
                fig.update_traces(textinfo="label+value")
                st.plotly_chart(fig, use_container_width=True)

            # Tab 2: Monthly Analysis
            with tab2:
                # Month selector
                all_months = sorted(df['YearMonth'].unique())
                selected_month = st.selectbox("Select Month", all_months)
                
                monthly_data = df[df['YearMonth'] == selected_month]
                
                # Monthly metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    month_total = monthly_data['INR'].sum()
                    st.metric("Total Expenses", f"\u20B9{month_total:,.2f}")
                with col2:
                    avg_daily = month_total / monthly_data['Date'].dt.day.nunique()
                    st.metric("Average Daily", f"\u20B9{avg_daily:,.2f}")
                with col3:
                    transactions = len(monthly_data)
                    st.metric("Total Transactions", transactions)
                with col4:
                    max_expense_day = monthly_data.groupby('Date')['INR'].sum().max()
                    st.metric("Max Daily Expense", f"\u20B9{max_expense_day:,.2f}")

                # Key Metrics of Category Breakdown
                st.subheader("Key Metrics of Category Breakdown")
                category_totals = monthly_data.groupby('Category')['INR'].sum().reset_index()
                category_totals.sort_values(by='INR', ascending=False, inplace=True)
                st.dataframe(category_totals.style.format({'INR': '₹{:,.2f}'}), use_container_width=True)

                # Category vs Amount Bar Chart
                fig = px.bar(category_totals.sort_values(by='INR', ascending=False), x='Category', y='INR', title='Category vs Amount', text='INR')
                st.plotly_chart(fig, use_container_width=True)

                # Stacked Bar Chart for Categories and Subcategories
                stacked_data = monthly_data.groupby(['Category', 'Subcategory'])['INR'].sum().reset_index()
                stacked_data.sort_values(by='INR', ascending=False, inplace=True)
                fig = px.bar(stacked_data, x='Category', y='INR', color='Subcategory',
                             title='Category and Subcategory Breakdown')
                st.plotly_chart(fig, use_container_width=True)

                # Treemap for Categories and Subcategories
                fig = px.treemap(stacked_data, path=['Category', 'Subcategory'], values='INR',
                                 title='Treemap of Categories and Subcategories')
                st.plotly_chart(fig, use_container_width=True)

                # Table of Categories and Totals
                st.subheader("Category Totals")
                st.dataframe(category_totals.style.format({'INR': '₹{:,.2f}'}), use_container_width=True)

                # Table for Subcategories by Selected Category
                st.subheader("Subcategories for Selected Category")
                selected_category = st.selectbox("Select a Category", category_totals['Category'].unique())
                subcategory_data = monthly_data[monthly_data['Category'] == selected_category]
                subcategory_totals = subcategory_data.groupby('Subcategory')['INR'].sum().reset_index()
                subcategory_totals.sort_values(by='INR', ascending=False, inplace=True)
                st.dataframe(subcategory_totals.style.format({'INR': '₹{:,.2f}'}), use_container_width=True)

            # Tab 3: Comparison Overview
            with tab3:
                st.subheader("Expense Comparison Overview")
                recent_months = df['YearMonth'].drop_duplicates().sort_values(ascending=False).head(3)
                comparison_data = df[df['YearMonth'].isin(recent_months)]
                
                # Summarized table
                comparison_table = comparison_data.groupby(['Category', 'Subcategory', 'YearMonth'])['INR'].sum().reset_index()
                grouped_table = comparison_table.groupby(['Category', 'Subcategory']).agg(
                    Subtotal=('INR', 'sum'),
                    Total=('INR', lambda x: x.sum())
                ).reset_index()
                st.dataframe(grouped_table.style.format({'Subtotal': '₹{:,.2f}', 'Total': '₹{:,.2f}'}), use_container_width=True)

if __name__ == "__main__":
    main()
