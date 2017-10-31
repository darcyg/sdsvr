#coding=utf-8  

# import 
##########################################################################
import sys  
import inspect  
import json
import types
import dbi
from flask import Flask

# variable
##########################################################################
app = Flask(__name__)

host="0.0.0.0"

port=5000

dflg=0

urls = [
	"http://101.132.153.33:5000/api/dev_dbm/register_device",
	"http://101.132.153.33:5000/api/dev_dbm/add_fingerprint",
	"http://101.132.153.33:5000/api/dev_dbm/report_access",
	"http://101.132.153.33:5000/api/dev_dbm/report_alarm",
	"http://101.132.153.33:5000/api/dev_dbm/report_device_status",
]

sts = {
	'OSA_STATUS_OK'			: 0,
	'OSA_STATUS_EINVAL' : 22,
	'OSA_STATUS_ENOMEM' : 12,
	'OSA_STATUS_EEXIST'	: 17,
	'OSA_STATUS_ENOENT'	: 2,
}

# util
##########################################################################
def print_array(ary):
	for i, item in enumerate(ary):
		print item
def valid_mac(mac):
	return 1
def valid_uuid(uuid):
	return 1
def valid_finger_type(ft):
	return 1
def valid_finger(f):
	return 1
def valid_cardno(card):
	return 1
def valid_opentype(ot):
	return 1
def valid_date(d):
	return 1
def valid_devnumber(dn):
	return 1
def valid_alarmtype(at):
	return 1
def valid_hw_ver(hw):
	return 1
def valid_sf_ver(sw):
	return 1
def valid_battery(b):
	return 1
def valid_temperature(t):
	return 1
def valid_signal(s):
	return 1
def valid_integer(i):
	return 1

# function arg check
##########################################################################
def check_register_device(payload):
	ret = 0

	if not payload.has_key('mac'):
		return ret
	mac = payload['mac']
	if not valid_mac(mac):
		return ret

	if not payload.has_key('uuid'):
		return ret
	uuid = payload['uuid']
	if not valid_uuid(uuid):
		return ret	

	ret = 1
	
	return ret

def check_add_fingerprint(payload):
	ret = 0

	if not payload.has_key('mac'):
		return ret
	mac = payload['mac']
	if not valid_mac(mac):
		return ret

	if not payload.has_key('person_uuid'):
		return ret
	person_uuid = payload['person_uuid']
	if not valid_uuid(person_uuid):
		return ret	

	if not payload.has_key('fingerprint_type'):
		return ret
	fingerprint_type = payload['fingerprint_type']
	if not valid_finger_type(fingerprint_type):
		return ret

	if not payload.has_key('fingerprint'):
		return ret
	fingerprint = payload['fingerprint']
	if not valid_finger(fingerprint):
		return ret

	ret = 1
	return ret

def check_report_access(payload):
	ret = 1

	if not payload.has_key('cardno'):
		return ret
	cardno = payload['cardno']
	if not valid_cardno(cardno):
		return ret

	if not payload.has_key('mac'):
		return ret
	mac = payload['mac']
	if not valid_mac(mac):
		return ret

	if not payload.has_key('opentype'):
		return ret
	opentype = payload['opentype']
	if not valid_opentype(opentype):
		return ret


	if not payload.has_key('slide_date'):
		return ret
	slide_data = payload['slide_date']
	if not valid_date(slide_date):
		return ret

	if not payload.has_key('dev_uuid'):
		return ret
	dev_uuid = payload['dev_uuid']
	if not valid_uuid(dev_uuid):
		return ret	

	if not payload.has_key('dev_number'):
		return ret
	dev_number = payload['dev_number']
	if not valid_devnumber(dev_number):
		return ret

	return ret

def check_report_alarm(payload):
	ret = 1

	if not payload.has_key('occur_date'):
		return ret
	occur_date = payload['occur_date']
	if not valid_date(occur_date):
		return ret

	if not payload.has_key('type'):
		return ret
	alarmtype = payload['type']
	if not valid_alarmtype(alarmtype):
		return ret

	if not payload.has_key('mac'):
		return ret
	mac = payload['mac']
	if not valid_mac(mac):
		return ret

	if not payload.has_key('cardno'):
		return ret
	cardno = payload['cardno']
	if not valid_cardno(cardno):
		return ret

	if not payload.has_key('dev_uuid'):
		return ret
	dev_uuid = payload['dev_uuid']
	if not valid_uuid(dev_uuid):
		return ret	

	return ret

