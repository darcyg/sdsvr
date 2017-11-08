#coding=utf-8  

import sys
import ctypes
import os
import dbm_entities
import json

from ctypes import *
from enum import IntEnum
from dbm_entities import *


# Struct From libdbmanage
class CtypesEnum(IntEnum):
    @classmethod
    def from_param(cls, obj):
        return int(obj)

class DBM_EntityType(CtypesEnum):
    DBM_ENTITY_TYPE_NONE                      = 0
    DBM_ENTITY_TYPE_HOUSE                     = 1
    DBM_ENTITY_TYPE_EXT_HOUSE                 = 2
    DBM_ENTITY_TYPE_PERSON                    = 3
    DBM_ENTITY_TYPE_FLOWING_PERSON            = 4
    DBM_ENTITY_TYPE_DEVICE                    = 5
    DBM_ENTITY_TYPE_CARD                      = 6
    DBM_ENTITY_TYPE_SAMCARD                   = 7
    DBM_ENTITY_TYPE_CARD_PERMISSION           = 8
    DBM_ENTITY_TYPE_CARD_OWNING               = 9
    DBM_ENTITY_TYPE_USER_HOUSE                = 10
    DBM_ENTITY_TYPE_ACCESS_RECORD             = 11
    DBM_ENTITY_TYPE_DEVICE_ALARM              = 12
    DBM_ENTITY_TYPE_DEVICE_STATUS             = 13
    DBM_ENTITY_TYPE_COUNT                     = 14
    DBM_ENTITY_TYPE_FIRST                     = DBM_ENTITY_TYPE_HOUSE 
    DBM_ENTITY_TYPE_LAST                      = DBM_ENTITY_TYPE_DEVICE_STATUS

class DBM_EntityOptions(Structure):
		_fields_ = [
			("entityType",	c_int		),
			("filter",			c_void_p		),
			("pConditions",	c_char_p		),
			("pCount",			POINTER(ctypes.c_uint)),
			("offset",			c_uint			),
			("pEntities",		c_void_p		)
	]


def finger_code(type, finger):
	return str(type) + finger
def finger_parse_type(code):
	return code[:1]
def finger_parse_finger(code): 
	return code[1:]

# Interface From libdbmanage.so
'''
int DBM_init(const Char *pConnectionString, DBM_Handle *pHandle);
int DBM_deinit(DBM_Handle handle);
size_t DBM_getEntitySize(const DBM_EntityType entityType);
int DBM_getEntitiesCount(DBM_Handle handle, DBM_EntityOptions *pOptions);
int DBM_getEntities(DBM_Handle handle, DBM_EntityOptions *pOptions);
int DBM_getUnsyncedEntity(DBM_Handle handle, const DBM_EntityType entityType, void *pEntity, void *pAssociation);
int DBM_updateEntities(DBM_Handle handle, const Char *pFieldValues, DBM_EntityOptions *pOptions);
int DBM_overwriteEntities(DBM_Handle handle, DBM_EntityOptions *pOptions);
int DBM_insertEntity(DBM_Handle handle, const DBM_EntityType entityType, void *pEntity, void *pAssociation);
int DBM_insertEntityFromVendor(DBM_Handle handle, const DBM_EntityType entityType, void *pEntity);
int DBM_printEntity(const DBM_EntityType entityType, const void *pEntity);
int DBM_deleteEntity(DBM_Handle handle, DBM_EntityOptions *pOptions);
'''

# Global Variable
osa = None
sql = None
dbm = None
hdl = c_void_p(0)

sql_path = b'./libmysqlclient.so.18'
osa_path = b'./libosa.so'
dbm_path = b'./libdbmanager.so'
con_path = b'User ID = harper; Password = Hello; Server = localhost; Initial Catalog = SAC'

def init(dbPath):
	global hdl, osa, sql, dbm, sql_path, osa_path, dbm_path, con_path

	sql	= CDLL(sql_path, RTLD_GLOBAL)
	if sql == None:
		print("Can't Load libmysqlclient:" + sql_path)
		return -1

	osa	= CDLL(osa_path, RTLD_GLOBAL)
	if osa == None:
		print("Can't Load libosa:" +  osa_path)
		return -2


	dbm	= CDLL(dbm_path)
	if dbm == None:
		print("Can't Load libdbmanageer:" + dbm_path)
		return -3


	ret = dbm.DBM_init(con_path, pointer(hdl))
	
	if ret != 0:
		print("Can't Connect to mysql with :" + con_path)
		return -4

	print("Init dbmanage OK!")
	print(con_path)

	return 0

