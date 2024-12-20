#!/usr/bin/env python
# coding: utf-8

# # **Happy Deliveries Case Study Solutions**

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt

hd_customers = pd.read_excel('/content/hd_customers.xlsx')
hd_deliveries= pd.read_csv('/content/hd_delivery.csv')


# In[ ]:


hd_deliveries.head()


# In[ ]:


hd_customers.head()


# In[ ]:


# CLEAN DATASET
# 1. Input errors may have resulted in errors in ‘customer’ dataset


hd_customers['age'].value_counts()


# In[ ]:


hd_customers.loc[(hd_customers['age'] >= 80) | (hd_customers['age'] <= 10)]


# In[ ]:


hd_customers.isnull().sum()


# In[ ]:


hd_customers["city"].value_counts()


# In[ ]:


# Task 2: Data Cleaning

# name_of_data.plot(kind = "box", figsize = (x,y))

hd_customers.plot(kind="box", figsize=(14,8))

# ZOOM IN
# hd_customers["age"].plot(kind="box", figsize=(14,8))


# In[ ]:


hd_customers["age"].plot(kind="box", figsize=(14,8))


# In[ ]:





# In[ ]:


hd_customers.loc[hd_customers['age'] < 18]

# FOR COMPARISON
# hd_customers.loc[hd_customers['age'] < min_threshold]


# In[ ]:


hd_customers.loc[hd_customers['age'] > 100]

# FOR COMPARISON
# hd_customers.loc[hd_customers['age'] > max_threshold]


# In[ ]:


customers_clean = hd_customers.loc[(hd_customers['age'] > 18) & (hd_customers['age'] < 100)]


# In[ ]:


customers_clean["age"].describe()


# In[ ]:


# hd_customers
hd_customers.isnull().sum()


# In[ ]:


### Outliers

#hd_deliveries
hd_deliveries.describe()


# In[ ]:


#hd_customers
hd_customers.describe()

# We can see some ages very high and very low, likely to be an error by user when inputting their details.


# In[ ]:


def plot_boxplot(df, ft):
  df.boxplot(column = [ft])
  plt.grid(False)
  plt.show()


# In[ ]:


plot_boxplot(hd_customers, 'age')


# In[ ]:


hd_customers['age'].quantile(0.75)


# In[ ]:


# Removing outliers
min_threshold, max_threshold = hd_customers['age'].quantile([0.006, 0.994])
min_threshold, max_threshold


# In[ ]:


hd_customers[hd_customers['age'] < min_threshold]


# In[ ]:


hd_customers[hd_customers['age'] > max_threshold]


# In[ ]:





# In[ ]:


# THRESHOLD 1
min_threshold, max_threshold = hd_customers['age'].quantile([0.006, 0.994])
min_threshold, max_threshold

threshold_1 = hd_customers[(hd_customers['age'] < max_threshold) & (hd_customers['age'] > min_threshold)]


# In[ ]:


threshold_1.describe()


# In[ ]:


# THRESHOLD 2
min_threshold, max_threshold = hd_customers['age'].quantile([0.001, 0.999])
min_threshold, max_threshold

threshold_2 = hd_customers[(hd_customers['age'] < max_threshold) & (hd_customers['age'] > min_threshold)]


# In[ ]:


threshold_2.describe()


# In[ ]:


# Removing outliers
min_threshold, max_threshold = hd_customers['age'].quantile([0.006, 0.994])
min_threshold, max_threshold

customers_df = hd_customers[(hd_customers['age'] < max_threshold) & (hd_customers['age'] > min_threshold)]


# In[ ]:


customers_df.describe()


# In[ ]:


# NOT USEFUL FOR OUR ANALYSIS USE OTHER METHOD
# v_name = df["col_name"]  .quantile(0.25)
q1 = hd_customers['age'].quantile(0.25)
q3 = hd_customers['age'].quantile(0.75)

IQR = q3 - q1
IQR

# Same code written

other_method = hd_customers[~((hd_customers['age'] < (q1 - 1.5 * IQR)) | (hd_customers['age'] > (q3 + 1.5 * IQR)))]


# In[ ]:


other_method["age"].describe()


# In[ ]:


