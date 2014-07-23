Feature: SendGrid Mail Web API
	Test should acquire sendgrid client and create a message
	Mail should be sent with appropriate data and response should indicate success

@email_success_a
Scenario: Valid Email A - html, existing file attachment
	Given I have a sendgrid client and a message to send
	When I create a message using sendgrid python web api library
	And I add parameter "to" with value "Anthony Wang <antcwang@gmail.com>" 
	And I add parameter "subject" with value "Test E-mail"
	And I add parameter "html" with value "<h3>Welcome test customer! You're my favorite guy!</h3>"
	And I add parameter "from" with value "Tony Wang <anthony.wang@emc.com>"
	And I add parameter "bcc" with value "antcwang@yahoo.com"
	And I add parameter "replyto" with value "anthony.wang@emc.com"
	And I add parameter "date" with value "now"
	And I add parameter "file" with value "attachment.txt, features/test_attachment.txt"
	And I send the post request
	Then the response should indicate "success" with message ""

@email_success_b
Scenario: Valid Email B - plain text, file attachment stream, and custom header
	Given I have a sendgrid client and a message to send
	When I create a message using sendgrid python web api library
	And I add parameter "to" with value "Anthony Wang <antcwang@gmail.com>" 
	And I add parameter "subject" with value "Test E-mail"
	And I add parameter "text" with value "Welcome test customer! You're my favorite guy!"
	And I add parameter "from" with value "Tony Wang <anthony.wang@emc.com>"
	And I add parameter "bcc" with value "antcwang@yahoo.com"
	And I add parameter "replyto" with value "anthony.wang@emc.com"
	And I add parameter "date" with value "now"
	And I add parameter "headers" with value {"X-Awesome":"msgid"}
	And I add parameter "file_stream" with value "attachment.txt, Random content I want in the attachment"
	And I send the post request
	Then the response should indicate "success" with message ""

@email_fail_a
Scenario: Invalid Email - missing destination email and from email
	Given I have a sendgrid client and a message to send
	When I create a message using sendgrid python web api library
	And I add parameter "subject" with value "Test E-mail"
	And I add parameter "text" with value "Hello world! My name is Anthony and I would like to welcome you to my site!"
	And I add parameter "bcc" with value "antcwang@yahoo.com"
	And I add parameter "replyto" with value "anthony.wang@emc.com"
	And I send the post request
	Then the response should indicate "error" with message "Missing destination email"

@email_fail_b
Scenario: Invalid Email - missing destination email and from email
	Given I have a sendgrid client and a message to send
	When I create a message using sendgrid python web api library
	And I add parameter "to" with value "Anthony Wang <antcwang@gmail.com>"
	And I add parameter "subject" with value "Test E-mail"
	And I add parameter "text" with value "Hello world! My name is Anthony and I would like to welcome you to my site!"
	And I add parameter "bcc" with value "antcwang@yahoo.com"
	And I add parameter "replyto" with value "anthony.wang@emc.com"
	And I send the post request
	Then the response should indicate "error" with message "Empty from email address (required)"