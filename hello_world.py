import streamlit as st
import pandas as pd
import datetime

st.markdown('# Hello World')
st.title('Hello World')
st.caption('This is a caption')
st.latex(r'''e^{i\pi} + 1 = 0''')

col1, col2, col3 = st.columns(3)

with col1:
    st.text_input('Text Input')

with col2:
    st.text_area('Text Area')

with col3:
    d = st.date_input('Date', value=None)
    st.write('Date :', d)

tab1, tab2, tab3 = st.tabs(['Tab 1', 'Tab 2', 'Tab 3'])

with tab1:
    number = st.number_input('Number Umur')
    st.write('Umur :', int(number), 'Tahun')

with tab2:
    selectbox = st.selectbox('Select Box', [1, 2, 3])
    st.write('Select Box :', selectbox)
with tab3:
    multiselect = st.multiselect('Multiselect', [1, 2, 3])
    st.write('Multiselect :', multiselect)


with st.sidebar:
    slide = st.slider('Slider', 0, 100, 50)
    st.write('Slider Value:', slide)


upload_file = st.file_uploader('Upload File')
if upload_file is not None:
    df = pd.read_csv(upload_file)
    st.dataframe(df)

st.write(pd.DataFrame({
    
    'first column': [1, 2, 3],
    'second column': [10, 20, 30],

}))

df = pd.DataFrame({
    'first column': [1, 2, 3],
    'second column': [10, 20, 30],
    'third column': [100, 200, 300],
    'fourth column': [1000, 2000, 3000]
})

st.dataframe(df)
st.table(df)
st.metric(label="Temperature", value="28 °C", delta="1.2 °C")
st.json({
    'first': [1, 2, 3],
    'second': [2, 4, 6],
    'third': [3, 6, 9]
})

st.code('print("Hello World")', language='python')

x = 10
'x', x

import matplotlib.pyplot as plt
import numpy as np


with st.container():
    arr = np.random.normal(1, 1, 100)
    fig, ax = plt.subplots()
    ax.hist(arr, bins=20)
    plt.show()
st.write("Outside the container")
fig

with st.container():
    st.title('Histogram')
    y = np.random.normal(15, 5, 250)
    fig, ax = plt.subplots()
    ax.hist(y, bins=20)
    st.pyplot(fig)

with st.expander('See code'):
    st.write('''
        Lorem ipsum dolor sit amet
        ''')

