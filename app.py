from __future__ import annotations

import hashlib
from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="DormVest", page_icon="🏘️", layout="wide", initial_sidebar_state="expanded")

# Minimal CSS only: hide Streamlit chrome. No global text/color overrides.
st.markdown("""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
[data-testid="stToolbar"] {visibility:hidden; height:0; position:fixed;}
.stDeployButton {display:none;}
</style>
""", unsafe_allow_html=True)

PROPERTIES = pd.DataFrame([
    {"id":"BOL-01","name":"Bologna University Residence","city":"Bologna","country":"Italy","type":"Student residence","occupancy":96,"yield":7.4,"risk_score":86,"risk_level":"Low","token_price":50,"available_tokens":7200,"gross_rent":420000,"costs":156000,"min_investment":100,"why":"Central asset serving University of Bologna demand with high occupancy stability."},
    {"id":"MIL-01","name":"Milan Polytechnic Co-Living","city":"Milan","country":"Italy","type":"Co-living","occupancy":94,"yield":6.8,"risk_score":82,"risk_level":"Low","token_price":50,"available_tokens":11600,"gross_rent":690000,"costs":282000,"min_investment":150,"why":"Co-living exposure to Milan's international student and young professional market."},
    {"id":"AMS-01","name":"Amsterdam Student Rooms Portfolio","city":"Amsterdam","country":"Netherlands","type":"Rooms portfolio","occupancy":98,"yield":6.1,"risk_score":90,"risk_level":"Very Low","token_price":100,"available_tokens":5400,"gross_rent":780000,"costs":340000,"min_investment":200,"why":"Diversified room portfolio in a structurally undersupplied student housing market."},
    {"id":"BCN-01","name":"Barcelona International Student Hub","city":"Barcelona","country":"Spain","type":"Student hub","occupancy":92,"yield":7.9,"risk_score":76,"risk_level":"Medium","token_price":50,"available_tokens":9300,"gross_rent":615000,"costs":220000,"min_investment":100,"why":"Student hub targeting exchange students and postgraduate programs."},
    {"id":"LIS-01","name":"Lisbon Erasmus Residence","city":"Lisbon","country":"Portugal","type":"Erasmus residence","occupancy":91,"yield":8.2,"risk_score":73,"risk_level":"Medium","token_price":50,"available_tokens":6800,"gross_rent":360000,"costs":130000,"min_investment":100,"why":"Smaller residence positioned for Erasmus and international mobility demand."},
    {"id":"BER-01","name":"Berlin Applied Sciences Housing","city":"Berlin","country":"Germany","type":"Student apartments","occupancy":95,"yield":6.5,"risk_score":84,"risk_level":"Low","token_price":100,"available_tokens":6100,"gross_rent":610000,"costs":265000,"min_investment":200,"why":"Student apartment portfolio in a large university and technology market."},
])