fig, ax = plt.subplots(figsize=(10, 10))
sns.boxplot(data=[hd_customers['age'], customers_df['age']])


# In[ ]:


customers_df.describe()


# In[ ]:


# 2. Actual payment for order needs to be calculated from the ‘delivery’ dataset
hd_deliveries.columns


# In[ ]:


hd_deliveries.head(20)


# In[ ]:


hd_deliveries.isnull().sum()


# In[ ]:


hd_deliveries['discount_pc'] = hd_deliveries['discount_pc'].fillna(0)


# In[ ]:


hd_deliveries["discount_pc"].isnull().sum()


# In[ ]:


hd_deliveries["payment_received"] = hd_deliveries["order_total"] - (hd_deliveries["order_total"] * hd_deliveries["discount_pc"])/100
hd_deliveries.head()


# In[ ]:


hd_deliveries.head()


# In[ ]:


# delivery_df['actual_payment'] = delivery_df['order_total'] - (delivery_df['order_total'] * (delivery_df['discount_pc']/100))


# In[ ]:


# 3. Orders with the status ‘CANCELLED’ payments should be removed from sales since they had to be refunded (already done)


# In[ ]:


hd_deliveries.isnull().sum()


# In[ ]:


hd_deliveries = hd_deliveries.loc[hd_deliveries["status"]=="COMPLETED"]
hd_deliveries.status.value_counts()


# In[ ]:


# ANOTHER METHOD IF SEE DELIVERED TIMESTAMP NULL, REMOVING ENTRIES WITH NULL


# In[ ]:


# Nulls
# hd_deliveries
hd_deliveries.isnull().sum()


# In[ ]:


hd_deliveries['discount_applied'].value_counts()


# In[ ]:


hd_deliveries['discount_pc'].value_counts()


# In[ ]:


#  Remove
hd_deliveries[hd_deliveries['delivered_timestamp'].isnull()]


# In[ ]:


dt_null = hd_deliveries['delivered_timestamp'].isnull()
deliveries_df = hd_deliveries.loc[~dt_null,:]


# In[ ]:


deliveries_df.isnull().sum()


# In[ ]:


hd_deliveries.columns


# In[ ]:


hd_customers.columns

# customers - id => deliveries - cust_id


# In[ ]:


# JOINING THE DATASETS

# customers dataset -> id => deliveries dataset -> cust_id

hd_customers = hd_customers.rename(columns={"id":"cust_id"})


# In[ ]:


# JOINING THE DATASETS

# METHOD 1 RENAME
# customers dataset -> id => deliveries dataset -> cust_id

hd_customers = hd_customers.rename(columns={"id":"cust_id"})

inner_join = pd.merge(hd_customers, hd_deliveries, on = "cust_id", how = "inner")

## METHOD 2:

merged = pd.merge(hd_deliveries, customers_df, left_on = 'cust_id', right_on = 'id', how = 'inner')
merged


# In[ ]:


inner_join.head()


# In[ ]:


## METHOD 1: example changing name

other_example = hd_deliveries.rename(columns={'cust_id': 'id'})


# In[ ]:


## example changing name

other_example.columns


# In[ ]:


## example changing name

example_merge = pd.merge(other_example, customers_df, on = 'id', how = 'inner')
example_merge


# In[ ]:


hd_deliveries = hd_deliveries.rename(columns={'id': 'cust_id'})


# In[ ]:


hd_deliveries["cust_id"].nunique()


# In[ ]:


customers_df["id"].nunique()


# In[ ]:


merged["id"].nunique()


# In[ ]:


## METHOD 2:

merged = pd.merge(hd_deliveries, customers_df, left_on = 'cust_id', right_on = 'id', how = 'inner')
merged


# In[ ]:


merged.columns


# In[ ]:


merged.head()


# # Task 4:
# 
# ### Question 1

# Compare monthly 2021 sales to 2022 and determine has ‘Happy Deliveries’ sales growth

# In[ ]:


merged.dtypes


# In[ ]:


# STEP 1 =  Convert date to correct datatype
merged['delivered_timestamp'] = pd.to_datetime(merged['delivered_timestamp'])
merged['order_timestamp'] = pd.to_datetime(merged['order_timestamp'])


