#coding=utf-8  

# import 
##########################################################################
import sys  
import inspect  
import json
import types
import dbi
import re
from flask import Flask

# variable
##########################################################################
app = Flask(__name__)

dpath = "./sq.db"

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
		print(' * ' + item)

# function arg check
##########################################################################
def checkarg(payload, pl):
	ret = 1
	
	for arg in payload:
		argval = payload[arg]
		defval = argval['defval']
		type	 = argval['type']
		len		 = argval['len']
		regexp = argval['regexp']

		if not pl.has_key(arg):
			ret = 0
			return ret
	
		#val = pl[arg]
		val = pl[arg]['defval']

		
		p = re.compile(regexp)
		m = p.match(val)
		if not m:
			ret = 0
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
		ret['status'] = sts['OSA_STATUS_EINVAL']
		return ret

	ret['status'] = sts['OSA_STATUS_OK']
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
		return  ret
	
	rc = dbi.update_finger(person_uuid, fingerprint_type, fingerprint)
	if rc != 0:
		ret['status'] = sts['OSA_STATUS_ENOENT']
		return  ret

	#person = dbi.person_search_person_by_uuid(person_uuid)

	#dbi.card_insert_card(fingerprint_type, fingerprint)
	#card = dbi.card_search_card_by_type_and_id(fingerprint_type, fingerprint)
	
	
	ret['status'] = sts['OSA_STATUS_OK']
	#ret['payload']['uuid']								= card['uuid']
	#ret['payload']['card_number']					= card['card_number']
	#ret['payload']['card_type']						= card['card_type']
	#ret['payload']['state_']							= card['state_']
	#ret['payload']['effective_start_time']= card['effective_start_time']
	#ret['payload']['effective_end_time']	= card['effective_end_time']
	

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
	if not card or not device:
		ret['status'] = sts['OSA_STATUS_EINVAL']
		return ret
	
	dbi.access_insert(payload);

	return ret

def report_alarm(payload):
	ret = {'status':0, 'payload': {}}

	occur_date	= payload['occur_date']
	type_				= payload['type_']
	mac					= payload['mac']
	device_uuid	= payload['device_uuid']
	cardno			= payload['cardno']


	card = dbi.card_search_card_by_cardno(cardno)
	device = dbi.device_search_device_by_uuid(device_uuid)
	if not card or not device:
		ret['status'] = sts['OSA_STATUS_EINVAL']
		return ret

	dbi.alarm_insert(payload)

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
	if not device['mac'] == mac :
		ret['status'] = sts['OSA_STATUS_EINVAL']
		return ret

	dbi.device_status_insert(payload)


	
	return ret

