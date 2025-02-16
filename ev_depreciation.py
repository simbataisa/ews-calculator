import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import numpy as np

# Constants and Initial Data
VINFAST_MODELS = {
    'VF3': {'initial_price': 240_000_000},
    'VF34': {'initial_price': 550_000_000},
    'VF5': {'initial_price': 458_000_000},
    'VF6': {'initial_price': 675_000_000},
    'VF7': {'initial_price': 850_000_000},
    'VF8': {'initial_price': 1_090_000_000},
    'VF9': {'initial_price': 1_470_000_000}
}


def format_vnd(amount):
    """Format amount in VND currency"""
    if amount >= 1_000_000_000:
        return f"{amount / 1_000_000_000:,.2f} Tỷ VNĐ"
    return f"{amount / 1_000_000:,.1f} Triệu VNĐ"


def create_model_comparison_chart(models_data):
    """Create comparison chart for VinFast models"""
    fig = go.Figure()

    # Add bars for initial prices
    fig.add_trace(go.Bar(
        name='Giá Ban Đầu',
        x=list(models_data.keys()),
        y=[data['initial_price'] for data in models_data.values()],
        text=[format_vnd(data['initial_price']) for data in models_data.values()],
        textposition='auto',
    ))

    fig.update_layout(
        title="So Sánh Giá Các Mẫu VinFast",
        xaxis_title="Mẫu Xe",
        yaxis_title="Giá (VNĐ)",
        height=500,
        yaxis=dict(tickformat=","),
        showlegend=True
    )

    return fig


def create_depreciation_comparison(models_data):
    """Create depreciation comparison chart"""
    fig = go.Figure()

    # Simulate depreciation for each model (example data)
    months = list(range(0, 61, 12))
    for model, data in models_data.items():
        initial_price = data['initial_price']
        # Simulate depreciation rates (can be replaced with actual data)
        depreciation_rates = [1.0, 0.85, 0.75, 0.65, 0.58]
        values = [initial_price * rate for rate in depreciation_rates]

        fig.add_trace(go.Scatter(
            x=months,
            y=values,
            name=model,
            mode='lines+markers',
            hovertemplate="Năm %{x//12}<br>" +
                          "Giá: %{text}<br>" +
                          "Tỷ lệ: %{customdata}%",
            text=[format_vnd(v) for v in values],
            customdata=[rate * 100 for rate in depreciation_rates]
        ))

    fig.update_layout(
        title="So Sánh Khấu Hao Theo Thời Gian",
        xaxis_title="Số Tháng",
        yaxis_title="Giá Trị (VNĐ)",
        height=600,
        yaxis=dict(tickformat=","),
        showlegend=True,
        hovermode='x unified'
    )

    return fig


def show_model_details(model_name, model_data):
    """Display detailed information for a specific model"""
    st.subheader(f"Chi Tiết Mẫu {model_name}")

    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            "Giá Ban Đầu",
            format_vnd(model_data['initial_price'])
        )

    with col2:
        st.metric(
            "Giá Sau 3 Năm (Ước Tính)",
            format_vnd(model_data['initial_price'] * 0.65),
            delta="-35%"
        )


def create_model_specs_comparison():
    """Create model specifications comparison"""
    specs_data = {
        'VF3': {
            'Công Suất': '100 kW',
            'Pin': '35 kWh',
            'Phạm Vi': '~200 km',
            'Chỗ Ngồi': '4',
        },
        'VF34': {
            'Công Suất': '150 kW',
            'Pin': '51 kWh',
            'Phạm Vi': '~300 km',
            'Chỗ Ngồi': '5',
        },
        'VF5': {
            'Công Suất': '130 kW',
            'Pin': '42 kWh',
            'Phạm Vi': '~280 km',
            'Chỗ Ngồi': '5',
        },
        'VF6': {
            'Công Suất': '170 kW',
            'Pin': '59.6 kWh',
            'Phạm Vi': '~350 km',
            'Chỗ Ngồi': '5',
        },
        'VF7': {
            'Công Suất': '260 kW',
            'Pin': '75.3 kWh',
            'Phạm Vi': '~450 km',
            'Chỗ Ngồi': '5',
        },
        'VF8': {
            'Công Suất': '300 kW',
            'Pin': '87.7 kWh',
            'Phạm Vi': '~550 km',
            'Chỗ Ngồi': '7',
        },
        'VF9': {
            'Công Suất': '300 kW',
            'Pin': '92 kWh',
            'Phạm Vi': '~600 km',
            'Chỗ Ngồi': '7',
        }
    }

    # Create DataFrame for comparison
    df = pd.DataFrame(specs_data).T
    return df

