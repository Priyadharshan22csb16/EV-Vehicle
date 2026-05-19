import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector
df=pd.read_csv("ev_data.csv")
df = df[['County', 'City', 'Model Year', 'Make', 'Model',
         'Electric Vehicle Type', 'Electric Range', 'Base MSRP']]

df.rename(columns={'County': 'Country'}, inplace=True)
df.dropna(inplace=True)
print(df.isnull().sum())
#top 10 brands of ev manufacturing
print(df['Make'].value_counts().head(10))
#Ev growth by year
print(df['Model Year'].value_counts().sort_index())
#ev range
print(df['Electric Range'].mean())
#top countries in ev usage
print(df['Country'].value_counts().head(10))
#top models in ev
print(df['Model'].value_counts().head(10))

print(df['Electric Vehicle Type'].value_counts())

print(df['City'].value_counts().head(10))

print(df.groupby('Make')['Electric Range'].mean().sort_values(ascending=False).head(10))

print(df.groupby('Make')['Base MSRP'].max().sort_values(ascending=False).head(10))

#Ev growth trend by year


yearly_growth = df['Model Year'].value_counts().sort_index()

plt.figure(figsize=(10,5))

plt.plot(yearly_growth.index, yearly_growth.values)

plt.xlabel("Model Year")
plt.ylabel("Number of EV Vehicles")
plt.title("EV Growth Trend Over Years")

plt.show()

# top 10 ev brands chart

top_brands = df['Make'].value_counts().head(10)

plt.figure(figsize=(10,5))

plt.bar(top_brands.index, top_brands.values)

plt.xlabel("EV Brand")
plt.ylabel("Vehicle Count")
plt.title("Top 10 EV Brands")

plt.xticks(rotation=45)

plt.show()

#top cities using ev

top_cities = df['City'].value_counts().head(10)

plt.figure(figsize=(10,5))

plt.bar(top_cities.index, top_cities.values)

plt.xlabel("City")
plt.ylabel("EV Count")
plt.title("Top 10 Cities with EV Usage")

plt.xticks(rotation=45)

plt.show()

#ev type distribution

ev_type = df['Electric Vehicle Type'].value_counts()

plt.figure(figsize=(7,7))

plt.pie(ev_type.values, labels=ev_type.index, autopct='%1.1f%%')

plt.title("EV Type Distribution")

plt.show()


conn = mysql.connector.connect(
    host="localhost",
    user="root",

    password="2468dharshan",
    port=3305,
    database="ev_analysis",

)

print("Connected Successfully")

cursor = conn.cursor()

sql = """
INSERT INTO ev_vehicles
(county, city, model_year, make, model,
ev_type, electric_range, base_msrp)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

values = []

for index, row in df.iterrows():
    values.append((
        row['Country'],
        row['City'],
        row['Model Year'],
        row['Make'],
        row['Model'],
        row['Electric Vehicle Type'],
        row['Electric Range'],
        row['Base MSRP']
    ))

cursor.executemany(sql, values)

conn.commit()

print("Data Inserted Successfully")