# OPMstatus_bot
A Reddit bot that checks the Washington, DC OPM status and posts to /r/WashingtonDC as /u/OPMstatus_bot. Deployed via Heroku.

# What does this do?
See above. The bot checks [OPM](https://www.opm.gov/policy-data-oversight/snow-dismissal-procedures/current-status/) every 15 seconds and posts to the subreddit...

```python
if (operatingStatus != "Open") and ((dateStatusPosted != previousDateStatusPosted) or (operatingStatus != previousOperatingStatus)):
```

# Why would I want to use this?
You could reconfigure this for your own city's subreddit. You could also use this as a general framework for building a Reddit bot.

# What's missing?
In order to deploy this successfully, you'll need to create a `credentials.py` file that holds the following:

```python
username = "YourRedditBotUsername"
password = "YourRedditBotPassword"
client_id = "YourClientID"
client_secret = "YourClientSecret"
user_agent = "WhateverYouWantAsUserAgent"
```

# How do I deploy?
After you've created your bot's username and created and properly filled out the `credentials.py` file...

 1. [Set up](https://devcenter.heroku.com/articles/getting-started-with-nodejs#set-up) Heroku
 2. Open a local command shell or terminal in the directory
 3. `heroku create`
 4. `git push heroku master`
 5. `heroku ps:scale bot=1`
 6. Check the logs with `heroku logs --tail`
