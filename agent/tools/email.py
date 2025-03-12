import smtplib

def contact(senders_email:str, message:str):
    """
    Send an email to No Loop Tech from a given sender with a given message.
    
    Parameters:
    senders_email (str): The email address of the sender.
    message (str): The message to be sent.
    
    Returns:
    str: A success message if the email is sent, otherwise the exception message.
    """
    
    try:
        """# creates SMTP session
        s = smtplib.SMTP('smtp.gmail.com', 587)
        # start TLS for security
        s.starttls()
        # Authentication
        s.login("pinildissanayka@gmail.com", "Dissanayaka.1")
        # sending the mail
        s.sendmail(senders_email, "pinildissanayka@gmail.com" , message)
        # terminating the session
        s.quit()"""
        
        print("Mail sent successfully")    
    except Exception as e:
        return e