from config import Config

def send_notification(msg):
	_sendSMS_ncloud(msg)

def _sendSMS_ncloud(msg):
	print(Config.ncloud)

	def make_signature(uri):
		import sys
		import os
		import hashlib
		import hmac
		import base64
		import requests
		import time


		timestamp = int(time.time() * 1000)
		timestamp = str(timestamp)

		access_key = Config.ncloud['accesskey']                 # access key id (from portal or Sub Account)
		secret_key = Config.ncloud['secretkey']                 # secret key (from portal or Sub Account)
		secret_key = bytes(secret_key, 'UTF-8')

		method = "POST"

		message = method + " " + uri + "\n" + timestamp + "\n" + access_key
		message = bytes(message, 'UTF-8')
		signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
		return {
				'x-ncp-apigw-timestamp': timestamp,
				'x-ncp-iam-access-key': access_key,
				'x-ncp-apigw-signature-v2': signingKey,
				'Content-type': 'application/json'
		}

	import requests
	req_body = {
		"type": "SMS",
		"contentType": "COMM",
		"countryCode": "82",
		"from": Config.ncloud['from_number'],
		"content": msg,
		"messages": list(map(lambda num: {'to': num}, Config.ncloud['to_number'])),
	}

	import requests, json
	uri = "/sms/v2/services/{}/messages".format(Config.ncloud['serviceid'])
	header = make_signature(uri)
	print('SEND via naver', flush=True)
	
	try:
		req = requests.post('https://sens.apigw.ntruss.com' + uri, headers=header, data=json.dumps(req_body))
		if req.status_code != 202:
			print('error while sending sms', req, req.text, flush=True)
	except:
		pass