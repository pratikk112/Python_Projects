import streamlit as st
import pyautogui
import base64
import smtplib
import io
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

st.title("Screenshot Emailer")

# Get user inputs securely
from_email = st.text_input("Your Email", "your_email@example.com")
password = st.text_input("Your Password", type="password")
to_email = st.text_input("Recipient Email", "admin@example.com")
subject = st.text_input("Subject", "Screenshot")

if st.button("Take Screenshot and Send Email"):
    try:
        # Capture the screenshot in memory
        screenshot = pyautogui.screenshot()
        img_bytes = io.BytesIO()
        screenshot.save(img_bytes, format="PNG")
        encoded_string = base64.b64encode(img_bytes.getvalue()).decode()

        # Send email
        def send_email(encoded_image):
            try:
                msg = MIMEMultipart()
                msg["From"] = from_email
                msg["To"] = to_email
                msg["Subject"] = subject

                body = f'<img src="data:image/png;base64,{encoded_image}">'
                msg.attach(MIMEText(body, "html"))

                # Use a proper SMTP server (e.g., Gmail)
                with smtplib.SMTP("smtp.gmail.com", 587) as server:
                    server.starttls()
                    server.login(from_email, password)
                    server.sendmail(from_email, to_email, msg.as_string())

                st.success("Email sent successfully!")
            except Exception as e:
                st.error(f"Error: {str(e)}")

        send_email(encoded_string)

    except Exception as e:
        st.error(f"Screenshot Error: {str(e)}")
