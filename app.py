import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response
from firebase import firebase
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r





def makeWebhookResult(req):
    global speech
    from firebase import firebase

    if req.get("result").get("action") == "input.welcome":
        timestamp = req.get("timestamp")
        timestamp = timestamp[:10]
        name = req.get("result").get("parameters").get("Name")
        print(name)
        phone_number = req.get("result").get("parameters").get("PhoneNumber")
        print(phone_number)
        email = req.get("result").get("parameters").get("email")

        Subject = req.get("result").get("parameters").get("course")
        Subject = Subject.lower()
        print(Subject)
        #from firebase import firebase




        firebase = firebase.FirebaseApplication('https://edubot-91d09.firebaseio.com/', None)
        firebase.put("userProfiles/{}".format(timestamp), "{}".format(phone_number),
                     {"Name": name, "Phone-Number": phone_number,"email": email, "Subject": Subject})
        fromaddr = "riju.banerjee93@gmail.com"
        toaddr = firebase.get("https://edubot-91d09.firebaseio.com/userProfiles/{}/{}/".format(timestamp,phone_number), "email")
        print(toaddr)
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Course Details Attached"
        body = "Hi {},\n \n PFB the details of the course, you did a query for.\n \n Thanks and regards,\n ExcelR Team".format(name.upper())
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login("riju.banerjee93@gmail.com", "moto@riju93")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        speech = firebase.get("https://edubot-91d09.firebaseio.com/{}".format(Subject), "overview")


    elif req.get("result").get("action") == "user.query":
        Subject = req.get("result").get("contexts")[0].get("parameters").get("course")
        Subject = Subject.lower()

        firebase = firebase.FirebaseApplication('https://edubot-91d09.firebaseio.com/', None)
        speech = firebase.get("https://edubot-91d09.firebaseio.com/{}".format(Subject),"overview")
        print(speech)

    elif req.get("result").get("action") == "what.price":


        Subject = req.get("result").get("parameters").get("course")
        Subject = Subject.lower()
        print(Subject)

        firebase = firebase.FirebaseApplication('https://edubot-91d09.firebaseio.com/', None)
        speech = firebase.get("https://edubot-91d09.firebaseio.com/{}".format(Subject),"price")

    elif req.get("result").get("action") == "trainer":

        Subject = req.get("result").get("parameters").get("course")
        Subject = Subject.lower()
        print(Subject)

        firebase = firebase.FirebaseApplication('https://edubot-91d09.firebaseio.com/', None)
        speech = firebase.get("https://edubot-91d09.firebaseio.com/{}".format(Subject), "trainer")

    elif req.get("result").get("action") == "course.details":

        Subject = req.get("result").get("parameters").get("course")
        Subject = Subject.lower()
        print(Subject)

        firebase = firebase.FirebaseApplication('https://edubot-91d09.firebaseio.com/', None)
        speech = firebase.get("https://edubot-91d09.firebaseio.com/{}".format(Subject), "course details")

    elif req.get("result").get("action") == "certification.provided":

        Subject = req.get("result").get("parameters").get("course")
        Subject = Subject.lower()
        print(Subject)

        firebase = firebase.FirebaseApplication('https://edubot-91d09.firebaseio.com/', None)
        speech = firebase.get("https://edubot-91d09.firebaseio.com/{}".format(Subject), "certification")

    elif req.get("result").get("action") == "followup.certification":

        Subject = req.get("result").get("contexts")[0].get("parameters").get("course")
        Subject = Subject.lower()
        print(Subject)

        firebase = firebase.FirebaseApplication('https://edubot-91d09.firebaseio.com/', None)
        speech = firebase.get("https://edubot-91d09.firebaseio.com/{}".format(Subject), "certification")

    elif req.get("result").get("action") == "followup.course.details":
        Subject = req.get("result").get("contexts")[0].get("parameters").get("course")
        Subject = Subject.lower()
        print(Subject)

        firebase = firebase.FirebaseApplication('https://edubot-91d09.firebaseio.com/', None)
        speech = firebase.get("https://edubot-91d09.firebaseio.com/{}/course details".format(Subject), None)

    elif req.get("result").get("action") == "followup.price":
        Subject = req.get("result").get("contexts")[0].get("parameters").get("course")
        Subject = Subject.lower()
        print(Subject)

        firebase = firebase.FirebaseApplication('https://edubot-91d09.firebaseio.com/', None)
        speech = firebase.get("https://edubot-91d09.firebaseio.com/{}".format(Subject), "price")
    elif req.get("result").get("action") == "followupprice.followupprice-custom":
        Subject = req.get("result").get("contexts")[0].get("parameters").get("course")
        Subject = Subject.lower()
        print(Subject)

        firebase = firebase.FirebaseApplication('https://edubot-91d09.firebaseio.com/', None)
        speech = firebase.get("https://edubot-91d09.firebaseio.com/{}".format(Subject), "price")


    elif req.get("result").get("action") == "followup.trainer":
        Subject = req.get("result").get("contexts")[0].get("parameters").get("course")
        Subject = Subject.lower()
        print(Subject)

        firebase = firebase.FirebaseApplication('https://edubot-91d09.firebaseio.com/', None)
        speech = firebase.get("https://edubot-91d09.firebaseio.com/{}".format(Subject), "trainer")

    elif req.get("result").get("action") == "any.prerequisites":

        Subject = req.get("result").get("parameters").get("course")
        Subject = Subject.lower()
        firebase = firebase.FirebaseApplication('https://edubot-91d09.firebaseio.com/', None)
        speech = firebase.get("https://edubot-91d09.firebaseio.com/{}".format(Subject), "eligibility")

    elif req.get("result").get("action") == "followup.eligibility":
        Subject = req.get("result").get("contexts")[0].get("parameters").get("course")
        Subject = Subject.lower()
        print(Subject)

        firebase = firebase.FirebaseApplication('https://edubot-91d09.firebaseio.com/', None)
        speech = firebase.get("https://edubot-91d09.firebaseio.com/{}".format(Subject), "eligibility")

    elif req.get("result").get("action") == "training.duration":
        Subject = req.get("result").get("parameters").get("course")
        Subject = Subject.lower()
        mode = req.get("result").get("parameters").get("mode")
        mode = mode.lower()
        modeDays = req.get("result").get("parameters").get("modeDays")
        modeDays = modeDays.lower()
        print(modeDays)

        firebase = firebase.FirebaseApplication('https://edubot-91d09.firebaseio.com/', None)
        speech = firebase.get("https://edubot-91d09.firebaseio.com/{}/duration/{}/{}".format(Subject,mode,modeDays), None)

    elif req.get("result").get("action") == "followup.training.duration":
        Subject = req.get("result").get("contexts")[0].get("parameters").get("course")
        Subject = Subject.lower()
        mode = req.get("result").get("parameters").get("mode")
        mode = mode.lower()
        modeDays = req.get("result").get("parameters").get("modeDays")
        modeDays = modeDays.lower()
        print(modeDays)

        firebase = firebase.FirebaseApplication('https://edubot-91d09.firebaseio.com/', None)
        speech = firebase.get("https://edubot-91d09.firebaseio.com/{}/duration/{}/{}".format(Subject, mode, modeDays),
                              None)

    elif req.get("result").get("action") == "followup.followup.duration":
        Subject = req.get("result").get("contexts")[0].get("parameters").get("course")
        Subject = Subject.lower()
        mode = req.get("result").get("parameters").get("mode")
        mode = mode.lower()
        modeDays = req.get("result").get("contexts")[0].get("parameters").get("modeDays")
        modeDays = modeDays.lower()
        firebase = firebase.FirebaseApplication('https://edubot-91d09.firebaseio.com/', None)
        speech = firebase.get("https://edubot-91d09.firebaseio.com/{}/duration/{}/{}".format(Subject, mode, modeDays),
                              None)
    elif req.get("result").get("action") == "followup.class_online_availability":
        Subject = req.get("result").get("contexts")[0].get("parameters").get("course")
        Subject = Subject.lower()
        mode = req.get("result").get("parameters").get("mode")
        mode = mode.lower()
        firebase = firebase.FirebaseApplication('https://edubot-91d09.firebaseio.com/', None)
        speech = firebase.get("https://edubot-91d09.firebaseio.com/{}/availability/{}".format(Subject, mode),
                              None)

    elif req.get("result").get("action") == "followup.available_modes_of_training":
        Subject = req.get("result").get("contexts")[0].get("parameters").get("course")
        Subject = Subject.lower()
        firebase = firebase.FirebaseApplication('https://edubot-91d09.firebaseio.com/', None)
        speech = firebase.get("https://edubot-91d09.firebaseio.com/{}/available modes of training".format(Subject),
                              None)

    elif req.get("result").get("action") == "availablemodesoftraining.availablemodesoftraining-custom":
        Subject = req.get("result").get("parameters").get("course")
        Subject = Subject.lower()
        firebase = firebase.FirebaseApplication('https://edubot-91d09.firebaseio.com/', None)
        speech = firebase.get("https://edubot-91d09.firebaseio.com/{}/available modes of training".format(Subject),
                              None)
    elif req.get("result").get("action") == "asking.address":
        Location = req.get("result").get("parameters").get("location")
        Location = Location.lower()
        available_city = ["bangalore","hyderabad"]
        if Location in available_city:
            firebase = firebase.FirebaseApplication('https://edubot-91d09.firebaseio.com/', None)
            speech = firebase.get("https://edubot-91d09.firebaseio.com/address/{}".format(Location), None)
        else:
            speech ="We don't have our training centre in {}".format(Location)

    elif req.get("result").get("action") == "available.modes.of.training":
        Subject = req.get("result").get("parameters").get("course")
        Subject = Subject.lower()
        firebase = firebase.FirebaseApplication('https://edubot-91d09.firebaseio.com/', None)
        speech = firebase.get("https://edubot-91d09.firebaseio.com/{}/available modes of training".format(Subject),
                              None)
    elif req.get("result").get("action") == "available_modes_of_training.followup":
        mode = req.get("result").get("parameters").get("mode")
        mode = mode.lower()
        Subject = req.get("result").get("contexts")[0].get("parameters").get("course")
        Subject = Subject.lower()
        firebase = firebase.FirebaseApplication('https://edubot-91d09.firebaseio.com/', None)
        speech = firebase.get("https://edubot-91d09.firebaseio.com/{}/availability/{}".format(Subject,mode),
                              None)























    return {
        "speech": speech,
        "displayText": speech,
        "source": "nothing"
    }






























if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')