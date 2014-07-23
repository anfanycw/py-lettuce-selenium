# @author: Anthony Wang

from lettuce import *
from lettuce_webdriver.util import (assert_true,
                                    assert_false,
                                    AssertContextManager,
                                    find_button,
                                    find_field) 

from selenium.common.exceptions import (NoSuchElementException,
									    StaleElementReferenceException,
									    WebDriverException)
from nose.tools import assert_equals
import time, re, os
from email.Utils import formatdate
import sendgrid
from sendgrid import SendGridError, SendGridClientError, SendGridServerError

##################
## HELPER FUNCS ##
##################
  
def find_field_by_id(browser, attribute):  
	xpath = "//input[@id = '%s']" % attribute  
	elems = browser.find_elements_by_xpath(xpath)  
	return elems[0] if elems else False

def click_input_by_id(browser, btnId):
	xpath = "(//input[@id = '%s'])[1]" % btnId
	elems = browser.find_elements_by_xpath(xpath)
	elems[0].click()
	time.sleep(5)

def find_text(browser, text):  
	xpath = "//span[@class = '%s']" % text  
	span = browser.find_elements_by_xpath(xpath)  
	return span[0] if span else False  

def addParamToReq(step, mail, param, data):
	if param == "to":
		mail.add_to(data)
		to = str(mail.to_name[0]) + " <" + mail.to[0] + ">" \
			 if len(mail.to_name) > 0 != None else mail.to[0]
		assert_true(step, to == data)
	elif param == "subject":
		mail.set_subject(data)
		assert_true(step, mail.subject == data)
	elif param == "html":
		mail.set_html(data)
		assert_true(step, mail.html == data)
	elif param == "from":
		mail.set_from(data)
		sender = mail.from_name + " <" + mail.from_email + ">" \
			 	 if mail.from_name != "" else mail.from_email
		assert_true(step, sender == data)
	elif param == "text":
		mail.set_text(data)
		assert_true(step, mail.text == data)
	elif param == "bcc":
		recips = [d.lstrip() for d in data.split(",")]
		recips = str(recips[0]) if len(recips) < 2 else recips
		mail.add_bcc(recips)
		assert_true(step, set(mail.bcc) == set([recips]) if recips == type("") < 2 else set(recips))
	elif param == "replyto":
		mail.set_replyto(data)
		assert_true(step, mail.reply_to == data)
	elif param == "date":
		date = formatdate(localtime=True)
		mail.set_date(date)
		assert_true(step, mail.date == date)
	elif param == "headers":
		mail.set_headers(data)
		assert_true(step, mail.headers == data)
	elif param == "file_stream":
		attachment = [a.lstrip() for a in data.split(",")]
		mail.add_attachment_stream(attachment[0], attachment[1])
		assert_true(step, mail.files['attachment.txt'] == attachment[1])
	elif param == "file":
		attachment = [a.lstrip() for a in data.split(",")]
		mail.add_attachment(attachment[0], str(attachment[1]))
		assert_true(step, mail.files['attachment.txt'] != '')
	elif param == "x-smtpapi":
		params = [f.lstrip() for f in data.split(",")]
		if params[0] == "category":
			mail.add_category(params[1])
		if params[0] == "filter":
			mail.add_filter(params[0], params[1], params[2])

###########
## STEPS ##
###########

#### FEATURE 1 - realestate.com.au ####

@step('I go to "(.*?)"$')
def gotoURL(step, url):
    with AssertContextManager(step):
        world.browser.get(url)
        time.sleep(2)

@step('I return to "(.*?)"')  
def find_span_by_text(step, url):  
    with AssertContextManager(step):  
        gotoURL(step, url) 

@step('I fill in search box with id "(.*?)" with "(.*?)"')  
def fill_in_textfield_by_class(step, field, value):  
    with AssertContextManager(step):  
        text_field = find_field_by_id(world.browser, field)  
        text_field.clear()  
        text_field.send_keys(value)

@step('I click form button with id "(.*?)"')  
def find_span_by_text(step, btnId):  
    with AssertContextManager(step):  
        click_input_by_id(world.browser, btnId)  

@step('I should see a span with class "(.*?)"')  
def find_span_by_text(step, text):  
    with AssertContextManager(step):  
        find_text(world.browser, text)

@step('I should be at "(.*?)"$')
def url_should_be(step, url):
	print url, world.browser.current_url
	assert_true(step, url == world.browser.current_url)

