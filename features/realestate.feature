Feature: RealEstate navigability and search
	Users should be able to reach the sign in and registration pages
	Header links should lead the user to the correct URLs
	Search criteria should match results

@landing
Scenario: Basic visit to RealEstate AU with empty search
	Given I go to "http://www.realestate.com.au"  
	When I fill in search box with id "where" with "Irvine"
	And I do not include surrounding suburbs
	And I click form button with id "searchBtn"
	Then I should see a span with class "noExact"

@links
Scenario: Verify login and registration header links lead user to correct URLs
	Given I go to "http://www.realestate.com.au" 
	When I click "Sign In"
	Then I should be at "https://www.realestate.com.au/my-real-estate/login"
	When I go to "http://www.realestate.com.au"
	And I click "Join"
	Then I should be at "https://www.realestate.com.au/my-real-estate/register"

@links
Scenario Outline: Verify header links go to appropriate URLs
	Given I go to "http://www.realestate.com.au/buy"
	When I click "<tab>"
	Then I should be at "<url>"

Examples:
	| tab 			| url 													|
	| Buy 			| http://www.realestate.com.au/buy 						|
	| Rent 			| http://www.realestate.com.au/rent 					|
	| Invest 		| http://www.realestate.com.au/invest 					|
	| Sold 			| http://www.realestate.com.au/sold 					|
	| Share 		| http://www.realestate.com.au/share 					|
	| New homes 	| http://www.realestate.com.au/new-homes/new-apartments |
	| Retire 		| http://www.realestate.com.au/retire 					|
	| Find agents 	| http://www.realestate.com.au/find-agent 				|
	| Home ideas 	| http://www.realestate.com.au/home-ideas/ 				|
	| Blog 			| http://www.realestate.com.au/blog/ 					|

@links
Scenario: Verify new window header link leads user to correct URL
	Given I go to "http://www.realestate.com.au"
	When I click on target link "Commercial"
	Then I should be at "http://www.realcommercial.com.au/for-sale" on a new window

@search
Scenario: Verify search feature works correctly given specific criteria
	Given I go to "http://www.realestate.com.au"  
	When I fill in search box with id "where" with "Richmond, VIC"
	And I select the following from dropdown with id "LMIDD_propertyType"
		"""
		apartment
		"""
	And I select "500,000" from dropdown with id "LMIDD_maxPrice"
	And I do not include surrounding suburbs
	And I click form button with id "searchBtn"
	Then I should see results that all contain the suburb and state "Richmond, Vic"