# In[ ]:


# STEP 2 =  Extract date and create columns for month and year
merged['year'] = merged["order_timestamp"].dt.year
merged['month'] = merged["order_timestamp"].dt.month


# In[ ]:


# STEP 3
sales_2021 =merged.loc[merged["year"] == 2021]
sales_2022 =merged.loc[merged["year"] == 2022]


# In[ ]:


sales_2022.head()


# In[ ]:


sales_2021.columns


# In[ ]:


# STEP 3 = Split the years required for comparison
monthly_21 = sales_2021.groupby('month')['payment_received'].sum().to_frame('Amount')
monthly_22 = sales_2022.groupby('month')['payment_received'].sum().to_frame('Amount')


# In[ ]:


monthly_21.head()


# In[ ]:


fig = plt.figure(figsize=(15,10))

# Adding labels
labels = ["Sales 2021", "Sales 2022"]

sns.set(style="whitegrid")

ax = sns.lineplot(data = monthly_21, x='month', y='Amount', label='2021')
ax = sns.lineplot(data = monthly_22, x='month', y='Amount', label='2022')

plt.legend(labels)

ax.set_title('Yearly Sales')
ax.set_xlabel('Month')
ax.set_ylabel('Sales')


# In[ ]:


merged["order_timestamp"] = pd.to_datetime(merged["order_timestamp"])
merged["year"] = merged["order_timestamp"].dt.year
merged["month"] = merged["order_timestamp"].dt.month


# In[ ]:


merged.head()


# In[ ]:


# Filter 2 dfs
df_2021 = merged.loc[merged["year"] == 2021]
df_2022 = merged.loc[merged["year"] == 2022]


# In[ ]:


df_2021["year"].value_counts()


# In[ ]:


df_2022["year"].value_counts()


# In[ ]:


# Get total sales by month
sales_21 = df_2021.groupby('month')['payment_received'].sum().to_frame('msales_21')
sales_22 = df_2022.groupby('month')['payment_received'].sum().to_frame('msales_22')


# In[ ]:


sales_21


# In[ ]:


sales_22


# In[ ]:


# Graph with both graphs together, and code
fig = plt.figure(figsize=(15,10))
labels = ["Sales 2021", "Sales 2022"]

sns.set(style="whitegrid")
ax = sns.lineplot(data = [sales_21['msales_21'], sales_22['msales_22']], palette = 'viridis')
plt.legend(labels)
plt.xticks(df_2021['month'])
ax.set_title('Yearly Sales')
ax.set_xlabel('Month')
ax.set_ylabel('Sales (€)')


# In[ ]:


# Graph with both graphs together, and code
fig = plt.figure(figsize=(15,10))
labels = ["Sales 2021", "Sales 2022"]

sns.set(style="whitegrid")
ax = sns.lineplot(data = [sales_21['msales_21'], sales_22['msales_22']], palette = 'viridis')

plt.legend(labels)

 # plt.xticks(sales_2021['month']) # Why do I have to put in this line of code to refer to 2021 df
ax.set_title('Yearly Sales')
ax.set_xlabel('Month')
ax.set_ylabel('Sales (€)')


# In[ ]:


# Graph with both graphs together, and code
fig = plt.figure(figsize=(15,10))
labels = ["Sales 2021", "Sales 2022"]

# X LABELS FROM LIST
# IF USING LIST OF NAMES
labels_x = [1,2,3,4,5,6,7,8,9,10,11,12]

sns.set(style="whitegrid")
ax = sns.lineplot(data = [sales_21['msales_21'], sales_22['msales_22']], palette = 'viridis')

plt.legend(labels)

# PLT.XTICK(LIST_LABELS)
plt.xticks(labels_x) # Why do I have to put in this line of code to refer to 2021 df
# For comparison
# plt.xticks(sales_2021["Month"])
ax.set_title('Yearly Sales')
ax.set_xlabel('Month')
ax.set_ylabel('Sales (€)')


# In[ ]:


sales_2021["month"].value_counts()


# ### Question 2
# 
# Looking to the loyalty card holders, what is the age distribution of those customers?