# When opening new window
@step('I click on target link "(.*?)"')
def browser_url_should_be(step, text):
	with AssertContextManager(step):  
		elem = world.browser.find_element_by_link_text(text)
		elem.click()
		time.sleep(2) # in case of latency
		handles = world.browser.window_handles
		world.browser.switch_to_window(handles[-1])

# Handle new window then close
@step('I should be at "(.*?)" on a new window')
def url_should_be(step, url):
	assert_true(step, url == world.browser.current_url)
	world.browser.close()
	handles = world.browser.window_handles
	world.browser.switch_to_window(handles[0])

# drop downs
@step('I select the following from dropdown with id "([^"]*?)":?$')
def select_multi_items(step, selectId):
    with AssertContextManager(step):
    	# show dropdown
    	dd = world.browser.find_element_by_xpath(
    		str('(//fieldset[@class="propertyType"]//img[@class="LMIDDArrow"])[2]')
    	)
    	dd.click()
    	time.sleep(5)
    	# parse desired options
        options = step.multiline.split('\n')
        # make sure dropdown is present
        dropdown = world.browser.find_element_by_id(selectId)
        assert_true(step, dropdown)
        # clear before selecting
        clear = world.browser.find_element_by_link_text("clear all")
        clear.click()

        for opt in options:
            try:
                world.browser.find_element_by_xpath(
                	str('//div[@id="'+selectId+'"]//input[@value="'+opt+'"]')
                ).click()
            except NoSuchElementException:
                print "\tERROR: no such option in "+selectId+" dropdown"
                return False

@step('I select "(.*?)" from dropdown with id "(.*?)"$')
def select_single_item(step, option, selectId):
	with AssertContextManager(step):
		# show dropdown
		dd = world.browser.find_element_by_xpath(
			str('(//fieldset[@class="maxPrice last"]//img[@class="LMIDDArrow"])[2]')
		).click()
		try:
			option = world.browser.find_element_by_xpath(
				str('(//div[@id="'+selectId+'"]//dd[text() = "'+option+'"])[1]')
			).click()
		except NoSuchElementException:
			print "\tERROR: no such option in "+selectId+" dropdown"
			return False

@step('I do not include surrounding suburbs')
def uncheckSurrounding(step):
	checkbox = find_field_by_id(world.browser, "includeSurrounding")
	checkbox.click()

@step('Then I should see results that all contain the suburb and state "(.*?)"')
def checkResults(step, location):
	results = world.browser.find_elements_by_xpath("//div[@id='searchResultsTbl']//div[@class='vcard']//a")
	for title in results:
		try:
			assert_true(step, title.text.index(location) > -1)
		except ValueError:
			print "\tNote: found a result with location cut-off: '" + title.text + "'"
			print "\tChecking for partial match ..."
			keywords = [x.lstrip() for x in location.split(',')]
			confirmed = filter(lambda x: x in title.text, keywords)
			assert_true(step, len(confirmed) > 0)
			print "\tMatch found for search keyword '" + ", ".join(confirmed) + "'"

#### FEATURE 2 - SendGrid.com ####

@step('I have a sendgrid client and a message to send')
def createSgClient(step):
	world.sgc = sendgrid.SendGridClient(world.username, world.password)
	# established sendgrid client
	assert_true(step, world.sgc.host == 'https://api.sendgrid.com')
	assert_true(step, world.sgc.port == '443')
	assert_true(step, world.sgc.endpoint == '/api/mail.send.json')
	assert_true(step, world.sgc.username == world.username)
	assert_true(step, world.sgc.password == world.password)

@step('I create a message using sendgrid python web api library')
def createSgMessage(step):
	world.message = sendgrid.Mail()
	assert_true(step, world.message.to == [])
	
@step('I add parameter "(.*?)" with value "(.*?)"')
def addParam(step, param, data):
	addParamToReq(step, world.message, param, data)

# handle json
@step('I add parameter "(.*?)" with value (\{".*?"\})')
def addJsonParam(step, param, data):
	addParamToReq(step, world.message, param, data)

@step('I send the post request')
def sendMail(step):
	sgc = world.sgc
	world.status, world.response = sgc.send(world.message)

@step('Then the response should indicate "(.*?)" with message "(.*)"')
def checkResponse(step, result, message):
	if result == "success":
		print "\tRESPONSE: " + world.response + " | CODE: " + str(world.status)
		assert_true(step, world.status == 200 and "success" in world.response)
	else:
		print "\tRESPONSE: " + world.response + " | CODE: " + str(world.status)
		assert_true(step, world.status == 400 and "error" in world.response)
		# check message for error
		assert_true(step, message in world.response)