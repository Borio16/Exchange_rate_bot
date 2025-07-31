import requests
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
import smtplib

import requests
from bs4 import BeautifulSoup

def get_exchange_rates():


    url = "https://www.cbe.org.eg/en/economic-research/statistics/exchange-rates"

    # ** tricks firewall into thinking im a user not a bot
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/118.0.5993.70 Safari/537.36"
        )
    }


    # fetches the html from the website, takes to parameters the first one is to go the url provided
    # and the second is to trick the browser into thinking im a user
    # third is to avoid your script hanging forever if the server is slow.
    # Note that this function takes multiple parameters
    response = requests.get(url, headers=headers,timeout=10)


    # If the server gives an error (like 403), return a failure message.
    if response.status_code != 200:
        return f"❌ Failed to load page: {response.status_code}"


    # Parse the HTML into a BeautifulSoup object.
    soup = BeautifulSoup(response.text, "html.parser")

    # Finds the exchange rate table using its class, you have to inspect page and look for the class
    table = soup.find("table", class_="table-comp")

    if not table:
        return "❌ Exchange rate table not found."

    rows = table.find("tbody").find_all("tr")
    lines = []

    for row in rows:
        cols = row.find_all("td")
        if len(cols) == 3:
            currency = cols[0].text.strip()
            buy = round(float(cols[1].text.strip()),2)
            sell = round(float(cols[2].text.strip()),2)
            lines.append(currency + " Buy " + str(buy) + " Sell " + str(sell))

    return "\n".join(lines)



def send_email(subject, body, sender_email, receiver_email, smtp_server, smtp_port, login, password):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())


if __name__ == "__main__":
    rates = get_exchange_rates()
    print(rates)  # optional

    # Replace these with your actual details
    sender = "your-email@gmail.com"
    receiver = "your-email@gmail.com"
    smtp_server = "smtp.gmail.com"
    smtp_port = 465
    login = "your-email@gmail.com"
    password = "your-password"

    send_email("Daily Exchange Rates", rates, sender, receiver, smtp_server, smtp_port, login, password)


