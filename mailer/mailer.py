import os
import mimetypes
import smtplib

from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_html(recipients, subject, message, sender="", cc=[], bcc=[], files=[]):
    print("sending email through smtp")
    server = 'localhost'
    user = ''
    password = ''

    if len(files) > 0:
        outer = MIMEMultipart()
        outer['Subject'] = subject
        outer['From'] = sender
        outer['To'] = ', '.join(recipients)

        for file in files:
            filename = os.path.basename(file)
            attachment_filename = '.'.join(filename.replace('.', '-').rsplit('-', 1))
            # Guess the content type based on the file's extension.  Encoding
            # will be ignored, although we should check for simple things like
            # gzip'd or compressed files.
            ctype, encoding = mimetypes.guess_type(file)
            if ctype is None or encoding is not None:
                # No guess could be made, or the file is encoded (compressed), so
                # use a generic bag-of-bits type.
                ctype = 'application/octet-stream'
            if encoding == 'gzip':
                ctype = 'application/octet-stream'
            maintype, subtype = ctype.split('/', 1)
            #print(file, filename, ctype, encoding, maintype, subtype)
            if maintype == 'text':
                fp = open(file)
                # Note: we should handle calculating the charset
                msg = MIMEText(fp.read(), _subtype=subtype)
                fp.close()
            elif maintype == 'image':
                fp = open(file, 'rb')
                msg = MIMEImage(fp.read(), _subtype=subtype)
                fp.close()
            elif maintype == 'audio':
                fp = open(file, 'rb')
                msg = MIMEAudio(fp.read(), _subtype=subtype)
                fp.close()
            else:
                fp = open(file, 'rb')
                msg = MIMEBase(maintype, subtype)
                msg.set_payload(fp.read())
                fp.close()
                # Encode the payload using Base64
                encoders.encode_base64(msg)
            # Set the filename parameter
            #msg.add_header('Content-Disposition', 'attachment', filename=filename)
            msg.add_header('Content-Disposition', 'attachment', filename=attachment_filename)
            outer.attach(msg)
        msg = MIMEText(message)
        outer.attach(msg)
        # Now send or store the message
        composed = outer.as_string()
        mail_session = smtplib.SMTP(server)
        mail_session.sendmail(sender, recipients, composed)
        mail_session.quit()


def send_text(recipients, subject, message, sender, server='localhost'):
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)

    mail_session = smtplib.SMTP(server)
    #mail_session.login(user, password)
    mail_session.sendmail(sender, recipients, msg.as_string())
    mail_session.quit()
