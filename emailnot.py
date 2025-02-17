import streamlit as st
import pyautogui 
import base64
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText

st.title("Screenshot Emailer")

# Get user inputs
from_email = st.text_input("Your Email", "your_email@example.com")
password = st.text_input("Your Password", type="password")
to_email = st.text_input("Recipient Email", "admin@example.com")
subject = st.text_input("Subject", "Screenshot")

if st.button("Take Screenshot and Send Email"):
    # Capture the screenshot 
    screenshot = pyautogui.screenshot() 
    screenshot.save("screenshot.png")

    # Convert the screenshot to Base64
    with open("screenshot.png", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

# Send the email
def send_email(encoded_image):
    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject

    body = f'<img src="data:image/png;base64,{encoded_image}">'
    msg.attach(MIMEText(body, "html"))

    with smtplib.SMTP("smtp.example.com", 587) as server:  # Replace with your SMTP server and port
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        st.success("Email sent successfully!")

send_email(encoded_string)
