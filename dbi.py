#coding=utf-8  

import dbm

hdl = None
def init(dbPath):
	ret, hdl = dbm.DBM_init(dbPath)
	# check ret and hdl 

	
	return 

def deinit():

	ret = dbm.DBM_deinit(hdl)
	
	return


# 在设备表中根据mac地址查找设备,同时返回设备信息,
# 信息包含 设备uuid, mac, dev_number, key(通讯)
def device_search_device_by_mac(mac):
	ret = {
		"uuid"				: "0000000000000001",
		"mac"					: "0102030405060708",
		"dev_number"	:	"0000000000000001",
		"key"					: "123456",
	}
	'''
	entityType	= DBM_EntityType.DBM_ENTITY_TYPE_DEVICE
	entity			= dbm_entities.DBM_Device()
	options			= DBM_EntityOptions()
	options.entityType	= entityType
	options.filter			= 0
	options.pConditions	= dbm_utilities.DBM_utlToString('mac = ' + mac)
	options.pCount			= ctypes.addressof(ctypes.c_int())
	options.pEntities		= ctypes.addressof(entity)

	ret = DBM_getEntities(hdl, options)

	ret.uuid				= entity.uuid
	ret.mac					= entity.mac
	ret.dev_number	= entity.dev_number
	ret.key					= ret.key
	'''
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

	'''
	entityType	= DBM_EntityType.DBM_ENTITY_TYPE_DEVICE
	entity			= dbm_entities.DBM_Device()
	options			= DBM_EntityOptions()
	options.entityType	= entityType
	options.filter			= 0
	options.pConditions	= dbm_utilities.DBM_utlToString('uuid = ' + uuid)
	options.pCount			= ctypes.addressof(ctypes.c_int())
	options.pEntities		= ctypes.addressof(entity)

	
	ret = DBM_getEntities(hdl, options)

	ret.uuid				= entity.uuid
	ret.mac					= entity.mac
	ret.dev_number	= entity.dev_number
	ret.key					= ret.key
	'''
	return ret



# 在人表中根据uuid查找人, 返回人的基本信息
# 信息包含 人uuid, name, sex
def person_search_person_by_uuid(uuid):
	ret = {
		"uuid"	: "0000000000000001",
		"name"	:	"kevin",
		"sex"		: "0",		# man
	}

	'''
	entityType	= DBM_EntityType.DBM_ENTITY_TYPE_PERSON
	entity			= dbm_entities.DBM_Person()
	options			= DBM_EntityOptions()
	options.entityType	= entityType
	options.filter			= 0
	options.pConditions	= dbm_utilities.DBM_utlToString('uuid = ' + uuid)
	options.pCount			= ctypes.addressof(ctypes.c_int())
	options.pEntities		= ctypes.addressof(entity)

	ret = DBM_getEntities(hdl, options)

	ret.uuid				= entity.uuid
	ret.name				= entity.name
	ret.sex					= entity.sex
	'''

	return ret

# 在card表中根据type及cardid搜索卡
# 返回卡的基本信息
# 信息包含 卡 uuid, card_number, card_type, state_, effective_start_time, effective_end_time
def card_search_card_by_type_and_id(type, finger):
	ret = {
		"uuid"				: "0000000000000001",
		"card_number" : "00000000000000AB",
		"card_type"		: 1,
		"state_"			: 0,
		"effective_start_time"	: "20171022",
		"effective_end_time"		: "20171023",
	}

	'''
	entityType	= DBM_EntityType.DBM_ENTITY_TYPE_CARD
	entity			= dbm_entities.DBM_Card()
	options			= DBM_EntityOptions()
	options.entityType	= entityType
	options.filter			= 0
	options.pConditions	= dbm_utilities.DBM_utlToString('idcode = ' + finger_code(type, finger))
	options.pCount			= ctypes.addressof(ctypes.c_int())
	options.pEntities		= ctypes.addressof(entity)

	ret = DBM_getEntities(hdl, options)

	ret.uuid									= entity.uuid
	ret.card_number						= entity.card_number
	ret.card_type							= entity.card_type
	ret.state_								= entity.state_
	ret.effective_start_time	= entity.effective_start_time
	ret.effective_end_time		= entity.effective_end_time
	'''


	return ret


# 在card表中插入card,卡类型为type, 卡数据为finger
# 返回 0 成功, 非0失败
def card_insert_card(type, finger):
	ret = 0

	'''
	entityType	= DBM_EntityType.DBM_ENTITY_TYPE_CARD
	entity			= dbm_entities.DBM_Card()
	entity.code	= finger_code(type, finger)
	
	options			= DBM_EntityOptions()
	options.entityType	= entityType
	options.filter			= 0
	options.pConditions	= dbm_utilities.DBM_utlToString('idcode = ' + finger_code(type, finger))
	options.pCount			= ctypes.addressof(ctypes.c_int())
	options.pEntities		= ctypes.addressof(entity)

	# check the pCount
	'''

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

	'''
	entityType	= DBM_EntityType.DBM_ENTITY_TYPE_CARD
	entity			= dbm_entities.DBM_Card()
	options			= DBM_EntityOptions()
	options.entityType	= entityType
	options.filter			= 0
	options.pConditions	= dbm_utilities.DBM_utlToString('idcode = ' + cardno)
	options.pCount			= ctypes.addressof(ctypes.c_int())
	options.pEntities		= ctypes.addressof(entity)

	ret.uuid				= entity.uuid
	ret.card_number = entity.card_number
	ret.card_type		= entity.card_type
	ret.state				= entity.state
	ret.effective_start_time = entity.effective_start_time
	ret.effective_end_time	 = entity.effective_end_time
	'''

	return ret

# 在access表中插入access log
# 返回0 成功, 非0失败
def access_insert():
	ret = 0 
	return ret

# 在alarm表中插入alarm log
# 返回0 成功, 非0失败
def alarm_insert():
	ret = 0
	return ret

# 在dev status表中插入dev status
# 返回0 成功, 非0失败
def device_status_insert():
	ret = 0
	return ret

