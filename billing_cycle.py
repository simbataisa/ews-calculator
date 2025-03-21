import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import calendar
import locale

# Cài đặt locale cho Việt Nam để định dạng tiền tệ
try:
    locale.setlocale(locale.LC_ALL, 'vi_VN.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_ALL, 'vi_VN')
    except:
        pass  # Nếu không có locale Tiếng Việt, sử dụng mặc định


# Hàm tính ngày cuối cùng của tháng
def get_last_day_of_month(date):
    next_month = date.replace(day=28) + timedelta(days=4)
    return next_month - timedelta(days=next_month.day)


# Hàm tính ngày đầu tiên của tháng
def get_first_day_of_month(date):
    return date.replace(day=1)


# Hàm tính số ngày trong tháng
def get_days_in_month(date):
    return calendar.monthrange(date.year, date.month)[1]


# Hàm định dạng tiền tệ Việt Nam
def format_vnd(amount):
    try:
        return locale.currency(amount, grouping=True, symbol=True)
    except:
        return f"{amount:,.0f} VND"


# Hàm tính toán phương pháp 1: Cố định 30 ngày
def calculate_method1(start_date, num_months, monthly_rate):
    cycles = []
    current_date = start_date

    for i in range(num_months):
        end_date = current_date + timedelta(days=30)

        cycles.append({
            "Chu kỳ": i + 1,
            "Ngày bắt đầu": current_date.strftime("%d/%m/%Y"),
            "Ngày kết thúc": end_date.strftime("%d/%m/%Y"),
            "Số ngày": 30,
            "Số tiền": monthly_rate
        })

        current_date = end_date

    return cycles


# Hàm tính toán phương pháp 2: Prorated theo tháng
def calculate_method2(start_date, num_months, monthly_rate):
    cycles = []
    current_date = start_date
    remaining_months = num_months

    # Tháng đầu tiên - prorated
    first_month_end = get_last_day_of_month(current_date)
    days_in_first_month = get_days_in_month(current_date)
    first_month_days = (first_month_end.day - current_date.day + 1)
    first_month_rate = round((first_month_days / days_in_first_month) * monthly_rate)

    cycles.append({
        "Chu kỳ": 1,
        "Ngày bắt đầu": current_date.strftime("%d/%m/%Y"),
        "Ngày kết thúc": first_month_end.strftime("%d/%m/%Y"),
        "Số ngày": first_month_days,
        "Số tiền": first_month_rate,
        "Prorated": True
    })

    remaining_months -= 1

    # Các tháng giữa - tính đầy đủ
    next_month = first_month_end.replace(day=1) + timedelta(days=32)
    next_month = next_month.replace(day=1)

    for i in range(remaining_months - 1):
        if remaining_months <= 1:
            break

        month_start = get_first_day_of_month(next_month)
        month_end = get_last_day_of_month(next_month)
        days_in_month = get_days_in_month(next_month)

        cycles.append({
            "Chu kỳ": len(cycles) + 1,
            "Ngày bắt đầu": month_start.strftime("%d/%m/%Y"),
            "Ngày kết thúc": month_end.strftime("%d/%m/%Y"),
            "Số ngày": days_in_month,
            "Số tiền": monthly_rate,
            "Prorated": False
        })

        next_month = (next_month.replace(day=1) + timedelta(days=32)).replace(day=1)

    # Tháng cuối - prorated nếu còn
    if remaining_months > 0:
        last_month_start = get_first_day_of_month(next_month)

        # Ngày kết thúc tương ứng với ngày bắt đầu - 1
        last_month_end = last_month_start.replace(day=start_date.day - 1)

        # Xử lý trường hợp ngày không hợp lệ (ví dụ: 31 tháng 2)
        if last_month_end.day < last_month_start.day:
            last_month_end = get_last_day_of_month(last_month_start)

        days_in_last_month = get_days_in_month(last_month_start)
        last_month_days = last_month_end.day
        last_month_rate = round((last_month_days / days_in_last_month) * monthly_rate)

        cycles.append({
            "Chu kỳ": len(cycles) + 1,
            "Ngày bắt đầu": last_month_start.strftime("%d/%m/%Y"),
            "Ngày kết thúc": last_month_end.strftime("%d/%m/%Y"),
            "Số ngày": last_month_days,
            "Số tiền": last_month_rate,
            "Prorated": True
        })

    return cycles


# Thiết lập giao diện Streamlit
st.set_page_config(
    page_title="So sánh phương pháp tính hóa đơn",
    layout="wide"
)

st.title("So sánh phương pháp tính hóa đơn")

# Tạo giao diện nhập liệu
st.subheader("Thông tin đầu vào")

col1, col2, col3 = st.columns(3)

with col1:
    start_date = st.date_input(
        "Ngày bắt đầu",
        value=datetime.now().date(),
        format="DD/MM/YYYY"
    )

with col2:
    num_months = st.number_input(
        "Số tháng",
        min_value=1,
        max_value=24,
        value=6
    )

with col3:
    monthly_rate = st.number_input(
        "Giá mỗi tháng (VND)",
        min_value=1000,
        value=1000000,
        step=10000
    )

# Tính toán các chu kỳ
method1_cycles = calculate_method1(start_date, num_months, monthly_rate)
method2_cycles = calculate_method2(start_date, num_months, monthly_rate)

# Chuyển đổi sang DataFrame
df_method1 = pd.DataFrame(method1_cycles)
df_method2 = pd.DataFrame(method2_cycles)

# Tính tổng
method1_total = sum(cycle["Số tiền"] for cycle in method1_cycles)
method2_total = sum(cycle["Số tiền"] for cycle in method2_cycles)
difference = method1_total - method2_total

# Hiển thị kết quả
st.subheader("So sánh hai phương pháp")

tab1, tab2 = st.tabs(["Bảng chi tiết", "Tóm tắt"])

with tab1:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"### Phương pháp 1: Cố định 30 ngày")
        st.markdown(f"**Tổng tiền: {format_vnd(method1_total)}**")
        st.dataframe(
            df_method1.style.format({
                "Số tiền": lambda x: format_vnd(x)
            }),
            hide_index=True,
            use_container_width=True
        )

    with col2:
        st.markdown(f"### Phương pháp 2: Prorated theo tháng")
        st.markdown(f"**Tổng tiền: {format_vnd(method2_total)}**")


        # Tạo CSS cho hàng prorated
        def highlight_prorated(row):
            if 'Prorated' in row and row['Prorated']:
                return ['background-color: #FFF9C4'] * len(row)
            return [''] * len(row)


        # Hiển thị dataframe với highlight
        df_display = df_method2.drop(columns=['Prorated']) if 'Prorated' in df_method2 else df_method2
        st.dataframe(
            df_display.style.apply(highlight_prorated, axis=1).format({
                "Số tiền": lambda x: format_vnd(x)
            }),
            hide_index=True,
            use_container_width=True
        )

