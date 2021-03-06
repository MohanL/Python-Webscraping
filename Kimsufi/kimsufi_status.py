# kimsufi_status.py
# Kimsufi Status
# Created by Noah Christiano on 8/15/2014.
# noahchristiano@rochester.edu

import requests
import json
import smtplib
from selenium import webdriver

#email parameters
email = #your email
password = #your password
name = #your name
host = #your smtp email host
port = #your smtp email host port (normally 587)

#scraping parameters
ovh_page = 'https://ws.ovh.com/dedicated/r2/ws.dispatcher/getAvailability2'

#auto-purchase parameters
kim_email = #kimsufi account email
kim_password = #kimsufi account password

#construct email
def message(str):
	from = 'From: ' + name + ' <' + email + '>'
	to = 'To: ' + name + ' <' + email + '>'
	subject = 'Subject: KS-1 Servers in Stock\n'
	content = 'Servers were available at these locations:\n\n' + str + '\nLove,\n' + name
	msg = from + '\n' + to + '\n' + subject + '\n' + content
	server = smtplib.SMTP(host, port)
	server.ehlo()
	server.starttls()
	server.login(email, password)
	server.sendmail(email, email, msg)
	server.quit()

#try-catch to prevent crash if network outage
try:
	r = requests.get(ovh_page).text
	j = json.loads(r)
	avail = ''
	for s in j['answer']['availability']:
		if s['reference'] == '142sk1': #analyze ovh_page to find the correct reference number for the server you want. 142sk1 is KS-1.
			for i in s['zones']:
				if i['availability'] != 'unavailable':
					avail = avail + i['zone'] + ': ' + i['availability'] + '\n'

	if avail != '':

		#scrape availability information
		driver = webdriver.Firefox()
		driver.get('http://www.kimsufi.com/en/')
		driver.find_element_by_xpath('//td[@data-ref="142sk1"]/a[@class="order-button"]').click()
		driver.find_element_by_xpath('//a[@id="aButtonValidation"]').click()
		driver.find_element_by_xpath('//a[@id="aButtonValidation"]').click()

		#this page does not always load evenly, while loop waits for complete load
		check = None
		while check != 'Identification':
			try:
				check = driver.find_element_by_xpath('//td/h6[@qtlid="7174"]').text
				print check
			except:
				driver.find_element_by_xpath('//a[@id="aButtonValidation"]').click()

		radio = driver.find_element_by_xpath('//input[@value="existing"]').click()
		driver.find_element_by_xpath('//input[@name="session_nicData_nic"]').send_keys(kim_email)
		driver.find_element_by_xpath('//input[@name="session_nicData_password"]').send_keys(kim_password)
		driver.find_element_by_xpath('//a[@id="aButtonValidation"]').click()
		driver.find_element_by_xpath('//a[@id="aButtonValidation"]').click()
		driver.find_element_by_xpath('//img[@onclick="check_unckeck_box();"]').click()
		driver.find_element_by_xpath('//a[@id="aButtonValidation"]').click()
		driver.find_element_by_xpath('//input[@src="https://www.ovh.com/fr/common/webaffaires/VISA.gif"]').click()
		
		#send availability email
		message(avail)
		
		#i only automated up until this point
		#automating the payment process would be the next step
		raw_input("Press Enter to continue...")
except:
	pass
