import os
import time
from slackclient import SlackClient
from textblob import TextBlob
import sqlite3

# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

AT_BOT = "<@" + BOT_ID + ">"

# instantiate Slack client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

def handle_request(request, channel):
    text = TextBlob(request)
    list_tags = text.tags
    list_pnoun = []
    list_noun = []
    for tag in list_tags:
        if tag[1] == "NNP" or tag[1] == "NNPS":
            list_pnoun.append(tag[0])
        elif tag[1] == "CD":
            list_pnoun.append(tag[0])
        else:
            list_noun.append(tag[0])
    noun = " ".join(list_noun)
    proper_noun = " ".join(list_pnoun)
    #print "Noun:", noun
    #print "Proper Noun:",proper_noun
    query_keywords(noun, str(proper_noun), channel)

def query_keywords(keywords,name, channel):
    db = sqlite3.connect('chatbot.db')
    #print "Connected to DB!"
    cur = db.cursor()
    query = "SELECT clmn,tbl,source FROM data WHERE keywords = '%s';" % keywords.lower()
    result = cur.execute(query)
    #print "Result:", result
    row = cur.fetchone()
    #print "Row:", row
    if row == None:
        response = "I am yet to learn that"
        slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
    else:
        query = "SELECT {} FROM {} WHERE {} = :n".format(row[0], row[1], row[2])
        #print "Query to main table:", query
        if cur.execute(query,{"n":name}) == 0:
            response = "I am yet to learn that"
            slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
        else:    
            res = cur.fetchone()
            for r in res:
                response = r    
                slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
    db.close()

def parse_slack_output(slack_rtm_output):
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
        print "Office Hour Bot connected and running!"
        while True:
            request, channel = parse_slack_output(slack_client.rtm_read())
            if request and channel:
                handle_request(request, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")

