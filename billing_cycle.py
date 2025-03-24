import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, date
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


# Hàm lấy ngày cụ thể của tháng, nếu không hợp lệ thì lấy ngày cuối tháng
def get_specific_day_of_month(year, month, day):
    try:
        return date(year, month, day)
    except ValueError:
        # Nếu ngày không hợp lệ (ví dụ: 30/2), lấy ngày cuối cùng của tháng
        return get_last_day_of_month(date(year, month, 1))


# Hàm tính ngày đầu tiên của tháng
def get_first_day_of_month(date):
    return date.replace(day=1)


# Hàm tính số ngày trong tháng
def get_days_in_month(date):
    return calendar.monthrange(date.year, date.month)[1]


# Hàm tính số ngày giữa hai ngày
def days_between(d1, d2):
    return (d2 - d1).days + 1  # +1 vì tính cả ngày cuối


# Hàm định dạng tiền tệ Việt Nam
def format_vnd(amount):
    try:
        return locale.currency(amount, grouping=True, symbol=True)
    except:
        return f"{amount:,.0f} VND"


# Hàm tính tỷ lệ pro-rate dựa trên số ngày
def calculate_prorated_amount(days, month_days, monthly_rate):
    return round((days / month_days) * monthly_rate)


# Thiết lập giao diện Streamlit
st.set_page_config(
    page_title="So sánh phương pháp tính hóa đơn",
    layout="wide"
)

st.title("So sánh phương pháp tính hóa đơn")

# Khởi tạo session state nếu chưa có
if "billing_cycles" not in st.session_state:
    st.session_state.billing_cycles = {
        "method1": [],
        "method2": [],
        "method3": []  # Phương pháp mới với ngày kết thúc chu kỳ cố định
    }

# Tab chính
tab_input, tab_custom, tab_results = st.tabs(["Nhập thông tin cơ bản", "Tùy chỉnh chu kỳ", "Kết quả so sánh"])

