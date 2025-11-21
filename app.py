import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ==========================================
# 1. CONFIGURATION & SETUP
# ==========================================
st.set_page_config(
    page_title="CreditWise: Advanced Score Simulator",
    page_icon="💳",
    layout="wide"
)

# ==========================================
# 2. LOGIC: THE FICO SIMULATION ENGINE
# ==========================================
def calculate_credit_score(data):
    """
    A deterministic algorithm mimicking FICO weightings.
    UPDATED: Now distinguishes between Revolving (Card) and Installment (Loan) debt.
    """
    # 1. BASE SCORE UPDATE: Increased floor to 550 for realism
    score = 500 
    
    # --- A. Payment History (35% Impact) ---
    if data['Missed_Payments'] == 0 and data['Defaults'] == 0:
        score += 110
    elif data['Missed_Payments'] == 1:
        score += 60
    elif data['Missed_Payments'] <= 2:
        score += 30
    else:
        score -= 20
        
    if data['Defaults'] == 1:
        score -= 70

    # --- B. Amounts Owed / Utilization (30% Impact) ---
    util = data['Revolving_Utilization']
    
    if util == 0:
        score += 60
    elif util < 10:
        score += 85
    elif util < 30:
        score += 70
    elif util < 50:
        score += 40
    elif util < 75:
        score += 10
    else:
        score -= 30

    # --- C. Length of History (15% Impact) ---
    years = data['Credit_History_Years']
    if years < 2:
        score += 10
    elif years < 5:
        score += 35
    elif years < 10:
        score += 55
    elif years < 20:
        score += 70
    else:
        score += 85

    # --- D. Credit Mix (10% Impact) ---
    if data['Num_Credit_Cards'] > 0 and data['Num_Loans'] > 0:
        score += 40
    elif data['Num_Credit_Cards'] > 0 or data['Num_Loans'] > 0:
        score += 20
    
    # --- E. New Credit / Inquiries (10% Impact) ---
    inq = data['Recent_Inquiries']
    if inq == 0:
        score += 30
    elif inq <= 1:
        score += 20
    elif inq <= 2:
        score += 10
    else:
        score -= 10

    # --- Logic Correction Bounds ---
    score = max(300, min(850, int(score)))
    return score

def get_score_rating(score):
    if score >= 800: return "Exceptional", "#00C851"
    if score >= 740: return "Very Good", "#90EE90"
    if score >= 670: return "Good", "#33b5e5"
    if score >= 580: return "Fair", "#ffbb33"
    return "Poor", "#ff4444"

# ==========================================
# 3. UI: SIDEBAR INPUTS
# ==========================================
st.sidebar.title("⚙️ Profile Settings")

with st.sidebar.form("user_input_form"):
    st.subheader("Financial Snapshot")
    
    # UPDATED: Min value decreased to 0
    income = st.number_input("Annual Income (INR)", min_value=0, value=1200000, step=50000)
    
    st.markdown("---")
    st.markdown("**Debt Breakdown**")
    card_limit = st.number_input("Total Credit Card Limit ($)", min_value=0, value=500000)
    card_balance = st.number_input("Current Credit Card Balance ($)", min_value=0, value=30000)
    loan_balance = st.number_input("Remaining Loan Balance (Home/Auto) ($)", min_value=0, value=2000000)
    
    st.markdown("---")
    st.subheader("Credit History")
    history = st.slider("Age of Oldest Account (Years)", 0, 50, 8)
    missed = st.slider("Missed Payments (Last 2 Years)", 0, 12, 0)
    defaults = st.checkbox("Prior Bankruptcy or Default?")
    
    st.subheader("Activity")
    cards = st.number_input("Number of Credit Cards", min_value=0, value=3)
    loans = st.number_input("Number of Loans (Auto/Home)", min_value=0, value=1)
    inquiries = st.slider("Hard Inquiries (Last 6 Months)", 0, 10, 1)
    
    submit_button = st.form_submit_button("Calculate Score")

# ==========================================
# 4. DATA PREPARATION (This was missing)
# ==========================================
revolving_util_ratio = (card_balance / card_limit) * 100 if card_limit > 0 else 0

user_data = {
    'Revolving_Utilization': revolving_util_ratio,
    'Loan_Balance': loan_balance,
    'Credit_History_Years': history,
    'Num_Credit_Cards': cards,
    'Num_Loans': loans,
    'Missed_Payments': missed,
    'Recent_Inquiries': inquiries,
    'Defaults': 1 if defaults else 0
}

# ==========================================
# 5. MAIN DASHBOARD
# ==========================================

st.title("💳 CreditWise: Advanced Simulator")

# Calculate Score
current_score = calculate_credit_score(user_data)
rating_text, rating_color = get_score_rating(current_score)

