import requests
from bs4 import BeautifulSoup
from twilio.rest import Client
import secrets

# Twilio
TWILIO_SID = secrets.twilio_sid
TWILIO_TOKEN = secrets.twilio_token
NUMERO_TWILIO = secrets.number
NUMERO_DA_CHIAMARE = secrets.cecche_number
TWILIO = Client(TWILIO_SID, TWILIO_TOKEN)


# Function to send the message on Telegram
def telegram_bot_sendtext(bot_message):
    bot_token = secrets.bot_token
    bot_chat_id = secrets.bot_chat_id_cecche
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chat_id + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()


def call():
    TWILIO.calls.create(
        twiml='<Response><Say voice="alice" language="it-IT">MUOVITI CECCHE!</Say></Response>',
        to=NUMERO_DA_CHIAMARE,
        from_=NUMERO_TWILIO)


if __name__ == '__main__':
    not_available = True

    # Run the program until the product is available
    while not_available:
        urls = ["https://www.amazon.it/dp/B08HN4DSTC", "https://www.amazon.fr/dp/B08HN4DSTC", "https://www.amazon.es/dp/B08HN4DSTC", "https://www.amazon.de/dp/B08HN4DSTC"]
        countries = ["Amazon.it", "Amazon.fr", "Amazon.es", "Amazon.de"]
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}

        # time.sleep(0.5 * random.random())

        for i in range(len(urls)):
            if not_available:

                # Open the session
                s = requests.session()
                r = s.get(urls[i], headers=headers)
                r.cookies.clear()
                page_html = r.text

                # Scraping the html page
                soup = BeautifulSoup(page_html, features="lxml")

                # checking if there is "Out of stock" on a first possible position of html page.
                try:
                    soup.select('#availability .a-color-state')[0].get_text().strip()
                    stock = str(countries[i]) + ': Out of Stock'
                except:
                    # checking if there is "Out of stock" on a second possible position of html page.
                    try:
                        soup.select('#availability .a-color-price')[0].get_text().strip()
                        stock = str(countries[i]) + ': Out of Stock'
                    except:
                        # checking if there is "Available" on html page.
                        try:
                            soup.select('#availability .a-color-success')[0].get_text().strip()
                            stock = str(countries[i]) + ': Available'
                        # Error due to amazon anti-scraping.
                        except:
                            stock = str(countries[i]) + ': Errore di richiesta'

                # If the product is available, send a Telegram message and play an mp3 file.
                if "Available" in stock:
                    print("Buy")
                    test = telegram_bot_sendtext(urls[i])
                    call()
                    not_available = False