def deinit():
	global hdl, osa, sql, dbm, sql_path, osa_path, dbm_path, con_path

	ret = dbm.DBM_deinit(hdl)
	
	return 0


# 在设备表中根据mac地址查找设备,同时返回设备信息,
# 信息包含 设备uuid, mac, dev_number, key(通讯)
def device_search_device_by_mac(mac):
	global hdl, osa, sql, dbm, sql_path, osa_path, dbm_path, con_path

	ret = {
		"uuid"				: "0000000000000001",
		"mac"					: "0102030405060708",
		"dev_number"	:	"0000000000000001",
		"key"					: "123456",
	}


	entityType	= DBM_EntityType.DBM_ENTITY_TYPE_DEVICE
	entity			= DBM_Device()
	options			= DBM_EntityOptions()

	options.entityType	= entityType
	options.filter			= None
	options.pConditions	= b'mac = \'' + mac + '\'';
	count = c_uint(1)
	options.pCount			= pointer(count)
	options.pEntities		= cast(pointer(entity), c_void_p)

	rc = dbm.DBM_getEntities(hdl, pointer(options))
	if rc != 0:
		print('Error Call [DBM_getEntities]: ' + str(rc))
		return None

	if count.value == 0:
		print('Not Found this Device: ' + mac)
		return None


	dbm.DBM_printEntity(DBM_EntityType.DBM_ENTITY_TYPE_DEVICE, cast(pointer(entity), c_void_p))

	ret['uuid']					= entity.uuid
	ret['mac']					= entity.mac
	ret['pdev_number']	= entity.dev_number
	#ret['key']					= entity.key
	ret['key']					= ''
	

	return ret


# 在设备表中根据uuid找设备,同时返回设备信息,
# 信息包含 设备uuid, mac, dev_number, key(通讯)
def device_search_device_by_uuid(uuid):
	ret = {
		"uuid"				: "0000000000000001",
		"mac"					: "0102030405060708",
		"dev_number"	:	"0000000000000001",
		"key"					: "123456",
	}

	entityType	= DBM_EntityType.DBM_ENTITY_TYPE_DEVICE
	entity			= DBM_Device()
	options			= DBM_EntityOptions()

	options.entityType	= entityType
	options.filter			= None
	options.pConditions	= b'uuid = \'' + uuid + '\'';
	count = c_uint(1)
	options.pCount			= pointer(count)
	options.pEntities		= cast(pointer(entity), c_void_p)

	rc = dbm.DBM_getEntities(hdl, pointer(options))
	if rc != 0:
		print('Error Call [DBM_getEntities]: ' + str(rc))
		return None

	if count.value == 0:
		print('Not Found this Device: ' + uuid)
		return None


	ret['uuid']					= entity.uuid
	ret['mac']					= entity.mac
	ret['pdev_number']	= entity.dev_number
	#ret['key']					= entity.key
	ret['key']					= ''
	
	return ret


# 在人表中根据uuid查找人, 返回人的基本信息
# 信息包含 人uuid, name, sex
def person_search_person_by_uuid(uuid):
	ret = {
		"uuid"	: "0000000000000001",
		"name"	:	"kevin",
		"sex"		: "0",		# man
	}

	entityType	= DBM_EntityType.DBM_ENTITY_TYPE_PERSON
	entity			= dbm_entities.DBM_Person()
	options			= DBM_EntityOptions()

	options.entityType	= entityType
	options.filter			= None
	options.pConditions	= b'uuid = \'' + uuid + '\''
	count = c_uint(1)
	options.pCount			= pointer(count)
	options.pEntities		= cast(pointer(entity), c_void_p)

	rc = dbm.DBM_getEntities(hdl, pointer(options))
	if rc != 0:
		print('Error Call [DBM_getEntities]: ' + str(rc))
		return None

	if count.value == 0:
		print('Not Found this Person: ' + uuid)
		return None


	ret['uuid']			= entity.uuid
	ret['name']			= entity.name
	ret['sex']			= entity.sex

	return ret

