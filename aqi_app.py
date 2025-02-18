import streamlit as st
import requests
import matplotlib.pyplot as plt

# Category descriptions
category_descriptions = {
    "good": "Air quality is considered satisfactory.",
    "moderate": "Air quality is acceptable.",
    "unhealthy for sensitive groups": "Members of sensitive groups may experience health effects.",
    "unhealthy": "Everyone may begin to experience health effects.",
    "very unhealthy": "Health warnings of emergency conditions.",
    "hazardous": "Health alert: everyone may experience more serious health effects."
}

source_info = "\nSource: World Air Quality Index Project and originating EPA"

# Function to return category description based on AQI
def category_name(aqi):
    if aqi <= 50:
        return "Good", category_descriptions["good"]
    elif aqi <= 100:
        return "Moderate", category_descriptions["moderate"]
    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups", category_descriptions["unhealthy for sensitive groups"]
    elif aqi <= 200:
        return "Unhealthy", category_descriptions["unhealthy"]
    elif aqi <= 300:
        return "Very Unhealthy", category_descriptions["very unhealthy"]
    else:
        return "Hazardous", category_descriptions["hazardous"]

# Function to fetch AQI data
def check_aqi(city):
    api_key = "33c09fc4c020747411569af6a6f594ced314634a"
    url = f"https://api.waqi.info/feed/{city}/?token={api_key}"
    
    response = requests.get(url)
    json_data = response.json()
    
    if json_data['status'] == 'error':
        return None, None, f"Error: No AQI data found for the specified city: {city}."
    
    aqi = json_data['data']['aqi']
    city_name = json_data['data']['city']['name']
    category, description = category_name(aqi)
    
    return city_name, aqi, f"The Air Quality Index (AQI) in {city_name} is {aqi}, which is {category}.\n{description}{source_info}"

# Function to plot AQI
def plot_aqi(city_name, aqi):
    fig, ax = plt.subplots(figsize=(6, 4))
    
    # Determine color
    if aqi <= 50:
        color = 'green'
    elif aqi <= 100:
        color = 'yellow'
    elif aqi <= 150:
        color = 'orange'
    elif aqi <= 200:
        color = 'red'
    elif aqi <= 300:
        color = 'purple'
    else:
        color = 'brown'
    
    ax.bar(city_name, aqi, color=color)
    ax.set_title(f"AQI for {city_name}")
    ax.set_xlabel("City")
    ax.set_ylabel("AQI")
    
    return fig

# Streamlit UI
st.title("Air Quality Index (AQI) Checker")
city = st.text_input("Enter city name:")

if st.button("Check AQI"):
    if city:
        city_name, aqi, result_text = check_aqi(city)
        
        if aqi is not None:
            st.success(result_text)
            st.pyplot(plot_aqi(city_name, aqi))
        else:
            st.error(result_text)
    else:
        st.warning("Please enter a city name.")
