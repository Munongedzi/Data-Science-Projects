import streamlit as st
import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

# Load data
@st.cache
def load_data():
    df = pd.read_csv("Mall_Customers.csv", encoding='latin1')
    return df

df = load_data()

# Data Cleaning
df['Description'] = df['Description'].str.strip()
df.dropna(axis=0, subset=['InvoiceNo'], inplace=True)
df['InvoiceNo'] = df['InvoiceNo'].astype('str')
df = df[~df['InvoiceNo'].str.contains('C')]

# Basket Creation
basket = (df[df['Country'] =="France"]
          .groupby(['InvoiceNo', 'Description'])['Quantity']
          .sum().unstack().reset_index().fillna(0)
          .set_index('InvoiceNo'))

# Encode units
def encode_units(x):
    if x <= 0:
        return 0
    if x >= 1:
        return 1

basket_sets = basket.applymap(encode_units)

# Frequent Itemsets
frequent_itemsets = apriori(basket_sets, min_support=0.07, use_colnames=True)

# Association Rules
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)

# Streamlit App
st.title("Market Basket Analysis using Apriori Algorithm")

# Display Data
st.subheader("Original Data:")
st.write(df.head())

st.subheader("Cleaned Data:")
st.write(basket_sets.head())

# Display Rules
st.subheader("Association Rules:")
st.write(rules)

# Filter Rules
st.subheader("Filtered Rules:")
filtered_rules = rules[(rules['lift'] >= 6) & (rules['confidence'] >= 0.8)]
st.write(filtered_rules)

# Conclusion
st.subheader("Conclusion:")
st.write("In looking at the rules, it seems that the green and red alarm clocks are purchased together "
         "and the red paper cups, napkins, and plates are purchased together in a manner that is higher than "
         "the overall probability would suggest.")

# Display the Streamlit app
if __name__ == '__main__':
    st.run()