# In[ ]:


customers_df.head(1)


# In[ ]:


plt.figure(figsize=(12,6))

ax = sns.countplot(data = customers_df, x= "age")


# In[ ]:


merged["age"].value_counts()


# In[ ]:


# lib_np.arange(start, stop, step)
np.arange(10,80,2)


# In[ ]:


# MEDIAN / MEAN / MODE
customers_df['age'].median(), customers_df['age'].mean(), customers_df['age'].mode()


# In[ ]:


# import numpy as np
fig = plt.figure(figsize=(12,6))
ax = fig.add_subplot()
ax.hist(customers_df['age'], bins = np.arange(10,80,2), color = 'blue')
ax.set_title('Age Distribution of the Loyalty Card Customers', fontweight ='ultralight', fontsize = 'xx-large')
ax.set_xlabel('Age')
ax.set_ylabel('Number of Customers')


# In[ ]:


plt.figure(figsize=(20, 10))

sns.countplot(customers_df["age"])



# ### Question 3
# 
# Is there a relationship between the total amount spend by a loyalty card holder and their age?

# In[ ]:


merged.groupby(['cust_id','age'])['payment_received'].sum()


# In[ ]:


# Group together
amount_spent = merged.groupby(['cust_id','age'])['payment_received'].sum().to_frame('cust_total')


# In[ ]:


# Group together
amount_spent = merged.groupby(['cust_id','age'])['payment_received'].sum().to_frame('cust_total')

amount_spent.reset_index(inplace = True)


# In[ ]:


# spend_age = merged[["age","payment_received"]]

plt.figure(figsize=(12, 10))
ax = sns.scatterplot(data = amount_spent, x = amount_spent["cust_total"], y=amount_spent["age"])

# LINE OF BEST FIT
x = amount_spent["cust_total"]
y = amount_spent["age"]


a, b = np.polyfit(x,y , 1)
ax.plot(x, a*x+b,  color='red', linestyle='--', linewidth=2)

plt.title('Age vs. Actual Payment')


# In[ ]:


# EXAMPLE OF PERFECT FIT
# NOT GOOD ANALYSIS
# EXAMPLE FOR COMPARISON


plt.figure(figsize=(12, 10))
ax = sns.scatterplot(data = amount_spent, x = amount_spent["age"], y= amount_spent["age"])


x = amount_spent["age"]
y = amount_spent["age"]

# LINE OF BEST FIT

a, b = np.polyfit(x,y , 1)
ax.plot(x, a*x+b,  color='red', linestyle='--', linewidth=2)


# In[ ]:


# x = amount_spent["cust_total"]
# y = amount_spent["age"]
# CORRELATION COFF

compare_one = amount_spent[['cust_total','age']]

compare_one.corr(method = 'pearson')


# In[ ]:


# HEATMAP OF ALL VARIABLES

cor_delivery = merged.corr()

plt.figure(figsize=(13, 6))

sns.heatmap(data = cor_delivery, vmax=1, annot=True, linewidths=.5)

plt.xticks(rotation=30, horizontalalignment='right')

plt.show()


# In[ ]:


merged["discount_code"].value_counts()


# In[ ]:


amount_spent.head()


# In[ ]:


amount_spent.columns


# ### Question 4
# 
# Is there a relationship between the amount of a payment, the age of a person and whether or not they used discount codes (HINT: scatterplot with 3 layers )

# In[ ]:





# In[ ]:


amount_spent_code = merged[['order_id','age','discount_applied','payment_received']]


# In[ ]:


# STEP 1: SCATTERPLOT OF DISCOUNT APPLIED TRUE / FALSE

# ax = sns.scatterplot(x='cust_total', y = 'age', data = amount_spent)

fig = plt.figure(figsize=(12,6))
sns.set(style="darkgrid")
ax = sns.scatterplot(x='payment_received', y = 'age', data = amount_spent_code, hue = 'discount_applied')
ax.set_title('Amount Spent Vs Age', fontweight ='ultralight', fontsize = 'xx-large')
ax.set_xlabel('Amount Spent')
ax.set_ylabel('Age')


# In[ ]:


# STEP 2: SCATTERPLOT OF ACTUAL DISCOUNTS APPLIED

