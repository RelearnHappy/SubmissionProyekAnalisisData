import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set_style('dark')

def create_daily_recap(df):
    daily_recap = df.groupby(by='dteday').agg({
        'count_cr': 'sum'
    }).reset_index()
    return daily_recap

def count_by_day(day):
    day_count_2011 = day.query(str('dteday >= "2011-01-01" and dteday < "2012-12-31"'))
    return day_count_2011

def total_registered(day):
   reg =  day.groupby(by="dteday").agg({
      "registered": "sum"
    })
   reg = reg.reset_index()
   reg.rename(columns={
        "registered": "register_sum"
    }, inplace=True)
   return reg

def total_casual(day):
   cas =  day.groupby(by="dteday").agg({
      "casual": ["sum"]
    })
   cas = cas.reset_index()
   cas.rename(columns={
        "casual": "casual_sum"
    }, inplace=True)
   return cas

def macem_season(day): 
    season_ = day.groupby(by="season").count_cr.sum().reset_index() 
    return season_

# Membaca file CSV
main_data_day = pd.read_csv("dashboard/main_data_day.csv")
main_data_hour = pd.read_csv("dashboard/main_data_hour.csv")

datetime_columns = ["dteday"]
main_data_day.sort_values(by="dteday", inplace=True)
main_data_day.reset_index(inplace=True)   

main_data_hour.sort_values(by="dteday", inplace=True)
main_data_hour.reset_index(inplace=True)

for column in datetime_columns:
    main_data_day[column] = pd.to_datetime(main_data_day[column])
    main_data_hour[column] = pd.to_datetime(main_data_hour[column])

min_date_days = main_data_day["dteday"].min()
max_date_days = main_data_day["dteday"].max()

min_date_hour = main_data_hour["dteday"].min()
max_date_hour = main_data_hour["dteday"].max()

with st.sidebar:
    st.image("dashboard/foto_sepeda.png")
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date_days,
        max_value=max_date_days,
        value=[min_date_days, max_date_days])
  
main_days = main_data_day[(main_data_day["dteday"] >= str(start_date)) & 
                       (main_data_day["dteday"] <= str(end_date))]

main_hour = main_data_hour[(main_data_hour["dteday"] >= str(start_date)) & 
                        (main_data_hour["dteday"] <= str(end_date))]

daily_recap_df = create_daily_recap(main_hour)
day_count_2011 = count_by_day(main_days)
reg = total_registered(main_days)
cas = total_casual(main_days)
season = macem_season(main_hour)

st.title('Bike Sharing :bar_chart:')

st.subheader('Daily Sharing')
col1, col2, col3 = st.columns(3)
 
with col1:
    daily_recap = daily_recap_df['count_cr'].sum()
    st.metric('Total User', value= daily_recap)

with col2:
    total_sum = reg.register_sum.sum()
    st.metric("Total Registered", value=total_sum)

with col3:
    total_sum = cas.casual_sum.sum()
    st.metric("Total Casual", value=total_sum)
    
st.subheader("Visualisasi Bar Chart Antar-Musim")
grouped_day = pd.DataFrame({
    "count_cr": [0.471348, 0.841613, 0.918589, 1.061129],
}, index=["Musim Dingin", "Musim Panas", "Musim Semi", "Musim Gugur"])

grouped_day = grouped_day.sort_values(by="count_cr", ascending=False)
colors = sns.color_palette(["#FF7043", "#FFEB3B", "#80D6FF", "#66BB6A"], n_colors=len(grouped_day))

fig, ax = plt.subplots(figsize=(15, 6))  
sns.barplot(
    y=grouped_day.index,   
    x=grouped_day["count_cr"],  
    palette=colors,  
    ax=ax, 
    order=grouped_day.index  
)

ax.set_title("Bar Chart Antar-Musim", loc="center", fontsize=22)
ax.set_ylabel('Season', fontsize=20)
ax.set_xlabel('Count_cr', fontsize=20)

ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=20)
st.pyplot(fig)

st.subheader('Data Count_cr per Musim')
st.write(grouped_day)

st.subheader("Total Peminjaman Setiap Bulannya")

monthly_revenue = pd.Series({
    'Januari': 134933,
    'Febuari': 151352,
    'Maret': 228920,
    'April': 269094,
    'Mei': 331686,
    'Juni': 346342,
    'Juli': 344948,
    'Agustus': 351194,
    'September': 345991,
    'Oktober': 322352,
    'November': 254831,
    'Desember': 211036
})

colors = ['red' if month == 'Agustus' else 'tab:blue' for month in monthly_revenue.index]

plt.figure(figsize=(12, 6))  
bars = plt.bar(monthly_revenue.index, monthly_revenue.values, color=colors)

red_patch = plt.Line2D([0], [0], color='red', lw=4, label='Bulan Sewa Terbanyak (Agustus)')
blue_patch = plt.Line2D([0], [0], color='tab:blue', lw=4, label='Bulan Lainnya')
plt.legend(handles=[red_patch, blue_patch], loc='upper right', fontsize=10)

plt.title('Total Penyewaan Sepeda per Bulan', fontsize=16, pad=20)
plt.xlabel('Bulan', fontsize=14, labelpad=10)
plt.ylabel('Total Penyewaan', fontsize=14, labelpad=10)
plt.xticks(rotation=45, fontsize=12)  
plt.yticks(fontsize=12)

for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2, height + 5000,  
        f'{int(height)}',  
        ha='center', va='bottom', fontsize=10
    )

plt.tight_layout()
st.pyplot(plt)
st.subheader('Data Penyewaan Sepeda per Bulan')
st.write(monthly_revenue)
