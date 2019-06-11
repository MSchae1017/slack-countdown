#!/usr/bin/python
from flask.ext.script import Manager
from flask import Flask
from datetime import datetime
import json
import os
import requests
import workdays

app = Flask(__name__)


manager = Manager(app)

"""Creates web app to be deployed on Heroku."""

SLACK_URL = os.environ.get('SLACK_URL')
if not SLACK_URL:
    print("Missing environment variable SLACK_URL")
    exit(1)

def days_from_christmas():
    """Calculates the number of days between the current date and the next 
    Christmas. Returns the string to displayed.
    """
    currentdate = datetime.now()
    christmas = datetime(datetime.today().year, 12, 25)
    if christmas < currentdate:
        christmas = date(datetime.today().year + 1, 12, 25)
    delta = christmas - currentdate
    days = delta.days
    if days == 1:
        return "%d day from the nearest Christmas" % days
    else:
        return "%d days from the nearest Christmas" % days


def days_from_date(strdate, business_days):
    """ Returns the number of days between strdate and today. Add one to date
    as date caclulate is relative to time
    """
    currentdate = datetime.today()
    futuredate = datetime.strptime(strdate, '%Y-%m-%d')
    if business_days:
        delta = workdays.networkdays(currentdate, futuredate)
    else:
        delta = (futuredate - currentdate).days + 1
    return delta

    
def events(strdate, event, business_days):
    """ Returns string to be displayed with the event mentioned. Sends an error
    if date is incorrect
    """
    days = days_from_date(strdate, business_days)
    day_qualifier = ""
    if business_days:
        day_qualifier = "business "
    assert (days >= -2), "Date needs to be in the future"
    if days == -1:
        return "%d %sday since %s" % (1, day_qualifier, event)
    elif days == -2:
        return "%d %sdays since %s" % (2, day_qualifier, event)
    elif days == 1:
        return "%d %sday until %s" % (days, day_qualifier, event)
    else:
        return "%d %sdays until %s" % (days, day_qualifier, event)


def date_only(strdate, business_days):
    """ Returns string to be displayed. Sends error message if date is
    in the past
    """
    days = days_from_date(strdate)
    day_qualifier = ""
    if business_days:
        day_qualifier = "business "
    assert (days >= -2), "Date needs to be in the future"
    futuredate = datetime.strptime(strdate, '%Y-%m-%d')
    if days == -1:
        return "%d %sday since %s" % (1, day_qualifier, futuredate.strftime("%d %B, %Y"))
    if days == -2:
        return "%d %sdays since %s" % (days, day_qualifier, futuredate.strftime("%d %B, %Y")) 
    if days == 1:
        return "%d %sday until %s" % (days, day_qualifier, futuredate.strftime("%d %B, %Y")) 
    else:
        return "%d %sdays until %s" % (days, day_qualifier, futuredate.strftime("%d %B, %Y"))
    


