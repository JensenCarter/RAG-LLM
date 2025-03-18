import streamlit as st
import pandas as pd
import openai
import pydeck as pdk
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from shapely.geometry import Point, Polygon
from math import radians, sin, cos, sqrt, atan2
import re
import os
# OpenAI API key

client = openai.OpenAI(api_key="KEY-HERE")
staffordshire_polygon = Polygon([
    (-2.1815, 52.9994), (-2.1289, 52.9912), (-2.0432, 52.9658),
    (-1.9519, 52.9333), (-1.8723, 52.8967), (-1.8064, 52.8583),
    (-1.7542, 52.8194), (-1.7153, 52.7811), (-1.6885, 52.7444),
    (-1.6720, 52.7097), (-1.6639, 52.6767), (-1.6624, 52.6448),
    (-1.6660, 52.6134), (-1.6735, 52.5819), (-1.6842, 52.5500),
    (-1.6977, 52.5175), (-1.7141, 52.4847), (-1.7340, 52.4521),
    (-1.7583, 52.4205), (-1.7882, 52.3906), (-1.8245, 52.3631),
    (-1.8677, 52.3385), (-1.9178, 52.3171), (-1.9741, 52.2992),
    (-2.0354, 52.2850), (-2.1001, 52.2743), (-2.1666, 52.2671),
    (-2.2333, 52.2633), (-2.2988, 52.2626), (-2.3621, 52.2647),
    (-2.4225, 52.2695), (-2.4797, 52.2766), (-2.5337, 52.2859),
    (-2.5847, 52.2972), (-2.6330, 52.3104), (-2.6791, 52.3255),
    (-2.7233, 52.3424), (-2.7660, 52.3611), (-2.8074, 52.3817),
    (-2.8476, 52.4041), (-2.8866, 52.4284), (-2.9242, 52.4545),
    (-2.9602, 52.4823), (-2.9942, 52.5118), (-3.0259, 52.5428),
    (-3.0548, 52.5752), (-3.0807, 52.6089), (-3.1034, 52.6437),
    (-3.1227, 52.6794), (-3.1387, 52.7159), (-3.1513, 52.7531),
    (-3.1607, 52.7907), (-3.1670, 52.8287), (-3.1703, 52.8669),
    (-3.1709, 52.9051), (-3.1689, 52.9432), (-3.1645, 52.9810),
    (-3.1579, 53.0184), (-3.1492, 53.0553), (-3.1386, 53.0916),
    (-3.1261, 53.1272), (-3.1118, 53.1620), (-3.0957, 53.1958),
    (-3.0779, 53.2287), (-3.0584, 53.2605), (-3.0372, 53.2912),
    (-3.0143, 53.3207), (-2.9897, 53.3490), (-2.9635, 53.3761),
    (-2.9355, 53.4019), (-2.9059, 53.4264), (-2.8746, 53.4496),
    (-2.8417, 53.4715), (-2.8072, 53.4921), (-2.7713, 53.5113),
    (-2.7340, 53.5292), (-2.6954, 53.5458), (-2.6557, 53.5610),
    (-2.6150, 53.5750), (-2.5734, 53.5876), (-2.5310, 53.5990),
    (-2.4880, 53.6091), (-2.4445, 53.6180), (-2.4006, 53.6257),
    (-2.3565, 53.6322), (-2.3123, 53.6376), (-2.2681, 53.6418),
    (-2.2241, 53.6450), (-2.1803, 53.6471), (-2.1369, 53.6482),
    (-2.0939, 53.6483), (-2.0514, 53.6475), (-2.0095, 53.6457),
    (-1.9683, 53.6431), (-1.9278, 53.6396), (-1.8881, 53.6353),
    (-1.8492, 53.6302), (-1.8111, 53.6244), (-1.7740, 53.6179),
    (-1.7377, 53.6107), (-1.7024, 53.6029), (-1.6680, 53.5945),
    (-1.6346, 53.5855), (-1.6021, 53.5760), (-1.5705, 53.5660),
    (-1.5399, 53.5555), (-1.5102, 53.5446), (-1.4814, 53.5333),
    (-1.4535, 53.5216), (-1.4265, 53.5095), (-1.4004, 53.4971),
    (-1.3751, 53.4844), (-1.3506, 53.4714), (-1.3269, 53.4581),
    (-1.3040, 53.4445), (-1.2818, 53.4307), (-1.2603, 53.4167),
    (-1.2395, 53.4025), (-1.2193, 53.3881), (-1.1998, 53.3735),
    (-1.1809, 53.3588), (-1.1626, 53.3439), (-1.1449, 53.3289),
    (-1.1277, 53.3138), (-1.1111, 53.2985), (-1.0950, 53.2831),
    (-1.0794, 53.2676), (-1.0643, 53.2520), (-1.0497, 53.2363),
    (-1.0355, 53.2206), (-1.0218, 53.2047), (-1.0085, 53.1888),
    (-0.9957, 53.1728), (-0.9833, 53.1568), (-0.9713, 53.1407),
    (-0.9597, 53.1245), (-0.9485, 53.1083), (-0.9377, 53.0921),
    (-0.9273, 53.0758), (-0.9173, 53.0595), (-0.9076, 53.0431),
    (-0.8983, 53.0267), (-0.8894, 53.0103), (-0.8808, 52.9939),
    (-0.8726, 52.9774), (-0.8647, 52.9609), (-0.8572, 52.9444),
    (-0.8500, 52.9279), (-0.8431, 52.9113), (-0.8366, 52.8947),
    (-0.8304, 52.8781), (-0.8245, 52.8615), (-0.8189, 52.8449),
    (-0.8137, 52.8283), (-0.8087, 52.8116), (-0.8041, 52.7949),
    (-0.7998, 52.7783), (-0.7958, 52.7616), (-0.7921, 52.7449),
    (-0.7887, 52.7282), (-0.7856, 52.7115), (-0.7828, 52.6948),
    (-0.7802, 52.6781), (-0.7780, 52.6614), (-0.7760, 52.6447),
    (-0.7743, 52.6280), (-0.7729, 52.6113), (-0.7718, 52.5946),
    (-0.7710, 52.5779), (-0.7704, 52.5612), (-0.7701, 52.5445),
    (-0.7701, 52.5278), (-0.7703, 52.5111), (-0.7708, 52.4944),
    (-0.7716, 52.4777), (-0.7726, 52.4611), (-0.7739, 52.4444),
    (-0.7754, 52.4278), (-0.7772, 52.4112), (-0.7793, 52.3946),
    (-0.7816, 52.3780), (-0.7841, 52.3614), (-0.7869, 52.3448),
    (-0.7900, 52.3283), (-0.7933, 52.3118), (-0.7968, 52.2953),
    (-0.8006, 52.2788), (-0.8046, 52.2623), (-0.8088, 52.2459),
    (-0.8133, 52.2295), (-0.8180, 52.2131), (-0.8230, 52.1968),
    (-0.8282, 52.1805), (-0.8336, 52.1642), (-0.8392, 52.1480),
    (-0.8451, 52.1318), (-0.8512, 52.1156), (-0.8575, 52.0995),
    (-0.8641, 52.0834), (-0.8709, 52.0674), (-0.8779, 52.0514),
    (-0.8851, 52.0354), (-0.8926, 52.0195), (-0.9003, 52.0037),
    (-0.9082, 51.9879), (-0.9163, 51.9721), (-0.9247, 51.9564),
    (-0.9333, 51.9408), (-0.9421, 51.9252), (-0.9511, 51.9097),
    (-0.9604, 51.8942), (-0.9699, 51.8788), (-0.9796, 51.8634),
    (-0.9895, 51.8481), (-1.0000, 51.8328)
])

