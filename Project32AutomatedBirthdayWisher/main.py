import pandas as pd
import smtplib
import random
import datetime as dt

MY_EMAIL = ""
PASSWORD = ""
today = dt.datetime.now()


data = pd.read_csv("birthdays.csv")

birthdays_dict = {
    (row["month"], row["day"]): row
    for(_, row) in data.iterrows()
}

if (today.month, today.day) in birthdays_dict:
    number = random.randint(1, 3)
    person = birthdays_dict[(today.month, today.day)]
    name = person["name"]
    with open(f"letter_templates/letter_{number}.txt", "r") as file:
        letter_content = file.read()
        letter_content = letter_content.replace("[NAME]", name)

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(MY_EMAIL, PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs=person["email"],
                            msg=f"Subject:Happy Birthday!\n\n{letter_content}"
                            )