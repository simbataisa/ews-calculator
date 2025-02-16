import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import numpy as np

# Set page config
st.set_page_config(
    page_title="VF3 Value Depreciation",
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

def format_price(price, include_delta=False, base_price=None):
    """Format price in millions of VND with optional delta percentage"""
    if include_delta and base_price:
        delta = ((price / base_price) - 1) * 100
        return f"{price/1_000_000:.1f}M VND", f"{delta:.1f}%"
    return f"{price/1_000_000:.1f}M VND"

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
        name='Price Distribution'
    ))
    
    # Add vertical lines for important values
    lines = [
        ('Predicted', price_dist['predicted_price'], 'red'),
        ('Mean', price_dist['mean'], 'blue'),
        ('Median', price_dist['q2'], 'green'),
        ('Min', price_dist['min'], 'gray'),
        ('Max', price_dist['max'], 'gray')
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
        title="Price Distribution",
        xaxis_title="Price (VND)",
        yaxis_title="Density",
        showlegend=False,
        height=300,
        xaxis=dict(tickformat=",")
    )
    
    return fig

# Title
st.markdown('<p class="big-font">VF3 Value Depreciation Analysis</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("Data Input")
    
    # File upload
    uploaded_file = st.file_uploader("Upload depreciation data (CSV)", type=['csv'])
    
    # Price prediction input with example
    st.header("Price Prediction Data")
    
    with st.expander("View Example JSON Format", expanded=False):
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
    use_example = st.checkbox("Use example data", value=True)
    
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
        predicted_price_json = st.text_area("Enter custom prediction data (JSON)", height=300)

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
        price_dist['predicted_price'] = predicted_price  # Add predicted price to distribution data
        
        # Create price distribution visualization
        st.plotly_chart(create_distribution_plot(price_dist), use_container_width=True)
        
        # Create metrics with explanations
        st.header("Price Analysis")
        
        metric_cols = st.columns(4)
        
        with metric_cols[0]:
            price, delta = format_price(INITIAL_PRICE, True, INITIAL_PRICE)
            st.metric("Initial Price", price)
            st.markdown("**Base price** for a new VF3")
            
        with metric_cols[1]:
            current_value = df[df['Months After Purchasing'] == 36]['Median Remaining Value_VND'].iloc[0]
            price, delta = format_price(current_value, True, INITIAL_PRICE)
            st.metric("Current Value (36 months)", price, delta)
            st.markdown("**Estimated value** after 36 months")
            
        with metric_cols[2]:
            price, delta = format_price(predicted_price, True, INITIAL_PRICE)
            st.metric("Predicted Price", price, delta)
            st.markdown("**AI model prediction** based on market data")
            
        with metric_cols[3]:
            price, delta = format_price(price_dist['mean'], True, INITIAL_PRICE)
            st.metric("Market Average", price, delta)
            st.markdown("**Average price** in the market")

        # Create detailed statistics
        st.header("Market Statistics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("Basic Statistics")
            st.markdown(f"""
            - **Sample Size**: {price_dist['n']:.0f} vehicles
            - **Mean Price**: {format_price(price_dist['mean'])}
            - **Median Price**: {format_price(price_dist['q2'])}
            """)
            
        with col2:
            st.subheader("Price Ranges")
            st.markdown(f"""
            - **Full Range**: {format_price(price_dist['min'])} - {format_price(price_dist['max'])}
            - **Interquartile Range**: {format_price(price_dist['q1'])} - {format_price(price_dist['q3'])}
            - **Standard Deviation**: {format_price(price_dist['std'])}
            """)
            
        with col3:
            st.subheader("Confidence Intervals")
            lower_ci = price_dist['mean'] - 1.96 * price_dist['std']
            upper_ci = price_dist['mean'] + 1.96 * price_dist['std']
            st.markdown(f"""
            - **95% Confidence Interval**:
            - Lower: {format_price(lower_ci)}
            - Upper: {format_price(upper_ci)}
            """)

        # Create depreciation plot
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Add value lines
        for col, base_col, color, name in zip(
            ['Floor Remaining Value_VND', 'Median Remaining Value_VND', 'Ceiling Remaining Value_VND'],
            ['Floor Remaining Value', 'Median Remaining Value', 'Ceiling Remaining Value'],
            ['rgb(136, 132, 216)', 'rgb(130, 202, 157)', 'rgb(255, 198, 88)'],
            ['Floor Value', 'Median Value', 'Ceiling Value']
        ):
            hover_text = [
                f"Month {row['Months After Purchasing']}<br>" +
                f"{name}: {format_price(row[col])}<br>" +
                f"Percentage: {row[base_col] * 100:.1f}%"
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
            annotation_text="Initial Price",
            annotation_position="right"
        )
        
        fig.add_vline(
            x=36,
            line_dash="dash",
            line_color="blue",
            annotation_text="Current Age",
            annotation_position="top"
        )

        # Update layout
        fig.update_layout(
            title="Value Depreciation Over Time",
            xaxis_title="Months After Purchase",
            yaxis_title="Value (VND)",
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
        st.error(f"Error processing data: {str(e)}")
else:
    st.info("Please upload a CSV file containing the depreciation data to begin the analysis.")