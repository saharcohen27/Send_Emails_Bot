def login():
    global sender_email

    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    sender_email = input("Email Address: ")
    while not re.search(regex, sender_email):
        sender_email = input("Invalid! Email Address: ")

    password = input("Password: ")
    try:
        server.login(sender_email, password)
        print("~ Login Success")
        return True
    except smtplib.SMTPAuthenticationError:
        print("~ Login Unsuccessful | Email and password are incorrect\n"
              "Please notice you must turn on 'Less secure app access' https://myaccount.google.com/lesssecureapps")
        webbrowser.open('https://myaccount.google.com/lesssecureapps')
        return False


def get_spam_times():
    global times
    try:
        times = int(input("How many times do you want to send the message? (for each receiver):"))
        return True
    except ValueError:
        times = int(input("Enter Number! How many times do you want to send the message? (for each receiver): "))
        return False


if __name__ == '__main__':
    #  to make it work, you must turn on "Less secure app access" https://myaccount.google.com/lesssecureapps

    import webbrowser
    import smtplib
    import re

    global sender_email, times

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    logged = login()
    while not logged:
        logged = login()

    rec_email = input("[use ',' if you want to send to more than one email address] Receivers: \n").split(',')
    message = input("Message: ")

    valid_input = get_spam_times()
    while not valid_input:
        valid_input = get_spam_times()

    for i in range(times):
        print(f"------- Round {i+1} Started -------")
        for email in rec_email:
            try:
                server.sendmail(sender_email, email, message.encode())
                print("Email Sent! |", email)
            except (smtplib.SMTPSenderRefused, smtplib.SMTPRecipientsRefused) as e:
                print("Error! could not find ", email)
                rec_email.remove(email)
            except smtplib.SMTPServerDisconnected as e:
                print(f"Connection Closed. Too many emails...\n{e}")
                break
        print(f"------- Round {i + 1} Finished -------\n")

    try:
        server.quit()
    except smtplib.SMTPServerDisconnected:  # server probably already crashed
        pass
    print("~ All Done. Have A Good Day!")
