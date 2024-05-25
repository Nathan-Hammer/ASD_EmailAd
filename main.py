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
    sender_email = 'Ruguillio3@gmail.com'  # Replace with your Gmail address
    sender_password = 'nkdr zaal parh jkgk'  # Replace with your Gmail password

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
        .container {{
          width: 100%;
          max-width: 600px;
          margin: 0 auto;
          padding: 20px;
          font-family: Arial, sans-serif;
        }}
        .image-container img {{
          max-width: 100%;
          height: auto;
        }}
      </style>
    </head>
    <body>
      <div class="container">
        <h1>{title}</h1>
        <p>{message}</p>
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
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(email_message)
        print('Email sent successfully!')
    except Exception as e:
        print('An error occurred while sending the email:', str(e))

# Get ad data
ad_data = get_ad_data()
print("Data from server: ", ad_data)

# Prompt the user for input
title = input('Enter the title:  ')
message = input('Enter the message:  ')
recipient = input('Enter the recipient email address: ')

# Send the email with ad data
send_email(title, message, recipient, ad_data)
