lettuce-selenium
================

**@author**: Anthony Wang

**@description**: lettuce-seleium webdriver testing for realestate.com.au and sendgrid.com

**Pre-reqs:**

* cygwin (tested under cygwin with firefox in windows)
* python 2.7.x
* lettuce
* lettice-webdriver
* sendgrid-python

**Before running:**

  * In terrain.py, change the following line to match your account creds:
```
world.username, world.password = "<username>", "<password>"
```
  * You can also change the sendgridapi.feature test values if you wish to see the fruit of your labor (i.e. destination e-mail)

**To run:**

* Go to top folder lettuce-selenium/
```
: lettuce

or 

: lettuce features/sendgridapi.feature

or

: lettuce -t @email_success_a features/sendgridapi.feature
```

**Task Descriptions:**

1. Using Lettuce & Selenium w/Python complete the following tasks. Starting at http://www.realestate.com.au:
  * Scenario 1: 
    * Build a Test that clicks through the main header links and verifies the landing page matches. i.e. Buy link = realestate.com.au/buy
  * Scenario 2: 
    * Build a Test that performs a search meeting the following criteria. 1 - State = VIC, Suburb = Richmond, Property Type = Apartment, Max Price = 500,000. Verify the listing number results returns and that you actually are searching in this proper State, Suburb.

2. Using Lettuce w/Python Framework complete the following tasks:
  * Scenario 1: 
    * Build a test that fills out the api method for mail. Verify you can fill out all the supported fields and that the email will send properly.


**Known Issues**
------------

* RealEstate.au
  * 'New homes' tab assert may fail as the url found sometimes is a sub-tab of that page
  * Caching causing auto-redirect to /buy and /new-homes on step 'Given I go to "http://www.realestate.com.au"' 