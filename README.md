# 💳 CreditWise: Advanced Credit Score Simulator

CreditWise is an interactive **Streamlit** web app that simulates a credit score based on a FICO-style model.  
It lets users:

- Enter their financial and credit profile
- See an estimated credit score with a gauge chart
- Understand how different factors (utilization, history, inquiries, etc.) impact the score
- Run **“What if?”** simulations to see how actions like paying down debt could change the score

> ⚠️ **Disclaimer:**  
> This is an educational tool only. It does **not** use any real credit bureau or FICO data and should not be used for financial decisions. :contentReference[oaicite:0]{index=0}

---

## 🧩 Features

- **Interactive UI with Streamlit**
  - Sidebar form for user inputs (income, card limits, balances, history, etc.)
  - Real-time display of the calculated credit score
- **Custom Scoring Engine**
  - FICO-inspired model with:
    - Payment history (35%)
    - Amounts owed / utilization (30%)
    - Length of history (15%)
    - New credit / inquiries (10%)
    - Credit mix (10%)
- **Visualizations**
  - Plotly gauge chart for the credit score
  - Streamlit bar chart for factor weights
  - Utilization progress bar
- **Real-Time Scenario Simulator**
  - Sliders to simulate:
    - Paying down credit card debt
    - Paying down loan balances
    - Waiting for hard inquiries to drop off
  - Shows projected score and difference from current score
- **Insight Panel**
  - Textual explanation of how:
    - Card utilization affects the score
    - Loan balances differ from revolving card debt

---

## 🏗️ Tech Stack

- **Language:** Python
- **Framework:** Streamlit
- **Data Handling:** pandas, numpy
- **Visualizations:** Plotly (gauge chart), Streamlit charts
- **UI Layout:** Streamlit columns, tabs, sidebar, metrics

---

## 📁 Project Structure

```text
.
├── app.py          # Main Streamlit application
└── README.md       # Project documentation (this file)