# Load mental health locations
mental_health_places = []
try:
    with open('mental_health_places.txt', 'r', encoding='utf-8') as f:
        for line in f:
            if ': ' in line:
                try:
                    name, coords = line.strip().split(': ')
                    lat, lon = map(float, coords.split(', '))
                    mental_health_places.append({
                        'name': name,
                        'latitude': lat,
                        'longitude': lon
                    })
                except ValueError as e:
                    st.error(f"Error parsing line: {line.strip()} - {str(e)}")
except FileNotFoundError:
    st.error("Mental health places file not found")
except Exception as e:
    st.error(f"Error loading mental health places: {str(e)}")

# Configure geolocator
geolocator = Nominatim(
    user_agent="healthcare_app/1.0 (contact@example.com)",
    timeout=10
)
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)


@st.cache_data
def load_healthcare_services(file_path):
    healthcare_services = []
    # Read the spreadsheet and cache result
    spreadsheet = pd.ExcelFile(file_path)

    for sheet_name in spreadsheet.sheet_names:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        for index, row in df.iterrows():
            try:
                # Extract service information
                name = row.get('Service Name', '')
                postcode = row.get('Postcode', '')
                if not postcode:
                    continue

                # Geocode the postcode
                location = cached_geocode(postcode)
                if not location:
                    st.error(f"Could not geocode postcode: {postcode}")
                    continue

                healthcare_services.append({
                    'name': name,
                    'postcode': postcode,
                    'latitude': location.latitude,
                    'longitude': location.longitude,
                    'type': sheet_name
                })
            except Exception as e:
                st.error(f"Error processing row {index} in {sheet_name}: {str(e)}")
    # print(healthcare_services)
    return healthcare_services