plt.figure(figsize=(12, 10))
ax = sns.scatterplot(x="age", y="payment_received", hue="discount_code",data=merged)

ax.set_title('Amount Spent Vs Age', fontweight ='ultralight', fontsize = 'xx-large')
ax.set_xlabel('Amount Spent')
ax.set_ylabel('Age')


# ### Question 5
# 
# Compare the sales for 2022 across all regions.

# In[ ]:


# 2022 only
df_2022.head()


# In[ ]:


df_2022["delivery_region"].value_counts()


# In[ ]:


df_2022.groupby('delivery_region')['payment_received'].sum().to_frame("name")


# In[ ]:


regions_sales = df_2022.groupby('delivery_region')['payment_received'].sum().to_frame('region_sales_22').sort_values(by='region_sales_22', ascending = False)


# In[ ]:


regions_sales.columns


# In[ ]:


regions_sales.reset_index(inplace = True)


# In[ ]:


regions_sales.columns


# In[ ]:


regions_sales.columns


# In[ ]:


# STEP 1 CALCULATE TOTAL SALES PER REGION
# regions_sales = df_2022.groupby('delivery_region')['payment_received'].sum().to_frame('region_sales_22').sort_values(by='region_sales_22', ascending = False)

# STEP 2 GRAPH THE REGIONS BY TOTAL SALES IN A BAR PLOT
fig, ax = plt.subplots(figsize=(10, 10))
sns.set(style="darkgrid")
sns.barplot(data = regions_sales, x = regions_sales["delivery_region"], y =regions_sales["region_sales_22"], palette = "Spectral")
ax.set_title('Region Sales 2022', fontweight ='bold')
ax.set_xlabel('Delivery Region')
ax.set_ylabel('Sales (€)')


# # Task 5:
# 
# ### Question 6
# 
# Christmas is coming and Happy Deliveries want to reward their high spending customers. Who are the top 10 highest spending customers in 2022?
# Find their ID, name and email address for the marketing department to contact them with a reward.

# In[ ]:


df_2022.head()


# In[ ]:


# Get the total spent
top_cust_22 = df_2022.groupby('cust_id')['payment_received'].sum().to_frame('total_spent').sort_values(by = 'total_spent', ascending = False).reset_index()


# In[ ]:


top_cust_22.head()


# In[ ]:


# GET TOTAL SPENT BY GROUPING

# .head(n), if you don't suspect ties in ranking
top_cust_22 = df_2022.groupby('cust_id')['payment_received'].sum().to_frame('total_spent').sort_values(by = 'total_spent', ascending = False).reset_index().head(10)

# INCASE YOU SUSPECT TIES IN OUTPUT YOU CAN APPLY A RANK
# MIN RANK SKIPS TIES
# RANK()

# WHOLE NUMBERS WITH LIKELYHOOD OF TIES

# ADDING EXTRA COLUMN CALLED 'rank_min'

# name_df           = name_df["col_rank_wanted_on"].rank(method = 'min', ascending = False))
top_cust_22['rank_min'] = top_cust_22['total_spent'].rank(method = 'min', ascending = False)



# name_df           = name_df["col_rank_wanted_on"].rank(method = 'min', ascending = False))
# DENSE RANK DOES NOT SKIPS TIES
# DENSE_RANK
top_cust_22['rank_dense'] = top_cust_22['total_spent'].rank(method = 'dense', ascending = False)


# In[ ]:


# name_df           = name_df["col_rank_wanted_on"].rank(method = 'min', ascending = False))
# DENSE RANK DOES NOT SKIPS TIES
# DENSE_RANK
top_cust_22['rank_dense'] = top_cust_22['total_spent'].rank(method = 'dense', ascending = False)


# In[ ]:


top_cust_22[["total_spent","rank_min","rank_dense"]].head(20)


# In[ ]:


# EXAMPLE OF RANK
data = {'Sales': [2, 3,3, 3, 8, 1, 8],
        'Continent':['America','Europe','Europe','Europe','Asia','Europe','America']}

# Creating a dataframe with our data
df = pd.DataFrame(data)


# In[ ]:


df


# In[ ]:


