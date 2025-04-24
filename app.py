import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler

st.set_page_config(page_title="Financial Risk Assessment App", layout="wide")
st.title("💰 Financial Risk Assessment Tool")

uploaded_file = st.file_uploader("Upload the Online Retail CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')

    # Clean data
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df = df.dropna(subset=['CustomerID'])
    df = df[~df['InvoiceNo'].astype(str).str.startswith('C')]
    df['TotalAmount'] = df['Quantity'] * df['UnitPrice']

    # RFM features
    rfm = df.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (df['InvoiceDate'].max() - x.max()).days,
        'InvoiceNo': 'nunique',
        'TotalAmount': 'sum'
    })
    rfm.columns = ['Recency', 'Frequency', 'Monetary']

    # Risk scoring logic
    rfm['RiskScore'] = (
        (rfm['Recency'] > rfm['Recency'].median()).astype(int) +
        (rfm['Monetary'] < rfm['Monetary'].median()).astype(int) +
        (rfm['Frequency'] > rfm['Frequency'].median()).astype(int)
    )

    # Categorize risk
    rfm['RiskLevel'] = rfm['RiskScore'].apply(
        lambda x: 'High' if x >= 2 else ('Medium' if x == 1 else 'Low')
    )

    st.subheader("🧾 Financial Risk Scores")
    st.dataframe(rfm[['Recency', 'Frequency', 'Monetary', 'RiskScore', 'RiskLevel']].sort_values(by='RiskScore', ascending=False))

    st.subheader("📊 Risk Level Distribution")
    st.bar_chart(rfm['RiskLevel'].value_counts())

else:
    st.info("Please upload the Online Retail dataset (CSV file) to assess financial risk.")
