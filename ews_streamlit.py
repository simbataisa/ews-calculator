import streamlit as st
import pandas as pd

def format_currency(value, step_value):
    """Format currency value based on step value"""
    return f"{value * step_value:,.2f}"

def calculate_pvr_status(actual_volume, target_volume, consecutive_periods, step_value):
    """Calculate Procurement Volume Ratio status with configurable step value"""
    if not actual_volume or not target_volume:
        return "N/A"
    
    pvr = (actual_volume / target_volume) * 100
    periods = consecutive_periods * step_value
    
    if pvr >= 50:
        return "Green"
    elif periods <= step_value:
        return "Yellow"
    elif periods <= 2 * step_value:
        return "Orange"
    elif periods > 2 * step_value:
        return "Red"
    return "Green"

def calculate_ilr_status(actual_level, planned_level):
    """Calculate Inventory Level Ratio status"""
    if not actual_level or not planned_level:
        return "N/A"
    
    ilr = (actual_level / planned_level) * 100
    
    if ilr <= 120:
        return "Green"
    elif ilr <= 150:
        return "Yellow"
    elif ilr <= 170:
        return "Orange"
    return "Red"

def calculate_olr_status(outstanding_loan, credit_limit):
    """Calculate Outstanding Loan Ratio status"""
    if not outstanding_loan or not credit_limit:
        return "N/A"
    
    olr = (outstanding_loan / credit_limit) * 100
    
    if olr <= 15:
        return "Green"
    elif olr <= 25:
        return "Yellow"
    return "Orange"

def calculate_clr_status(cash_balance, loan_amount, consecutive_periods, step_value):
    """Calculate Cash-to-Loan Ratio status with configurable step value"""
    if not cash_balance or not loan_amount:
        return "N/A"
    
    clr = (cash_balance / loan_amount) * 100
    periods = consecutive_periods * step_value
    
    if clr >= 80:
        return "Green"
    elif periods <= step_value:
        return "Yellow"
    elif periods <= 2 * step_value:
        return "Orange"
    elif periods > 2 * step_value:
        return "Red"
    return "Green"

def calculate_abr_status(account_balance, loan_amount):
    """Calculate Account Balance Ratio status"""
    if not account_balance or not loan_amount:
        return "N/A"
    
    abr = (account_balance / loan_amount) * 100
    return "Green" if abr >= 100 else "Orange"

def get_status_color(status):
    """Return color code for status"""
    colors = {
        "Green": "green",
        "Yellow": "yellow",
        "Orange": "orange",
        "Red": "red",
        "N/A": "gray"
    }
    return colors.get(status, "gray")