# 在card表中根据type及cardid搜索卡
# 返回卡的基本信息
# 信息包含 卡 uuid, card_number, card_type, state_, effective_start_time, effective_end_time
def card_search_card_by_type_and_id(type, finger):
	print('now not support insert card')
	ret = None
	return ret


# 在card表中插入card,卡类型为type, 卡数据为finger
# 返回 0 成功, 非0失败
def card_insert_card(type, finger):
	print('now not support insert card')
	ret = None
	return ret

# update person finger
def update_finger(person_uuid, fingertype, finger):
	ret = {
		"uuid"	: "0000000000000001",
		"name"	:	"kevin",
		"sex"		: "0",		# man
	}

	entityType	= DBM_EntityType.DBM_ENTITY_TYPE_PERSON
	entity			= dbm_entities.DBM_Person()
	options			= DBM_EntityOptions()

	options.entityType	= entityType
	options.filter			= None
	options.pConditions	= b'uuid = \'' + person_uuid + '\''
	count = c_uint(1)
	options.pCount			= pointer(count)
	options.pEntities		= None

	pFieldValues = b'set fingertype1 = \'' + fingertype + 'and \' finger1 = \'' + finger + '\''
	rc = dbm.DBM_updateEntities(hdl, pFieldValues, pointer(options))
	if rc != 0:
		print('Error Call [DBM_updateEntities]: ' + str(rc))
		return None

	ret = 0

	return ret
		

# 在card表中根据cardno搜索卡
# 返回卡的基本信息
# 信息包含 卡 uuid, card_number, card_type, state_, effective_start_time, effective_end_time
def card_search_card_by_cardno(cardno):
	ret = {
		"uuid"				: "00000000000000001",
		"card_number" : "00000000000000AB",
		"card_type"		: 1,
		"state_"			: 0,
		"effective_start_time"	: "20171022",
		"effective_end_time"		: "20171023",
	}


	entityType	= DBM_EntityType.DBM_ENTITY_TYPE_CARD
	entity			= dbm_entities.DBM_Card
	options			= DBM_EntityOptions()

	options.entityType	= entityType
	options.filter			= None
	options.pConditions	= b'crkno = \'' + cardno + '\''
	count = c_uint(1)
	options.pCount			= pointer(count)
	options.pEntities		= cast(pointer(entity), c_void_p)

	rc = dbm.DBM_getEntities(hdl, pointer(options))
	if rc != 0:
		print('Error Call [DBM_getEntities]: ' + str(rc))
		return None

	if count.value == 0:
		print('Not Found this Card: ' + cardno)
		return None

	ret['uuid']									= entity.uuid
	ret['card_number']					= finger_parse_type(entity.crkno)
	ret['card_type']						= finger_parse_finger(entity.crkno)
	ret['state']								= entity.state_
	ret['effective_start_time']	= entity.etime
	ret['effective_end_time']		= entity.stime

	return ret

# 在access表中插入access log
# 返回0 成功, 非0失败
def access_insert(pl):
	ret = 0 

	entityType	= DBM_EntityType.DBM_ENTITY_TYPE_ACCESS_RECORD
	entity			= dbm_entities.DBM_AccessRecord
	entity.cardno				=	pl['cardno']
	entity.person_uuid	=	'' # DBM_CardOwning
	entity.mac					= pl['mac']
	entity.opentype			= pl['opentype']
	entity.area_uuid		= '' #
	entity.slide_date		= pl['slide_date'] 
	entity.cdate				= '' #.
	entity.dev_uuid			= pl['dev_uuid'] 
	entity.dev_number		= pl['dev_number']
	entity.area_code		= '' #.
	entity.dev_date			= '' #.
	entity.flag					= '' #.
	entity.sync					= '' #

	rc = dbm.DBM_insertEntity(hdl, entityType, pointer(entity), None)
	if rc != 0:
		print('Error Call [DBM_insertEntity]: ' + str(rc))
		return None

	ret = 0

	return ret