@st.cache_data
def cached_geocode(postcode):
    return geocode(f"{postcode}, UK")


# Use the cached function to load services:
file_path = 'Spreadsheet.xlsx'
healthcare_services = load_healthcare_services(file_path)


# Spreadsheet processing for AI
def format_data(dataframe, sheet_name, max_rows=50):
    try:
        dataframe = dataframe.head(max_rows)
        headers = "| " + " | ".join(dataframe.columns) + " |"
        separator = "| " + " | ".join(["---"] * len(dataframe.columns)) + " |"
        rows = "\n".join(
            "| " + " | ".join(
                str(cell).replace("\n", " ").strip() if not pd.isna(cell) else "N/A"
                for cell in row
            ) + " |"
            for row in dataframe.values
        )
        return f"### {sheet_name}\n{headers}\n{separator}\n{rows}\n"
    except Exception as e:
        st.error(f"Error formatting {sheet_name} data: {str(e)}")
        return ""


try:
    file_path = 'Spreadsheet.xlsx'
    spreadsheet = pd.ExcelFile(file_path)
    combined_data = "\n".join([
        format_data(pd.read_excel(file_path, sheet_name), sheet_name)
        for sheet_name in spreadsheet.sheet_names
    ])
except FileNotFoundError:
    st.error("Spreadsheet file not found")
except Exception as e:
    st.error(f"Error loading spreadsheet data: {str(e)}")

try:
    combined_data = "\n".join([
        format_data(pd.read_excel(file_path, sheet_name), sheet_name)
        for sheet_name in spreadsheet.sheet_names
    ])
except Exception as e:
    st.error(f"Error loading spreadsheet data: {str(e)}")
    combined_data = ""


def haversine(lat1, lon1, lat2, lon2):
    try:
        R = 3958.8
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c
    except Exception as e:
        st.error(f"Distance calculation error: {str(e)}")
        return None


def is_in_staffordshire(location_str):
    try:
        if not location_str.endswith(", UK"):
            location_str += ", UK"

        location_data = geocode(location_str, exactly_one=True)

        if not location_data:
            if " " in location_str:
                postcode = location_str.split()[-1]
                location_data = geocode(f"{postcode}, UK", exactly_one=True)

            if not location_data:
                st.error("Location not found. Please try a different format")
                return False

        point = Point(location_data.longitude, location_data.latitude)
        st.session_state.user_coords = (location_data.latitude, location_data.longitude)
        return staffordshire_polygon.contains(point)

    except Exception as e:
        st.error(f"Geocoding error: {str(e)}")
        return False


