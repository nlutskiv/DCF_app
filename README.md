# 💰 DCF Valuation App

An automated **Discounted Cash Flow (DCF)** valuation tool built in **Python** with a **Streamlit** interface.  
It integrates **Yahoo Finance** data to estimate a company’s **intrinsic value** using projected cash flows, WACC, and terminal growth.

---

## 📈 Overview

This app lets you:
- Fetch financial data automatically from Yahoo Finance  
- Estimate **enterprise value** and **intrinsic stock price**  
- Adjust key assumptions (growth, WACC, terminal growth) dynamically  
- Visualize results via a **sensitivity grid** (WACC × Terminal Growth)

The goal is to make **equity valuation fast, transparent, and reproducible** — ideal for investment analysis, academic projects, or finance interviews.

---

## 🧮 Core Financial Logic

Implemented within `finance.py`:
- **CAPM** — calculates cost of equity  
- **WACC** — computes weighted average cost of capital  
- **DCF** — projects free cash flows, discounts them, and adds terminal value  
- **Intrinsic Value** — divides enterprise value by shares outstanding, net of debt  

Each component draws data from Yahoo Finance through the `Stock` class.

---

## 🧠 How It Works

1. Enter a **ticker symbol** (e.g., `AAPL`, `MSFT`, `UNH`)  
2. The app retrieves the latest financial data  
3. Adjust key assumptions:  
   - **Growth Rate** (next 5 years)  
   - **Terminal Growth Rate**  
   - **WACC (discount rate)**  
4. Click *Calculate DCF* to see:  
   - **Enterprise Value (EV)**  
   - **Intrinsic Value per Share**  
   - **Sensitivity grid** across WACC/g scenarios  

---
## ⚙️ Installation

### 1️⃣ Clone the repo
```bash
git clone https://github.com/nlutskiv/DCF_app.git
cd DCF_app