# 在alarm表中插入alarm log
# 返回0 成功, 非0失败
def alarm_insert(pl):
	ret = 0 

	entityType	= DBM_EntityType.DBM_ENTITY_TYPE_DEVICE_ALARM
	entity			= dbm_entities.DBM_DeviceAlarm
	entity.uuid					= ''
	entity.occur_date		= pl['occur_date']
	entity.cdate				= ''
	entity.type_				= pl['type_']
	entity.status				= ''
	entity.udate				= ''
	entity.mac					= pl['mac']
	entity.area_uuid		= ''
	entity.account_uuid = ''
	entity.device_uuid	= pl['device_uuid']
	entity.remark				= ''
	entity.cardno				= pl['cardno']
	entity.flag					= ''
	entity.sync					= 0

	rc = dbm.DBM_insertEntity(hdl, entityType, pointer(entity), None)
	if rc != 0:
		print('Error Call [DBM_insertEntity]: ' + str(rc))
		return None

	ret = 0


	return ret

# 在dev status表中插入dev status
# 返回0 成功, 非0失败
def device_status_insert(pl):
	ret = 0 

	entityType	= DBM_EntityType.DBM_ENTITY_TYPE_DEVICE_STATUS
	entity			= dbm_entities.DBM_DeviceStatuse
	entity.uuid									= pl['dev_uuid']
	entity.status								= ''
	entity.hwversion						= pl['hw_ver']
	entity.sfversion						= pl['sf_ver']
	entity.imsi									= pl['imsi']
	entity.msidn								= pl['imsi']
	entity.battery							= pl['msisdn']
	entity.temperature					= pl['temperature']
	entity.signal_							= pl['signal_']
	entity.udate								= ''
	entity.cardpopedomcapacity	= ''
	entity.cardpopedomcount			= ''
	entity.fingercapacity				=	pl['finger_capacity']
	entity.fingercount					= pl['finger_count']
	entity.opened								= pl['opened']
	entity.cdate								= ''
	entity.cuser								= ''
	entity.workmode							= pl['work_mode']
	entity.powermode						= pl['power_mode']
	entity.flag									= ''
	entity.sync									= 0
	

	rc = dbm.DBM_insertEntity(hdl, entityType, pointer(entity), None)
	if rc != 0:
		print('Error Call [DBM_insertEntity]: ' + str(rc))
		return None

	ret = 0


	return ret


# dbi_test()
def dbi_test():
	global hdl, osa, sql, dbm, sql_path, osa_path, dbm_path, con_path

	init("./sq.db")

	es	= dbm.DBM_getEntitySize(DBM_EntityType.DBM_ENTITY_TYPE_DEVICE)
	print("size is " + str(es))

	
	options = DBM_EntityOptions()
	options.entityType = DBM_EntityType.DBM_ENTITY_TYPE_PERSON
	options.filter = None
	options.pConditions = b'1 = 1'
	count = c_uint(0)
	options.pCount = pointer(count)
	options.offset = c_uint(0)
	options.pEntities = None
	
	ret = dbm.DBM_getEntitiesCount(hdl, pointer(options))
	if ret != 0:
		print('Error Call : DBM_getEntitiesCount!')
		return
	print('count is ' + str(count))

	deinit();
	return 0

# dbi_test_iface()
def dbi_test_iface():
	init("./sq.db")

	
	ret = device_search_device_by_mac('00-1f-d1-7f-16-0a')
	if not ret:
		print('not such device')
	else:
		print(json.dumps(ret, indent=4, sort_keys=False, ensure_ascii=False))

	ret = device_search_device_by_uuid('0eaf035f956348dbb031a589a7005630')	
	if not ret:
		print('not such device')
	else:
		print(json.dumps(ret, indent=4, sort_keys=False, ensure_ascii=False))


	ret = person_search_person_by_uuid('0236c41d6fc6481f96a0c5d776396877')
	if not ret:
		print('not such person')	
	else:
		print(json.dumps(ret, indent=4, sort_keys=False, ensure_ascii=False))

	
	ret = card_search_card_by_type_and_id('1','111')
	if not ret:
		print('not such card')
	else:
		print(json.dumps(ret, indent=4, sort_keys=False, ensure_ascii=False))
	
	
	deinit();
	return 0

if "__main__" == __name__:    
	#dbi_test();
	dbi_test_iface();
