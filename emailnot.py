import streamlit as st
import pyautogui
import base64
import smtplib
import io
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

st.title("Screenshot Emailer")

# Function to capture screenshot and send email
def screenshot_and_send_email(from_email, password, to_email, subject):
    try:
        # Capture the screenshot in memory
        screenshot = pyautogui.screenshot()
        img_bytes = io.BytesIO()
        screenshot.save(img_bytes, format="PNG")
        encoded_string = base64.b64encode(img_bytes.getvalue()).decode()

        # Prepare the email
        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = subject

        body = f'<img src="data:image/png;base64,{encoded_string}">'
        msg.attach(MIMEText(body, "html"))

        # Send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:  # Use proper SMTP server
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, to_email, msg.as_string())

        st.success("Email sent successfully!")

    except Exception as e:
        st.error(f"Error: {str(e)}")

# Streamlit UI Inputs
from_email = st.text_input("Your Email", "your_email@example.com")
password = st.text_input("Your Password", type="password")
to_email = st.text_input("Recipient Email", "admin@example.com")
subject = st.text_input("Subject", "Screenshot")

if st.button("Take Screenshot and Send Email"):
    screenshot_and_send_email(from_email, password, to_email, subject)