# HEAD FUNCTION

# GET THE TOP SALES FIRST POSITION

df.groupby(["Continent"])["Sales"].sum().sort_values(ascending = False).head(1)


# In[ ]:


df.groupby(["Continent"])["Sales"].sum().sort_values(ascending = False)


# In[ ]:


c_sales = df.groupby(["Continent"])["Sales"].sum().to_frame('total_sales').sort_values(by = 'total_sales', ascending = False).reset_index()


# In[ ]:


c_sales


# In[ ]:


# name_df           = name_df["col_rank_wanted_on"].rank(method = 'min', ascending = False))
c_sales['rank_min'] = c_sales['total_sales'].rank(method = 'min', ascending = False)


# In[ ]:


c_sales


# In[ ]:


c_sales.loc[c_sales["rank_min"] == 1]


# In[ ]:


# name_df           = name_df["col_rank_wanted_on"].rank(method = 'min', ascending = False))
c_sales['dense_min'] = c_sales['total_sales'].rank(method = 'dense', ascending = False)


# In[ ]:


c_sales


# In[ ]:


# SIMPLE EXAMPLE OF RANK
data = {'Sales': [2, 3,3, 3, 8, 1, 8],
        'Continent':['America','Europe','Europe','Europe','Asia','Europe','America']}

# Creating a dataframe with our data
df = pd.DataFrame(data)

# .head(n), if you don't suspect ties in ranking
df.groupby(["Continent"])["Sales"].sum().sort_values(ascending = False).head(1)

# INCASE YOU SUSPECT TIES IN OUTPUT YOU CAN APPLY A RANK
# MIN RANK SKIPS TIES
# RANK()

c_sales = df.groupby(["Continent"])["Sales"].sum().to_frame('total_sales').sort_values(by = 'total_sales', ascending = False).reset_index()

# WHOLE NUMBERS WITH LIKELYHOOD OF TIES

# ADDING EXTRA COLUMN CALLED 'rank_min'

# name_df           = name_df["col_rank_wanted_on"].rank(method = 'min', ascending = False))
c_sales['rank_min'] = c_sales['total_sales'].rank(method = 'min', ascending = False)

# DENSE RANK DOES NOT SKIPS TIES
# DENSE_RANK
# name_df           = name_df["col_rank_wanted_on"].rank(method = 'min', ascending = False))
c_sales['dense_min'] = c_sales['total_sales'].rank(method = 'dense', ascending = False)

# NOW CAN FILTER BASED ON EITHER RANK TO WHERE RANK == 1

c_sales.loc[c_sales["rank_min"] == 1]


# In[ ]:


# name_df["total_spent_rank"] = name_df["col_ranking_on"].rank(method = "min", ascending = False)


# In[ ]:


top_cust_22


# In[ ]:


# Filter to under 10
result = top_cust_22.loc[top_cust_22['rank_min'] < 11]


# In[ ]:


result.drop(["rank_min", "rank_dense"], axis= 1, inplace = True)


# In[ ]:


result


# In[ ]:


customers_df.head()


# In[ ]:


# Rejoin to original df with left join
result_details = pd.merge(result, customers_df, left_on = 'cust_id', right_on = 'id', how = 'left')


# In[ ]:


result_details


# In[ ]:


result_details[['cust_id','total_spent','first_name','last_name','email']]


# ### Question 7

# In order to keep up with the anticipated increase in sales over Christmas, Happy Deliveries want to find what are the top 3 restaurants, so they can allocate their resources more efficiently. What are the top 3 restaurants in terms of sales for 2022?

# In[ ]:


df_2022.head()


# In[ ]:


top_rest_22 = (df_2022.groupby("restaurant_id")["payment_received"].sum().to_frame("restaurant_sales").sort_values(by="restaurant_sales", ascending=False).reset_index())


# In[ ]:


top_rest_22.head()


# In[ ]:


# Create a rank
top_rest_22["rest_rank"] = top_rest_22["restaurant_sales"].rank(method='min', ascending=False)


# In[ ]:


top_rest_22.head()


# In[ ]:


top_3= top_rest_22.loc[top_rest_22["rest_rank"] < 4][['restaurant_id', 'restaurant_sales']]