with tab_input:
    st.subheader("Thông tin cơ bản")

    col1, col2, col3 = st.columns(3)

    with col1:
        start_date = st.date_input(
            "Ngày bắt đầu",
            value=datetime.now().date(),
            format="DD/MM/YYYY"
        )

    with col2:
        contract_months = st.number_input(
            "Số tháng hợp đồng",
            min_value=1,
            max_value=36,
            value=6
        )

    with col3:
        monthly_rate = st.number_input(
            "Giá mỗi tháng (VND)",
            min_value=1000,
            value=1000000,
            step=10000
        )

    # Phần mới: Chọn ngày kết thúc chu kỳ cố định
    st.subheader("Cấu hình ngày kết thúc chu kỳ (cho Phương pháp 3)")

    col1, col2 = st.columns(2)

    with col1:
        cycle_end_day = st.number_input(
            "Ngày kết thúc chu kỳ hàng tháng",
            min_value=1,
            max_value=31,
            value=15
        )

    with col2:
        st.info(
            f"Chu kỳ thanh toán sẽ kết thúc vào ngày {cycle_end_day} hàng tháng. Nếu tháng nào không có ngày này (ví dụ: ngày 31/2), sẽ sử dụng ngày cuối cùng của tháng đó.")

    # Tính toán chu kỳ cho 3 phương pháp
    # 1. Phương pháp 1: Cố định 30 ngày
    method1_cycles = []
    current_date = start_date

    for i in range(contract_months):
        end_date = current_date + timedelta(days=30 - 1)  # -1 vì tính cả ngày đầu

        method1_cycles.append({
            "index": i,
            "Chu kỳ": i + 1,
            "Ngày bắt đầu": current_date,
            "Ngày kết thúc": end_date,
            "Số ngày": 30,
            "Số tiền": monthly_rate,
            "Custom": False
        })

        current_date = end_date + timedelta(days=1)

    # 2. Phương pháp 2: Prorated theo tháng
    method2_cycles = []
    current_date = start_date
    remaining_months = contract_months

    # Tháng đầu tiên - prorated
    first_month_end = get_last_day_of_month(current_date)
    days_in_first_month = get_days_in_month(current_date)
    first_month_days = (first_month_end - current_date).days + 1
    first_month_rate = calculate_prorated_amount(first_month_days, days_in_first_month, monthly_rate)

    method2_cycles.append({
        "index": 0,
        "Chu kỳ": 1,
        "Ngày bắt đầu": current_date,
        "Ngày kết thúc": first_month_end,
        "Số ngày": first_month_days,
        "Số tiền": first_month_rate,
        "Prorated": True,
        "Custom": False
    })

    remaining_months -= 1

    # Các tháng giữa - tính đầy đủ
    next_month = first_month_end + timedelta(days=1)

    for i in range(remaining_months - 1):
        if remaining_months <= 1:
            break

        month_start = next_month
        month_end = get_last_day_of_month(month_start)
        days_in_month = (month_end - month_start).days + 1

        method2_cycles.append({
            "index": len(method2_cycles),
            "Chu kỳ": len(method2_cycles) + 1,
            "Ngày bắt đầu": month_start,
            "Ngày kết thúc": month_end,
            "Số ngày": days_in_month,
            "Số tiền": monthly_rate,
            "Prorated": False,
            "Custom": False
        })

        next_month = month_end + timedelta(days=1)

    # Tháng cuối - prorated nếu còn
    if remaining_months > 0:
        last_month_start = next_month

        # Tính ngày kết thúc (tương tự ngày bắt đầu của tháng tới)
        temp_date = last_month_start.replace(day=start_date.day)
        if temp_date.month == last_month_start.month:
            # Ngày hợp lệ trong tháng cuối
            last_month_end = temp_date - timedelta(days=1)
            if last_month_end.month != last_month_start.month:
                last_month_end = get_last_day_of_month(last_month_start)
        else:
            # Ngày không hợp lệ, lấy ngày cuối tháng
            last_month_end = get_last_day_of_month(last_month_start)

        days_in_last_month = get_days_in_month(last_month_start)
        last_month_days = (last_month_end - last_month_start).days + 1
        last_month_rate = calculate_prorated_amount(last_month_days, days_in_last_month, monthly_rate)

        method2_cycles.append({
            "index": len(method2_cycles),
            "Chu kỳ": len(method2_cycles) + 1,
            "Ngày bắt đầu": last_month_start,
            "Ngày kết thúc": last_month_end,
            "Số ngày": last_month_days,
            "Số tiền": last_month_rate,
            "Prorated": True,
            "Custom": False
        })

    # 3. Phương pháp 3: Ngày kết thúc chu kỳ cố định
    method3_cycles = []

    # Xác định ngày kết thúc chu kỳ đầu tiên
    current_date = start_date
    if current_date.day <= cycle_end_day:
        # Ngày bắt đầu trước hoặc bằng ngày kết thúc chu kỳ của tháng hiện tại
        first_cycle_end = get_specific_day_of_month(current_date.year, current_date.month, cycle_end_day)
    else:
        # Ngày bắt đầu sau ngày kết thúc chu kỳ, lấy ngày kết thúc chu kỳ của tháng sau
        next_month = current_date.month + 1 if current_date.month < 12 else 1
        next_year = current_date.year if current_date.month < 12 else current_date.year + 1
        first_cycle_end = get_specific_day_of_month(next_year, next_month, cycle_end_day)

    # Chu kỳ đầu tiên (có thể ngắn hơn một tháng đầy đủ)
    first_cycle_days = (first_cycle_end - current_date).days + 1
    days_in_first_month = get_days_in_month(current_date)
    first_cycle_rate = calculate_prorated_amount(first_cycle_days, days_in_first_month, monthly_rate)

    method3_cycles.append({
        "index": 0,
        "Chu kỳ": 1,
        "Ngày bắt đầu": current_date,
        "Ngày kết thúc": first_cycle_end,
        "Số ngày": first_cycle_days,
        "Số tiền": first_cycle_rate,
        "Prorated": True,
        "Custom": False
    })

    # Các chu kỳ tiếp theo
    current_start = first_cycle_end + timedelta(days=1)
    remaining_cycles = contract_months - 1

    for i in range(remaining_cycles):
        # Tính ngày kết thúc chu kỳ tiếp theo
        next_month = current_start.month + 1 if current_start.month < 12 else 1
        next_year = current_start.year if current_start.month < 12 else current_start.year + 1
        next_cycle_end = get_specific_day_of_month(next_year, next_month, cycle_end_day)

        cycle_days = (next_cycle_end - current_start).days + 1

        # Tính toán số tiền dựa trên số ngày trong chu kỳ
        if i == remaining_cycles - 1:  # Chu kỳ cuối cùng
            # Tính toán số ngày trong tháng
            days_in_month = get_days_in_month(current_start)
            cycle_rate = calculate_prorated_amount(cycle_days, days_in_month, monthly_rate)
            is_prorated = True
        else:
            # Chu kỳ giữa - giá đầy đủ
            cycle_rate = monthly_rate
            is_prorated = False

        method3_cycles.append({
            "index": len(method3_cycles),
            "Chu kỳ": len(method3_cycles) + 1,
            "Ngày bắt đầu": current_start,
            "Ngày kết thúc": next_cycle_end,
            "Số ngày": cycle_days,
            "Số tiền": cycle_rate,
            "Prorated": is_prorated,
            "Custom": False
        })

        current_start = next_cycle_end + timedelta(days=1)

    # Cập nhật session state
    st.session_state.billing_cycles = {
        "method1": method1_cycles,
        "method2": method2_cycles,
        "method3": method3_cycles
    }

    # Hiển thị tổng quan
    st.subheader("Tổng quan chu kỳ")

    method1_total = sum(cycle["Số tiền"] for cycle in method1_cycles)
    method2_total = sum(cycle["Số tiền"] for cycle in method2_cycles)
    method3_total = sum(cycle["Số tiền"] for cycle in method3_cycles)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Phương pháp 1: Cố định 30 ngày", format_vnd(method1_total))
        st.write(f"Số chu kỳ: {len(method1_cycles)}")

    with col2:
        st.metric("Phương pháp 2: Prorated theo tháng", format_vnd(method2_total))
        st.write(f"Số chu kỳ: {len(method2_cycles)}")

    with col3:
        st.metric(f"Phương pháp 3: Ngày kết thúc cố định ({cycle_end_day})", format_vnd(method3_total))
        st.write(f"Số chu kỳ: {len(method3_cycles)}")

