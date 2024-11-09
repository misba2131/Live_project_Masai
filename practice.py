import pandas as pd
import numpy as np
import streamlit as st
import Preprocessor

# Reading the data
df = pd.read_csv("data.csv")

# Creatiing time features
df = Preprocessor.fetch_time_features(df)

# sidebar
st.sidebar.title("Filters")


#financial Year Filter

selected_year=Preprocessor.multiselect("Select Year",df["Financial_Year"].unique())

# Retailer Filter
selected_retailer = Preprocessor.multiselect("Select Retailer",df["Retailer"].unique())

# Company Filter
selected_company = Preprocessor.multiselect("Select Company",df["Company"].unique())

# Financial month filter
selected_month = Preprocessor.multiselect("Select Finacial Month",df["Financial_Month"].unique())

st.title("Sales Dash Board")


filter_df = df[(df["Financial_Year"].isin(selected_year)) &
               (df["Retailer"].isin(selected_retailer)) &
               (df["Company"].isin(selected_company)) &
               (df["Financial_Month"].isin(selected_month))]

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label = "Total Sales", value = int(filter_df["Amount"].sum()))
with col2:
    st.metric(label = "Total Margin", value = int(filter_df["Margin"].sum()))
with col3:
    st.metric(label="Total Trancsactions", value = len(filter_df["Margin"]))
with col4:
    st.metric(label= "Margin Percentage(in %)", value = int(filter_df["Margin"].sum()*100/df["Amount"].sum()))


yearly_sales = filter_df[["Financial_Year", "Financial_Month", "Amount"]].groupby(["Financial_Year", "Financial_Month"]).sum().reset_index().pivot(index = "Financial_Month", columns = "Financial_Year", values = "Amount")
st.line_chart(yearly_sales, x_label = "Financial Month", y_label = "Total sales")

col5, col6 = st.columns(2)
# Retailer Revenue
with col5:
    st.title("Retailers count by revenue %")
    retailer_count = Preprocessor.fetch_top_revenue_retailers(filter_df)
    retailer_count.set_index("percentage revenue", inplace = True)
    st.bar_chart(retailer_count, x_label = "percentage revenue",y_label = "retailer_count")

with col6:
    st.title("Companies count by revenue %")
    company_count = Preprocessor.fetch_top_revenue_companies(filter_df)
    company_count.set_index("percentage revenue", inplace = True)
    st.bar_chart(company_count, x_label = "percentage revenue",y_label = "company_count")
