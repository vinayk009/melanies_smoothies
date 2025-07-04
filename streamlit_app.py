#import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

#write directly to the app
st.title('Welcome Here :apple:')
st.write(
  """Customize your Smoothie: 
  """
)
name_on_order = st.text_input("Name on SMoothie")
st.write("The name on your Smoothie will be: ", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table(
  "smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
pd_df = my_dataframe.to_pandas()


ingredient_list = st.multiselect('Choose upto 5 ingredients: ', my_dataframe, max_selections = 5)

time_to_insert = st.button('Submit Order')
if time_to_insert:
  if ingredient_list:
    ingredients_string = ''
    for fruit_chosen in ingredient_list:
      ingredients_string += fruit_chosen + ' '
      search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
      st.write('The search value for ', fruit_chosen, ' is ', search_on, '.')
      smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit"+search_on)
      st.subheader(fruit_chosen + ' Nutrition Information')
      sf_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width=True)
  
  my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order) values('""" + ingredients_string + """','""" + name_on_order + """')"""
  session.sql(my_insert_stmt).collect()
  st.success('Your Smoothie is ordered!')









