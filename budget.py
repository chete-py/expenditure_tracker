import streamlit as st
import pandas as pd
import numpy as np
import plotly as px
import calendar
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
        f'<div style="background-color: #50c878; padding: 10px; border-radius: 10px; width: 250px; margin-right: 20px;">'
        f'<strong style="color: black;">MOST EXPENSIVE ITEM</strong> <br>'
        f"{most_expensive_item['Use'].values[0]}<br>"
        f"Ksh. {int(most_expensive_item['Amount'].values[0]):,}"
        f'</div>'
        f'<div style="background-color: #DBAE58; padding: 10px; border-radius: 10px; width: 250px;">'
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
        
        # Set the color for bars
        bar_color = '#488A99'
        for trace in fig.data:
            trace.marker.color = bar_color

        st.plotly_chart(fig)

        
        # Calculate highest monthly expense
        newdf['Date'] = pd.to_datetime(newdf['Date'])  # Convert 'Date' column to datetime
        newdf['Month'] = newdf['Date'].dt.to_period('M')  # Create a new 'Month' column
        highest_monthly_expense = newdf.groupby('Month')['Amount'].sum().idxmax()

        # Get the highest expense amount for the corresponding month
        highest_expense_amount = newdf[newdf['Month'] == highest_monthly_expense]['Amount'].sum()
        # Get the name of the month
        month_name = highest_monthly_expense.strftime('%B %Y')


        fig_clock = go.Figure(go.Indicator(
        mode="gauge+number",
        value=highest_expense_amount,
        domain={'x': [0, 1], 'y': [0, 1]},
        # Change the 'title' property to 'number'
        number={'suffix': " "},
        gauge={'shape': 'angular',
               'axis': {'range': [None, highest_expense_amount * 1.2]},
                'bar': {'color': "#DBAE58"},                               
                'steps': [
                    {'range': [0, highest_expense_amount * 0.5], 'color': "#488A99"},
                    {'range': [highest_expense_amount * 0.5, highest_expense_amount * 0.8], 'color': "#488A99"}],
                },
        ))
        
        fig_clock.update_layout(title_text='MONTH WITH HIGHEST EXPENDITURE: {month_name}', title_x=0.5)  # Add title using update_layout
        
        # Display the Clock figure
        st.plotly_chart(fig_clock)      
        
        
    
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

        lastdf = lastdf.to_html(index=False)
        last_df = lastdf.replace('<table', '<table style="font-size: 12px;"')

        # Convert the data frame to Markdown table format
        # markdown_table = lastdf.to_markdown(index=False)

        # Display the Markdown-formatted table using st.markdown()
        # st.markdown(markdown_table, unsafe_allow_html=True)
        #st.table(lastdf)

        st.markdown(last_df, unsafe_allow_html=True)
        
       
if __name__ == "__main__":
    main()