MARKET = pd.DataFrame({
    "Month":["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
    "Average Occupancy %":[92.5,93,93.2,93.6,94.1,94.3,94.5,95,96.4,96,95.5,94.8],
    "Average Yield %":[7,7,7.1,7.1,7.2,7.2,7.2,7.3,7.4,7.4,7.3,7.3],
})

if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "user" not in st.session_state: st.session_state.user = {"name":"Demo Investor","email":"demo@dormvest.app","wallet":"0xDV2026DEMO","profile":"Balanced"}
if "transactions" not in st.session_state:
    st.session_state.transactions = []
if "onboarded" not in st.session_state: st.session_state.onboarded = False


def money(x: float) -> str: return f"€{x:,.0f}"
def risk_label(score: int) -> str:
    if score >= 85: return "Very Low"
    if score >= 78: return "Low"
    if score >= 70: return "Medium"
    return "High"

def tx_hash(email: str, pid: str, amount: float) -> str:
    raw = f"{email}-{pid}-{amount}-{datetime.utcnow().isoformat()}".encode()
    return "0x" + hashlib.sha256(raw).hexdigest()[:18]


def login_page():
    st.title("DormVest")
    st.subheader("Tokenized student-housing investing, explained simply.")
    st.write("This academic FinTech app demonstrates fractional access to rental-income rights from student housing properties using a simulated blockchain ledger and smart-contract distribution logic.")
    left, right = st.columns([1,1])
    with left:
        st.info("Demo login: demo@dormvest.app / demo")
        mode = st.radio("Choose action", ["Login", "Register demo account"], horizontal=True)
        email = st.text_input("Email", value="demo@dormvest.app")
        password = st.text_input("Password", value="demo", type="password")
        if mode == "Register demo account":
            name = st.text_input("Full name", value="Demo Investor")
        else:
            name = "Demo Investor"
        if st.button("Enter DormVest", use_container_width=True):
            st.session_state.logged_in = True
            st.session_state.user = {"name": name, "email": email, "wallet": "0xDV" + hashlib.md5(email.encode()).hexdigest()[:8].upper(), "profile":"Balanced"}
            st.rerun()
    with right:
        st.markdown("### What you can do in the demo")
        st.write("1. Complete a beginner investor questionnaire.")
        st.write("2. Browse student-housing investment opportunities.")
        st.write("3. Simulate token purchases and rental income.")
        st.write("4. Review your portfolio, wallet, and blockchain ledger.")
        st.write("5. Understand how the business model makes money.")


def sidebar():
    st.sidebar.title("DormVest")
    st.sidebar.caption(f"Signed in as {st.session_state.user['email']}")
    page = st.sidebar.radio("Navigation", [
        "Start Here", "Dashboard", "Marketplace", "Invest", "Portfolio", "Wallet & Ledger", "Risk Center", "Secondary Market", "Operator Portal", "Business Model", "Help"
    ])
    if st.sidebar.button("Log out"):
        st.session_state.logged_in = False
        st.rerun()
    return page


def start_here():
    st.title("Start Here")
    st.write("DormVest is not a crypto-trading app. It is a student-housing investment infrastructure demo.")
    st.markdown("### Simple explanation")
    st.write("Property operators tokenize future rental-income rights. Investors buy fractions of those rights. Rental income is then distributed proportionally using smart-contract logic.")
    st.markdown("### Investor questionnaire")
    st.write("Answer these questions so the app can explain investments based on your profile.")
    q1 = st.selectbox("1. What is your investment experience?", ["Beginner", "Some experience", "Advanced"])
    q2 = st.selectbox("2. What matters most to you?", ["Stable monthly income", "Higher yield", "Diversification", "Learning the concept"])
    q3 = st.selectbox("3. How much risk are you comfortable with?", ["Low", "Medium", "High"])
    q4 = st.selectbox("4. How long would you hold this type of investment?", ["Less than 1 year", "1-3 years", "3+ years"])
    q5 = st.selectbox("5. Preferred city exposure?", ["Italy", "Spain/Portugal", "Northern Europe", "Diversified Europe"])
    if st.button("Save my profile", use_container_width=True):
        profile = "Conservative" if q3 == "Low" else "Balanced" if q3 == "Medium" else "Growth"
        st.session_state.user["profile"] = profile
        st.session_state.onboarded = True
        st.success(f"Profile saved: {profile}. You can now explore the dashboard and marketplace.")
    st.markdown("### Quick tutorial")
    st.write("Use Marketplace to choose a property, Invest to simulate a purchase, Portfolio to see your holdings, and Wallet & Ledger to see the blockchain-style transaction record.")


def dashboard():
    st.title("Dashboard")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Cities", len(PROPERTIES["city"].unique()))
    c2.metric("Average Yield", f"{PROPERTIES['yield'].mean():.1f}%")
    c3.metric("Average Occupancy", f"{PROPERTIES['occupancy'].mean():.1f}%")
    c4.metric("Avg Risk Score", f"{PROPERTIES['risk_score'].mean():.0f}/100")
    st.markdown("### European Student Housing Index")
    st.write("A simple demo index showing average occupancy and yield assumptions for the student-housing portfolio.")
    fig1 = px.line(MARKET, x="Month", y="Average Occupancy %", markers=True)
    st.plotly_chart(fig1, use_container_width=True)
    fig2 = px.bar(PROPERTIES, x="city", y="yield", text="yield", title="Projected annual yield by city")
    st.plotly_chart(fig2, use_container_width=True)


def marketplace():
    st.title("Marketplace")
    st.write("Browse tokenized student-housing rental-income opportunities.")
    city = st.multiselect("Filter by city", sorted(PROPERTIES.city.unique()), default=list(sorted(PROPERTIES.city.unique())))
    risk = st.multiselect("Filter by risk level", sorted(PROPERTIES.risk_level.unique()), default=list(sorted(PROPERTIES.risk_level.unique())))
    data = PROPERTIES[PROPERTIES.city.isin(city) & PROPERTIES.risk_level.isin(risk)]
    for _, row in data.iterrows():
        with st.container(border=True):
            left, right = st.columns([2,1])
            with left:
                st.subheader(row["name"])
                st.write(f"{row['city']}, {row['country']} · {row['type']}")
                st.write(row["why"])
            with right:
                st.metric("Projected yield", f"{row['yield']:.1f}%")
                st.metric("Occupancy", f"{row['occupancy']:.0f}%")
                st.metric("Risk score", f"{row['risk_score']}/100")
                st.caption(f"Minimum investment: {money(row['min_investment'])}")


def invest():
    st.title("Invest")
    st.write("This is a simulation. No real money, tokens, or securities are issued.")
    options = {f"{r['name']} ({r['city']})": r for _, r in PROPERTIES.iterrows()}
    choice = st.selectbox("Choose property", list(options.keys()))
    row = options[choice]
    c1,c2,c3 = st.columns(3)
    c1.metric("Token price", money(row["token_price"]))
    c2.metric("Projected yield", f"{row['yield']:.1f}%")
    c3.metric("Risk level", row["risk_level"])
    amount = st.number_input("Investment amount (€)", min_value=float(row["min_investment"]), max_value=100000.0, value=float(max(500, row["min_investment"])), step=50.0)
    tokens = int(amount // row["token_price"])
    invested = tokens * row["token_price"]
    annual_income = invested * row["yield"] / 100
    monthly_income = annual_income / 12
    st.markdown("### Simulation result")
    r1,r2,r3 = st.columns(3)
    r1.metric("Tokens received", f"{tokens:,}")
    r2.metric("Expected monthly income", money(monthly_income))
    r3.metric("Expected annual income", money(annual_income))
    st.write("Plain English: you are buying simulated digital units representing a proportional claim on future rental-income distributions from this property.")
    if st.button("Simulate investment", use_container_width=True):
        st.session_state.transactions.append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"), "property_id": row["id"], "property": row["name"], "city": row["city"],
            "action": "BUY", "amount": invested, "tokens": tokens, "monthly_income": monthly_income, "tx_hash": tx_hash(st.session_state.user["email"], row["id"], invested), "status":"Confirmed"
        })
        st.success("Investment simulated and added to portfolio/ledger.")


