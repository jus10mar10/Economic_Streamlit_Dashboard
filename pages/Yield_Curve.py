import streamlit as st
import plotly.express as px
from modules.treasury import yield_curve_full_data_pull
from modules.footer import footer


@st.cache_data
def data_pull_yields():
    """Fetches yield curve data and caches it using streamlit cache."""
    data = yield_curve_full_data_pull()
    return data


st.title("Yield Curve Viewer")

data = data_pull_yields()

dates = st.multiselect("Select Date", data.columns, default=list(data.columns))
checkbox = st.checkbox("Show Data")
if checkbox:
    st.write(data[dates].apply(lambda x: x.map("{:,.2%}".format)))

fig = px.line(
    data[dates],
    x=data.index,
    y=dates,
    title="Yield Curve",
    labels={"value": "Yield (%)", "index": "Maturity"},
)

# Customize figure formatting
fig.update_traces(line=dict(width=4, shape="spline"))  # Adjust line width and shape
fig.update_yaxes(tickformat=".2%")  # Format y-axis as percentage with 2 decimals
fig.update_layout(
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    legend_title_text="Effective Date",
    xaxis_tickangle=-45,  # Rotate x-axis labels
)

st.plotly_chart(fig)

# Differences Section
st.subheader("Compare Differences Between Maturing Dates")
anchor = st.selectbox("Select Anchor Maturity", data.index.unique(), index=10)
comparison = st.selectbox("Select Comparison Maturity", data.index.unique(), index=6)

diff = {col: data[col][anchor] - data[col][comparison] for col in data.columns}

fig2 = px.bar(
    x=diff.keys(),
    y=diff.values(),
    title=f"Difference between {anchor} and {comparison}",
    labels={"x": "Effective Date", "y": "Yield Difference (%)"},
)

# Format y-axis as percentage with 2 decimals
fig2.update_yaxes(tickformat=".2%")

st.plotly_chart(fig2)

st.write("Data Source: U.S. Department of the Treasury")

#############
footer()
