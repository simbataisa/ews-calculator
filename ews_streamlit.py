import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io

def load_and_process_csv(uploaded_file):
    """Load and process the uploaded CSV file"""
    df = pd.read_csv(uploaded_file)
    
    # Convert date column if exists
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    
    return df

def calculate_all_metrics(row, step_values):
    """Calculate all EWS metrics for a single row"""
    results = {}
    
    # PVR Calculation
    if 'actual_volume' in row and 'target_volume' in row:
        actual = row['actual_volume'] * step_values['procurement']
        target = row['target_volume'] * step_values['procurement']
        pvr = (actual / target * 100) if target != 0 else 0
        results['PVR'] = 'Green' if pvr >= 50 else 'Red'
        results['PVR_Value'] = pvr
    
    # ILR Calculation
    if 'actual_inventory' in row and 'planned_inventory' in row:
        actual = row['actual_inventory'] * step_values['inventory']
        planned = row['planned_inventory'] * step_values['inventory']
        ilr = (actual / planned * 100) if planned != 0 else 0
        if ilr <= 120:
            results['ILR'] = 'Green'
        elif ilr <= 150:
            results['ILR'] = 'Yellow'
        elif ilr <= 170:
            results['ILR'] = 'Orange'
        else:
            results['ILR'] = 'Red'
        results['ILR_Value'] = ilr
    
    # OLR Calculation
    if 'outstanding_loan_other' in row and 'credit_limit' in row:
        loan = row['outstanding_loan_other'] * step_values['loan']
        limit = row['credit_limit'] * step_values['loan']
        olr = (loan / limit * 100) if limit != 0 else 0
        if olr <= 15:
            results['OLR'] = 'Green'
        elif olr <= 25:
            results['OLR'] = 'Yellow'
        else:
            results['OLR'] = 'Orange'
        results['OLR_Value'] = olr
    
    # CLR Calculation
    if 'cash_balance' in row and 'loan_amount' in row:
        cash = row['cash_balance'] * step_values['balance']
        loan = row['loan_amount'] * step_values['balance']
        clr = (cash / loan * 100) if loan != 0 else 0
        results['CLR'] = 'Green' if clr >= 80 else 'Red'
        results['CLR_Value'] = clr
    
    # ABR Calculation
    if 'account_balance' in row and 'loan_amount' in row:
        balance = row['account_balance'] * step_values['balance']
        loan = row['loan_amount'] * step_values['balance']
        abr = (balance / loan * 100) if loan != 0 else 0
        results['ABR'] = 'Green' if abr >= 100 else 'Orange'
        results['ABR_Value'] = abr
    
    return results

def create_summary_charts(df_results):
    """Create summary charts from results DataFrame"""
    charts = []
    
    # Status Distribution Chart
    status_cols = [col for col in df_results.columns if not col.endswith('_Value') and col != 'date']
    for metric in status_cols:
        status_counts = df_results[metric].value_counts()
        fig = go.Figure(data=[
            go.Bar(
                x=status_counts.index,
                y=status_counts.values,
                marker_color=['green' if x == 'Green' else 
                            'yellow' if x == 'Yellow' else
                            'orange' if x == 'Orange' else 'red' 
                            for x in status_counts.index]
            )
        ])
        fig.update_layout(
            title=f"{metric} Status Distribution",
            xaxis_title="Status",
            yaxis_title="Count",
            showlegend=False
        )
        charts.append(fig)
    
    # Trend Analysis Chart
    value_cols = [col for col in df_results.columns if col.endswith('_Value')]
    if 'date' in df_results.columns and value_cols:
        fig = go.Figure()
        for col in value_cols:
            metric_name = col.replace('_Value', '')
            fig.add_trace(go.Scatter(
                x=df_results['date'],
                y=df_results[col],
                name=metric_name,
                mode='lines+markers'
            ))
        fig.update_layout(
            title="Metrics Trend Over Time",
            xaxis_title="Date",
            yaxis_title="Value (%)",
            showlegend=True
        )
        charts.append(fig)
    
    return charts

