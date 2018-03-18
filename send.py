import sendgrid
from sendgrid.helpers.mail import *

sg = sendgrid.SendGridAPIClient(apikey="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")
from_email = Email("samtan106@gmail.com")


def send(gp, ig, em="rohan.rodrigues2016@vitstudent.ac.in"):
    to_email = Email(em)
    subject = "Regarding missing children"
    x = open("template.html")
    st = x.read()
    x.close()
    st = st.replace("__img__", str(ig))
    st = st.replace("__gps__", str(gp))
    content = Content("text/html", st)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    return response.status_code
