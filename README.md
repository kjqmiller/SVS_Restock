# svs-restock - Script to check for subwoofer restock
## Introduction
`svs_restock.py` is a script that uses BeautifulSoup to scrape the SVS Outlet website to check for a restock of a specific product. It runs on Amazon Web Services (AWS) Lambda once a day via an AWS EventBridge trigger. If the product is in stock it will send a text using Twilio with a link to it, otherwise it will send a text informing the recipient that it is still out of stock.

## Why?
I developed this project because I wanted to:
  * Create a web scraper using BeautifulSoup
  * Get more experience using AWS Lambda and creating deployment packages
  * Be able to know when a specific product I want is back in stock because it's a good deal on there and I don't want to miss out on a restock because I forgot to check one day

## Technologies
  * Python 3.9
  * BeautifulSoup 4.10
  * Twilio 7.4
  * AWS Lambda
  * AWS EventBridge

## `svs_restock.py`
`svs_restock.py` contains the `Handler` function called by AWS Lambda. The function takes two parameters, both set to `None` as there is nothing passed to it. 

Inside `Handler` we set up Twilio by providing our Account SID and Auth Token, these are essentially a username/password that Twilio uses to identify the account the request is coming from.

Next we set up BeautifulSoup by using `requests.get()` to store the response of our GET request and the `.content` method to store the content of the response. Then we pass `content` and `html.parser` to `BeautifulSoup()` allowing us to navigate the document as a `BeautifulSoup` object.

Lastly we set up our search parameters, as well as a URL that will be concatenated to the front of the product URL upon a successful search.

Then we use BeautifulSoup to scrape all product cards from the outlet page, and search through each one for an H3 that matches our product search. If a match is found, we grab the URL from the href. We then construct a full URL by concatenating the product url and the website url. This full URL then sent via SMS, using Twilio, to the recipient informing them of a restock. If no match is found though, a SMS is sent letting them know the product is still out of stock.

## Setup
The two main things you need to run this program are a [Twilio](https://www.twilio.com/try-twilio) account and an [AWS](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/) account.
### Twilio setup
After creating a Twilio account you can follow Step 1 to get your Account SID and Auth Token. Continue with Step 2 and get your starter code by clicking "Read Quickstart doc" and selecting your preferred language, in this case I used Python. 

In the code snippet on the right, you do not need `import os` on line 1 or `os.environ[]` on lines 8 and 9 but do keep the string inside the brackets as this is where you will have your Account SID and Auth Token. You can also get rid of the `print()` statement at the end on line 19. Finally, you will replace the `from_` variable with your Twilio number, and the `to` variable with the recipient number. See `svs_restock.py` to see how it is used in this application.

### AWS Setup
After following the guide to create an free tier account go to the AWS Management Console and search for "Lambda". Now that you are at the Lambda console you will create a new function, select "Author from scratch", giving it a relevant name, a runtime of Python 3.9 (as of this writing), and an architecture of "x86_64".

Once created, we need to host our code on AWS S3 in a deployment package. To create a deployment package you need your script and all dependencies listed in `requirements.txt` in a folder together. **IMPORTANT** AWS Lambda uses a Linux runtime so all of your dependencies must Linux compatable. If any are not compatable you can by find them by seaching [PyPi](https://pypi.org/) and downoading ones with filenames ending in `x86_64.whl` or `none-any.whl` and unzipping in the deployment folder. Once all dependencies are unzipped you can zip them and your script together by `cd`ing into the deployment folder and using the terminal command `zip -r deployment_package.zip .` to create a `.zip` file that will be uploaded to S3.

Now that you have your deployment package, go back to the AWS Management Console and search for S3. Once in the S3 Management Console create a bucket and give it a name. Leave settings as default and create the bucket. Now that you have a bucket go to "Upload" > "Add files" and select your deployment package. After it uploads go to the package object and copy the "Object URL". Go back to your Lambda function and under "Code" select "Upload from" > "S3 location", paste the URL into it, and save. Now your deployment package is stored in S3 and accessed by Lambda, check that everything is working by going to "Test" on your function page and using the defaults. You should get a "Success" message, if not you will get an error messsage stating what went wrong.

Finally, we have to automate the process, go to your function and at the top of the page click on "+ Add trigger" and select EventBridge from the dropdown. Create a new rule with a name, optional description, and schedule expression using a Cron expression. Make sure your expression includes at least one "?", and if it does not accept it try surrounding it with `cron()`. Keep in mind that Cron expressions use UTC time so you may need to do some converting.