def is_mental_health_query(query):
    keywords = ['mental health', 'crisis', 'suicidal', 'suicide', 'depression',
                'anxiety', 'psychological', 'emotional', 'depressed', 'mentally', 'mental', 'upset', 'feel down', 'sad']
    return any(keyword in query.lower() for keyword in keywords)


# AI response functions
def get_help_staffordshire(query, document, return_service=False):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Updated model
            messages=[
                {"role": "system",
                 "content": "You are a data analyst who interprets tabular data from multiple sheets to answer questions, helping people find the most relevant healthcare service."},
                {"role": "user",
                 "content": f"The following is data from multiple sheets:\n\n{document}\n\n"
                            f"Answer the following question in a simple and age-specific way if needed:\n"
                            f"Question: {query}\n\n"
                            f"At the end of your response, include the exact recommended service name in this format:\n"
                            f"Recommended Service: [SERVICE_NAME]"}
            ],
            temperature=0.3
        )

        ai_response = response.choices[0].message.content

        if return_service:
            match = re.search(r"Recommended Service:\s*(?:\[(.*?)\]|(.*))", ai_response)
            recommended_service = match.group(1) if match and match.group(1) else match.group(
                2).strip() if match else None

            if not recommended_service:
                st.error(
                    "No recommended service extracted from AI response. Please ensure the response contains the required format.")
            return ai_response, recommended_service

        return ai_response

    except Exception as e:
        st.error(f"AI API error: {str(e)}")
        return "Unable to generate response", None if return_service else "Unable to generate response"


def get_help_other_location(query, age):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Updated model
            messages=[
                {"role": "system", "content": "Provide nearest healthcare facilities."},
                {"role": "user",
                 "content": f"Location: {st.session_state.get('location', 'Unknown')}\nAge: {age}\nQuestion: {query}\nGive advice on nearest services specific to their problem and age."}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"AI API error: {str(e)}")
        return "Unable to generate response"


# Streamlit UI
st.title("Healthcare Assistant Chatbot")

# Initialize session state
session_defaults = {
    "location": "Staffordshire",
    "messages": [],
    "age": None,
    "asked_for_age": False,
    "pending_question": None,
    "user_coords": None,
    "map_data": None
}

for key, val in session_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# Main content container
with st.container():
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Display map if available
    if st.session_state.map_data is not None:
        st.subheader("🗺️ Nearby Services Map")
        try:
            scatter_layer = pdk.Layer(
                "ScatterplotLayer",
                data=st.session_state.map_data,
                get_position='[longitude, latitude]',
                get_color='[200, 30, 0, 160]',
                get_radius=30,
                radius_scale=3,
                radius_min_pixels=10,
                radius_max_pixels=20,
                pickable=True,
                stroked=True,
                filled=True,
                auto_highlight=True
            )

            user_layer = pdk.Layer(
                "ScatterplotLayer",
                data=st.session_state.map_data[st.session_state.map_data['name'] == 'Your Location'],
                get_position='[longitude, latitude]',
                get_color='[0, 120, 250, 200]',
                get_radius=30,
                radius_scale=3,
                radius_min_pixels=10,
                radius_max_pixels=20,
                pickable=True
            )

            initial_lat = st.session_state.user_coords[0]
            initial_lon = st.session_state.user_coords[1]
            view_state = pdk.ViewState(
                latitude=initial_lat,
                longitude=initial_lon,
                zoom=12,
                pitch=0,
                bearing=0
            )

            tooltip = {
                "html": "<b>{name}</b>",
                "style": {
                    "backgroundColor": "#1a1a1a",
                    "color": "white",
                    "fontSize": "14px"
                }
            }

            st.pydeck_chart(pdk.Deck(
                map_style='mapbox://styles/mapbox/light-v9',
                initial_view_state=view_state,
                layers=[scatter_layer, user_layer],
                tooltip=tooltip,
                parameters={
                    'layersOpacity': 0.8,
                    'blending': 'additive'
                }
            ))
        except Exception as e:
            st.error(f"Map error: {str(e)}")