def main():
    st.set_page_config(page_title="EWS Criteria Calculator", layout="wide")
    
    st.title("Early Warning System (EWS) Criteria Calculator")

    # Add configuration section for step values
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
    
    # Create two columns for main layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Input Values")
        
        # Procurement Volume Section
        st.markdown("### 1. Procurement Volume")
        st.markdown(f"Step Value: {procurement_step:,}")
        actual_volume_units = st.number_input(
            "Actual Procurement Volume (in thousands)",
            min_value=0,
            value=0,
            step=1,
            help=f"Enter units of {procurement_step:,}"
        )
        actual_volume = actual_volume_units * procurement_step
        st.markdown(f"Actual Value: {format_currency(actual_volume_units, procurement_step)}")
        
        target_volume_units = st.number_input(
            "Target Procurement Volume (in thousands)",
            min_value=0,
            value=0,
            step=1,
            help=f"Enter units of {procurement_step:,}"
        )
        target_volume = target_volume_units * procurement_step
        st.markdown(f"Target Value: {format_currency(target_volume_units, procurement_step)}")
        
        pvr_periods = st.number_input(
            f"Consecutive Low PVR Periods (Step: {pvr_step} days)", 
            min_value=0, 
            max_value=10, 
            value=0,
            help=f"Each increment represents {pvr_step} days"
        )
        
        # Inventory Level Section
        st.markdown("### 2. Inventory Level")
        st.markdown(f"Step Value: {inventory_step:,}")
        actual_inventory_units = st.number_input(
            "Actual Inventory Level (in thousands)",
            min_value=0,
            value=0,
            step=1,
            help=f"Enter units of {inventory_step:,}"
        )
        actual_inventory = actual_inventory_units * inventory_step
        st.markdown(f"Actual Value: {format_currency(actual_inventory_units, inventory_step)}")
        
        planned_inventory_units = st.number_input(
            "Planned Inventory Level (in thousands)",
            min_value=0,
            value=0,
            step=1,
            help=f"Enter units of {inventory_step:,}"
        )
        planned_inventory = planned_inventory_units * inventory_step
        st.markdown(f"Planned Value: {format_currency(planned_inventory_units, inventory_step)}")
        
        # Outstanding Loan Section
        st.markdown("### 3. Outstanding Loan")
        st.markdown(f"Step Value: {loan_step:,}")
        other_loans_units = st.number_input(
            "Outstanding Loan at Other Banks (in thousands)",
            min_value=0,
            value=0,
            step=1,
            help=f"Enter units of {loan_step:,}"
        )
        other_loans = other_loans_units * loan_step
        st.markdown(f"Loan Value: {format_currency(other_loans_units, loan_step)}")
        
        credit_limit_units = st.number_input(
            "Approved Credit Limit (in thousands)",
            min_value=0,
            value=0,
            step=1,
            help=f"Enter units of {loan_step:,}"
        )
        credit_limit = credit_limit_units * loan_step
        st.markdown(f"Credit Limit Value: {format_currency(credit_limit_units, loan_step)}")
        
        # Cash and Balance Section
        st.markdown("### 4. Cash and Balance")
        st.markdown(f"Step Value: {balance_step:,}")
        cash_balance_units = st.number_input(
            "Cash Average Balance (in thousands)",
            min_value=0,
            value=0,
            step=1,
            help=f"Enter units of {balance_step:,}"
        )
        cash_balance = cash_balance_units * balance_step
        st.markdown(f"Cash Balance Value: {format_currency(cash_balance_units, balance_step)}")
        
        loan_amount_units = st.number_input(
            "Outstanding Loan Amount (in thousands)",
            min_value=0,
            value=0,
            step=1,
            help=f"Enter units of {balance_step:,}"
        )
        loan_amount = loan_amount_units * balance_step
        st.markdown(f"Loan Amount Value: {format_currency(loan_amount_units, balance_step)}")
        
        account_balance_units = st.number_input(
            "Account Balance (in thousands)",
            min_value=0,
            value=0,
            step=1,
            help=f"Enter units of {balance_step:,}"
        )
        account_balance = account_balance_units * balance_step
        st.markdown(f"Account Balance Value: {format_currency(account_balance_units, balance_step)}")
        
        clr_periods = st.number_input(
            f"Consecutive Low CLR Periods (Step: {clr_step} days)", 
            min_value=0, 
            max_value=10, 
            value=0,
            help=f"Each increment represents {clr_step} days"
        )
        
        # Credit Rating Section
        st.markdown("### 5. Credit Rating")
        credit_rating = st.selectbox(
            "Current Credit Rating",
            ["Good (No Change)", "Dropped from Previous", "B1", "B2", "B3", "Bad Debt"]
        )
    
    with col2:
        st.subheader("Results")
        
        # Calculate and display results
        results = {
            "Procurement Volume Ratio (PVR)": calculate_pvr_status(
                actual_volume, target_volume, pvr_periods, pvr_step
            ),
            "Inventory Level Ratio (ILR)": calculate_ilr_status(
                actual_inventory, planned_inventory
            ),
            "Outstanding Loan Ratio (OLR)": calculate_olr_status(
                other_loans, credit_limit
            ),
            "Cash-to-Loan Ratio (CLR)": calculate_clr_status(
                cash_balance, loan_amount, clr_periods, clr_step
            ),
            "Account Balance Ratio (ABR)": calculate_abr_status(
                account_balance, loan_amount
            )
        }
        
        # Credit Rating Status
        if credit_rating == "Good (No Change)":
            credit_status = "Green"
        elif credit_rating == "Dropped from Previous":
            credit_status = "Yellow"
        elif credit_rating in ["B1", "B2", "B3"]:
            credit_status = "Orange"
        elif credit_rating == "Bad Debt":
            credit_status = "Red"
        else:
            credit_status = "N/A"
        
        results["Credit Rating Status"] = credit_status
        
        # Display results with colored boxes
        for metric, status in results.items():
            color = get_status_color(status)
            st.markdown(
                f"""
                <div style="
                    padding: 10px;
                    border-radius: 5px;
                    margin: 5px 0;
                    background-color: {color};
                    opacity: 0.7;
                ">
                    <strong>{metric}:</strong> {status}
                </div>
                """,
                unsafe_allow_html=True
            )

        # Display detailed values
        st.markdown("### Value Details")
        st.markdown("#### Inventory")
        st.info(f"""
        - Actual: {format_currency(actual_inventory_units, inventory_step)}
        - Planned: {format_currency(planned_inventory_units, inventory_step)}
        """)
        
        st.markdown("#### Loans")
        st.info(f"""
        - Outstanding at Other Banks: {format_currency(other_loans_units, loan_step)}
        - Credit Limit: {format_currency(credit_limit_units, loan_step)}
        - Outstanding Loan Amount: {format_currency(loan_amount_units, balance_step)}
        """)
        
        st.markdown("#### Balances")
        st.info(f"""
        - Cash Average: {format_currency(cash_balance_units, balance_step)}
        - Account: {format_currency(account_balance_units, balance_step)}
        """)

        # Display period details
        st.markdown("### Period Details")
        if pvr_periods > 0:
            st.info(f"PVR Effective Period: {pvr_periods * pvr_step} days")
        if clr_periods > 0:
            st.info(f"CLR Effective Period: {clr_periods * clr_step} days")
        
        # Add export functionality
        if st.button("Export Results"):
            # Create results DataFrame with additional details
            results_data = {
                "Metric": list(results.keys()) + [
                    "PVR Effective Period",
                    "CLR Effective Period",
                    "Actual Procurement Volume",
                    "Target Procurement Volume",
                    "Actual Inventory",
                    "Planned Inventory",
                    "Outstanding Loans",
                    "Credit Limit",
                    "Cash Balance",
                    "Account Balance"
                ],
                "Value/Status": list(results.values()) + [
                    f"{pvr_periods * pvr_step} days" if pvr_periods > 0 else "N/A",
                    f"{clr_periods * clr_step} days" if clr_periods > 0 else "N/A",
                    format_currency(actual_volume_units, procurement_step),
                    format_currency(target_volume_units, procurement_step),
                    format_currency(actual_inventory_units, inventory_step),
                    format_currency(planned_inventory_units, inventory_step),
                    format_currency(other_loans_units, loan_step),
                    format_currency(credit_limit_units, loan_step),
                    format_currency(cash_balance_units, balance_step),
                    format_currency(account_balance_units, balance_step)
                ]
            }
            df = pd.DataFrame(results_data)
            
            st.download_button(
                "Download Results as CSV",
                df.to_csv(index=False).encode('utf-8'),
                "ews_results.csv",
                "text/csv",
                key='download-csv'
            )

if __name__ == "__main__":
    main()