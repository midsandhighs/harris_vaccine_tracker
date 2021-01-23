# harris_vaccine_tracker

A quick Python script to check the [Harris County Public Health COVID-19 Vaccination program website](https://vacstrac.hctx.net/landing) and send a SMS to a single number indicating whether appointments for eligible individuals are available to be booked.

## Requirements
These instructions / code are intended to run on macOS using the system’s built in process scheduling module, `launchd`. 

For now it is reliant on the user to edit the appropriate files and put them in place on their system. 

Once configured the launchd job will run the script at the assigned times, output to `/tmp/vaxmanage.log`, and use the Twilio-CLI with the proper environment variables to send the message. 
- - - -
# Why don’t you do this in cron?
You can do cron on macOS, but launchd is officially supported and behaves better.
To learn more, checkout:  [launchd.info](https://launchd.info/) 
- - - -
### Environment
	
* **[Twilio Account ](https://www.twilio.com/try-twilio)**
	* The destination number will need to be `Verified` with Twilio so it will receive messages. 
* **Twilio-Cli installed**
	* `brew tap twilio/brew && brew install twilio`
		* configure `twilio.env` with the correct  environment variables
```diff
-twilio.env can contain privileged credential information and should not be committed to any repository or shared with anyone else. 
```
* **Python**
	* `tested against 3.4, 3.6 and 3.9`
	* `requests`
		*  [requests · PyPI](https://pypi.org/project/requests/)
	* `twilio`
		* [twilio · PyPI](https://pypi.org/project/twilio/)
- - - -
### Usage
This tool currently requires knowledge of Python environments on macOS and familiarity with [`launchd`](https://launchd.info), an Apache licensed macOS framework for scheduling almost any task. 
- - - - 
#### Python Script standalone usage
Instructions for running the script manually from your `tty`
* verify the `Twilio-CLI` is properly logged in. 
* `pip install requests && pip install twilio`
* In **vaxstack.py**
	* edit the `sender` and `receiver` variables with the correct phone numbers
	* Needs to include country code, `+1` (US) given as default.

`python3 vaxstack.py`
- - - - 
#### Setting up the script scheduling
Scheduling the script to run as the logged in user at certain intervals.

In `com.harriscountyvax.plist`: 
* Edit **Environment Variables**
	* `TWILIO_ACCOUNT_SID`
		* *account_sid* from twilio.com/console
	* `TWILIO_AUTH_TOKEN`
		* *auth_token* from twilio.com/console
* Edit **Label**
	* *(not required)* change the string from `com.midsandhighs.twilio` to  something of your choosing
		* Make sure to follow [Reverse Domain Naming standards ](https://en.wikipedia.org/wiki/Reverse_domain_name_notation) otherwise there will be many pain points.
* Edit **StartCalendarInterval** and / or **StartInterval** with your own schedule
	* **EXAMPLES:**
		* Run at load, and everyday at 9am.

```
	<key>RunAtLoad</key>
	<true/>
	<key>StartCalendarInterval</key>
	<dict>
		<key>Hour</key>
		<integer>9</integer>
		<key>Minute</key>
		<integer>0</integer>
	</dict>	
```
		
        * Run every hour

```
	<key>StartInterval</key>
	<integer>3600</integer>		
```

	
* For more information, check   [launchd.info](https://launchd.info/)  and head towards the **When to Start** section.

* Edit **ProgramArguments** with the correct paths for the appropriate Python executable & the script itself on your local machine. 
	* I recommend using full canonical paths with no shorthand for the script
		* **DO:** `/Users/midsandhighs/src/vaxtrack.py`
		* **DON’T:**  `~/src/vaxtrack.py`
	* I recommend double, triple, and quadruple checking the paths of your Python executable and where it has been installing modules.  

```diff
+virtual environments are amazing and extremely useful but in my experience they are fragile and difficult to schedule correctly regardles of OS, and macOS is the most difficult in terms of Python version and module maintenance.
```














