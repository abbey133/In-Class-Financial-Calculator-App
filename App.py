
import streamlit as st

st.set_page_config(
    page_title="Financial Problem Solver",
    page_icon="💰",
    layout="centered"
)

st.title("💰 Financial Problem Solver")
st.write("Solve common finance problems using Python.")
st.divider()

problem = st.selectbox(
    "Choose a financial problem:",
    [
        "Present Value",
        "Future Value",
        "Net Present Value (NPV)",
        "Bond Pricing",
        "Bond Duration",
        "DV01",
    ]
)

if problem == "Present Value":
    st.header("Present Value Calculator")

    fv = st.number_input("Future Value ($)", value=1000.0)
    r = st.number_input("Interest Rate (%)", value=5.0) / 100
    n = st.number_input("Number of Years", min_value=1, value=5)

    if st.button("Calculate"):
        pv = fv / (1 + r) ** n
        st.success(f"Present Value: ${pv:,.2f}")
        st.latex(r"PV = \frac{FV}{(1+r)^n}")


elif problem == "Future Value":
    st.header("Future Value Calculator")

    pv = st.number_input("Present Value ($)", value=1000.0)
    r = st.number_input("Interest Rate (%)", value=5.0) / 100
    n = st.number_input("Number of Years", min_value=1, value=5)

    if st.button("Calculate"):
        fv = pv * (1 + r) ** n
        st.success(f"Future Value: ${fv:,.2f}")
        st.latex(r"FV = PV(1+r)^n")


elif problem == "Net Present Value (NPV)":
    st.header("NPV Calculator")

    investment = st.number_input(
        "Initial Investment ($)", min_value=0.0, value=1000.0
    )
    r = st.number_input("Discount Rate (%)", value=10.0) / 100

    cash_flows = st.text_input(
        "Annual Cash Flows (separate with commas)",
        "300, 400, 500, 600"
    )

    if st.button("Calculate"):
        try:
            flows = [float(x.strip()) for x in cash_flows.split(",")]
            if not flows:
                raise ValueError("Enter at least one cash flow.")

            npv = -investment + sum(
                cf / (1 + r) ** t
                for t, cf in enumerate(flows, start=1)
            )
            st.success(f"Net Present Value: ${npv:,.2f}")
            st.latex(
                r"NPV = -C_0 + \sum_{t=1}^{n}"
                r"\frac{CF_t}{(1+r)^t}"
            )
        except ValueError:
            st.error("Enter valid cash flows separated by commas.")


elif problem == "Bond Pricing":
    st.header("Bond Price Calculator")

    face = st.number_input("Face Value ($)", value=1000.0)
    coupon = st.number_input("Annual Coupon Rate (%)", value=5.0) / 100
    ytm = st.number_input("Annual Yield (%)", value=4.0) / 100
    years = st.number_input("Years to Maturity", min_value=1, value=10)

    if st.button("Calculate"):
        periods = years * 2
        payment = face * coupon / 2
        rate = ytm / 2

        price = sum(
            payment / (1 + rate) ** t
            for t in range(1, periods + 1)
        ) + face / (1 + rate) ** periods

        st.success(f"Bond Price: ${price:,.2f}")
        st.latex(
            r"P = \sum_{t=1}^{N}"
            r"\frac{C}{(1+y/2)^t}"
            r"+\frac{F}{(1+y/2)^N}"
        )


elif problem == "Bond Duration":
    st.header("Modified Duration Calculator")

    face = st.number_input("Face Value ($)", value=1000.0)
    coupon = st.number_input("Annual Coupon Rate (%)", value=5.0) / 100
    ytm = st.number_input("Annual Yield (%)", value=4.0) / 100
    years = st.number_input("Years to Maturity", min_value=1, value=10)

    if st.button("Calculate"):
        periods = years * 2
        rate = ytm / 2
        payment = face * coupon / 2

        pv_flows = [
            (payment + (face if t == periods else 0)) /
            (1 + rate) ** t
            for t in range(1, periods + 1)
        ]

        price = sum(pv_flows)

        macaulay = sum(
            (t / 2) * pv
            for t, pv in enumerate(pv_flows, start=1)
        ) / price

        modified = macaulay / (1 + rate)

        st.success(f"Modified Duration: {modified:.4f} years")
        st.write(f"Macaulay Duration: {macaulay:.4f} years")
        st.latex(r"D_{mod} = \frac{D_{Mac}}{1+y/2}")


elif problem == "DV01":
    st.header("DV01 Calculator")

    price = st.number_input("Bond Price ($)", value=100.0)
    duration = st.number_input(
        "Modified Duration (years)", value=8.0
    )
    face = st.number_input(
        "Total Face Value ($)", value=1000000.0
    )
    quote_face = st.number_input(
        "Price Quotation Face Value ($)",
        min_value=0.01,
        value=100.0
    )

    if st.button("Calculate"):
        market_value = price / quote_face * face
        dv01 = duration * market_value * 0.0001

        st.success(f"DV01: ${dv01:,.2f}")
        st.write("This is the approximate dollar price change for a 1 basis point yield move.")
        st.latex(r"DV01 = D_{mod} \times MV \times 0.0001")

st.divider()
st.caption("Financial Problem Solver | Python & Streamlit")
