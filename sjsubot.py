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

def query_keywords(keywords,name, channel):
    db = sqlite3.connect('chatbot.db')

    cur = db.cursor()
    result = cur.execute('SELECT clmn,tbl,source FROM data WHERE keywords = :k', {"k":keywords})
    row = cur.fetchone()
    if row == None:
        response = "I am yet to learn that"
        slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
    else:
        query = "SELECT {} FROM {} WHERE {} = :n".format(row[0], row[1], row[2])
        cur.execute(query,{"n":name})
        res = cur.fetchone()
        if res == None:
            response = "I am yet to learn that"
            slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
        else:    
            for r in res:
                response = r    
                slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
    db.close()

def handle_words(request, channel):
    text = TextBlob(request)
    list_tags = text.tags
    list_pnoun = []
    list_noun = []
    for el in list_tags:
        if el[1] == "NNP" or el[1] == "NNPS":
            list_pnoun.append(el[0])
        elif el[1] == "NN":
             list_noun.append(el[0])
        elif el[1] == "CD":
             list_pnoun.append(el[0])
    noun = " ".join( list_noun)
    proper_noun = " ".join(list_pnoun)
    query_keywords(noun,str(proper_noun), channel)

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
