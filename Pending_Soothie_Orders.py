#Import python packages
import streamlit as st
from snowflake.snowpark.context import Session
@st.cache_resource
def get_session():
  return Session.builder.configs(st.secrets).create()
from snowflake.snowpark.functions import col, when_matched



# write directly to the app
st.title(f"Orders Devlivered Check :cup_with_straw:")
st.write("""Check the **Orders**""")

session = get_active_session()
my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()

if my_dataframe:
  editable_df = st.data_editor(my_dataframe)
  submitted = st.button('Submit')
  if submitted:
    st.success("Someone clicked the button.")
    try:
      og_dataset = session.table("smoothies.public.orders")
      edited_dataset = session.create_dataframe(editable_df)
      og_dataset.merge(edited_dataset
                       , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                       , [when_mated().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                      )
      st.success("Order(s) Updated!")
    except:
      st.write('Something went wrong.')
  
else:
  st.success('There are no pending orders right now')













  
