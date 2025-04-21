import streamlit as st

st.title("Unit Conveter App")

st.markdown("### Convert Weights, Length and Time Instantly")

st.write("Select the unit type, enter the value, and get instant conversions.")



category = st.selectbox("Chooose a category", ["Time", "Length", "Weight"])


def convert_unit(category, value, unit):
    if category == "Time":
        if unit == "Seconds to minutes":
            return value / 60
        elif unit == "Minutes to seconds":
            return value * 60
        elif unit == "Minutes to hours":
            return value / 60
        elif unit == "Hours to Minutes":
            return value * 60
        elif unit == "Hours to days":
            return value / 24
        elif unit == "Days to hous":
            return value * 60
        

    if category == "Length":
        if unit == "Kilometers to miles":
            return value * 0.621371
        elif unit == "Miles to Kilometers":
            return value /  0.621371
    

    if category == "Weight":
        if unit == "Kilogramsto pounds":
            return value * 2.20462
        elif unit == "Pounds to Kilograms":
            return value / 2.20462
    return 0

if category == "Length":
    unit = st.selectbox("📏 Select Conversation", ["Miles to kiloeter", "Kilometers to miles" ])
 
elif category == "Weight":
    unit = st.selectbox("⚖ Select Conversation", ["Kilograms to pounds", "Pounds to kilograms"])

elif category == "Time":
    unit = st.selectbox("⏰ Select Conversation", ["Seconds to minutes", "minutes to seconds", "Minutes to hours", "Hours to minutes", "Hours to days", "Days to hours"])


value = st.number_input("Enter the value to convert")

if st.button("Convert"):
    result = convert_unit(category, value, unit)
    st.success(f"the result is {result:.2f}")