# Set page config
st.set_page_config(
    page_title="Phân Tích Giá Trị VF3",
    page_icon="📊",
    layout="wide"
)

# Constants
INITIAL_PRICE = 240_000_000  # VND

# Styling
st.markdown("""
    <style>
    .big-font {
        font-size:24px !important;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 5px;
        margin: 5px;
    }
    .stExpander {
        border: none !important;
        box-shadow: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

def format_vnd(amount):
    """Format amount in VND currency"""
    if amount >= 1_000_000:
        return f"{amount/1_000_000:,.1f} Triệu"
    return f"{amount:,.0f} VNĐ"

def format_price(price, include_delta=False, base_price=None):
    """Format price in VND with optional delta percentage"""
    if include_delta and base_price:
        delta = ((price / base_price) - 1) * 100
        return f"{price/1_000_000:,.1f} Triệu VNĐ", f"{delta:,.1f}%"
    return f"{price/1_000_000:,.1f} Triệu VNĐ"

def create_distribution_plot(price_dist):
    """Create a distribution plot for price prediction"""
    mean = price_dist['mean']
    std = price_dist['std']
    x = np.linspace(mean - 3*std, mean + 3*std, 100)
    y = np.exp(-0.5 * ((x - mean) / std) ** 2) / (std * np.sqrt(2 * np.pi))
    
    fig = go.Figure()
    
    # Add distribution curve with gradient fill
    fig.add_trace(go.Scatter(
        x=x, 
        y=y,
        fill='tozeroy',
        fillcolor='rgba(100, 149, 237, 0.6)',  # Cornflower blue with transparency
        line=dict(color='rgba(100, 149, 237, 1)'),
        name='Phân Phối Giá'
    ))
    
    # Add vertical lines for important values
    lines = [
        ('Giá Dự Đoán', price_dist['predicted_price'], 'red'),
        ('Trung Bình', price_dist['mean'], 'blue'),
        ('Trung Vị', price_dist['q2'], 'green'),
        ('Tối Thiểu', price_dist['min'], 'gray'),
        ('Tối Đa', price_dist['max'], 'gray')
    ]
    
    for name, value, color in lines:
        fig.add_vline(
            x=value,
            line_color=color,
            line_dash="dash",
            annotation_text=name,
            annotation_position="top",
            annotation_font=dict(size=12, color=color)
        )
    
    fig.update_layout(
        title=dict(text="Phân Phối Giá", x=0.5, xanchor='center', font=dict(size=20)),
        xaxis_title="Giá (VNĐ)",
        yaxis_title="Mật Độ",
        showlegend=False,
        height=400,
        xaxis=dict(tickformat=",", gridcolor='lightgray'),
        yaxis=dict(gridcolor='lightgray'),
        plot_bgcolor='rgba(240, 240, 240, 0.8)'
    )
    
    return fig

# Title
st.markdown('<p class="big-font">Phân Tích Giá Trị VF3 Theo Thời Gian</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("Dữ Liệu Đầu Vào")
    
    # File upload
    uploaded_file = st.file_uploader("Tải lên dữ liệu khấu hao (CSV)", type=['csv'])
    
    # Price prediction input with example
    st.header("Dữ Liệu Dự Đoán Giá")
    
    with st.expander("Xem Mẫu Định Dạng JSON", expanded=False):
        st.code('''{
    "predicted_price": 205713162.28,
    "price_distribution": [{
        "max": 315000000.0,
        "mean": 237422978.47,
        "min": 15000000.0,
        "model": "VF3",
        "n": 191.0,
        "q1": 240000000.0,
        "q2": 240000000.0,
        "q3": 250000000.0,
        "std": 42962982.30
    }]
}''', language="json")
    
    # Option to use example or custom data
    use_example = st.checkbox("Sử dụng dữ liệu mẫu", value=True)
    
    if use_example:
        predicted_price_json = '''{
            "predicted_price": 205713162.2800351,
            "price_distribution": [
                {
                    "max": 315000000.0,
                    "mean": 237422978.46596855,
                    "min": 15000000.0,
                    "model": "VF3",
                    "n": 191.0,
                    "q1": 240000000.0,
                    "q2": 240000000.0,
                    "q3": 250000000.0,
                    "std": 42962982.297662295
                }
            ]
        }'''
    else:
        predicted_price_json = st.text_area("Nhập dữ liệu dự đoán (JSON)", height=300)

# Create tabs
tab1, tab2 = st.tabs(["Phân Tích Khấu Hao", "So Sánh Các Mẫu"])

with tab1:
    # Original depreciation analysis code here
    st.title("Phân Tích Khấu Hao VF3")
    if uploaded_file is not None:
        try:
            # Read CSV data
            df = pd.read_csv(uploaded_file)

            # Convert percentage values to actual prices
            value_columns = ['Floor Remaining Value', 'Median Remaining Value', 'Ceiling Remaining Value']
            for col in value_columns:
                df[f'{col}_VND'] = df[col] * INITIAL_PRICE

            # Parse prediction JSON
            pred_data = json.loads(predicted_price_json)
            predicted_price = pred_data['predicted_price']
            price_dist = pred_data['price_distribution'][0]
            price_dist['predicted_price'] = predicted_price

            # Create price distribution visualization
            st.plotly_chart(create_distribution_plot(price_dist), use_container_width=True)

            # Create metrics with explanations
            st.header("Phân Tích Giá")

            metric_cols = st.columns(4)

            with metric_cols[0]:
                price, delta = format_price(INITIAL_PRICE, True, INITIAL_PRICE)
                st.metric("Giá Ban Đầu", price)
                st.markdown("**Giá xe** VF3 mới")

            with metric_cols[1]:
                current_value = df[df['Months After Purchasing'] == 36]['Median Remaining Value_VND'].iloc[0]
                price, delta = format_price(current_value, True, INITIAL_PRICE)
                st.metric("Giá Trị Hiện Tại (36 tháng)", price, delta)
                st.markdown("**Giá trị ước tính** sau 36 tháng")

            with metric_cols[2]:
                price, delta = format_price(predicted_price, True, INITIAL_PRICE)
                st.metric("Giá Dự Đoán", price, delta)
                st.markdown("**Dự đoán theo mô hình AI** dựa trên dữ liệu thị trường")

            with metric_cols[3]:
                price, delta = format_price(price_dist['mean'], True, INITIAL_PRICE)
                st.metric("Giá Trung Bình Thị Trường", price, delta)
                st.markdown("**Giá trung bình** trên thị trường")

            # Create detailed statistics
            st.header("Thống Kê Thị Trường")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.subheader("Thống Kê Cơ Bản")
                st.markdown(f"""
                - **Cỡ Mẫu**: {price_dist['n']:.0f} xe
                - **Giá Trung Bình**: {format_price(price_dist['mean'])}
                - **Giá Trung Vị**: {format_price(price_dist['q2'])}
                """)

            with col2:
                st.subheader("Khoảng Giá")
                st.markdown(f"""
                - **Khoảng Giá**: {format_price(price_dist['min'])} - {format_price(price_dist['max'])}
                - **Khoảng Tứ Phân Vị**: {format_price(price_dist['q1'])} - {format_price(price_dist['q3'])}
                - **Độ Lệch Chuẩn**: {format_price(price_dist['std'])}
                """)

            with col3:
                st.subheader("Khoảng Tin Cậy")
                lower_ci = price_dist['mean'] - 1.96 * price_dist['std']
                upper_ci = price_dist['mean'] + 1.96 * price_dist['std']
                st.markdown(f"""
                - **Khoảng Tin Cậy 95%**:
                - Cận Dưới: {format_price(lower_ci)}
                - Cận Trên: {format_price(upper_ci)}
                """)

            # Create depreciation plot
            fig = make_subplots(specs=[[{"secondary_y": True}]])

            # Add value lines
            line_names = {
                'Floor Remaining Value_VND': 'Giá Trị Sàn',
                'Median Remaining Value_VND': 'Giá Trị Trung Vị',
                'Ceiling Remaining Value_VND': 'Giá Trị Trần'
            }

            for col, base_col, color, name in zip(
                ['Floor Remaining Value_VND', 'Median Remaining Value_VND', 'Ceiling Remaining Value_VND'],
                ['Floor Remaining Value', 'Median Remaining Value', 'Ceiling Remaining Value'],
                ['rgb(136, 132, 216)', 'rgb(130, 202, 157)', 'rgb(255, 198, 88)'],
                [line_names[key] for key in line_names.keys()]
            ):
                hover_text = [
                    f"Tháng {row['Months After Purchasing']}<br>" +
                    f"{name}: {format_price(row[col])}<br>" +
                    f"Tỷ Lệ: {row[base_col] * 100:.1f}%"
                    for _, row in df.iterrows()
                ]

                fig.add_trace(
                    go.Scatter(
                        x=df['Months After Purchasing'],
                        y=df[col],
                        name=name,
                        line=dict(color=color),
                        hovertext=hover_text,
                        hoverinfo='text'
                    ),
                    secondary_y=False
                )

            # Add reference lines
            fig.add_hline(
                y=INITIAL_PRICE,
                line_dash="dash",
                line_color="red",
                annotation_text="Giá Ban Đầu",
                annotation_position="right"
            )

            fig.add_vline(
                x=36,
                line_dash="dash",
                line_color="blue",
                annotation_text="Tuổi Hiện Tại",
                annotation_position="top"
            )

            # Update layout
            fig.update_layout(
                title="Giá Trị Khấu Hao Theo Thời Gian",
                xaxis_title="Số Tháng Sau Khi Mua",
                yaxis_title="Giá Trị (VNĐ)",
                hovermode='closest',
                height=600,
                showlegend=True,
                legend=dict(
                    yanchor="top",
                    y=0.99,
                    xanchor="left",
                    x=0.01
                )
            )

            # Update axes
            fig.update_yaxes(
                tickformat=",",
                secondary_y=False
            )

            # Display plot
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Lỗi xử lý dữ liệu: {str(e)}")
    else:
        st.info("Vui lòng tải lên tệp CSV chứa dữ liệu khấu hao để bắt đầu phân tích.")

with tab2:
    st.title("So Sánh Các Mẫu VinFast")

    # Price Comparison
    st.header("So Sánh Giá")
    price_comparison_fig = create_model_comparison_chart(VINFAST_MODELS)
    st.plotly_chart(price_comparison_fig, use_container_width=True)

    # Depreciation Comparison
    st.header("So Sánh Khấu Hao")
    depreciation_fig = create_depreciation_comparison(VINFAST_MODELS)
    st.plotly_chart(depreciation_fig, use_container_width=True)

    # Model Details
    st.header("Chi Tiết Từng Mẫu")
    selected_model = st.selectbox(
        "Chọn mẫu xe để xem chi tiết",
        list(VINFAST_MODELS.keys())
    )
    show_model_details(selected_model, VINFAST_MODELS[selected_model])

    # Specifications Comparison
    st.header("So Sánh Thông Số Kỹ Thuật")
    specs_df = create_model_specs_comparison()
    st.dataframe(
        specs_df,
        use_container_width=True,
        height=400
    )

    # Market Share and Trends
    st.header("Xu Hướng Thị Trường")
    market_col1, market_col2 = st.columns(2)

    with market_col1:
        st.metric(
            "Thị Phần Xe Điện VinFast",
            "65.8%",
            "12.3%"
        )

    with market_col2:
        st.metric(
            "Tăng Trưởng Doanh Số 2024",
            "147%",
            "52%"
        )

    # Additional Analysis
    with st.expander("Phân Tích Chi Tiết"):
        st.write("""
        ### Phân Tích Thị Trường
        - VF3 là mẫu xe có giá bán thấp nhất, hướng đến phân khúc phổ thông
        - VF8 và VF9 cạnh tranh trong phân khúc cao cấp
        - Các mẫu xe mới (VF6, VF7) đang tạo được sự chú ý lớn trên thị trường

        ### Xu Hướng Giá Trị
        - Các mẫu xe điện VinFast có tỷ lệ giữ giá tốt hơn so với xe xăng cùng phân khúc
        - Giá trị sau 3 năm sử dụng trung bình đạt 65% giá trị ban đầu
        - Chi phí vận hành thấp hơn 30-40% so với xe xăng
        """)