def check_report_device_status(payload):
	ret = 1

	if not payload.has_key('dev_uuid'):
		return ret
	dev_uuid = payload['dev_uuid']
	if not valid_uuid(dev_uuid):
		return ret	

	if not payload.has_key('mac'):
		return ret
	mac = payload['mac']
	if not valid_mac(mac):
		return ret

	if not payload.has_key('hw_ver'):
		return ret
	hw_ver = payload['hw_ver']
	if not valid_hw_ver(hw_ver):
		return ret

	if not payload.has_key('sf_ver'):
		return ret
	sf_ver = payload['sf_ver']
	if not valid_sf_ver(sf_ver):
		return ret

	if not payload.has_key('battery'):
		return ret
	battery = payload['battery']
	if not valid_battery(battery):
		return ret

	if not payload.has_key('temperature'):
		return ret
	temperature = payload['temperature']
	if not valid_temperature(temperature):
		return ret

	if not payload.has_key('signal_'):
		return ret
	signal = payload['signal_']
	if not valid_signal(signal):
		return ret

	if not payload.has_key('card_capacity'):
		return ret
	card_capacity = payload['card_capacity']
	if not valid_integer(card_capacity):
		return ret

	if not payload.has_key('whitelist_count'):
		return ret
	whitelist_count = payload['whitelist_count']
	if not valid_integer(whitelist_count):
		return ret

	if not payload.has_key('finger_capacity'):
		return ret
	finger_capacity = payload['finger_capacity']
	if not valid_integer(finger_capacity):
		return ret


	if not payload.has_key('finger_count'):
		return ret
	finger_count = payload['finger_count']
	if not valid_integer(finger_count):
		return ret


	if not payload.has_key('opened'):
		return ret
	opened = payload['opened']
	if not valid_integer(opened):
		return ret

	if not payload.has_key('work_mode'):
		return ret
	work_mode = payload['work_mode']
	if not valid_integer(work_mode):
		return ret

	if not payload.has_key('power_mode'):
		return ret
	power_mode = payload['power_mode']
	if not valid_integer(power_mode):
		return ret

	return ret


# function
##########################################################################
def register_device(payload):
	ret = {'status':0, 'payload': {}}

	mac		= payload['mac']
	uuid	= payload['uuid']

	device = dbi.device_search_device_by_mac(mac)
	if not device:
		ret['status'] = sts['OSA_STATUS_ENOENT']
		return ret

	if not uuid == device['uuid']:
		ret['status'] = 'OSA_STATUS_EINVAL'
		return ret

	ret['status'] = 'OSA_STATUS_OK'
	ret['payload']['mac']					= payload['mac']
	ret['payload']['uuid']				= payload['uuid']
	ret['payload']['dev_number']	= device['dev_number']
	ret['payload']['key']					= device['key']
	
	return ret

def add_fingerprint(payload):
	ret = {'status':0, 'payload': {}}

	mac								= payload['mac']
	person_uuid				= payload['person_uuid']
	fingerprint_type	= payload['fingerprint_type']
	fingerprint				= payload['fingerprint']

	device = dbi.device_search_device_by_mac(mac)
	person = dbi.person_search_person_by_uuid(person_uuid)

	if not device or not person :
		ret['status'] = sts['OSA_STATUS_ENOENT']
		return 

	dbi.card_insert_card(fingerprint_type, fingerprint)
	card = dbi.card_search_card_by_type_and_id(fingerprint_type, fingerprint)
	
	
	ret['status'] = 'OSA_STATUS_OK'
	ret['payload']['uuid']								= card['uuid']
	ret['payload']['card_number']					= card['card_number']
	ret['payload']['card_type']						= card['card_type']
	ret['payload']['state_']							= card['state_']
	ret['payload']['effective_start_time']= card['effective_start_time']
	ret['payload']['effective_end_time']	= card['effective_end_time']
	

	return ret

def report_access(payload):
	ret = {'status':0, 'payload': {}}

	cardno		= payload['cardno']
	mac				= payload['mac']
	opentype	= payload['opentype']
	slide_date= payload['slide_date']
	dev_uuid	= payload['dev_uuid']
	dev_number= payload['dev_number']

	card = dbi.card_search_card_by_cardno(cardno)
	device = dbi.device_search_device_by_mac(mac)
	
	dbi.access_insert();

	return ret