with tab_custom:
    st.subheader("Tùy chỉnh chu kỳ billing")

    method_selection = st.radio(
        "Chọn phương pháp để tùy chỉnh",
        ["Phương pháp 1: Cố định 30 ngày",
         "Phương pháp 2: Prorated theo tháng",
         f"Phương pháp 3: Ngày kết thúc cố định ({cycle_end_day})"]
    )

    if method_selection.startswith("Phương pháp 1"):
        selected_cycles = st.session_state.billing_cycles["method1"]
    elif method_selection.startswith("Phương pháp 2"):
        selected_cycles = st.session_state.billing_cycles["method2"]
    else:
        selected_cycles = st.session_state.billing_cycles["method3"]

    st.write("Chọn chu kỳ để chỉnh sửa:")

    # Tạo các tab cho từng chu kỳ
    if selected_cycles:
        cycle_tabs = st.tabs([f"Chu kỳ {cycle['Chu kỳ']}" for cycle in selected_cycles])

        for i, tab in enumerate(cycle_tabs):
            with tab:
                cycle = selected_cycles[i]

                col1, col2, col3 = st.columns(3)

                with col1:
                    new_start_date = st.date_input(
                        "Ngày bắt đầu",
                        value=cycle["Ngày bắt đầu"],
                        key=f"start_{method_selection}_{i}",
                        format="DD/MM/YYYY"
                    )

                with col2:
                    new_end_date = st.date_input(
                        "Ngày kết thúc",
                        value=cycle["Ngày kết thúc"],
                        key=f"end_{method_selection}_{i}",
                        format="DD/MM/YYYY"
                    )

                    if new_end_date < new_start_date:
                        st.error("Ngày kết thúc phải sau ngày bắt đầu!")
                        new_end_date = new_start_date

                with col3:
                    days = days_between(new_start_date, new_end_date)

                    if (method_selection.startswith("Phương pháp 2") or method_selection.startswith(
                            "Phương pháp 3")) and cycle.get("Prorated", False):
                        st.write(f"Số ngày: {days}")
                        days_in_month = get_days_in_month(new_start_date)
                        prorated_amount = calculate_prorated_amount(days, days_in_month, monthly_rate)
                        new_amount = st.number_input(
                            "Số tiền (VND)",
                            value=prorated_amount,
                            min_value=0,
                            step=10000,
                            key=f"amount_{method_selection}_{i}"
                        )
                        st.write(f"Tỷ lệ: {days}/{days_in_month} = {days / days_in_month:.2f}")
                    else:
                        st.write(f"Số ngày: {days}")
                        new_amount = st.number_input(
                            "Số tiền (VND)",
                            value=cycle["Số tiền"],
                            min_value=0,
                            step=10000,
                            key=f"amount_{method_selection}_{i}"
                        )

                # Cập nhật chu kỳ nếu có thay đổi
                if new_start_date != cycle["Ngày bắt đầu"] or new_end_date != cycle["Ngày kết thúc"] or new_amount != \
                        cycle["Số tiền"]:
                    cycle["Ngày bắt đầu"] = new_start_date
                    cycle["Ngày kết thúc"] = new_end_date
                    cycle["Số ngày"] = days
                    cycle["Số tiền"] = new_amount
                    cycle["Custom"] = True

                    # Cập nhật session state
                    if method_selection.startswith("Phương pháp 1"):
                        st.session_state.billing_cycles["method1"][i] = cycle
                    elif method_selection.startswith("Phương pháp 2"):
                        st.session_state.billing_cycles["method2"][i] = cycle
                    else:
                        st.session_state.billing_cycles["method3"][i] = cycle
    else:
        st.warning("Không có chu kỳ nào để tùy chỉnh. Vui lòng quay lại tab 'Nhập thông tin cơ bản' để cài đặt.")