def main():
    st.set_page_config(page_title="EWS Criteria Calculator", layout="wide")
    
    st.title("Early Warning System (EWS) Criteria Calculator")
    
    # File upload section
    st.markdown("### Upload Data")
    uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
    
    # Example CSV format
    st.markdown("""
    #### Expected CSV Format:
    Your CSV should include these columns:
    - date (optional, format: YYYY-MM-DD)
    - actual_volume, target_volume
    - actual_inventory, planned_inventory
    - outstanding_loan_other, credit_limit
    - cash_balance, loan_amount, account_balance
    """)
    
    # Configuration section
    with st.expander("⚙️ Configure Step Values", expanded=True):
        st.markdown("### Step Value Configuration")
        
        # Time-based step values
        st.markdown("#### Time-based Steps")
        col_pvr, col_clr = st.columns(2)
        with col_pvr:
            pvr_step = st.number_input(
                "PVR Step Value (days)",
                min_value=1,
                value=1,
                help="Number of days to increment for each consecutive PVR period"
            )
        with col_clr:
            clr_step = st.number_input(
                "CLR Step Value (days)",
                min_value=1,
                value=1,
                help="Number of days to increment for each consecutive CLR period"
            )
        
        # Monetary step values
        st.markdown("#### Monetary Steps (in thousands)")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            procurement_step = st.number_input(
                "Procurement Step Value",
                min_value=1000,
                value=1000,
                step=1000,
                help="Step value for procurement amounts"
            )
        
        with col2:
            inventory_step = st.number_input(
                "Inventory Step Value",
                min_value=1000,
                value=1000,
                step=1000,
                help="Step value for inventory amounts"
            )
        
        with col3:
            loan_step = st.number_input(
                "Loan Step Value",
                min_value=1000,
                value=1000,
                step=1000,
                help="Step value for loan amounts"
            )
        
        with col4:
            balance_step = st.number_input(
                "Balance Step Value",
                min_value=1000,
                value=1000,
                step=1000,
                help="Step value for balance amounts"
            )
    
    # Process uploaded file
    if uploaded_file is not None:
        try:
            df = load_and_process_csv(uploaded_file)
            
            # Create step values dictionary
            step_values = {
                'procurement': procurement_step,
                'inventory': inventory_step,
                'loan': loan_step,
                'balance': balance_step
            }
            
            # Calculate metrics for each row
            results_list = []
            for _, row in df.iterrows():
                results = calculate_all_metrics(row, step_values)
                if 'date' in df.columns:
                    results['date'] = row['date']
                results_list.append(results)
            
            df_results = pd.DataFrame(results_list)
            
            # Display summary statistics
            st.markdown("### Summary Statistics")
            
            # Status distribution
            status_cols = [col for col in df_results.columns if not col.endswith('_Value') and col != 'date']
            for metric in status_cols:
                st.write(f"#### {metric} Distribution")
                status_counts = df_results[metric].value_counts()
                st.write(status_counts)
            
            # Create and display charts
            st.markdown("### Visualization")
            charts = create_summary_charts(df_results)
            
            for chart in charts:
                st.plotly_chart(chart, use_container_width=True)
            
            # Export results
            st.markdown("### Export Results")
            if st.button("Export Results"):
                output = io.BytesIO()
                df_results.to_excel(output, index=False, engine='openpyxl')
                output.seek(0)
                
                st.download_button(
                    label="Download Results as Excel",
                    data=output,
                    file_name=f"ews_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
            st.markdown("""
            Please ensure your CSV file follows the expected format:
            ```
            date,actual_volume,target_volume,actual_inventory,planned_inventory,outstanding_loan_other,credit_limit,cash_balance,loan_amount,account_balance
            2024-01-01,100,200,150,100,50,500,400,300,350
            2024-01-02,150,200,120,100,40,500,450,300,400
            ```
            """)

if __name__ == "__main__":
    main()