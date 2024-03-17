import streamlit as st
import plotly.express as px
from modules.treasury import yield_curve_full_data_pull

@st.cache_data
def data_pull_yields():
    data = yield_curve_full_data_pull()
    return data
    
st.title('Yield Curve Viewer')

data = data_pull_yields()

dates = st.multiselect('Select Date', data.columns, default=list(data.columns))
checkbox = st.checkbox('Show Data')
if checkbox:
    st.write(data[dates])

fig = px.line(data[dates], x=data.index, y=dates, title='Yield Curve', 
            labels={'value': 'Yield (%)', 'term': 'Term (Years)'})
# line width
fig = fig.update_traces(line=dict(width=4))
# round line caps
fig = fig.update_traces(line_shape='spline')
# format y axis as percentage round to 2 decimal places
fig = fig.update_yaxes(tickformat=".2%")
# legend at top right
fig = fig.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
))
# legend title
fig = fig.update_layout(legend_title_text='Effective Date')
st.plotly_chart(fig)