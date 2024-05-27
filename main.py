import streamlit as st
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random

# Function to get ad data
def get_ad_data():
    url = 'https://ad.simaneka.com/api/get'
    headers = {'authorisation': 'oK8T7ocigzWnY0RGNv5UzfBx33GSEFa5'}
    ad_types = ['Vertical Strip', 'Thick Vertical', 'Thick Horizontal', 'Light Square', 'Horizontal Strip']
    selected_ad_type = random.choice(ad_types)
    tags = ('food,nutrition,blog,fashion,car,automotive,music,party,sports,news,travel,education,agriculture,'
            'technology,health,fitness,finance,beauty,home,lifestyle,parenting,pets,environment,science,real estate,'
            'marketing,entertainment,gaming,relationships,career,art,photography,diy,recipes,outdoor,history,books,'
            'movies,television,gadgets,personal development,spirituality,holidays')
    data = {
        'type': selected_ad_type,
        'tags': tags
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json()

# Modified send_email function to accept ad data
def send_email(title, message, recipient, ad_data=None):
    # Email configuration
    sender_email = 'asddemo4project@gmail.com'  # Replace with your Gmail address
    sender_password = 'bkxs uqlq pxzo qpbl'  # Replace with your Gmail password

    # Create the email message
    email_message = MIMEMultipart('alternative')
    email_message['Subject'] = title
    email_message['From'] = sender_email
    email_message['To'] = recipient

    # Create the HTML content of the email
    html_content = f'''
    <!DOCTYPE html>
    <html>
    <head>
      <style>
        body {{ background-color: white; }}
       .container {{ background-color: lightblue; padding: 20px; border-radius: 10px; }}
       .image-container {{ margin-top: 20px; }}
      </style>
    </head>
    <body>
      <div class="container">
        <h1 style="color: darkblue;">{title}</h1>
        <p style="color: darkblue;">{message}</p>
        <div class="image-container">
          <!-- Placeholder for the ad image -->
        </div>
      </div>
    </body>
    </html>
    '''
    
    # Check if ad_data contains link and href, and insert it into the HTML content
    if ad_data and 'link' in ad_data and 'href' in ad_data:
        ad_image_url = ad_data['link']
        ad_link = ad_data['href']
        html_content = html_content.replace('<!-- Placeholder for the ad image -->', f'<a href="{ad_link}"><img src="{ad_image_url}" alt="{ad_data.get("alt", "Advertisement Image")}"></a>')
    else:
        html_content = html_content.replace('<!-- Placeholder for the ad image -->', '<img src="https://example.com/default-ad-image.jpg" alt="Advertisement Image">')  # Use a default image URL if no ad image is available

    # Attach the HTML content to the email
    email_message.attach(MIMEText(html_content, 'html'))

    # Send the email
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient, email_message.as_string())
    except Exception as e:
        print(f'An error occurred while sending the email: {str(e)}')
        print(f'Detailed error: {e}')  # Log the detailed error

# Streamlit UI
st.title('Send Ad Data Email')
title = st.text_input('Enter the title:')
message = st.text_area('Enter the message:')
recipient = st.text_input('Enter the recipient email address:')

if st.button('Send Email'):
    ad_data = get_ad_data()
    send_email(title, message, recipient, ad_data)
