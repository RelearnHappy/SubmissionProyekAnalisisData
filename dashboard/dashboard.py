# Fungsi untuk mengelompokkan weekday dan weekend
def group_by_weekday_weekend(data):
    data['day_of_week'] = data['dteday'].dt.dayofweek
    data['is_weekend'] = data['day_of_week'].apply(lambda x: 'Weekend' if x >= 5 else 'Weekday')
    
    grouped = data.groupby('is_weekend').agg({
        'casual': 'sum',
        'registered': 'sum'
    }).reset_index()
    return grouped

# Data weekday vs weekend
weekday_weekend_data = group_by_weekday_weekend(main_days)

# Visualisasi Bar Chart
st.subheader("Pola Penyewaan Sepeda: Weekday vs Weekend")

fig, ax = plt.subplots(figsize=(10, 6))

# Bar chart untuk casual dan registered
ax.bar(weekday_weekend_data['is_weekend'], weekday_weekend_data['casual'], label='Casual', color='tab:blue', alpha=0.7)
ax.bar(weekday_weekend_data['is_weekend'], weekday_weekend_data['registered'], label='Registered', color='tab:orange', alpha=0.7, bottom=weekday_weekend_data['casual'])

# Menambahkan label
ax.set_title('Pola Penyewaan Sepeda Antara Hari Kerja vs Akhir Pekan', fontsize=16)
ax.set_xlabel('Kategori', fontsize=14)
ax.set_ylabel('Jumlah Penyewaan', fontsize=14)
ax.legend(title='Tipe Pengguna', fontsize=12)

# Menambahkan angka total di atas bar
for index, row in weekday_weekend_data.iterrows():
    total = row['casual'] + row['registered']
    ax.text(index, total, f'{total:,}', ha='center', va='bottom', fontsize=12)

plt.tight_layout()
st.pyplot(fig)

# Tampilkan tabel data
st.subheader('Data Penyewaan Sepeda Weekday vs Weekend')
st.write(weekday_weekend_data)
