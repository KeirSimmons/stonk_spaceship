## Intro

I wanted to get this out ASAP, so there's not much documentation, and code is a little messy.

The crux of things: it will track a stonk via yahoo finance, and speak to you about the movement 
via Google Home (speakers) and a light show (Philips Hue). See the `config.json` file for more 
info on what you can edit. If you don't have both of these setup, you should. Sorry, that's all I 
can help with straight away.

You will need the following libraries installed:

```
pip install googlecontroller
pip install qhue
```

In the config file you can change the stonk you want to track via `stonk`. Put in your IP address 
for your Google Home and Hue Bridge plus a username for the latter. If you don't know what this is, 
then go to the Philips developer site and it walks you through it in a couple of minutes.

The lights config allow for grouping (in my example I have two lights for the TV, and one by my 
coffee table). The IDs are found by pinging the Hue service.

If the price changes by more than `alert_on_jump` in either direction, it will notify you (via your 
speakers). If it goes above or below your `alarm` it will also speak to you and play a song :) . It 
will also adjust your alarms by +/- $1 each time this happens.