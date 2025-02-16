import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import numpy as np
import locale

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
    
    # Add distribution curve
    fig.add_trace(go.Scatter(
        x=x, 
        y=y,
        fill='tozeroy',
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
            annotation_position="top"
        )
    
    fig.update_layout(
        title="Phân Phối Giá",
        xaxis_title="Giá (VNĐ)",
        yaxis_title="Mật Độ",
        showlegend=False,
        height=300,
        xaxis=dict(tickformat=",")
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

# Main content
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