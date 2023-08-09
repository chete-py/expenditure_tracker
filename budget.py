import streamlit as st
import pandas as pd
import plotly as px
import plotly.graph_objects as go

# title of the app
#st.title("MONTHLY EXPENSES")

# Add a sidebar
st.sidebar.image('newlogo.png', use_column_width=True)
st.sidebar.subheader("Navigation Pane")

# Function to add a new entry to the CSV file
def add_entry_to_csv(data):
    # Load existing CSV data
    df = pd.read_csv("expenses.csv")

    # Append new data to the DataFrame
    new_entry = pd.DataFrame([data])
    newdf = pd.concat([df, new_entry], ignore_index=True)

    # Save the updated DataFrame back to the CSV file
    newdf.to_csv("expenses.csv", index=False)


    newdf = newdf.to_html(index=False)
    # Add inline CSS to change font size
    newdf = newdf.replace('<table', '<table style="font-size: 11px;"')       

    st.markdown(newdf, unsafe_allow_html=True)

   
# Main Streamlit app code
def main(): 


    # Create a sidebar to switch between views
    view = st.sidebar.radio("View", ["Dashboard", "New Item", "Records"])

    if view == "Dashboard":
        st.subheader("DASHBOARD")
        newdf = pd.read_csv("expenses.csv")       
       
        # Find the most expensive item
        most_expensive_item = newdf[newdf['Amount'] == newdf['Amount'].max()]
        
        # Find the most frequent category
        most_frequent_category = newdf['Category'].mode().values[0]
        
        # Convert 'Amount' column to numeric before calculating sum
        #newdf['Amount'] = pd.to_numeric(newdf['Amount'], errors='coerce')
    
        # Calculate total amount in the most frequent category
        total_amount_in_category = newdf[newdf['Category'] == most_frequent_category]['Amount'].sum()

        # Find the most visited store
        most_visited_store = newdf['Store'].mode().values[0]

        # Calculate the number of times the frequent category occurred
        frequent_category_count = newdf[newdf['Category'] == most_frequent_category].shape[0]
    
        # Calculate the percentage for the frequent outlet
        frequent_outlet_percentage = (newdf[newdf['Store'] == most_visited_store].shape[0] / len(newdf)) * 100
    
        # Calculate monthly average expenditure
        #monthly_average_expenditure = newdf.groupby(newdf['Date'].dt.to_period('M'))['Amount'].mean()
    
            
        # Display the most expensive item in a custom card-like layout
        st.markdown(
        f'<div style= "display: flex; flex-direction: row;">'  # Container with flex layout
        f'<div style="background-color: #f19584; padding: 10px; border-radius: 10px; width: 250px; margin-right: 20px;">'
        f'<strong style="color: black;">FREQUENT CATEGORY</strong> <br>'
        f"{most_frequent_category}<br>"
        f"{frequent_category_count} times<br>"
        f'</div>'
        f'<div style="background-color: #AED6F1; padding: 10px; border-radius: 10px; width: 250px; margin-right: 20px;">'
        f'<strong style="color: black;">MOST EXPENSIVE ITEM</strong> <br>'
        f"{most_expensive_item['Use'].values[0]}<br>"
        f"Ksh. {int(most_expensive_item['Amount'].values[0]):,}"
        f'</div>'
        f'<div style="background-color: #99b27f; padding: 10px; border-radius: 10px; width: 250px;">'
        f'<strong style="color: black;">FREQUENT OUTLET</strong> <br>'
        f"{most_visited_store}<br>"
        f"{frequent_outlet_percentage:.0f}% of the time<br>"
        f'</div>'
        f'</div>',  # End of container
        unsafe_allow_html=True
        )

         # Calculate the sum of amounts for each category
        category_sum_amounts = newdf.groupby('Category')['Amount'].sum()
    
        # Create a bar chart for Category vs. Sum of Amounts using Plotly
        fig = go.Figure(data=[go.Bar(
        x=category_sum_amounts.index,
        y=category_sum_amounts        
        )])
        
        fig.update_layout(title={'text': 'AGGREGATE EXPENSES', 'x': 0.5, 'xanchor': 'center'}, 
                                  xaxis_title='Category',
                                  yaxis_title='Amount',
                                  xaxis=dict(tickfont=dict(size=8)),                                  
                                  )
        st.plotly_chart(fig)

        
        # Create a bar graph using Matplotlib
        #fig = go.Figure(data=[go.Bar(x=newdf['Category'], y=newdf['Amount'])])
        #fig.update_layout(title='Category vs. Amount',xaxis_title='Category',yaxis_title='Amount',xaxis=dict(tickangle=-45),)
        #st.plotly_chart(fig)
    
    elif view == "New Item":
        # Add the dashboard elements here
        st.subheader("NEW ITEM")
    
        # Create a form to input data for the new entry
        new_entry_data = {}
        new_entry_data['Date'] = st.date_input("Date")
        new_entry_data['Use'] = st.text_input("Use")
        new_entry_data['Category'] = st.text_input("Category")        
        new_entry_data['Store'] = st.text_input("Store")
        new_entry_data['Amount'] = st.number_input("Amount")
    
    # Add more columns as needed

        if st.button("Add Entry"):
            add_entry_to_csv(new_entry_data)
            st.success("New Record added successfully!")


    elif view == "Records":
        # Show the saved DataFrame here
        st.subheader("RECORDS") 
        lastdf = pd.read_csv("expenses.csv")

        # Convert the data frame to Markdown table format
        markdown_table = lastdf.to_markdown(index=False)

        # Display the Markdown-formatted table using st.markdown()
        st.markdown(markdown_table, unsafe_allow_html=True)
        #st.write(lastdf)
        
       
if __name__ == "__main__":
    main()


