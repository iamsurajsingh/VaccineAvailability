# Import Libraries
import requests
import json
import time
import datetime
import smtplib, ssl

# Define Constants
# Do remember to remove <> while entering data. Only "" allowed below.
PINCODE = "<Enter Pin Code here>"  # Enter Pin Code here
MY_EMAIL = "<Sender's Email Address>"  # Sender's Email Id
MY_PASSWORD = "<Sender's Email pwd>"  # Sender's email password

# Derive the date and url
# url source is Cowin API - https://apisetu.gov.in/public/api/cowin
today = time.strftime("%d/%m/%Y")
url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={PINCODE}&date={today}"

# Write a loop which checks for every 1000 seconds
while True:
    # Start a session
    with requests.session() as session:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
        response = session.get(url, headers=headers)

        # Receive the response
        response = response.json()
        for center in response['centers']:
            for session in center['sessions']:

                # For Age not equal to 45 and capacity is above zero
                if (session['min_age_limit'] != 45) & (session['available_capacity'] > 0):
                    print("Mail Sent")  # Added to notify when the mail is sent.
                    message_string = f"Subject: {today}'s Vaccination Alert'!! \n\n Available Vaccine - {session['available_capacity']} at {center['name']} on {session['date']} for the age {session['min_age_limit']}"
                    context = ssl.create_default_context()
                    # Configure GMAIL settings
                    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                        connection.starttls()
                        connection.login(MY_EMAIL, MY_PASSWORD)
                        connection.sendmail(
                            from_addr=MY_EMAIL,
                            to_addrs=["<Receiver's Email Address>"],
                            # for multiple receipients, add another email id after a comma in the list
                            msg=message_string
                        )

        time.sleep(10)      # time duration(in ms) to fetch each hit on the website. I suggest not to increase.