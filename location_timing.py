import os
import time
from slackclient import SlackClient
from textblob import TextBlob
import sqlite3


# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

count = 0


def handle_command(command, channel):

    text = TextBlob(command)
    list_tags = text.tags
    list_pnoun = []
    list_noun = []
    for el in list_tags:
        if el[1] == "NNP" or el[1] == "NNPS":
            list_pnoun.append(el[0])
        elif el[1] == "CD":
            list_pnoun.append(el[0])
        else:
            list_noun.append(el[0])
    noun = " ".join(list_noun)
    proper_noun = " ".join(list_pnoun)
    #print noun
    #print proper_noun
    query_keywords(noun, str(proper_noun), channel)
    db = sqlite3.connect('chatbot.db')

def query_keywords(keywords,name, channel):
    db = sqlite3.connect('chatbot.db')
    cur = db.cursor()
    result = cur.execute('SELECT clmn, tbl, source FROM data WHERE keywords = :k', {"k":keywords})
    row = cur.fetchone()
    if row == None:
        response = "I am yet to learn that"
        slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
    else:
        query = 'SELECT {} FROM {} WHERE {} = :n'.format(row[0], row[1], row[2])
        cur.execute(query, {"n":name})
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
                    #print r[0]
                    #print r[1]
                    response = "Section " + a[0:len(a)-2] + " is in " + r[0]
                    slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
            elif row[0] ==  "section, class_day, class_time":
                for r in res:
                    str(r[1])
                    int(r[0])
                    str(r[2])
                    a = str(r[0])
                    a.split(".")
                    #print r[0]
                    #print r[1]
                    #print r[2]
                    response = "Section " + a[0:len(a)-2] + " schedule is " + r[1] + " " + r[2]
                    slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
        else:
            response = res 
            slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
    db.close()

def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                return output['text'].split(AT_BOT)[1].strip(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print "ProjectBot connected and running!"
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())

            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print "Connection failed. Invalid Slack token or bot ID?"