with tab_results:
    st.subheader("Kết quả so sánh")

    # Lấy dữ liệu từ session state
    method1_cycles = st.session_state.billing_cycles["method1"]
    method2_cycles = st.session_state.billing_cycles["method2"]
    method3_cycles = st.session_state.billing_cycles["method3"]


    # Tạo DataFrame để hiển thị
    def create_dataframe(cycles, include_prorated=False):
        data = []
        for cycle in cycles:
            row = {
                "Chu kỳ": cycle["Chu kỳ"],
                "Ngày bắt đầu": cycle["Ngày bắt đầu"].strftime("%d/%m/%Y"),
                "Ngày kết thúc": cycle["Ngày kết thúc"].strftime("%d/%m/%Y"),
                "Số ngày": cycle["Số ngày"],
                "Số tiền": cycle["Số tiền"],
                "Tùy chỉnh": "Có" if cycle.get("Custom", False) else "Không"
            }
            if include_prorated:
                row["Prorated"] = "Có" if cycle.get("Prorated", False) else "Không"
            data.append(row)
        return pd.DataFrame(data)


    df_method1 = create_dataframe(method1_cycles)
    df_method2 = create_dataframe(method2_cycles, include_prorated=True)
    df_method3 = create_dataframe(method3_cycles, include_prorated=True)

    # Tính tổng
    method1_total = sum(cycle["Số tiền"] for cycle in method1_cycles)
    method2_total = sum(cycle["Số tiền"] for cycle in method2_cycles)
    method3_total = sum(cycle["Số tiền"] for cycle in method3_cycles)

    # Hiển thị tổng quan
    st.subheader("Tổng quan chi phí")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Phương pháp 1: Cố định 30 ngày", format_vnd(method1_total))

    with col2:
        st.metric("Phương pháp 2: Prorated theo tháng", format_vnd(method2_total),
                  delta=f"{(method2_total - method1_total) / method1_total * 100:.2f}%" if method1_total else "0%")

    with col3:
        st.metric(f"Phương pháp 3: Ngày kết thúc cố định ({cycle_end_day})", format_vnd(method3_total),
                  delta=f"{(method3_total - method1_total) / method1_total * 100:.2f}%" if method1_total else "0%")

    # Hiển thị biểu đồ so sánh
    st.subheader("Biểu đồ so sánh tổng tiền")
    df_summary = pd.DataFrame({
        'Phương pháp': [
            'Phương pháp 1: Cố định 30 ngày',
            'Phương pháp 2: Prorated theo tháng',
            f'Phương pháp 3: Ngày kết thúc cố định ({cycle_end_day})'
        ],
        'Tổng tiền': [method1_total, method2_total, method3_total]
    })

    st.bar_chart(df_summary, x='Phương pháp', y='Tổng tiền')

    # Hiển thị bảng tóm tắt
    st.subheader("Bảng tóm tắt")

    df_method_summary = pd.DataFrame({
        'Phương pháp': [
            'Phương pháp 1: Cố định 30 ngày',
            'Phương pháp 2: Prorated theo tháng',
            f'Phương pháp 3: Ngày kết thúc cố định ({cycle_end_day})'
        ],
        'Tổng tiền': [method1_total, method2_total, method3_total],
        'Số chu kỳ': [len(method1_cycles), len(method2_cycles), len(method3_cycles)],
        'Tiền trung bình/chu kỳ': [
            method1_total / len(method1_cycles) if len(method1_cycles) > 0 else 0,
            method2_total / len(method2_cycles) if len(method2_cycles) > 0 else 0,
            method3_total / len(method3_cycles) if len(method3_cycles) > 0 else 0
        ],
        'Chênh lệch với P1': [
            "0%",
            f"{(method2_total - method1_total) / method1_total * 100:.2f}%" if method1_total else "0%",
            f"{(method3_total - method1_total) / method1_total * 100:.2f}%" if method1_total else "0%"
        ]
    })

    st.dataframe(
        df_method_summary.style.format({
            "Tổng tiền": lambda x: format_vnd(x),
            "Tiền trung bình/chu kỳ": lambda x: format_vnd(x)
        }),
        hide_index=True,
        use_container_width=True
    )

    # Hiển thị chi tiết các chu kỳ cạnh nhau
    st.subheader("Chi tiết chu kỳ theo từng phương pháp")


    # Tạo hàm highlight cho dataframe
    def highlight_custom(row):
        if row['Tùy chỉnh'] == 'Có':
            return ['background-color: #E8F4F9'] * len(row)
        return [''] * len(row)


    def highlight_prorated(row):
        if 'Prorated' in row and row['Prorated'] == 'Có':
            if row['Tùy chỉnh'] == 'Có':
                return ['background-color: #F3E5AB'] * len(row)  # Màu kết hợp
            return ['background-color: #FFF9C4'] * len(row)  # Màu vàng nhạt
        elif row['Tùy chỉnh'] == 'Có':
            return ['background-color: #E8F4F9'] * len(row)  # Màu xanh nhạt
        return [''] * len(row)


    # Hiển thị ba bảng dữ liệu cạnh nhau với khả năng cuộn ngang
    st.markdown("""
    <style>
    .stDataFrame {
        overflow-x: auto !important;
    }
    .scroll-container {
        width: 100%;
        overflow-x: auto;
        white-space: nowrap;
        display: flex;
        gap: 20px;
        margin-bottom: 20px;
    }
    .table-column {
        display: inline-block;
        vertical-align: top;
        min-width: 30%;
        white-space: normal;
    }
    </style>
    """, unsafe_allow_html=True)

    # Sử dụng HTML để tạo container cuộn ngang
    st.markdown('<div class="scroll-container">', unsafe_allow_html=True)

    # Phương pháp 1
    st.markdown('<div class="table-column">', unsafe_allow_html=True)
    st.markdown(f"### Phương pháp 1: Cố định 30 ngày")
    st.markdown(f"**Tổng tiền: {format_vnd(method1_total)}**")

    st.dataframe(
        df_method1.style.apply(highlight_custom, axis=1).format({
            "Số tiền": lambda x: format_vnd(x)
        }),
        hide_index=True,
        use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # Phương pháp 2
    st.markdown('<div class="table-column">', unsafe_allow_html=True)
    st.markdown(f"### Phương pháp 2: Prorated theo tháng")
    st.markdown(f"**Tổng tiền: {format_vnd(method2_total)}**")

    st.dataframe(
        df_method2.style.apply(highlight_prorated, axis=1).format({
            "Số tiền": lambda x: format_vnd(x)
        }),
        hide_index=True,
        use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # Phương pháp 3
    st.markdown('<div class="table-column">', unsafe_allow_html=True)
    st.markdown(f"### Phương pháp 3: Ngày kết thúc cố định ({cycle_end_day})")
    st.markdown(f"**Tổng tiền: {format_vnd(method3_total)}**")

    st.dataframe(
        df_method3.style.apply(highlight_prorated, axis=1).format({
            "Số tiền": lambda x: format_vnd(x)
        }),
        hide_index=True,
        use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # Đóng container cuộn ngang
    st.markdown('</div>', unsafe_allow_html=True)

    # Nút xuất báo cáo
    st.subheader("Xuất báo cáo")
    col1, col2 = st.columns(2)

    with col1:
        # Tạo dữ liệu xuất chi tiết
        all_cycles = []

        for cycle in method1_cycles:
            all_cycles.append({
                "Phương pháp": "Phương pháp 1: Cố định 30 ngày",
                "Chu kỳ": cycle["Chu kỳ"],
                "Ngày bắt đầu": cycle["Ngày bắt đầu"].strftime("%d/%m/%Y"),
                "Ngày kết thúc": cycle["Ngày kết thúc"].strftime("%d/%m/%Y"),
                "Số ngày": cycle["Số ngày"],
                "Số tiền": cycle["Số tiền"],
                "Prorated": "Không",
                "Tùy chỉnh": "Có" if cycle.get("Custom", False) else "Không"
            })

        for cycle in method2_cycles:
            all_cycles.append({
                "Phương pháp": "Phương pháp 2: Prorated theo tháng",
                "Chu kỳ": cycle["Chu kỳ"],
                "Ngày bắt đầu": cycle["Ngày bắt đầu"].strftime("%d/%m/%Y"),
                "Ngày kết thúc": cycle["Ngày kết thúc"].strftime("%d/%m/%Y"),
                "Số ngày": cycle["Số ngày"],
                "Số tiền": cycle["Số tiền"],
                "Prorated": "Có" if cycle.get("Prorated", False) else "Không",
                "Tùy chỉnh": "Có" if cycle.get("Custom", False) else "Không"
            })

        for cycle in method3_cycles:
            all_cycles.append({
                "Phương pháp": f"Phương pháp 3: Ngày kết thúc cố định ({cycle_end_day})",
                "Chu kỳ": cycle["Chu kỳ"],
                "Ngày bắt đầu": cycle["Ngày bắt đầu"].strftime("%d/%m/%Y"),
                "Ngày kết thúc": cycle["Ngày kết thúc"].strftime("%d/%m/%Y"),
                "Số ngày": cycle["Số ngày"],
                "Số tiền": cycle["Số tiền"],
                "Prorated": "Có" if cycle.get("Prorated", False) else "Không",
                "Tùy chỉnh": "Có" if cycle.get("Custom", False) else "Không"
            })

        # Tạo DataFrame từ tất cả chu kỳ
        df_all_cycles = pd.DataFrame(all_cycles)

        st.download_button(
            label="Tải xuống báo cáo chi tiết (CSV)",
            data=df_all_cycles.to_csv(index=False).encode('utf-8'),
            file_name='bao_cao_chi_tiet_hoa_don.csv',
            mime='text/csv',
        )

    with col2:
        # Tạo dữ liệu tóm tắt
        df_summary_export = pd.DataFrame({
            'Phương pháp': [
                'Phương pháp 1: Cố định 30 ngày',
                'Phương pháp 2: Prorated theo tháng',
                f'Phương pháp 3: Ngày kết thúc cố định ({cycle_end_day})'
            ],
            'Tổng tiền': [method1_total, method2_total, method3_total],
            'Số chu kỳ': [len(method1_cycles), len(method2_cycles), len(method3_cycles)],
            'Tiền trung bình/chu kỳ': [
                method1_total / len(method1_cycles) if len(method1_cycles) > 0 else 0,
                method2_total / len(method2_cycles) if len(method2_cycles) > 0 else 0,
                method3_total / len(method3_cycles) if len(method3_cycles) > 0 else 0
            ],
            'Chênh lệch với P1': [
                0,
                method2_total - method1_total,
                method3_total - method1_total
            ],
            'Chênh lệch %': [
                "0%",
                f"{(method2_total - method1_total) / method1_total * 100:.2f}%" if method1_total else "0%",
                f"{(method3_total - method1_total) / method1_total * 100:.2f}%" if method1_total else "0%"
            ]
        })

        st.download_button(
            label="Tải xuống báo cáo tóm tắt (CSV)",
            data=df_summary_export.to_csv(index=False).encode('utf-8'),
            file_name='tom_tat_so_sanh_hoa_don.csv',
            mime='text/csv',
        )

# Thêm ghi chú
st.markdown("""
---
### Ghi chú:
- **Phương pháp 1**: Mỗi chu kỳ thanh toán đều có 30 ngày cố định, không phụ thuộc vào số ngày trong tháng.
- **Phương pháp 2**: Chu kỳ thanh toán theo tháng (từ 1 đến cuối tháng), với chu kỳ đầu và cuối được tính theo tỷ lệ.
- **Phương pháp 3**: Chu kỳ thanh toán kết thúc vào một ngày cố định hàng tháng, với chu kỳ đầu và cuối được tính theo tỷ lệ.

### Màu sắc ký hiệu:
- **Màu vàng nhạt**: Chu kỳ được tính theo tỷ lệ (prorated).
- **Màu xanh nhạt**: Chu kỳ đã được tùy chỉnh thủ công.
- **Màu vàng-xanh**: Chu kỳ vừa tính theo tỷ lệ vừa được tùy chỉnh thủ công.
""")