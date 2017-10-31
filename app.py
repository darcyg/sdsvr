#coding=utf-8  
import sys  
import inspect  
import json
import types

from flask import Flask
app = Flask(__name__)

urls = [
	"http://101.132.153.33:5000/api/dev_dbm/register_device",
	"http://101.132.153.33:5000/api/dev_dbm/add_fingerprint",
	"http://101.132.153.33:5000/api/dev_dbm/report_access",
	"http://101.132.153.33:5000/api/dev_dbm/report_alarm",
	"http://101.132.153.33:5000/api/dev_dbm/report_device_status",
]

def register_device(payload):
	ret = {}
	return ret
def add_fingerprint(payload):
	ret = {}
	return ret
def report_access(payload):
	ret = {}
	return ret
def report_alarm(payload):
	ret = {}
	return ret
def report_device_status(payload):
	ret = {}
	return ret

apis = {
	'register_device'			: {
		'func':register_device, 
		'payload' : {
			"mac":"0102030405060708",
			"uuid":""
		}
	},
	'add_fingerprint'			: {
		'func': add_fingerprint,
		'payload' : {
			"person_uuid":"01020304",
			"fingerprint_type":1,
			"fingerprint":"12235677"
		}
	},
	'report_access'				: {
		'func':report_access,
		'payload': {
			"cardno":"1212",
			"mac":"0102030405060708",
			"opentype":1,
			"slide_date":"19293949",
			"dev_uuid":"01020304",
			"dev_number":"0100003"
		}
	},
	'report_alarm'				:	{
		'func': report_alarm,
		'payload': {
			"occur_date":"1920330303",
			"type_":1,
			"mac":"03030203030",
			"device_uuid":"3333",
			"cardno":"12121212",
		}
	},
	'report_device_status': {
		'func': report_device_status,
		'payload': {
			"dev_uuid":"1212121",		
			"mac":"0102030405060708",
			"hw_ver":"1.0",
			"sf_ver":"2.0",
			"imsi":"what?",
			"msisdn":"what?",
			"battery":2.3,
			"temperature":3.2,
			"signal_":-20.0,
			"card_capacity":1000,
			"whitelist_count":800,
			"finger_capacity":800,
			"finger_count":400,
			"opened":0,
			"work_mode":1,
			"power_mode":2
		}
	}
}

def print_array():
	for i, item in enumerate(urls):
		print item

@app.route('/api/dev_dbm/<an>')
def api_devdbm_an(an):
	if apis.has_key(an):
		api			= apis[an]
		func		=	api['func']
		payload	= api['payload']

		response = func(payload)

		info  = '----------------------------------------\n'
		info +=	'Call ' + an + ' with paylaod: ' + json.dumps(payload, indent=4, sort_keys=False, ensure_ascii=False) + '\n'
		info +=	"Respnose:" + json.dumps(response, indent=4,sort_keys=False,ensure_ascii=False) + '\n'
		print info
		return json.dumps(response)
	else:
		return "Not Found!"
    
if __name__ == "__main__":
	print_array()
	app.run('0.0.0.0', 5000, 1)
