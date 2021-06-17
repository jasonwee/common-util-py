#!/usr/bin/python

#import mailer
#mailer.gmail_send_text()
#mailer.gmail_send_html()
#mailer.mail_send_text()
#mailer.mail_send_html()

import cli
(output, error) = cli.run('echo hi')
print(output)
print(error)
