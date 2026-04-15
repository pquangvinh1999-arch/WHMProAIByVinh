import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# --- Cấu hình trang ---
st.set_page_config(page_title="Sales Analysis Dashboard", layout="wide")

# --- 1. Tạo dữ liệu giả lập (Mock Data) ---
@st.cache_data # Cache lại để không phải tạo lại mỗi khi nhấn nút
def load_data():
    np.random.seed(42)
    date_rng = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    categories = ['Electronics', 'Clothing', 'Home & Kitchen', 'Books']
    
    data = {
        'Date': np.random.choice(date_rng, 1000),
        'Category': np.random.choice(categories, 1000),
        'Sales': np.random.uniform(10, 500, 1000),
        'Profit': np.random.uniform(2, 100, 1000),
        'Quantity': np.random.randint(1, 10, 1000)
    }
    df = pd.DataFrame(data)
    df = df.sort_values('Date')
    return df

df = load_data()

# --- 2. Sidebar (Bộ lọc dữ liệu) ---
st.sidebar.header("Bộ lọc báo cáo")
category_filter = st.sidebar.multiselect(
    "Chọn danh mục sản phẩm:",
    options=df['Category'].unique(),
    default=df['Category'].unique()
)

# Lọc dữ liệu dựa trên sidebar
df_filtered = df[df['Category'].isin(category_filter)]

# --- 3. Giao diện chính (Main Dashboard) ---
st.title("📊 Hệ thống Phân tích Metric Tự động")
st.markdown("Đây là bản demo tool phân tích dữ liệu tự động dùng **Python + Streamlit + Plotly**.")

# --- Hiển thị Metric (KPIs) ---
col1, col2, col3, col4 = st.columns(4)
total_sales = df_filtered['Sales'].sum()
total_profit = df_filtered['Profit'].sum()
avg_order = df_filtered['Sales'].mean()
total_qty = df_filtered['Quantity'].sum()

col1.metric("Tổng Doanh Thu", f"${total_sales:,.0f}")
col2.metric("Tổng Lợi Nhuận", f"${total_profit:,.0f}")
col3.metric("Giá trị đơn trung bình", f"${avg_order:,.2f}")
col4.metric("Số lượng bán ra", f"{total_qty:,.0f}")

st.divider()

# --- 4. Vẽ biểu đồ ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📈 Xu hướng Doanh thu theo thời gian")
    # Gom nhóm dữ liệu theo ngày để vẽ line chart
    df_trend = df_filtered.groupby('Date')['Sales'].sum().reset_index()
    fig_line = px.line(df_trend, x='Date', y='Sales', 
                       labels={'Sales': 'Doanh thu ($)', 'Date': 'Ngày'},
                       color_discrete_sequence=['#00CC96'])
    st.plotly_chart(fig_line, use_container_width=True)

with col_right:
    st.subheader("🍰 Tỷ trọng Doanh thu theo Danh mục")
    fig_pie = px.pie(df_filtered, values='Sales', names='Category', 
                     hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig_pie, use_container_width=True)

# --- 5. Bảng dữ liệu chi tiết ---
st.subheader("📋 Dữ liệu chi tiết")
st.dataframe(df_filtered, use_container_width=True)

# Nút download dữ liệu đã lọc
csv = df_filtered.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Tải báo cáo về máy (CSV)",
    data=csv,
    file_name='filtered_report.csv',
    mime='text/csv',
)