def portfolio_df():
    txs = pd.DataFrame(st.session_state.transactions)
    if txs.empty:
        return txs
    return txs.groupby(["property_id","property","city"], as_index=False).agg(tokens=("tokens","sum"), invested=("amount","sum"), monthly_income=("monthly_income","sum"))


def portfolio():
    st.title("Portfolio")
    pf = portfolio_df()
    if pf.empty:
        st.info("No simulated investments yet. Go to the Invest page and make your first demo purchase.")
        return
    c1,c2,c3 = st.columns(3)
    c1.metric("Total invested", money(pf.invested.sum()))
    c2.metric("Expected monthly income", money(pf.monthly_income.sum()))
    c3.metric("Properties held", len(pf))
    st.dataframe(pf, use_container_width=True, hide_index=True)
    fig = px.pie(pf, values="invested", names="city", title="Portfolio allocation by city")
    st.plotly_chart(fig, use_container_width=True)


def wallet_ledger():
    st.title("Wallet & Blockchain Ledger")
    st.write("The wallet and ledger are simulated to demonstrate how blockchain infrastructure could record ownership and transfers.")
    st.metric("Wallet address", st.session_state.user["wallet"])
    txs = pd.DataFrame(st.session_state.transactions)
    if txs.empty:
        st.info("No transactions yet.")
    else:
        st.dataframe(txs[["date","property","action","amount","tokens","monthly_income","tx_hash","status"]], use_container_width=True, hide_index=True)
    st.markdown("### Smart-contract logic in the demo")
    st.write("Property contract stores asset data. Ownership contract stores token balances. Distribution contract calculates monthly income. Marketplace contract simulates secondary-market transfers.")


