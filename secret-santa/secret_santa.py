#!/usr/bin/env python3.8

import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import ssl
from email.message import EmailMessage
import random
import itertools


# settings for email using fake account secretsanta.forlol@gmail.com
port = 465
#password = input("Password for email: ")
fake_email = "?????????????"
password = "????????"

# Create a secure SSL context
server = "smtp.gmail.com"
context = ssl.create_default_context()

email_list = ["????????????"]

name_list = ["????????????"]

done = False
while(not done):
    
    new_name_list = random.sample(name_list, len(name_list))

    zipped = list(zip(name_list, new_name_list)) 

    # avoid tuples with same name
    different = True
    for el in zipped:
        if el[0] == el[1]:
            different = False
            break
            
    if different:
        done = True

with smtplib.SMTP_SSL(server, port, context=context) as server:
    server.login(fake_email, password)

    i = 0 # just to know which name take

    for email, name in zip(email_list, new_name_list):
        print(f'[+] Sending email to {email}')

        # send email

        # buil message
        msg = MIMEMultipart()
        msg['Subject'] = "Secret Santa"
        msg['From'] = fake_email
        msg["To"] = email
        
        santa = name_list[i] # retrieve the name from the list

        # insert the image embedded in html
        html = """\
        <html>
        <head></head>
            <body>
            <img src="cid:image1"><br>         
            </body>
        </html>
        """
        # Record the MIME types of text/html.
        part2 = MIMEText(html, 'html')

        # Attach parts into message container.
        msg.attach(part2)


        fp = open('secret_santa.jpg', 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()

        # Define the image's ID as referenced above
        msgImage.add_header('Content-ID', '<image1>')
        msg.attach(msgImage)

        # custom message
        
        msgText = MIMEText(f'\nCiao {santa},\n\nSarai il Babbo Natale Segreto di {name}!\n\nGrazie per fare il mio lavoro :)\n\nOh Oh Oh, see ya!\n\n\nBabbo Natale\n\nP.S. Babbo Natale, men che meno segreto, non esiste.', 'plain' )
        msg.attach(msgText)
        server.send_message(msg)

        i += 1

    server.quit()

print("[+] Done!")
