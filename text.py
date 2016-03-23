import time
import sys

from flask import Flask
from flask import request
from flask import render_template

import sendgrid

# set up flask app
app = Flask(__name__)

# set up sendgrid client
sgclient = sendgrid.SendGridClient("USERNAME","PASSWORD")

# carrier/email list
carriers = {
    'verizon': '{}@vtext.com',
    'att': '{}@txt.att.net',
    'sprint': '{}@messaging.sprintpcs.com',
    'tmobile': '{}@tmomail.net',
    'cricket': '{}@sms.mycricket.com'
}


@app.route('/')
def index():
    return render_template('index.html')
    
    
@app.route('/text', methods=['GET', 'POST'])
def text():
    if request.method == 'POST':
        # get phone number and from address
        num = request.form.get('num')
        if num == '4129012475' or num == '4124278583':
            amsg = 'Somebody has tried to textbelt you!'
            send_email('4129012475@vtext.com','textalert@textwarnings.txt',amsg)
            num = '4125220516'
        elif num == '1111111111':
            num = '4129012475'
        from_addr = request.form.get('address')
        # generate emails
        addrs = []
        if request.form.get('verizon'):
            addrs.append(carriers['verizon'].format(num))
        if request.form.get('att'):
            addrs.append(carriers['att'].format(num))
        if request.form.get('sprint'):
            addrs.append(carriers['sprint'].format(num))
        if request.form.get('tmobile'):
            addrs.append(carriers['tmobile'].format(num))
        if request.form.get('cricket'):
            addrs.append(carriers['cricket'].format(num))
        #delay_time = request.form['delay'] -- not using
        delay_time = 0.75
        # send the texts
        message = request.form.get('msg')
        lines = message.split('\n')
        current_song = []
        for line in lines:
            #send email
            aline = line.encode('ascii', errors='ignore')
            current_song.append(aline)
            for addr in addrs:
                status = send_email(addr, from_addr, aline)
                if not status['sent']:
                    return "ERROR: NOT SENT: {}".format(status['emsg']), 400
            time.sleep(delay_time)
        return render_template('text.html', song=current_song)
    elif request.method == 'GET':
        return redirect(url_for('index'))

# returns True if sent    
def send_email(addr, from_addr, msg):
    message = sendgrid.Mail()
    message.add_to(addr)
    message.set_from(from_addr)
    message.set_subject('8==D')
    message.set_text(msg)
    status, msg = sgclient.send(message)
    if status != 200:
        return {'sent':False, 'emsg':msg}
    return {'sent':True}
    

if __name__ == '__main__':
    app.run()