def risk_center():
    st.title("Risk Center")
    prop = st.selectbox("Select property for stress test", PROPERTIES["name"].tolist())
    row = PROPERTIES[PROPERTIES.name == prop].iloc[0]
    st.write("Test how lower occupancy or higher operating costs would affect estimated net income.")
    occ_drop = st.slider("Occupancy drop", 0, 30, 10, format="%d%%")
    cost_increase = st.slider("Cost increase", 0, 40, 15, format="%d%%")
    base_net = row.gross_rent - row.costs
    stressed_rent = row.gross_rent * (1 - occ_drop/100)
    stressed_cost = row.costs * (1 + cost_increase/100)
    stressed_net = stressed_rent - stressed_cost
    c1,c2,c3 = st.columns(3)
    c1.metric("Base net income", money(base_net))
    c2.metric("Stressed net income", money(stressed_net))
    c3.metric("Impact", money(stressed_net - base_net))
    st.progress(int(row.risk_score))
    st.caption(f"DormVest Risk Score: {row.risk_score}/100. Higher is safer.")


def secondary_market():
    st.title("Secondary Market")
    st.write("Demo market where investors could sell token positions to other investors. This is simulated only.")
    sample = PROPERTIES[["id","name","city","yield","token_price","available_tokens","risk_level"]].copy()
    sample["bid_price"] = sample.token_price * 0.99
    sample["ask_price"] = sample.token_price * 1.01
    st.dataframe(sample, use_container_width=True, hide_index=True)
    st.info("In a real version, secondary trading would require regulation, KYC/AML, custody rules, and compliant transfer restrictions.")


def operator_portal():
    st.title("Operator Portal")
    st.write("For property owners and student-housing operators seeking financing.")
    with st.form("operator"):
        name = st.text_input("Property name")
        city = st.text_input("City")
        units = st.number_input("Number of units", min_value=1, value=25)
        rent = st.number_input("Estimated annual gross rent (€)", min_value=0, value=250000, step=10000)
        needed = st.number_input("Capital needed (€)", min_value=0, value=500000, step=25000)
        submitted = st.form_submit_button("Submit for demo review")
    if submitted:
        st.success("Demo submission received. In the real model, DormVest would perform due diligence, legal structuring, and tokenization review.")


def business_model():
    st.title("Business Model")
    st.markdown("### Who pays DormVest?")
    st.write("DormVest has two customer groups: investors and property operators.")
    st.markdown("### Revenue streams")
    st.write("1. Primary token purchase fee: 1.0% on new investments.")
    st.write("2. Secondary market trading fee: 0.5% on resale transactions.")
    st.write("3. Property onboarding fee: fixed due-diligence/listing fee or 1-3% of capital raised.")
    st.write("4. Asset management fee: 1.0% annually on assets managed through the platform.")
    st.write("5. DormVest Pro subscription: advanced analytics, stress tests, portfolio reports.")
    st.markdown("### Example")
    st.write("If a property raises €1,000,000, a 2% onboarding fee generates €20,000. If investors trade €200,000 of tokens, a 0.5% trading fee generates €1,000.")
    st.markdown("### Why it is FinTech")
    st.write("The app combines tokenization, digital assets, blockchain ledger logic, smart-contract distribution, portfolio analytics, and alternative finance.")


def help_page():
    st.title("Help")
    st.markdown("### What is tokenization?")
    st.write("Tokenization means representing an economic right as a digital unit. In this demo, tokens represent simulated rental-income exposure, not legal ownership.")
    st.markdown("### Is this real investing?")
    st.write("No. This is an academic prototype. It does not process payments, issue securities, or connect to a real blockchain.")
    st.markdown("### Why student housing?")
    st.write("Student housing has recurring demand, measurable occupancy, city-level scarcity, and strong relevance in European university markets.")


if not st.session_state.logged_in:
    login_page()
else:
    page = sidebar()
    if page == "Start Here": start_here()
    elif page == "Dashboard": dashboard()
    elif page == "Marketplace": marketplace()
    elif page == "Invest": invest()
    elif page == "Portfolio": portfolio()
    elif page == "Wallet & Ledger": wallet_ledger()
    elif page == "Risk Center": risk_center()
    elif page == "Secondary Market": secondary_market()
    elif page == "Operator Portal": operator_portal()
    elif page == "Business Model": business_model()
    elif page == "Help": help_page()
