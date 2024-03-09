import streamlit as st
from src.inference import get_prediction

#Initialise session state variable
if 'input_features' not in st.session_state:
    st.session_state['input_features'] = {}

def app_sidebar():
    st.sidebar.header('Cars Detail')
    
    Age = st.sidebar.text_input('Car Age', key='Age_input')
    KM = st.sidebar.text_input('Car Distance', key='KM_input')
    Fueltype_options = ['Diesel','Petrol','CNG']
    Fueltype = st.sidebar.selectbox("Fueltype_options", Fueltype_options)
    HP = st.sidebar.text_input('Car HP',key='HP_input')
    MetColor = st.sidebar.text_input('MetColor, Input: 0 or 1', key='Color_input')
    Automatic = st.sidebar.text_input('Automatic, Input: 0 or 1', key='Auto_input')
    CC = st.sidebar.text_input('Car CC', key='CC_input')
    Doors = st.sidebar.text_input('Doors Number', key='Doors_input')
    Weight = st.sidebar.text_input('Cars Weight', key='Weight_input')
    
    def get_input_features():
        input_features = {'Age': Age,
                          'KM': KM,
                          'FuelType': Fueltype,
                          'HP':  HP,
                          'MetColor': MetColor,
                          'Automatic': Automatic,
                          'CC': CC,
                          'Doors': Doors,
                          'Weight': Weight
                         }
        return input_features
    
    sdb_col1, sdb_col2 = st.sidebar.columns(2)
    with sdb_col1:
        predict_button = st.sidebar.button("Assess", key="predict")
    with sdb_col2:
        reset_button = st.sidebar.button("Reset", key="clear")
    if predict_button:
        st.session_state['input_features'] = get_input_features()
    if reset_button:
        st.session_state['input_features'] = {}
    return None

def app_body():
    title = '<p style="font-family:arial, sans-serif; color:Black; font-size: 40px;"><b> Welcome to DSSI Car Price Prediction</b></p>'
    st.markdown(title, unsafe_allow_html=True)
    st.image(r"C:\Users\s1270693\Downloads\0309Workshop\Cars.png", use_column_width=True)
    default_msg = '**System assessment says:** {}'
    if st.session_state['input_features']:
        assessment = get_prediction(Age=st.session_state['input_features']['Age'],
                                    KM=st.session_state['input_features']['KM'],
                                    FuelType=st.session_state['input_features']['FuelType'],
                                    HP=st.session_state['input_features']['HP'],
                                    MetColor=st.session_state['input_features']['MetColor'],
                                    Automatic=st.session_state['input_features']['Automatic'],
                                    CC=st.session_state['input_features']['CC'],
                                    Doors=st.session_state['input_features']['Doors'],
                                    Weight=st.session_state['input_features']['Weight']
                                    )
        
        st.success(default_msg.format(assessment))
    return None

def main():
    app_sidebar()
    app_body()
    return None

if __name__ == "__main__":
    main()
