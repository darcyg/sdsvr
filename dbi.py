#coding=utf-8  


# 在设备表中根据mac地址查找设备,同时返回设备信息,
# 信息包含 设备uuid, mac, dev_number, key(通讯)
def device_search_device_by_mac(mac):
	ret = {
		"uuid"	: "0103043",
		"mac"		: "0102030405",
		"dev_number"	:	"01092032",
		"key"		: "1209102102",
	}
	return ret

# 在人表中根据uuid查找人, 返回人的基本信息
# 信息包含 人uuid, name, sex
def device_search_person_by_uuid(uuid):
	ret = {
		"uuid"	: "100203",
		"name"	:	"json",
		"sex"		: "man",
	}
	return ret

# 在card表中插入card,卡类型为type, 卡数据为finger
# 返回 0 成功, 非0失败
def card_insert_card(type, finger):
	ret = 0
	return ret

# 在card表中根据type及cardid搜索卡
# 返回卡的基本信息
# 信息包含 卡 uuid, card_number, card_type, state_, effective_start_time, effective_end_time
def card_search_card_by_type_and_id(type, finger):
	ret = {
		"uuid"				: "0102",
		"card_number" : "0102",
		"card_type"		: 1,
		"state_"			: 0,
		"effective_start_time"	: "20171022",
		"effective_end_time"		: "20171023",
	}
	return ret

# 在card表中根据cardno搜索卡
# 返回卡的基本信息
# 信息包含 卡 uuid, card_number, card_type, state_, effective_start_time, effective_end_time
def card_search_card_by_cardno(cardno):
	ret = {
		"uuid"				: "0102",
		"card_number" : "0102",
		"card_type"		: 1,
		"state_"			: 0,
		"effective_start_time"	: "20171022",
		"effective_end_time"		: "20171023",
	}
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

