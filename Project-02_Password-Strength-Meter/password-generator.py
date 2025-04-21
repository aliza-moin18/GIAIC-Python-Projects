import streamlit as st                     
import random
import string

def password_generator(length, use_digits, use_special_charcter):
    characters = string.ascii_letters

    if use_digits:                              
        characters += string.digits               

    if use_special_charcter:
        characters += string.punctuation

    return''.join(random.choice(characters) for _ in range(length))


st.title("🔐 Password Strenght Meter & Generator")

option = st.radio("👇 Choose an option", ["Check Password Strength", "Generate Password"])


# Password Strength 

def check_password_strength(password):
    score = 0

    # length    
    if len(password) >= 8:
        score += 1
    else:
        st.write("❌ Password should be at least 8 characters long.")

    # Upper & lower Case  
    if any(char.isupper() for char in password) and any(char.islower() for char in password):
        score += 1
    else:
        st.write("❌ Include both uppercase & lowercase letters")    

    # Digit case    
    if any(char.isdigit() for char in password):
        score += 1
    else:
        st.write("❌ Add atleast one number (0-9)")

    # Check Special character 
    if any(char in string.punctuation for char in password):
        score += 1
    else:
        st.write("❌ Include at least one special character (!@#$%^&*).")    


# Strength Rating

    if score == 4:
        st.write("✅ **Strong Password! 🔥**")

    elif score == 3:
        st.write("⚠️ **Moderate Password - Consider adding more security features.**")

    elif score == 2:
        st.write("❌ **Weak Password - Improve it using the suggestions above.**")

    return score


# Handling Options

if option == "Check Password Strength":
    user_password = st.text_input("🔑 Enter your password")
    if st.button("🔍 Check Strength"):
        check_password_strength(user_password)


if option == "Generate Password":
    length = st.slider("Select Password length", max_value=32, min_value=6, value=12)
    use_digits = st.checkbox("Include digits")
    use_special_charcter = st.checkbox("Include Special Character")

    if st.button("Generate password"):
        password = password_generator(length, use_digits, use_special_charcter)
        st.write(f"Generate password: `{password}`")


st.write("--------------------------------------------------------")
st.markdown("<h5 style= 'text-align: center;'> Built with ❤ by Aliza Moin </h5>", unsafe_allow_html=True)