with tab2:
    st.markdown("### Tóm tắt so sánh")

    st.markdown("""
    - **Phương pháp 1 (30 ngày cố định)**: Mỗi chu kỳ thanh toán đều có 30 ngày, không phụ thuộc vào tháng.
    - **Phương pháp 2 (Prorated)**: Tháng đầu và tháng cuối được tính theo tỷ lệ số ngày, các tháng giữa tính từ đầu đến cuối tháng.
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Phương pháp 1", format_vnd(method1_total))

    with col2:
        st.metric("Phương pháp 2", format_vnd(method2_total))

    with col3:
        st.metric("Chênh lệch", format_vnd(difference),
                  delta=f"{difference / method2_total * 100:.2f}%" if method2_total else "0%")

    # Biểu đồ so sánh
    df_summary = pd.DataFrame({
        'Phương pháp': ['Phương pháp 1: Cố định 30 ngày', 'Phương pháp 2: Prorated theo tháng'],
        'Tổng tiền': [method1_total, method2_total]
    })

    st.bar_chart(df_summary, x='Phương pháp', y='Tổng tiền')

# Thêm ghi chú
st.markdown("""
---
### Ghi chú:
- Các hàng có màu vàng nhạt trong Phương pháp 2 là chu kỳ được tính theo tỷ lệ (prorated).
- Phương pháp 1 luôn có chu kỳ cố định 30 ngày, không phụ thuộc vào số ngày thực tế trong tháng.
- Phương pháp 2 tính dựa trên lịch thực tế, với chu kỳ đầu và cuối được tính theo tỷ lệ ngày sử dụng.
""")