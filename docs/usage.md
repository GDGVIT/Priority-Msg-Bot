## Usage

First of all, to use this bot duo, you need to add them to your telegram group

**What kind of messages does the bot detect?**

Messages which notify the user about important events/projects/deadlines etc.
Messages like *"The project review for Operating Systems is due this week"* 
or something like *"We have scheduled a meeting on Monday"*

**What does this bot do with these detected messages?**

These messages are encrypted and stored safely in our database
And they can be listed anytime the user wishes to, the user need to use **/show** 
command to list the messages that are being tracked

**What is the reminder feature?**

While listing the message using */show*, there is an option to set a reminder for the message
or ignore it

If you want to be reminded about it, then click on the **Set Reminder** option, the bot
will ask you some additional details like **date** and **time**, after successfully collecting 
these details the bot will store these messages safely and will send you a **recurring reminder** 
starting from **3 days before the deadline**

**How to use the reminder feature?**

Although the bot will start sending a recurring reminder 3 days before the deadline
You can also check the upcoming events using **/remind**

**What format should the date and time be in?**

For dates you can use any format ranging from **dd/mm/yy** to saying **tmrw** ,**next week** or **this wednesday**

However for time you have to mention **am** or **pm** as **9am** or **6 pm**.
