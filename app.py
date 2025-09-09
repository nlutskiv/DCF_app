import streamlit as st
import numpy as np
import pandas as pd
from company import Company

st.title("DCF Calculator")

@st.cache_data
def get_default_fcf(ticker):
    c = Company(ticker)
    fcf = c.stock.get_FCF()
    return float(fcf) if fcf else 0

ticker = st.text_input("Ticker", value="UNH")

if ticker:
    # Only set default FCF when ticker changes
    if "last_ticker" not in st.session_state or st.session_state.last_ticker != ticker:
        st.session_state.last_ticker = ticker
        st.session_state.fcf_bil = get_default_fcf(ticker) / 1e9

    # FCF input in billions, only use key (no value param)
    st.number_input(
        "Last Year's Free Cash Flow (FCF) in billions",
        step=0.1,
        format="%.3f",
        key="fcf_bil"
    )
    fcf = st.session_state.fcf_bil * 1e9

    c = Company(ticker)
    std_wacc = c.finance.WACC() if hasattr(c, "finance") and hasattr(c.finance, "WACC") else 0.075
    wacc = st.slider("WACC (Discount Rate) in %", min_value=1., max_value=20., value=float(std_wacc * 100), step=0.1, format="%.1f")
    wacc = wacc / 100  # convert to decimal
    growth_rate = st.slider("Growth Rate (first 5 years)", min_value=0.00, max_value=20., value=5., step=0.1, format="%.1f")
    growth_rate = growth_rate / 100  # convert to decimal
    terminal_growth = st.slider("Terminal Growth Rate", min_value=0.00, max_value=10., value=2., step=0.1, format="%.1f")
    terminal_growth = terminal_growth / 100  # convert to decimal

    shares_outstanding = c.stock.get_shares_outstanding()
    debt = c.stock.get_debt()

    if st.button("Calculate DCF"):
        # Use your actual DCF function, passing the user FCF and parameters
        dcf_value = c.finance.DCF(
            growth_rate=growth_rate,
            terminal_growth=terminal_growth,
            discount_rate=wacc  # Use the user-selected WACC
        )

        st.write(f"Enterprise Value (DCF): ${dcf_value:,.2f}")

        if shares_outstanding > 0:
            intrinsic = (dcf_value - debt) / shares_outstanding
            st.write(f"Intrinsic Value per Share: ${intrinsic:,.2f}")
        else:
            st.write("Shares outstanding data not available.")

        # --- Sensitivity Grid ---
        st.subheader("Intrinsic Value per Share Sensitivity (3x3 Grid)")

        cash = c.stock.get_cash()
        net_debt = debt - cash if cash is not None else debt

        wacc_range = np.round(np.linspace(wacc - 0.01, wacc + 0.01, 3), 4)
        tg_range = np.round(np.linspace(terminal_growth - 0.01, terminal_growth + 0.01, 3), 4)

        grid = []
        for tg in tg_range:
            row = []
            for w in wacc_range:
                ev = c.finance.DCF(
                    growth_rate=growth_rate,
                    terminal_growth=tg,
                    discount_rate=w
                )
                if shares_outstanding > 0:
                    intrinsic = (ev - net_debt) / shares_outstanding
                else:
                    intrinsic = 0
                row.append(intrinsic)
            grid.append(row)

        df = pd.DataFrame(
            grid,
            index=[f"g={g*100:.2f}%" for g in tg_range],
            columns=[f"WACC={w*100:.2f}%" for w in wacc_range]
        )
        st.dataframe(df.style.format("${:,.2f}"))