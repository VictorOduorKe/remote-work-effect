import streamlit as st
import plotly.express as px
from morale import get_dataframe, get_summary

# PAGE CONFIG
st.set_page_config(
    page_title="2020 Remote Work Analytics",
    layout="wide"
)

st.title("2020 Remote Work Analytics Dashboard")
st.markdown("Interactive insights on morale, engagement, and burnout risk")

# LOAD DATA
df = get_dataframe()
summary = get_summary()

# FILTERS (SIDEBAR)
st.sidebar.header("🔎 Filters")

work_modes = st.sidebar.multiselect(
    "Select Work Mode",
    options=df["work_mode"].unique(),
    default=df["work_mode"].unique()
)

df = df[df["work_mode"].isin(work_modes)]

# SUMMARY
st.subheader("📋 Executive Summary")
st.dataframe(
    summary.loc[work_modes] if len(work_modes) else summary,
    width="stretch"
)

st.divider()

# CHART 1: MORALE BY WORK MODE
st.subheader("📈 Average Morale by Work Mode")

fig1 = px.bar(
    df.groupby("work_mode", as_index=False)["morale_score"].mean(),
    x="work_mode",
    y="morale_score",
    labels={
        "work_mode": "Work Mode",
        "morale_score": "Average Morale Score"
    },
    title="Average Morale by Work Mode"
)

st.plotly_chart(fig1, use_container_width=True)

# CHART 2: ENGAGEMENT BY WORK MODE
st.subheader("Employee Engagement by Work Mode")

fig2 = px.bar(
    df.groupby("work_mode", as_index=False)["engagement_score"].mean(),
    x="work_mode",
    y="engagement_score",
    title="Employee Engagement by Work Mode"
)

st.plotly_chart(fig2, use_container_width=True)

st.divider()

# CHART 3: ORG SUPPORT VS MORALE
st.subheader("🏢 Organisational Preparedness vs Morale")

fig3 = px.line(
    df.groupby("org_prepared", as_index=False)["morale_score"].mean(),
    x="org_prepared",
    y="morale_score",
    markers=True,
    title="Organisational Preparedness vs Morale"
)

st.plotly_chart(fig3, use_container_width=True)

# CHART 4: CARE LOAD VS AGE
st.subheader("Care Load vs Age (Burnout Risk)")

fig4 = px.scatter(
    df,
    x="total_care_load",
    y="age",
    color="work_mode",
    size="burnout_risk",
    hover_data=["burnout_risk"],
    title="Care Load vs Age"
)

st.plotly_chart(fig4, use_container_width=True)
