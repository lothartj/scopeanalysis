import streamlit as st
import pandas as pd
import plotly.express as px

def inventory_analysis_app():
    st.set_page_config(page_icon='🫗')
    hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
    st.markdown(hide_st_style, unsafe_allow_html=True)
    title_style = """
<style>
    /* Resetting body margin */
    
    body {
        margin: 0 !important;
    }
    
    /* Removing Streamlit's top padding */
    .main {
        padding-top: 70px !important;  /* Increase top padding to accommodate the custom title */
    }
    
    

    /* Custom title style */
    .title-style {
        font-family: 'Lucida Handwriting', cursive;
        font-size: 60px;
        font-weight: bold;
        text-align: center;
        width: 100%;
        z-index: 1000;  /* Ensuring it stays on top */
    }

    /* Custom author style */
    .author-style {
        font-size: 20px;
        text-align: center;
        font-family: 'Sans-Serif';
        width: 100%;
        margin-top: -10px;
        z-index: 1000;  /* Ensuring it stays on top */
    }
</style>
"""

    st.markdown(title_style, unsafe_allow_html=True)  # Setting the styles first
    st.markdown('<div class="title-style">SCOPE</div>', unsafe_allow_html=True)  # Then rendering the custom title
    st.markdown('<div class="author-style">Author: Lothar Tjipueja</div>', unsafe_allow_html=True)  # Rendering the author name

    st.title("Inventory Analysis Dashboard")

    uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

    if uploaded_file is not None:
        inventory_data = pd.read_excel(uploaded_file)

        # Dropdowns for selecting Row Ref. No. and Description
        st.write("Select a product by:")
        selected_row_ref = st.selectbox('Row Ref. No.', [None] + inventory_data['Row Ref. No.'].tolist())
        selected_description = st.selectbox('Description', [None] + inventory_data['Description'].tolist())

        # Check which dropdown has been used
        if selected_row_ref:
            selected_data = inventory_data[inventory_data['Row Ref. No.'] == selected_row_ref].iloc[0]
        elif selected_description:
            selected_data = inventory_data[inventory_data['Description'] == selected_description].iloc[0]
        else:
            st.write("Please select a product.")
            return

        # Periods definition
        periods = ['Current Month', 'Month 2', 'Month 3', 'Month 4', 'Month 5', 'Month 6', 'Month 7', 'Month 8', 'Month 9', 'Month 10', 'Month 11', 'Month 12']

        # Create a DataFrame for the line chart
        df_chart = pd.DataFrame({
            'Period': periods,
            'Sales': selected_data[periods].values
        })

        # Calculate the average monthly sales
        avg_sales = df_chart['Sales'].mean()

        

        # Plotting using plotly express for interactive charts
        fig = px.line(df_chart, x='Period', y='Sales', title=f"Sales for {selected_data['Description']}")
        fig.add_scatter(x=df_chart['Period'], y=df_chart['Sales'], mode='markers+text', text=df_chart['Sales'])
        fig.update_traces(texttemplate='%{text}', textposition='top center')

        # Display the chart without the Plotly logo
        st.plotly_chart(fig, config={'displayModeBar': True, 'displaylogo': False})

        # Displaying product details below the chart
        st.write("**Description:**", selected_data['Description'])
        st.write("**Inventory:**", selected_data['Inventory'])
        st.write("**Unit Cost:**", selected_data['Unit Cost'])
        st.write("**Stock Value:**", selected_data['Stock Value'])
        st.write("**Average Monthly Sales:**", avg_sales)  # Display average monthly sales

        hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
        st.markdown(hide_st_style, unsafe_allow_html=True)
        
    else:
        st.write("Please upload an Excel file.")

if __name__ == '__main__':
    inventory_analysis_app()
