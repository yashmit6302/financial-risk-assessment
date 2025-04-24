import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Financial Risk Dashboard", layout="wide")
st.title("💼 Financial Risk Assessment Dashboard")

uploaded_file = st.file_uploader("Upload your Financial Risk Assessment CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📋 Data Preview")
    st.dataframe(df.head())

    st.subheader("📊 Risk Rating Distribution")
    risk_counts = df['Risk Rating'].value_counts()
    st.bar_chart(risk_counts)

    st.subheader("💳 Average Credit Score by Risk Rating")
    avg_credit = df.groupby('Risk Rating')['Credit Score'].mean()
    st.bar_chart(avg_credit)

    st.subheader("📈 Debt-to-Income Ratio by Risk Rating")
    fig, ax = plt.subplots()
    sns.boxplot(x='Risk Rating', y='Debt-to-Income Ratio', data=df, ax=ax)
    st.pyplot(fig)

    st.subheader("💰 Income Distribution by Risk Level")
    fig2, ax2 = plt.subplots()
    sns.violinplot(x='Risk Rating', y='Income', data=df, ax=ax2)
    st.pyplot(fig2)

    st.subheader("🏦 Assets Value vs. Risk Rating")
    fig3, ax3 = plt.subplots()
    sns.boxplot(x='Risk Rating', y='Assets Value', data=df, ax=ax3)
    st.pyplot(fig3)

else:
    st.info("Please upload a CSV file containing your financial risk assessment data.")
