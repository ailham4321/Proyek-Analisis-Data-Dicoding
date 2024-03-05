import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import datetime


day_df = pd.read_csv("Dashboard/day.csv")
hour_df = pd.read_csv("Dashboard/hour.csv")

change_scale = {"temp":41, "atemp":50, "hum":100, "windspeed":67}

for key, values in change_scale.items():
    day_df[key] = round(day_df[key]*values, 2)
    hour_df[key] = round(hour_df[key]*values, 2)

day_df["dteday"] = pd.to_datetime(day_df["dteday"])
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])

hour_df['mnth'] = hour_df['mnth'].replace({1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'})
hour_df['season'] = hour_df['season'].replace({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
hour_df["holiday"] = hour_df["holiday"].replace({1: 'Yes', 0: 'No'})
hour_df['weekday'] = hour_df['weekday'].replace({0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'})
hour_df["workingday"] = hour_df["workingday"].replace({1: 'Yes', 0: 'No'})
hour_df['weathersit'] = hour_df['weathersit'].replace({1: 'Clear', 2: 'Cloudy', 3: 'Light Rain', 4: 'Heavy Rain'})

day_df['mnth'] = day_df['mnth'].replace({1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'})
day_df['season'] = day_df['season'].replace({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
day_df["holiday"] = day_df["holiday"].replace({1: 'Yes', 0: 'No'})
day_df['weekday'] = day_df['weekday'].replace({0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'})
day_df["workingday"] = day_df["workingday"].replace({1: 'Yes', 0: 'No'})
day_df['weathersit'] = day_df['weathersit'].replace({1: 'Clear', 2: 'Cloudy', 3: 'Light Rain', 4: 'Heavy Rain'})

categorical_column = ["mnth", "season", "holiday", "weekday", "workingday", "weathersit"]
for column in categorical_column:
    day_df.astype("category")
    hour_df.astype("category")


with st.sidebar:
    st.image("https://scx2.b-cdn.net/gfx/news/hires/2018/bikesharecom.jpg")
    
    st.subheader("About Bike Share")
    st.write("Bike Share is not just transportation, it's a revolution in urban mobility. With over 500 programs and 500,000 bicycles globally, we believe it's the key to a sustainable future. Our dataset, derived from Washington D.C.'s Capital Bikeshare system, holds the pulse of this movement. Predicting rental counts based on environmental factors, it opens doors to a greener and healthier urban lifestyle. Join us in embracing Bike Share – where every ride is a step towards a connected, sustainable world. 🚴‍♂️🌍 #BikeShare #SustainableUrbanMobility")
    st.subheader("Tentang Bike Share")
    st.write("Bike Share bukan hanya alat transportasi; ini adalah revolusi dalam mobilitas perkotaan. Dengan lebih dari 500 program dan 500,000 sepeda di seluruh dunia, kami yakin ini adalah kunci menuju masa depan yang berkelanjutan. Dataset kami, berasal dari sistem Capital Bikeshare di Washington D.C., menjadi pusat dari gerakan ini. Dengan memprediksi jumlah penyewaan berdasarkan faktor lingkungan, ini membuka pintu menuju gaya hidup perkotaan yang lebih hijau dan sehat. Bergabunglah bersama kami dalam merangkul Bike Share - di mana setiap perjalanan adalah langkah menuju dunia yang terhubung dan berkelanjutan. 🚴‍♂️🌍 #BikeShare #MobilitasPerkotaanBerkelanjutan")

st.header('Bikeshare Company 2011-2012 Dashboard')
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    total_users = f"{round(day_df.cnt.sum()*0.000001, 2)} M"
    st.metric("Total Users", value=total_users)

with col2:
    total_registered_users = f"{round(day_df.registered.sum()*0.000001, 2)} M"
    st.metric("Total Registered Users", value=total_registered_users)

with col3:
    total_casual_users = f"{round(day_df.casual.sum()*0.001, 2)} K"
    st.metric("Total Casual Users", value=total_casual_users)

st.markdown("---")

# for linechart
start_date, end_date = st.date_input(
        label='Date Range',min_value=day_df["dteday"].min(),
        max_value=day_df["dteday"].max(),
        value=[day_df["dteday"].min(), day_df["dteday"].max()]
    )
linechart1_df = day_df[(day_df["dteday"] >= str(start_date)) & (day_df["dteday"] <= str(end_date))]

user_type_1 = st.multiselect(
    label="Select type of user",
    options=("registered", "casual", "cnt"),
    default="cnt",
    key = "user_type_1"
)
user_type_1.append("dteday")

melted_df = pd.melt(linechart1_df[user_type_1], id_vars="dteday", var_name="numeric_column", value_name='Value')

fig1 = plt.figure(figsize=(10, 6))
sns.lineplot(x='dteday', y='Value', hue='numeric_column', data=melted_df, marker='o', markersize=8)

plt.xlabel('Date', fontsize=14)
plt.ylabel('Active Users', fontsize=14)
plt.title('Line Chart of Bike Share Users', fontsize=16, fontweight='bold')

plt.legend(title='Kind of Users')

st.pyplot(fig1)

# for Scatterplot Daily
# scatter Plot
user_type_3 = st.multiselect(
    label="Select type of user",
    options=("registered", "casual"),
    default="registered",
    key = "user_type_3"
)
user_type_3.append("atemp")
melted_df = pd.melt(linechart1_df[user_type_3], id_vars='atemp', var_name='Users', value_name='Value')

fig5 = plt.figure(figsize=(8, 6))
sns.scatterplot(x='atemp', y="Value", hue="Users", data=melted_df, palette='coolwarm', s=40)

plt.xlabel('Temperature (Feels Like) in degree Celcius', fontsize=14)
plt.ylabel('Count of Users', fontsize=14)
plt.title('Behavior of Users', fontsize=16, fontweight='bold')
plt.legend(title='Kinds of Users', loc='upper right')

st.pyplot(fig5)



#for linechart hourly
hourly_date = st.date_input(
        label='Select Date (2011-2012)',
        value = datetime.date(2011, 1, 1)
)
linechart2_df = hour_df[(hour_df["dteday"] == str(hourly_date))]
user_type_2 = st.multiselect(
    label="Select type of user",
    options=("registered", "casual", "cnt"),
    default="cnt",
    key = "user_type_2"
)
user_type_2.append("hr")

melted_df = pd.melt(linechart2_df[user_type_2], id_vars="hr", var_name="numeric_column", value_name='Value')

fig2 = plt.figure(figsize=(10, 6))
sns.lineplot(x='hr', y='Value', hue='numeric_column', data=melted_df, marker='o', markersize=8)

plt.xlabel('Hour', fontsize=14)
plt.ylabel('Active Users', fontsize=14)
plt.title(f'Bike Share Users on {hourly_date}', fontsize=16, fontweight='bold')

plt.legend(title='Kind of Users')

st.pyplot(fig2)

# New Section
col1, col2 = st.columns(2)

with col1:
    # Pie Chart
    label = ["casual", "registered"]
    values = [linechart2_df["casual"].sum(), linechart2_df["registered"].sum()]
    fig3, ax = plt.subplots()
    ax.pie(values, labels=label, autopct='%1.1f%%', startangle=90)

    ax.axis('equal')  

    plt.title(f'Casual vs Registered Bike Share Users on {hourly_date}', fontsize=16, fontweight='bold')

    st.pyplot(fig3)

with col2:
    melted_df = pd.melt(day_df, id_vars="season", value_vars=["registered", "casual", "cnt"],
                    var_name='Numeric_Column', value_name='Value')
    fig4 = plt.figure(figsize=(10, 6))
    sns.barplot(x="season", y='Value', hue='Numeric_Column', data=melted_df, palette='pastel')
    plt.title("Season vs. Bike Share Users", fontsize=20, fontweight='bold')
    plt.xlabel('Users', fontsize=14)
    plt.ylabel('Season', fontsize=14)
    plt.legend(title='Kind of Users')

    st.pyplot(fig4)




