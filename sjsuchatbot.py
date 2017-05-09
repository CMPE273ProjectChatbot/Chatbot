import os
import time
from slackclient import SlackClient
import sqlite3
from textblob import TextBlob

# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"
 

conn = sqlite3.connect('chatbot.db')
# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

def get_response(row,name,channel):
    db = sqlite3.connect('chatbot.db')

    cur = db.cursor()
    query = "SELECT {} FROM {} WHERE {} = :n".format(row[0], row[1], row[2])
    cur.execute(query,{"n":name})
    res = cur.fetchall()
    if res == []:
        response = "I am yet to learn that"
        slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)

    elif res > 0:
        if row[0] == "location, section":
            for r in res:
                str(r[0])
                int(r[1])
                a = str(r[1])
                a.split(".")
                response = "Section " + a[0:len(a)-2] + " is in " + r[0]
                slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
        elif row[0] ==  "section, class_day, class_time":
            for r in res:
                str(r[1])
                int(r[0])
                str(r[2])
                a = str(r[0])
                a.split(".")
                response = "Section " + a[0:len(a)-2] + " schedule is " + r[1] + " " + r[2]
                slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
        elif row[0] == "seats, section":
            for r in res:
                str(r[0])
                int(r[1])
                a = str(r[1])
                a.split(".")
                response = "Section " + a[0:len(a)-2] + " has " + r[0] + " seats."
                slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
        else:
            for r in res[0]:
                response = r    
                slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
            
    else:
        response = res   
        slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
    db.close()

def query_keywords(req,keywords,name, channel):
    db = sqlite3.connect('chatbot.db')

    cur = db.cursor()
    result = cur.execute('SELECT clmn,tbl,source FROM data WHERE keywords = :k', {"k":keywords})
    row = cur.fetchone()
    if row == None:
        result = cur.execute('SELECT clmn,tbl,source FROM data WHERE keywords = :k', {"k":req})
        row = cur.fetchone()
        if row == None:
            response = "I am yet to learn that"
            slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
        else:
            get_response(row,name,channel)
    else:
        get_response(row,name,channel)
    db.close()


def handle_multireq(req,noun,proper_noun,channel):
    nounlist=" ".join(["name","professor", "instructor"])
    if noun in nounlist:
        db = sqlite3.connect('chatbot.db')
        cur = db.cursor()
        cur.execute('INSERT INTO temp (noun, pnoun) VALUES (:n,:p)',{"n":noun, "p":proper_noun})
        db.commit()
        db.close()
        
        response = "which section are you looking for ?"
        slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)

    else:
        query_keywords(req,noun,str(proper_noun), channel)



def handle_section(value,channel):
    db = sqlite3.connect('chatbot.db')
    cur = db.cursor()
    result = cur.execute('SELECT * FROM temp')
    row = cur.fetchone()
    if row == None:
        response = "I am yet to learn that"
        slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
    else:
        name=row[1]
        key=row[0]
        re=cur.execute('DELETE FROM temp')
        db.commit()
        result = cur.execute('SELECT clmn,tbl,source FROM data WHERE keywords = :k', {"k":key})
        row = cur.fetchone()
        if row == None:
            response = "I am yet to learn that"
            slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
        else:
            query = "SELECT {} FROM {} WHERE {} = :n AND SECTION= :v".format(row[0], row[1], row[2])
            cur.execute(query,{"n":name,"v":value})
            res = cur.fetchone()
            if res == None:
                response = "I am yet to learn that"
                slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
            else:
                for r in res:
                    response = r
                    slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
        db.close()
    db.close()



def handle_words(request, channel):
    text1 = TextBlob(request)
    list_pnoun = []
    list_noun = []
    list_req = []
    for el in text1.tags:
        if el[1] == "NNP" or el[1] == "NNPS" or el[1] == "CD":
            list_pnoun.append(el[0])
        else: 
            list_req.append(el[0])
    req = " ".join(list_req)
    proper_noun = " ".join(list_pnoun)
    text2 = TextBlob(req)
    for elem in text2.tags:
        if elem[1] == "NN":
            list_noun.append(elem[0])
    noun = " ".join(list_noun)

    if proper_noun.isdigit():
        value = int(proper_noun)
        handle_section(value,channel)
    else:
        handle_multireq(req,noun,proper_noun,channel)

def handle_request(request, channel):
    db = sqlite3.connect('chatbot.db')
    cur = db.cursor()
    result = cur.execute('SELECT res FROM greet WHERE req = :k', {"k":request.lower()})
    res = cur.fetchone()
    if res == None :
        db.close()
        handle_words(request, channel)
    else:
            
        response = res[0]        
        slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
        db.close()
    

def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip(), \
                       output['channel']
    return None, None

if __name__ == "__main__":
    
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print "SJSUBot connected and running!"
        while True:
            request, channel = parse_slack_output(slack_client.rtm_read())
            if request and channel:
                handle_request(request, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