def report_alarm(payload):
	ret = {'status':0, 'payload': {}}

	occur_date	= payload['occur_date']
	type_				= payload['type_']
	mac					= payload['mac']
	device_uuid	= payload['dev_uuid']
	cardno			= payload['cardno']


	card = dbi.card_search_card_by_cardno(cardno)
	device = dbi.device_search_device_by_uuid(dev_uuid)

	dbi.alarm_insert()

	return ret


def report_device_status(payload):
	ret = {'status':0, 'payload': {}}

	dev_uuid	= payload['dev_uuid']
	mac				= payload['mac']
	hw_ver		= payload['hw_ver']
	sf_ver		= payload['sf_ver']
	imsi			= payload['imsi']
	msisdn		= payload['msisdn']
	battery		= payload['battery']
	temperature	= payload['temperature']
	signal_		= payload['signal_']
	card_capacity = payload['card_capacity']
	whitelist_count = payload['whitelist_count']
	finger_capacity = payload['finger_capacity']
	finger_count		= payload['finger_count']
	opened		= payload['opened']
	work_mode = payload['work_mode']
	power_mode= payload['power_mode']

	device = dbi.device_search_device_by_uuid(dev_uuid)
	if not device.mac == mac :
		ret['status'] = 'OSA_STATUS_EINVAL'
		return ret

	dbi.device_status_insert()
	
	return ret

# service & proto
##########################################################################
apis = {
	'register_device'			: {
		'func':register_device, 
		'checkarg' : check_register_device,
		'payload' : {
			"mac":"0102030405060708",
			"uuid":""
		},
		'response': {
			"status" : 0,
			"payload": { "mac":"01020304050708", "uuid":"12344567",
				"dev_number":"1231212",
				"key":"12122",
			}
		}
	},
	'add_fingerprint'			: {
		'func': add_fingerprint,
		'checkarg' : check_add_fingerprint,
		'payload' : {
			"mac":"0102030405060708",
			"person_uuid":"01020304",
			"fingerprint_type":1,
			"fingerprint":"12235677"
		},
		'response': {
			"status" : 0,
			"payload": {
				"uuid":"12121212",
				"card_number" : "12121212",
				"card_type": 1,
				"state_" : 2,
				"effective_start_time": "19982032",
				"effective_end_time": "19982302",
			},
		},
	},
	'report_access'				: {
		'func':report_access,
		'checkarg' : check_report_access,
		'payload': {
			"cardno":"1212",
			"mac":"0102030405060708",
			"opentype":1,
			"slide_date":"19293949",
			"dev_uuid":"01020304",
			"dev_number":"0100003"
		},
		"response": {
			"status": 0,
			"payload": {
			}
		},
	},
	'report_alarm'				:	{
		'func': report_alarm,
		'checkarg' : check_report_alarm,
		'payload': {
			"occur_date":"1920330303",
			"type_":1,
			"mac":"03030203030",
			"device_uuid":"3333",
			"cardno":"12121212",
		},
		"response": {
			"status": 0,
			"payload": {
			}
		},
	},
	'report_device_status': {
		'func': report_device_status,
		'checkarg' : check_report_device_status,
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
		},
		"response": {
			"status": 0,
			"payload": {
			}
		},
	}
}


@app.route('/api/dev_dbm/<an>')
def api_devdbm_an(an):
	if apis.has_key(an):
		api			 = apis[an]
		func		 = api['func']
		payload	 = api['payload']
		checkarg = api['checkarg']
		

		if not checkarg(payload):
			status	 = sts['OSA_STATUS_EINVAL']
			response = {'status' : status, 'payload': {}}
		else:
			response = func(payload)
			response = api['response']

		info  = '----------------------------------------\n'
		info +=	'Call ' + an + ' with:\n'
		info += 'paylaod: ' + json.dumps(payload,  indent=4, sort_keys=False, ensure_ascii=False) + '\n'
		info +=	"Respnose:" + json.dumps(response, indent=4, sort_keys=False, ensure_ascii=False) + '\n'
		print info
	else:
		response = {"status":sts['OSA_STATUS_ENOENT'], "payload":{}}

	return json.dumps(response)

    
# main
##########################################################################
if __name__ == "__main__":
	print_array(urls)
	app.run(host, port, dflg)