def post(out, days_left):
    """ Posts a request to the slack webhook. Payload can be customized
    so the message in slack is customized. The variable out is the text 
    to be displayed.
    """    
    if days_left:
           
        images = [#1
                  "", 
                  #2
                  "", 
                  #3
                  "", 
                  #4
                  "", 
                  #5
                  "", 
                  #6
                  "", 
                  #7
                  "", 
                  #8
                  "", 
                  #9
                  "", 
                  #10
                  "", 
                  #11
                  "", 
                  #12
                  "", 
                  #13
                  "", 
                  #14
                  "", 
                  #15
                  "", 
                  #16
                  "", 
                  #17
                  "", 
                  #18
                  "", 
                  #19
                  "", 
                  #20
                  "", 
                  #21
                  "", 
                  #22
                  "", 
                  #23
                  "", 
                  #24
                  "", 
                  #25
                  "", 
                  #26
                  "", 
                  #27
                  "", 
                  #28
                  "", 
                  #29
                  "", 
                  #30
                  "", 
                  #31
                  "", 
                  #32
                  "", 
                  #33
                  "", 
                  #34
                  "", 
                  #35
                  "", 
                  #36
                  "", 
                  #37
                  "", 
                  #38
                  "", 
                  #39
                  "", 
                  #40
                  "", 
                  #41
                  "", 
                  #42
                  "", 
                  #43
                  "", 
                  #44
                  "", 
                  #45
                  "", 
                  #46
                  "", 
                  #47
                  "", 
                  #48
                  "", 
                  #49
                  "",
                  #50
                  "", 
                  #51
                  "", 
                  #52
                  "", 
                  #53
                  "", 
                  #54
                  "", 
                  #55
                  "", 
                  #56
                  "", 
                  #57
                  "", 
                  #58
                  "", 
                  #59
                  "",
                  #60
                  "", 
                  #61
                  "", 
                  #62
                  "", 
                  #63
                  "", 
                  #64
                  "", 
                  #65
                  "", 
                  #66
                  "http://www.soconsports.com/pics31/1024/HQ/HQPPHOFVIWADLXP.20100805163708.jpg", 
                  #67
                  "https://usattci.files.wordpress.com/2019/01/albert-huggins.jpg?w=1000&h=600&crop=1", 
                  #68
                  "http://www3.pictures.zimbio.com/gi/David+Beasley+Clemson+v+Ohio+State+RwYygnTZYAql.jpg", 
                  #69
                  "https://farm1.static.flickr.com/322/32270065921_b3f6720893_b.jpg",
                  #70
                  "data:image/jpeg;base64,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", 
                  #71
                  "https://media.gettyimages.com/photos/jack-maddox-of-the-clemson-tigers-walks-off-the-field-after-his-teams-picture-id1079293414", 
                  #72
                  "https://i3.tigernet.com/stories/11/football/walker_landon_front-250.jpg",
                  #73
                  "https://clemsonpaws.com/wp-content/uploads/2016/07/Tremayne-Anchrum.jpg", 
                  #74
                  "https://bloximages.newyork1.vip.townnews.com/postandcourier.com/content/tncms/assets/v3/editorial/3/1e/31e09354-eb31-11e7-91a4-dfcab8482f44/5a43e22e7907d.image.jpg?resize=1200%2C1329", 
                  #75
                  "https://images2.minutemediacdn.com/image/upload/c_fill,w_912,h_516,f_auto,q_auto,g_auto/shape/cover/sport/cfp-national-championship-5bdde43404bc97a939000008.jpg", 
                  #76
                  "https://usattci.files.wordpress.com/2017/01/sean-pollard.jpg?w=1000&h=600&crop=1", 
                  #77
                  "https://nbccollegefootballtalk.files.wordpress.com/2019/01/gettyimages-1067333440-e1548777834805.jpg?w=610&h=343&crop=1", 
                  #78
                  "https://c8.alamy.com/comp/F87R19/clemson-offensive-lineman-eric-mac-lain-78-during-the-acc-college-F87R19.jpg", 
                  #79
                  "https://i3.tigernet.com/stories/18/football/carman_jackson_handsup_800-479.jpg", 
                  #80
                  "https://bloximages.newyork1.vip.townnews.com/postandcourier.com/content/tncms/assets/v3/editorial/8/89/8890b512-9019-11e7-9574-73a4610b6a14/59ab0e23c1250.image.jpg?resize=400%2C287", 
                  #81
                  "https://editorial01.shutterstock.com/wm-preview-1500/7688279eq/dd2198ba/playoff-fiesta-bowl-football-glendale-usa-shutterstock-editorial-7688279eq.jpg", 
                  #82
                  "https://c8.alamy.com/comp/R09NWR/clemson-south-carolina-usa-03rd-nov-2018-clemson-tigers-wide-receiver-will-brown-82-before-the-ncaa-college-football-game-between-louisville-and-clemson-on-saturday-november-3-2018-at-memorial-stadium-in-clemson-sc-jacob-kupfermancsm-credit-cal-sport-mediaalamy-live-news-R09NWR.jpg", 
                  #83
                  "https://lh6.googleusercontent.com/-nzZLAbeSkJI/UIgjZwvm6qI/AAAAAAABT1E/hJbp3YIwl6c/s1600/TNT_7222.jpg", 
                  #84
                  "", 
                  #85
                  "", 
                  #86
                  "", 
                  #87
                  "", 
                  #88
                  "", 
                  #89
                  "", 
                  #90
                  "", 
                  #91
                  "", 
                  #92
                  "", 
                  #93
                  "", 
                  #94
                  "", 
                  #95
                  "", 
                  #96
                  "", 
                  #97
                  "", 
                  #98
                  "",
                  #99
                  ""
                 ]
        
        img_url = images[days_left - 1]
                  
        payload = {
            "attachments": [
                {   
                    "title": "COUNTDOWN!",
                    "text": out,
                    "color": "#F66733",
                    "image_url": img_url
                }
            ]
        }
    else:
        payload = {
            "attachments": [
                {   
                    "title": "COUNTDOWN!",
                    "text": out,
                    "color": "#F66733"
                }
            ]
        }
    
    r = requests.post(SLACK_URL, data=json.dumps(payload))


def post_error():
    """Sends error message in Slack to alert the user
    about the incorrect date argument
    """
    
    payload = {
        "attachments": [
            {
                "title": "Error",
                "text": ("Date entered must be in the future. "
                        "\n Go to the <https://heroku.com|Heroku Scheduler> for you app and edit"
                        " the command"),
                        "color": "#525162"
            }
        ]
    }
    
    r = requests.post(SLACK_URL, data=json.dumps(payload))
 

@manager.option("-d", "--deadline", dest="date",
                      help="Specify the deadline in ISO format: yyyy-mm-dd", 
                      metavar="DEADLINE")
@manager.option("-e", "--event", dest="event", 
                      help="Name of the deadline event",metavar="EVENT")
@manager.option("-b", "--business-days", dest="business_days", action="store_true", 
                      help="Give the count of business days only")
def deadline(date, event, business_days):
    """ Method takes two optional arguments. Displays in slack channel
    the number of days till the event. If no arguments are given,
    the number of days till Christmas is displayed.
    """    
    try:
        result = ""
        if date:
            if event:
                result = events(date, event, business_days)
            else:
                result = date_only(date, business_days)
        else:
            result = days_from_christmas()
    except:
        post_error()
    else:
        days_left = days_from_date(date, business_days)
        if days_left > 0 and days_left < 100:
            post(result, days_left)
        else:
            post(result)
        


@manager.command
def initiate():
    payload = { "text": "App is now connected to your Slack Channel."}
    r = requests.post(SLACK_URL, data=json.dumps(payload))
    
    

    
if __name__ == "__main__":
    manager.run()