# Bottom input section
st.divider()
input_col1, input_col2 = st.columns([2, 3])
with input_col1:
    st.markdown("**📍 Your Location**")
    st.session_state.location = st.text_input(
        "Postcode or town name:",
        st.session_state.location,
        help="Example: ST16 3DP or Staffordshire",
        key="location_input",
        label_visibility="collapsed"
    )
with input_col2:
    st.markdown("**💬 Healthcare Question**")
    user_input = st.chat_input("Type your question here...")
# Process user input
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    try:
        if not st.session_state.asked_for_age:
            st.session_state.pending_question = user_input
            st.session_state.messages.append({
                "role": "assistant",
                "content": "Before I provide a response, could you please tell me your age?"
            })
            st.session_state.asked_for_age = True

        elif st.session_state.asked_for_age and st.session_state.age is None:
            try:
                st.session_state.age = int(user_input)
                is_local = is_in_staffordshire(st.session_state.location)
                if is_local:
                    response, recommended_service = get_help_staffordshire(
                        st.session_state.pending_question, combined_data, return_service=True)

                    if st.session_state.user_coords:
                        user_lat, user_lon = st.session_state.user_coords
                        map_data = []
                        nearby_services = []

                        # Add user location
                        map_data.append({
                            'latitude': user_lat,
                            'longitude': user_lon,
                            'name': 'Your Location'
                        })

                        # Find nearby services
                        if is_mental_health_query(st.session_state.pending_question):
                            for service in mental_health_places:
                                distance = haversine(user_lat, user_lon, service['latitude'], service['longitude'])
                                if distance and distance <= 10:
                                    map_data.append(service)
                                    if distance <= 5 and len(nearby_services) < 5:
                                        nearby_services.append(f"{service['name']} ({distance:.1f} miles)")
                        else:
                            if recommended_service:
                                for service in healthcare_services:
                                    if recommended_service.lower() in service['name'].lower():
                                        distance = haversine(user_lat, user_lon, service['latitude'],
                                                             service['longitude'])
                                        if distance and distance <= 100:
                                            map_data.append(service)
                                            nearby_services.append(f"{service['name']} ({distance:.1f} miles)")
                                            break

                        # Update response and map
                        if nearby_services:
                            response += "\n\n**Recommended Service Locations:**\n- " + "\n- ".join(nearby_services)
                            st.session_state.map_data = pd.DataFrame(map_data)
                        else:
                            response += "\n\n**No nearby locations found for the recommended service.**"

                else:
                    response = get_help_other_location(st.session_state.pending_question, st.session_state.age)

                st.session_state.messages.append({"role": "assistant", "content": response})
                st.session_state.pending_question = None

            except ValueError:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "Please enter a valid age (numbers only)."
                })

        else:
            is_local = is_in_staffordshire(st.session_state.location)
            if is_local:
                response, recommended_service = get_help_staffordshire(user_input, combined_data, return_service=True)
                if st.session_state.user_coords:
                    user_lat, user_lon = st.session_state.user_coords
                    map_data = [{
                        'latitude': user_lat,
                        'longitude': user_lon,
                        'name': 'Your Location'
                    }]
                    nearby_services = []

                    if is_mental_health_query(user_input):
                        for service in mental_health_places:
                            distance = haversine(user_lat, user_lon, service['latitude'], service['longitude'])
                            if distance and distance <= 10:
                                map_data.append(service)
                    else:
                        if recommended_service:
                            for service in healthcare_services:
                                if recommended_service.lower() in service['name'].lower():
                                    distance = haversine(user_lat, user_lon, service['latitude'], service['longitude'])
                                    if distance and distance <= 100:
                                        map_data.append(service)
                                        break

                    st.session_state.map_data = pd.DataFrame(map_data)

                st.session_state.messages.append({"role": "assistant", "content": response})
            else:
                response = get_help_other_location(user_input, st.session_state.age)
                st.session_state.messages.append({"role": "assistant", "content": response})

    except Exception as e:
        st.error(f"Application error: {str(e)}")
        st.session_state.messages.append({
            "role": "assistant",
            "content": "An error occurred processing your request."
        })
    st.rerun()
