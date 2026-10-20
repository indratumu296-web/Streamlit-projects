import streamlit as st

st.title("Weather API Demo")
API_KEY = st.secrets.get("API_KEY", "demo_key")
city = st.text_input("Enter city", "Chennai")

if st.button("Get Weather"):
	# Simulated response (replace with a real API request as needed).
	# url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
	# resp = requests.get(url).json()
	resp = {
		"city": city,
		"temperature": 30,
		"condition": "Sunny",
		"humidity": 65,
	}

	st.json(resp)
	c1, c2, c3 = st.columns(3)
	c1.metric("Temperature", f"{resp['temperature']}°C")
	c2.metric("Condition", resp["condition"])
	c3.metric("Humidity", f"{resp['humidity']}%")

st.markdown("---")
st.subheader("HTTP Methods")
st.markdown("""
- **GET** - Retrieve data
- **POST** - Send data
- **PUT** - Update data
- **DELETE** - Delete data
""")