# --- TOP SECTION: GAUGE CHART & METRICS ---
col_left, col_right = st.columns([1, 2])

with col_left:
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = current_score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': f"Rating: {rating_text}"},
        gauge = {
            'axis': {'range': [300, 850]},
            'bar': {'color': rating_color},
            'steps': [
                {'range': [300, 580], 'color': "#ffcccb"},
                {'range': [580, 670], 'color': "#ffe4b5"},
                {'range': [670, 740], 'color': "#e0ffff"},
                {'range': [740, 850], 'color': "#90EE90"}],
        }
    ))
    fig.update_layout(height=300, margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.markdown("### Key Factors Analysis")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Card Utilization", f"{revolving_util_ratio:.1f}%", 
              delta="-High" if revolving_util_ratio > 30 else "Healthy", delta_color="inverse")
    m2.metric("Payment History", f"{100 - (missed*10)}%", 
              "On Time" if missed == 0 else "Needs Work")
    m3.metric("Credit Age", f"{history} Yrs", 
              "Short" if history < 4 else "Established")
    
    st.info(f"""
    **Insight:** Your income is **₹{income:,.0f}**. While income isn't part of the score directly, 
    it supports your **₹{card_limit:,.0f}** credit limit. 
    
    Your score is primarily driven by your **{revolving_util_ratio:.1f}%** card utilization. 
    Note that your ₹{loan_balance:,.0f} loan balance affects the score much less than card debt.
    """)

st.markdown("---")

# ==========================================
# 6. REAL-TIME SIMULATOR
# ==========================================
st.subheader("🧪 Real-Time Simulator: 'What If?'")
st.markdown("Adjust scenarios to see instant impact.")

sim_col1, sim_col2 = st.columns(2)

with sim_col1:
    st.markdown("#### Simulate Actions")
    sim_pay_card = st.slider("Pay down Credit Card Debt ($):", 0, int(card_balance), 0, step=1000)
    sim_pay_loan = st.slider("Pay down Installment Loan ($):", 0, int(loan_balance) if loan_balance > 0 else 0, 0, step=5000)
    sim_remove_inq = st.checkbox("Wait 6 months (Inquiries drop off)")

with sim_col2:
    # Calculate Simulated Data
    sim_data = user_data.copy()
    
    # 1. Adjust Card Debt
    new_card_bal = card_balance - sim_pay_card
    sim_data['Revolving_Utilization'] = (new_card_bal / card_limit) * 100 if card_limit > 0 else 0
    
    # 2. Adjust Inquiries
    if sim_remove_inq:
        sim_data['Recent_Inquiries'] = max(0, inquiries - 2) 
        
    # Calculate New Score
    sim_score = calculate_credit_score(sim_data)
    score_diff = sim_score - current_score
    
    st.markdown("#### Projected Result")
    st.metric(label="Projected Credit Score", value=sim_score, delta=score_diff)
    
    if score_diff > 0:
        st.success(f"🚀 **Strategy:** Paying **${sim_pay_card}** off your credit cards is the fastest way to gain **{score_diff} points**.")
    elif score_diff == 0 and sim_pay_loan > 0:
         st.warning("⚠️ Paying off installment loans (like auto/home) helps your finances, but rarely boosts your credit score immediately.")
    elif score_diff == 0:
        st.caption("Adjust sliders to see potential changes.")

# ==========================================
# 7. DETAILED BREAKDOWN
# ==========================================
st.markdown("---")
tab1, tab2 = st.tabs(["📊 Factor Weights", "🎓 Why this matters"])

with tab1:
    factors = {
        'Payment History': 35,
        'Amounts Owed (Utilization)': 30,
        'Length of History': 15,
        'New Credit': 10,
        'Credit Mix': 10
    }
    df_factors = pd.DataFrame(list(factors.items()), columns=['Factor', 'Weight (%)'])
    st.bar_chart(df_factors.set_index('Factor'))

with tab2:
    st.markdown("### Understanding Credit Utilization")
    
    # Visualization of Utilization
    st.progress(min(revolving_util_ratio / 100, 1.0), text="Current Utilization Ratio")
    
    st.markdown("""
    ### The "Missing" Attribute: Revolving vs. Installment Debt
    
    The previous calculation treated all debt equally. Real credit scoring models treat them very differently:
    
    1.  **Revolving Debt (Credit Cards):** This is the most dangerous type. Utilizing >30% of your limit crashes your score.
    2.  **Installment Debt (Loans):** Having a huge home loan (e.g., 50 Lakhs) is fine as long as you pay on time. It does **not** hurt your utilization ratio the same way maxing out a 50k credit card does.
    """)