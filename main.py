# Joe McPhail 5/30
import get_weather
from datetime import datetime
import smtplib
from email.message import EmailMessage


def assemble_text():
    coords = {"Home": "38.02,-122.55", "Big Rock": "38.05,-122.62", "Point Reyes (Limantour Parking Lot)": "38.03, -122.88"}
    date = datetime.now().strftime(r'%A, %B %d')
    coords_info = {}
    for i, j in coords.items():
        coords_info[i] = get_weather.sky_forecast(j)
    

    text = f"Good morning! Here is your night sky forecast for {date}.\n\n"  # plaintext email to be returned **MAKE HTML / MIME in the future**

    text += f'~~General Info~~\n'
    gen_info = coords_info["Home"]  # Uses general info (daily high/low, sunset, etc.) from home
    # saves data to variable so I can format it better
    high = round(gen_info['High'])
    low = round(gen_info['Low'])
    moon_illumination = gen_info['Moon Illumination']
    moonrise = gen_info['Moonrise']
    sunset = gen_info['Sunset']
    # chops extra 0 from beginning of moonrise/sunset
    for i in ['moonrise', 'sunset']:
        if i.startswith('0'):
            i = i[1::]
    # now into the main text
    text += f'Today will have a high of {high}° and a low of {low}°\n'
    text += f'Sunset is at {sunset}. The moon will be visible after {moonrise} and have a brightness of {moon_illumination}%\n'
    
    # Location-specific stuff now
    text += "\n~~Locations~~"
    for place, info in coords_info.items():  # looking into the hourly part of that big dict to loop through each hour for info
        text += f'\n{place}:\n'
        for hour, i in info['hourly'].items():
            formatted_hour = f'{hour - 12} PM'
            condition = i['condition']
            cloud_cover = i['cloud']
            vis = i['vis']
            temp = round(i['temp']) # takes away decimal for cleaner temp

            text += f'{formatted_hour}: {temp}° and {condition} ({cloud_cover}% cloud cover, {vis} mi visibility)\n'
    text += '\nHappy Stargazing!'

    return text

def send_email():
    recipients_list = ['psh8ce@virginia.edu']
    sender_credentials = {'email':'jmstarforecast@outlook.com', 'password': 'pythonproject2004'}

    msg = EmailMessage()
    date = datetime.now().strftime(r'%B %d')
    msg['Subject'] = f'Night Sky Forecast - {date}'
    msg['From'] = sender_credentials['email']
    msg['To'] = ', '.join(recipients_list)  # fancy way to add multiple recipients if needed (thanks Barron Stone)
    
    msg_body = assemble_text()
    msg.set_content(msg_body)

    # connect to SMTP server (BIG thank you to Barron Stone)
    with smtplib.SMTP('smtp-mail.outlook.com', 587) as server:
        server.starttls()
        server.login(sender_credentials['email'], sender_credentials['password'])
        server.send_message(msg)
    


if __name__ == "__main__":
    send_email()
    