# In[ ]:


top_3


# In[ ]:


df_2022.groupby("restaurant_id")["payment_received"].sum().to_frame("restaurant_sales").sort_values(by="restaurant_sales", ascending=False).reset_index().head(3)


# In[ ]:


df_2022.groupby("restaurant_id")["payment_received"].sum().sort_values(ascending = False).head()


# In[ ]:


sales_2022.groupby(['restaurant_id'])['payment_received'].sum().sort_values(ascending = False).head(3)


# In[ ]:


sales_2022.groupby('restaurant_id')['payment_received'].sum().to_frame('Sales').sort_values(by = 'Sales', ascending = False).head(3)


# In[ ]:


# ONLY GROUP BY RESTAURANT_ID
# WRONG
# sales_2022.groupby(['restaurant_id', 'delivery_region'])['payment_received'].sum().to_frame('Sales').sort_values(by = 'Sales', ascending = False).head(3)


# ### Question 8

# The marketing department wants to reach out to non-returning loyalty card customers from 2021 in hopes they can lower their customer churn rate. Find all the customers who are considered non-returning including their id, name and email. (HINT: Non-returning means they have only made only one purchase)

# In[ ]:


merged.head()


# ## METHOD 1

# In[ ]:


merged.columns


# In[ ]:


merged["delivery_region"].count()


# In[ ]:


merged["delivery_region"].unique()


# In[ ]:


merged["delivery_region"].value_counts()


# In[ ]:


# COUNT VS VALUE_COUNTS

# merged.groupby('cust_id')['order_id'].value_counts().to_frame('order_count')


# In[ ]:


merged.groupby('cust_id')['order_id'].count().to_frame('order_count')


# In[ ]:


order_count = merged.groupby('cust_id')['order_id'].count().to_frame('order_count')


# In[ ]:


one_order = order_count[order_count['order_count'] == 1]


# In[ ]:


one_order["order_count"].value_counts()


# In[ ]:


one_order.head()


# In[ ]:


one_order.reset_index(inplace = True)


# In[ ]:


one_order.head()


# In[ ]:


# LIST OF ALL CUST IDS WHO PURCHASED ONCE

# BUT THESE PURCHASES COULD BE IN 2022 / 2021

one_order["cust_id"]


# In[ ]:


sales_2021.head()


# In[ ]:


# INNNER JOIN

cust_one_p_21 = pd.merge(one_order, sales_2021, on ="cust_id", how="inner")


# In[ ]:


cust_one_p_21.head()


# In[ ]:


solution_one = cust_one_p_21[['id','first_name','last_name','email']]


# In[ ]:


len(solution_one)


# In[ ]:


solution_one.head()


# ## METHOD 2

# In[ ]:


# first order of customer
first_order = merged.groupby('cust_id')['order_timestamp'].min()


# In[ ]:


first_order.head()


# In[ ]:


# last order of customer
last_order = merged.groupby('cust_id')['order_timestamp'].max()


# In[ ]:


last_order.head()


# In[ ]:


# join together
lifetime = pd.merge(first_order, last_order, on = 'cust_id', how = 'inner')


# In[ ]:


lifetime.count()


# In[ ]:


lifetime.head()


# In[ ]:


abs(lifetime['order_timestamp_x'] - lifetime['order_timestamp_y'])


# In[ ]:


# EXTRA NOT PART OF QUESTION
# create new column to calculte
lifetime['cust_lifetime'] = abs(lifetime['order_timestamp_x'] - lifetime['order_timestamp_y'])


# In[ ]:


lifetime.head()


# In[ ]:


lifetime["order_timestamp_x"] == lifetime["order_timestamp_y"]


# In[ ]:


non_returners = lifetime.loc[lifetime["order_timestamp_x"] == lifetime["order_timestamp_y"]]


# In[ ]:


non_returners.head()


# In[ ]:


non_returners["cust_lifetime"].value_counts()


# In[ ]:


non_returners.reset_index(inplace= True)


# In[ ]:


non_returners.nunique()


# In[ ]:


non_returning_details = pd.merge(non_returners, customers_df, left_on = 'cust_id',right_on = 'id', how = 'left')


