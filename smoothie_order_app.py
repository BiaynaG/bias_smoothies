#1. Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
# To call Fruityvice API from our SniS App. We will use 'requests' library to build and send REST API calls
import requests
import pandas as pd

#2. Write directly to the app
st.title(":cup_with_straw: Get The Smoothie of Your Dreams :cup_with_straw: :sunglasses:")
st.write(
    """Make your custom Smoothie, choose the fruits that your :heart: desires!
    """
)

#13 🥋 Add a Name Box for Smoothie Orders
name_on_order = st.text_input('Name on Smoothie')
st.write('The name on your smoothie will be:', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

#4. Get only the column we need
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))

#5. Write dataframe into our streamlit page
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

#16. Convert the Snowpark dataframe to a Pandas dataframe to use the LOC function
pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

#6. Add multi-select from streamlit
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    ,my_dataframe
    ,max_selections=5
    )

# Our ingredients variable is an object or data type called a LIST.
# So it's a list in the traditional sense of the word, 
# but it is also a datatype or object called a LIST. 
# A LIST is different than a DATAFRAME which is also different 
# from a STRING!

#st.write(ingredients_list)
#st.text(ingredients_list)

#7. 🥋 Cleaning Up Empty Brackets. If ingredients have not yet been 
# chosen, there is no need to show this. 

#if ingredients_list:
        #st.write(ingredients_list)
        #st.text(ingredients_list)

#8. 🥋 Create a Place to Store Order Data (Done In worksheets)

#9. 📓 Changing the LIST to a STRING
# In order to convert the list to a string, we need to first 
# create a variable and then make sure Python thinks it 
# contains a string.

if ingredients_list:
	ingredients_string = ''
	
	for fruit_chosen in ingredients_list:
		ingredients_string += fruit_chosen + ' '

		search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
		st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
		
		#15: Use fruite_chosen in the API call
		st.subheader(fruit_chosen + ' Nutrition Information')
		#14. Read from fruityvice website instead of the snowflake table
		fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + search_on)
		#Expose the JSON Data Inside the Response Object
		fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
	
	#10. 🥋 Build a SQL Insert Statement & Test It
	my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order) values ('""" + ingredients_string + """', '""" + name_on_order + """')"""

	#st.write(my_insert_stmt)
	#st.stop()

    	#12. 🥋 Add a Submit Button, otherwise every fruit selection
    	# will create a new row in the orders table
	time_to_insert = st.button('Submit Order')

	#11. 🥋 Insert the Order into Snowflake
	#11. if ingredients_string:
	if time_to_insert:
		session.sql(my_insert_stmt).collect()
		st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
    