# service & proto
##########################################################################
apis = {
	'register_device'			: {
		'func':register_device, 
		'payload' : {
			"mac":	{"defval":"0102030405060708", "type":"char", "len":32, "regexp":"^([0-9a-fA-F]{2}){6,8}$"},
			"uuid":	{"defval":"0120912019",				"type":"char", "len":32, "regexp":""},
		},
		'response': {
			"status" : 0,
			"payload": { 
				"mac":"01020304050708", 
				"uuid":"12344567",
				"dev_number":"1231212",
				"key":"12122",
			}
		}
	},
	'add_fingerprint'			: {
		'func': add_fingerprint,
		'payload' : {
			"mac":										{"defval":"0102030405060708", "type":"char", "len":32, "regexp":"^([0-9a-fA-F]{2}){6,8}$"},
			"person_uuid":						{"defval":"0102030000000001", "type":"char", "len":32, "regexp":""},
			"fingerprint_type":				{"defval":"1212",							"type":"int",  "len":1,	 "regexp":""},
			"fingerprint":						{"defval":"012910290129102",  "type":"char", "len":32, "regexp":""},
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
		'payload': {
			"cardno":									{"defval":"0102030405060708", "type":"char", "len":32, "regexp":""},
			"mac":										{"defval":"0102030405060708", "type":"char", "len":32, "regexp":"^([0-9a-fA-F]{2}){6,8}$"},
			"opentype":								{"defval":"1",								"type":"int",  "len":1,	 "regexp":""},
			"slide_date":							{"defval":"20170302",					"type":"char", "len":32, "regexp":""},
			"dev_uuid":								{"defval":"0102030000000001", "type":"char", "len":32, "regexp":""},
			"dev_number":							{"defval":"12121212",					"type":"char", "len":32, "regexp":""},
		},
		"response": {
			"status": 0,
			"payload": {
			}
		},
	},
	'report_alarm'				:	{
		'func': report_alarm,
		'payload': {
			"occur_date":						{"defval":"20170302",					"type":"char", "len":32, "regexp":""},
			"type_":								{"defval":"1",								"type":"int",  "len":1,	 "regexp":""},
			"mac":									{"defval":"0102030405060708", "type":"char", "len":32, "regexp":"^([0-9a-fA-F]{2}){6,8}$"},
			"device_uuid":					{"defval":"0102030000000001", "type":"char", "len":32, "regexp":""},
			"cardno":								{"defval":"20170302",					"type":"char", "len":32, "regexp":""},
		},
		"response": {
			"status": 0,
			"payload": {
			}
		},
	},
	'report_device_status': {
		'func': report_device_status,
		'payload': {
			"dev_uuid":						{"defval":"0102030000000001", "type":"char", "len":32, "regexp":""},
			"mac":								{"defval":"0102030405060708", "type":"char", "len":32, "regexp":"^([0-9a-fA-F]{2}){6,8}$"},
			"hw_ver":							{"defval":"1.0",							"type":"char", "len":32, "regexp":""},
			"sf_ver":							{"defval":"1.0",							"type":"char", "len":32, "regexp":""},
			"imsi":								{"defval":"what?",						"type":"char", "len":32, "regexp":""},
			"msisdn":							{"defval":"what?",						"type":"char", "len":32, "regexp":""},
			"battery":						{"defval":"2.3",							"type":"float","len":1,	 "regexp":""},
			"temperature":				{"defval":"3.2",							"type":"float","len":1,	 "regexp":""},
			"signal_":						{"defval":"-20.0",						"type":"float","len":1,	 "regexp":""},
			"card_capacity":			{"defval":"1000",							"type":"int",  "len":1,	 "regexp":""},
			"whitelist_count":		{"defval":"8000",							"type":"int",  "len":1,	 "regexp":""},
			"finger_capacity":		{"defval":"8000",							"type":"int",  "len":1,	 "regexp":""},
			"finger_count":				{"defval":"4000",							"type":"int",  "len":1,	 "regexp":""},
			"opened":							{"defval":"0",								"type":"int",  "len":1,	 "regexp":""},
			"work_mode":					{"defval":"1",								"type":"int",  "len":1,	 "regexp":""},
			"power_mode":					{"defval":"0",								"type":"int",  "len":1,	 "regexp":""},
		},
		"response": {
			"status": 0,
			"payload": {
			}
		},
	}
}


@app.route('/api/dev_dbm/<an>', methods = ['GET', 'POST'])
def api_devdbm_an(an):
	if apis.has_key(an):
		api			 = apis[an]
		func		 = api['func']
		payload	 = api['payload']
		pl			 = api['payload']

		if not checkarg(payload, pl):
			status	 = sts['OSA_STATUS_EINVAL']
			response = {'status' : status, 'payload': {}}
		else:
			response = func(pl)
			response = api['response']

		info  = '----------------------------------------\n'
		info +=	'Call ' + an + ' with:\n'
		info += 'paylaod: ' + json.dumps(payload,  indent=4, sort_keys=False, ensure_ascii=False) + '\n'
		info +=	"Respnose:" + json.dumps(response, indent=4, sort_keys=False, ensure_ascii=False) + '\n'
		print(info)
	else:
		response = {"status":sts['OSA_STATUS_ENOENT'], "payload":{}}

	return json.dumps(response)

    
# main
##########################################################################
if __name__ == "__main__":
	print('[Api Info]:')
	print_array(urls)
	
	print('[Init DB ' +  dpath + ']:')
	dbi.init(dpath)

	print('[Run Server]:')
	app.run(host, port, dflg)

	print("[Deinit DB]:")
	dbi.deinit()

	print('[Exit]')


