import streamlit as st
import pandas as pd
import plotly.express as px

def inventory_analysis_app():

    st.set_page_config(page_icon='💎')
    
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
    body {
        margin: 0 !important;
    }
    
    .main {
        padding-top: 70px !important; 
    }
    
    .title-style {
        font-family: 'Lucida Handwriting', cursive;
        font-size: 60px;
        font-weight: bold;
        text-align: center;
        width: 100%;
        z-index: 1000;
    }

    .author-style {
        font-size: 20px;
        text-align: center;
        font-family: 'Sans-Serif';
        width: 100%;
        margin-top: -10px;
        z-index: 1000;
    }
</style>
"""

    st.markdown(title_style, unsafe_allow_html=True)
    st.markdown('<div class="title-style">SCOPE</div>', unsafe_allow_html=True)
    st.markdown('<div class="author-style">Author: Lothar Tjipueja</div>', unsafe_allow_html=True)
    st.title("Inventory Analysis Dashboard")

    # Session state setup for button press memory
    if 'button_pressed' not in st.session_state:
        st.session_state.button_pressed = False

    if st.session_state.button_pressed or st.button("📉 Load Inventory Analysis Matrix"):
        uploaded_file = "Inventory Analysis Matrix (1).xlsx"
        st.session_state.button_pressed = True
    else:
        uploaded_file = st.file_uploader("Or, upload your Excel file", type=["xlsx"])

    if uploaded_file:
        inventory_data = pd.read_excel(uploaded_file)
        
        st.write("Select a product by:")
        selected_row_ref = st.selectbox('Row Ref. No.', [None] + inventory_data['Row Ref. No.'].tolist())
        selected_description = st.selectbox('Description', [None] + inventory_data['Description'].tolist())

        if selected_row_ref:
            selected_data = inventory_data[inventory_data['Row Ref. No.'] == selected_row_ref].iloc[0]
        elif selected_description:
            selected_data = inventory_data[inventory_data['Description'] == selected_description].iloc[0]
        else:
            st.write("Please select a product.")
            return

        periods = ['Current Month', 'Month 2', 'Month 3', 'Month 4', 'Month 5', 'Month 6', 'Month 7', 'Month 8', 'Month 9', 'Month 10', 'Month 11', 'Month 12']
        df_chart = pd.DataFrame({
            'Period': periods,
            'Sales': selected_data[periods].values
        })
        avg_sales = df_chart['Sales'].mean()

        fig = px.line(df_chart, x='Period', y='Sales', title=f"Sales for {selected_data['Description']}")
        fig.add_scatter(x=df_chart['Period'], y=df_chart['Sales'], mode='markers+text', text=df_chart['Sales'])
        fig.update_traces(texttemplate='%{text}', textposition='top center')
        st.plotly_chart(fig, config={'displayModeBar': True, 'displaylogo': False})

        st.write("**Description:**", selected_data['Description'])
        st.write("**Inventory:**", selected_data['Inventory'])
        st.write("**Unit Cost:**", selected_data['Unit Cost'])
        st.write("**Stock Value:**", selected_data['Stock Value'])
        st.write("**Average Monthly Sales:**", avg_sales)

    else:
        st.write("Please load an Excel file.")

if __name__ == '__main__':
    inventory_analysis_app()
