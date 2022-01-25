from selenium import webdriver
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from platform import python_version
from datetime import datetime


class Bot:
	def __init__(self): 
		self.driver = webdriver.Firefox()
		self.navigate()

	def navigate(self):
		self.driver.get('https://clearoutside.com/forecast/37.77/-122.42')

	def get_sunset_hour(self):
		daylight_data = self.driver.find_element_by_xpath('//div[contains(@class, "fc_daylight")]').get_attribute(
			'data-content').split()
		sunset = daylight_data[1]
		sunset_hour, sunset_minutes = sunset.split(":")
		if int(sunset_minutes) > 40:
			sunset_hour = int(sunset_hour)
			sunset_hour += 1
		return sunset_hour

	def get_sunrise_hour(self):
		daylight_data = self.driver.find_element_by_xpath('//div[contains(@class, "fc_daylight")]').get_attribute(
			'data-content').split()
		sunrise = daylight_data[1]
		sunrise_hour, sunrise_minutes = sunrise.split(":")
		if int(sunrise_minutes) > 40:
			sunrise_hour = int(sunrise_hour)
			sunrise_hour += 1
		return sunrise_hour

	def get_sunrise_data(self, sunrise_hour):
		data = []

		for li in self.driver.find_elements_by_xpath("//div[@class='fc_hours']/ul"):
			data.append(li.text)
		low_data = data[1].split('\n')
		medium_data = data[2].split('\n')
		high_data = data[3].split('\n')

		result = [low_data[int(sunrise_hour)],medium_data[int(sunrise_hour)],high_data[int(sunrise_hour)]]
		text = 'Forecast from Clearoutside.com on Sunrise<br>Low Clouds: {}<br>Medium Clouds: {}<br>High Clouds: {}'.format(*result)
		return text

	def get_sunset_data(self, sunset_hour):
		data = []

		for li in self.driver.find_elements_by_xpath("//div[@class='fc_hours']/ul"):
			data.append(li.text)
		low_data = data[1].split('\n')
		medium_data = data[2].split('\n')
		high_data = data[3].split('\n')

		result = [low_data[int(sunset_hour)], medium_data[int(sunset_hour)], high_data[int(sunset_hour)]]
		text = 'Forecast from Clearoutside.com on Sunset<br>Low Clouds: {}<br>Medium Clouds: {}<br>High Clouds: {}'.format(
			*result)
		return text


	def get_actual_data(self):
		sunrise_hour = self.get_sunrise_hour()
		sunset_hour = self.get_sunset_hour()

		if int(sunrise_hour) > int(
				datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S").split()[1].split(':')[0]) < sunset_hour:
			mail_text = self.get_sunset_data(sunset_hour)
		else:
			mail_text = self.get_sunrise_data(sunrise_hour)

		return mail_text


	def send_mail(self, text, recipients):

		server = 'smtp.gmail.com'
		user = 'clearoutside.bot@gmail.com'
		password = '9pq3aqsMpvm5WmN'


		sender = 'clearoutside.bot@gmail.com'
		subject = 'Clearoutside data({})'.format(datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S").split()[0])
		html = '<html><head></head><body><p>' + text + '</p></body></html>'

		msg = MIMEMultipart('alternative')
		msg['Subject'] = subject
		msg['From'] = 'ClearOutsideBot <' + sender + '>'
		msg['To'] = ', '.join(recipients)
		msg['Reply-To'] = sender
		msg['Return-Path'] = sender
		msg['X-Mailer'] = 'Python/' + (python_version())

		part_text = MIMEText(text, 'plain')
		part_html = MIMEText(html, 'html')


		msg.attach(part_text)
		msg.attach(part_html)

		mail = smtplib.SMTP_SSL(server)
		mail.login(user, password)
		mail.sendmail(sender, recipients, msg.as_string())
		mail.quit()




def main():

	b = Bot()

	b.send_mail(b.get_actual_data(), '*') #Your mail instead *
	b.driver.quit()


if __name__ == '__main__':
	main()