# In[ ]:


non_returning_details.head()


# In[ ]:


non_returning_details.count()


# In[ ]:


non_returning_details["year"] = non_returning_details["order_timestamp_x"].dt.year


# In[ ]:


# filter to 2021

details_21 = non_returning_details.loc[non_returning_details["year"] == 2021]


# In[ ]:


details_21.nunique()


# In[ ]:


# answer
solution_two = details_21[['cust_id','first_name','last_name','email']].reset_index(drop = True)


# In[ ]:


solution_two.head()


# ### Question 9

# The sales team want to find out if the discount code ‘BLACKFRIDAY22’ was as successful as last years ‘BLACKFRIDAY21’. Find the total amount of sales from both discount codes.

# In[ ]:


# FINDING THE AMOUNT (COUNT) OF DISCOUNT CODES USED

black_friday = merged.loc[(merged["discount_code"] == "BLACKFRIDAY22") | (merged["discount_code"] == "BLACKFRIDAY21")]


# In[ ]:


black_friday.groupby("discount_code")["order_id"].count()


# Finding sales of BLACKFRIDAY discount codes

# In[ ]:


code_2022 = merged.loc[merged["discount_code"] == 'BLACKFRIDAY22']
code_2021 = merged.loc[merged["discount_code"] == 'BLACKFRIDAY21']


# In[ ]:


code_2021["discount_code"].value_counts()


# In[ ]:


total_code_22 = code_2022.groupby('discount_code')['payment_received'].sum()
total_code_21 = code_2021.groupby('discount_code')['payment_received'].sum()


# In[ ]:


total_code_22


# In[ ]:


print('Sales 2022: €', total_code_22, '\nSales 2021: €', total_code_21)


# In[ ]:


df_2022.head()


# In[ ]:


df_2021.head()


# In[ ]:


customers_df.head()


# In[ ]:


# Filter to only Black Friday Discounts

# customers_df = customers_df[customers_df['discount_code'] == 'BLACKFRIDAY21']

bf_22 = df_2022['discount_code'] == 'BLACKFRIDAY22'
bf_21 = df_2021['discount_code'] == 'BLACKFRIDAY21'


# In[ ]:


bf_22.head()


# In[ ]:


bf_22.head()


# In[ ]:


df_2022.head()


# In[ ]:


bf_22_df = df_2022.loc[bf_22,:]
bf_21_df = df_2021.loc[bf_21,:]


# In[ ]:


bf_22_df["discount_code"].value_counts()


# In[ ]:


bf_21_df["discount_code"].value_counts()


# In[ ]:


bf_21_df.head()


# In[ ]:


bf_21_df['payment_received'].head()


# In[ ]:


bf_22_sales = bf_22_df['payment_received'].sum()
bf_21_sales = bf_21_df['payment_received'].sum()


# In[ ]:


bf_22_sales


# In[ ]:


# With out new line

print('Sales 2022: €', bf_22_sales, 'Sales 2021: €', bf_21_sales)


# In[ ]:


#\n

print('Sales 2022: €', bf_22_sales, '\nSales 2021: €', bf_21_sales)


# In[ ]:


print('Sales 2022: €', bf_22_sales, '\nSales 2021: €', bf_21_sales)


# In[ ]:





# ### Question 10
# 
# What were the locations with the lowest cumulative sales for 2022? Should the marketing department tailor their marketing efforts more towards this location (Perhaps other factors are responsible for example low population)

# In[ ]:


sales_2022.groupby("delivery_region")["payment_received"].sum().sort_values().head(1)


# In[ ]:





# In[ ]:


region_sales_22 = df_2022.groupby('delivery_region')['payment_received'].sum().to_frame('region_sales').reset_index()


# In[ ]:


# example
region_sales_22_example = df_2022.groupby('delivery_region')['payment_received'].sum().to_frame('region_sales').sort_values(by = 'region_sales', ascending = False).reset_index()


# In[ ]:


region_sales_22_example.tail()


# In[ ]:


region_sales_22.head()


# In[ ]:


#
region_sales_22[region_sales_22['region_sales'] == region_sales_22['region_sales'].min()]

