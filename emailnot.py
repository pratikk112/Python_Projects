import streamlit as st
import base64
import smtplib
import io
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

st.title("Email Sender")

# Function to send an email with/without an image
def send_email(from_email, password, to_email, subject, message, image_file=None, send_with_image=True):
    try:
        # Create email message
        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = subject

        if send_with_image and image_file is not None:
            # Read image and convert to base64
            img_bytes = io.BytesIO(image_file.read())
            encoded_string = base64.b64encode(img_bytes.getvalue()).decode()

            # HTML email with embedded image
            body = f"""
            <p>{message}</p>
            <img src="data:image/png;base64,{encoded_string}">
            """
            msg.attach(MIMEText(body, "html"))
        else:
            # Plain text email
            msg.attach(MIMEText(message, "plain"))

        # Send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:  # Use correct SMTP
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
subject = st.text_input("Subject", "Hello")
message = st.text_area("Message", "This is a test email.")
image_file = st.file_uploader("Upload an Image (Optional)", type=["png", "jpg", "jpeg"])

# Option to send with or without an image
send_with_image = st.radio("Send Mode", ["Message Only", "Message with Image"]) == "Message with Image"

if st.button("Send Email"):
    send_email(from_email, password, to_email, subject, message, image_file, send_with_image)
