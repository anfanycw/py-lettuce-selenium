from lettuce import before, after, world  
from selenium import webdriver 
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary 
import lettuce_webdriver.webdriver

@before.each_feature
def setup(feature):
	world.feature_name = feature.name
	# only applies to realestate feature
	if "RealEstate" in world.feature_name:
		world.browser = webdriver.Firefox()
		print "\nBEGIN :: REALESTATE FEATURE ============="
	else: # only applies to sendgrid feature
		print "\nBEGIN :: SENDGRID FEATURE ============="
		# EDIT THIS WITH YOUR OWN ACCOUNT INFORMATION
		world.username, world.password = "<username>", "<password>"

		# client
		world.sgc = None
		# message to send
		world.message = None
		# final response and status
		world.response, world.status = "", ""

# clear sendgrid client and globals after each scenario
@after.each_scenario
def teardown(scenario):
	if "Email" in str(scenario):
		world.sgc = None
		world.message = None
		world.response, world.status = "", ""

# quit browser if realestate feature
@after.each_feature
def teardown_browser(feature):
	if "RealEstate" in world.feature_name:
		world.browser.quit()
		print "\nEND :: REALESTATE FEATURE ============="
	else:
		print "\nEND :: SENDGRID FEATURE ============="
