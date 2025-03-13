import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 Báo cáo Doanh thu & Chi phí Shopee")

uploaded_file = st.file_uploader("📂 Tải lên file Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df["Ngày"] = pd.to_datetime(df["Ngày"])
    
    # Tính tổng doanh thu, chi phí, lợi nhuận
    total_revenue = df["Doanh thu"].sum()
    total_cost = df["Chi phí"].sum()
    profit = total_revenue - total_cost
    
    st.metric("💰 Tổng doanh thu", f"{total_revenue:,.0f} VND")
    st.metric("💸 Tổng chi phí", f"{total_cost:,.0f} VND")
    st.metric("📈 Lợi nhuận", f"{profit:,.0f} VND")

    # Vẽ biểu đồ
    df_grouped = df.groupby("Ngày").sum()
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(df_grouped.index, df_grouped["Doanh thu"], label="Doanh thu", marker="o")
    ax.plot(df_grouped.index, df_grouped["Chi phí"], label="Chi phí", marker="s")
    ax.set_xlabel("Ngày")
    ax.set_ylabel("Số tiền (VND)")
    ax.legend()
    ax.grid()

    st.pyplot(fig)

    # Hiển thị bảng dữ liệu
    st.dataframe(df)
