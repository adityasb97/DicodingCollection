# import library
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
sns.set_style('dark')
from babel.numbers import format_currency


#create daily_order_df
def create_daily_order_df(df):
    daily_order_df = df.resample(rule='D', on='order_date').agg({
        'order_id': 'nunique',
        'total_price': 'sum'
    })

    daily_order_df = daily_order_df.reset_index()
    daily_order_df.rename(columns={
        'order_id': 'order_count',
        'total_price': 'revenue'
    }, inplace=True)

    return daily_order_df

# create sum_order_item_df
def create_sum_order_item_df(df):
    sum_order_item_df = df.groupby('product_name').quantity_x.sum().sort_values(ascending=False).reset_index()

    return sum_order_item_df

# create bygender_df
def create_bygender_df(df):
    bygender_df = df.groupby('gender').customer_id.nunique().reset_index()
    bygender_df.rename(columns={
        'customer_id': 'customer_count'
    }, inplace=True)

    return bygender_df

# create byage_df
def create_byage_df(df):
    byage_df = df.groupby('age_group').customer_id.nunique().reset_index()
    byage_df.rename(columns={
        'customer_id': 'customer_count'
    }, inplace=True)

    return byage_df

# create bystate_df
def create_bystate_df(df):
    bystate_df = df.groupby('state').customer_id.nunique().reset_index()
    bystate_df.rename(columns={
        'customer_id': 'customer_count'
    }, inplace=True)

    return bystate_df

# create rfm_df
def create_rfm_df(df):
    rfm_df = df.groupby('customer_id', as_index=False).agg({
        'order_date' : 'max', # mengambil tanggal terakhir order
        'order_id' : 'nunique', # menghitung jumlah order
        'total_price' : 'sum' # menghitung total order
    })

    rfm_df.columns = ['customer_id', 'max_order_timestamp', 'frequency', 'monetary']

    # menghitung kapan terakhir pelanggan melakukan transaksi (hari)
    rfm_df['max_order_timestamp'] = pd.to_datetime(rfm_df['max_order_timestamp'])
    rfm_df['max_order_timestamp'] = rfm_df['max_order_timestamp'].dt.date

    recent_date = df['order_date'].dt.date.max()
    rfm_df['recency'] = rfm_df['max_order_timestamp'].apply(lambda x: (recent_date - x).days)
    rfm_df.drop('max_order_timestamp', axis=1, inplace=True)

    return rfm_df

#load data
all_df = pd.read_csv('all_data.csv')

datime_columns = ['order_date', 'delivery_date']
all_df.sort_values(by='order_date', inplace=True)
all_df.reset_index(drop=True, inplace=True)

for column in datime_columns:
    all_df[column] = pd.to_datetime(all_df[column])



#membuat filter sidebar
min_date = all_df['order_date'].min()
max_date = all_df['order_date'].max()

with st.sidebar:
    #menambahkan logo
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")

    #mengambil start_date & end_date dari input_date
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date, max_value= max_date,
        value=[min_date, max_date]
    )

start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

main_df = all_df[(all_df['order_date'] >= start_date) & (all_df['order_date'] <= end_date)]

daily_order_df = create_daily_order_df(main_df)
sum_order_item_df = create_sum_order_item_df(main_df)
bygender_df = create_bygender_df(main_df)
byage_df = create_byage_df(main_df)
bystate_df = create_bystate_df(main_df)
rfm_df = create_rfm_df(main_df)

#visualisasi
st.header('Dashboard Fashion Store Dicoding Academy')

st.subheader('Daily Order')
col1, col2, = st.columns(2)

with col1:
    total_order = daily_order_df['order_count'].sum()
    st.metric(label='Total Order', value=total_order)

with col2:
    total_revenue = format_currency(daily_order_df['revenue'].sum(), 'AUD', locale='es_CO')
    st.metric(label='Total Revenue', value=total_revenue)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_order_df['order_date'], 
    daily_order_df['order_count'],
    marker='o',
    linewidth=2,
    color='#90CAF9')
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)

# menampilkan 5 produk paling laris dan paling sedikit terjual
st.subheader('Best & Worst Selling Performing Products')

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x='quantity_x', y='product_name', data=sum_order_item_df.head(5),palette=colors ,ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel('Number of Sales', fontsize=30)
ax[0].set_title('Best Selling Products', fontsize=50, loc='center')
ax[0].tick_params(axis='x', labelsize=35)
ax[0].tick_params(axis='y', labelsize=30)

sns.barplot(x='quantity_x', y='product_name', data=sum_order_item_df.sort_values(by='quantity_x', ascending=False).head(5),palette=colors ,ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel('Number of Sales', fontsize=30)
ax[1].set_title('Worst Selling Products', fontsize=50, loc='center')
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig)

# visualisasi demografi
st.subheader('Customers Demografi')

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(20, 10))

    sns.barplot(data=bygender_df.sort_values(by='customer_count', ascending=False), x='gender', y='customer_count', ax=ax, palette=colors)

    ax.set_title("Number of Customer by Gender", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(20, 10))

    sns.barplot(data=byage_df.sort_values(by='customer_count', ascending=False), x='age_group', y='customer_count', ax=ax, palette=colors)

    ax.set_title("Number of Customer by Age", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

fig, ax = plt.subplots(figsize=(20, 10))
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(data=bystate_df.sort_values(by='customer_count', ascending=False), x='state', y='customer_count', ax=ax, palette=colors)

ax.set_title("Number of Customer by States", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

# visualisasi by RFM (Recency, Frequency, & Monetary)
st.subheader('Best Customer Based on RFM Parameters')

col1, col2, col3 = st.columns(3)

with col1:
    avg_recency = round(rfm_df['recency'].mean(),1)
    st.metric(label='Average Recency', value=avg_recency)

with col2:
    avg_frequency = round(rfm_df['frequency'].mean(),2)
    st.metric(label='Average Frequency', value=avg_frequency)

with col3:
    avg_frequency = format_currency(rfm_df['monetary'].mean(), 'AUD', locale='es_CO')
    st.metric(label='Average Monetary Value', value=avg_frequency)

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(35, 15))
colors = ["#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9"]

sns.barplot(x='recency', y='customer_id', data=rfm_df.sort_values(by='recency', ascending=True).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("customer_id", fontsize=30)
ax[0].set_title("By Recency (days)", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=30)
ax[0].tick_params(axis='x', labelsize=35)

sns.barplot(x='frequency', y='customer_id', data=rfm_df.sort_values(by='frequency', ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("customer_id", fontsize=30)
ax[1].set_title("By Frequency", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=30)
ax[1].tick_params(axis='x', labelsize=35)

sns.barplot(x='monetary', y='customer_id', data=rfm_df.sort_values(by='monetary', ascending=False).head(5), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel("customer_id", fontsize=30)
ax[2].set_title("By Monetary Value", loc="center", fontsize=50)
ax[2].tick_params(axis='y', labelsize=30)
ax[2].tick_params(axis='x', labelsize=35)

st.pyplot(fig)

st.caption('copyright @silentmonster')