import streamlit as st
import pandas as pd
import plotly.express as px

# Hàm tải dữ liệu
@st.cache_data
def load_data(file):
    df = pd.read_excel(file, sheet_name="orders")
    df['Ngày đặt hàng'] = pd.to_datetime(df['Ngày đặt hàng'])
    return df

# Giao diện Streamlit
st.title("📊 Công Cụ Phân Tích Đơn Hàng Shopee")

# Upload file
uploaded_file = st.file_uploader("Tải lên file Excel", type=["xlsx"])
if uploaded_file:
    df = load_data(uploaded_file)
    st.success("📂 Dữ liệu đã tải lên thành công!")
    
    # Bộ lọc thời gian
    min_date, max_date = df['Ngày đặt hàng'].min(), df['Ngày đặt hàng'].max()
    date_range = st.date_input("📅 Chọn khoảng thời gian", [min_date, max_date], min_value=min_date, max_value=max_date)
    df_filtered = df[(df['Ngày đặt hàng'] >= pd.to_datetime(date_range[0])) & (df['Ngày đặt hàng'] <= pd.to_datetime(date_range[1]))]
    
    # Bộ lọc trạng thái đơn hàng
    status_options = df_filtered['Trạng Thái Đơn Hàng'].unique()
    selected_status = st.multiselect("📌 Chọn trạng thái đơn hàng", status_options, default=status_options)
    df_filtered = df_filtered[df_filtered['Trạng Thái Đơn Hàng'].isin(selected_status)]
    
    # Tổng quan doanh thu
    total_revenue = df_filtered['Doanh thu ròng'].sum()
    total_orders = len(df_filtered)
    total_cancelled = len(df_filtered[df_filtered['Trạng Thái Đơn Hàng'].str.contains("hủy", case=False, na=False)])
    
    st.metric("💰 Tổng doanh thu", f"{total_revenue:,.0f} VND")
    st.metric("📦 Tổng số đơn", total_orders)
    st.metric("❌ Đơn bị hủy", total_cancelled)
    
    # Biểu đồ doanh thu theo ngày
    df_grouped = df_filtered.groupby(df_filtered['Ngày đặt hàng'].dt.date)['Doanh thu ròng'].sum().reset_index()
    fig = px.line(df_grouped, x='Ngày đặt hàng', y='Doanh thu ròng', title='📈 Biểu đồ doanh thu theo ngày')
    st.plotly_chart(fig)
    
    # Hiển thị bảng dữ liệu
    st.dataframe(df_filtered[['Mã đơn hàng', 'Ngày đặt hàng', 'Trạng Thái Đơn Hàng', 'Doanh thu ròng']])
    
    # Xuất báo cáo
    if st.button("📥 Tải xuống báo cáo"):
        df_filtered.to_excel("report.xlsx", index=False)
        st.success("✅ Báo cáo đã được tạo!")
