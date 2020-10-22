import yagmail

#yagmail.register('username', 'password')

def sendEmail(df):
    """Send email if there are new apartments added to the database"""
    if len(df) > 0:
        yag = yagmail.SMTP('bolignotification')

        to = 'youremail@gmail.com'
        subject = 'New Apartment Alert'
        body = 'List of new apartments:'
        html = df.to_html().replace("\n", "")
        yag.send(to=to, subject=subject, contents=[body, html])
        print('Email sent')
    else:
        print("No new apartments")




