import requests
import json
import time
import os
from urllib import parse

username = os.environ["USERNAME"]  # 北航统一认证账号;
password = os.environ["PASSWORD"]  # 登陆密码;
qq = os.environ["QQ"]
qmsg = os.environ["QMSGKEY"]
boarder = "1"  # 是否在校住宿; 是 "1"，否 "0". 若为 "0", 填写下一项;
wechat_key = os.environ["WECHAT"]


def bot_post(text):
        data = {
                "msg": text,  # 需要发送的消息
                "qq": qq  # 需要接收消息的QQ号码
        }
        url1 = 'https://sctapi.ftqq.com/' + wechat_key + '.send?title=check_ok' + '&desp='+text+time.strftime("%m-%d", time.localtime())
        re_result = requests.get(url1)
        url2 = 'https://qmsg.zendee.cn/send/'+qmsg
        requests.post(url2,data=data)
        print(re_result.text)

not_boarder_reasen = ""  # 若 boarder 为 "0", 请选数字: {
                         #    "1", 临时出校;
                         #    "2", 寒暑假返乡;
                         #    "3", 在境外科研学习;
                         #    "4", 在境内校外出差、实习;
                         #    "5", 病假、事假或休学中;
                         #    "6", 其他;
                         # }
                         # 若选 "6"，填写下一项; """

not_boarder_note = ""  # 若 not_boarder_reason 为 "6" (其他)，则要填写原因;

# 北航地址
boarder_address = "北京市海淀区花园路街道北京航空航天大学学生公寓15号楼北京航空航天大学学院路校区"
boarder_area = "北京市 海淀区"
boarder_city = "北京市"
boarder_province = "北京市"

# 离校去往住址
set_address = "xx市xx区xxxx小区xxx楼"  # 填写离校去往地址;
set_area = "xx省 xx市/州 xx区/市"  # 例如 "北京市 延庆区"；"广东省 深圳市 福田区";
set_city = "xx市"  # 例如 "北京市"；"深圳市";
set_province = "xx省/市"  # 例如 "北京市"；"广东省";

##################################################################################################

userdata = {"username": username, "password": password}

main_app = "https://app.buaa.edu.cn"
login_url = main_app + "/uc/wap/login/check"
info_url = main_app + "/buaaxsncov/wap/default/get-info"
save_url = main_app + "/buaaxsncov/wap/default/save"

print("北航师生报平安系统")


def out(str):
    print(time.strftime("%Y.%m.%d %H:%M:%S: ", time.localtime(time.time())) + str)
    bot_post(str)


def encode_formdata(obj):
    str = []
    for key in obj:
        str.append(parse.unquote(key) + "=" + parse.unquote(obj[key]))

    return_str = "&".join(str)
    return return_str


def check():
    session = requests.session()
    header = {"Content-Type": "application/x-www-form-urlencoded"}
    log_data = encode_formdata(userdata)
    # login

    resp = session.post(url=login_url, data=log_data, headers=header)

    verify = json.loads(resp.content.decode("utf-8"), parse_int=str)

    if (verify["e"] != "0" and verify["e"] != "1") or (resp.status_code != 200):
        out("Login Failed.")
        out("Status Code: %s" % verify["e"])
        print("\n登录失败！%s" % verify["m"])
        return

    print(time.strftime("%Y.%m.%d %H:%M:%S: ", time.localtime(time.time())) + "Login Success!")

    req_info = session.post(url=info_url, headers=header)

    info_data = json.loads(req_info.content.decode("utf-8"), parse_int=str)

    if req_info.status_code != 200:
        out("Rediret Failed.")
        out("获取信息失败！请检查网络环境，或稍后再试一次")
        return

    save_data = {
        "sfzs": "",
        "bzxyy": "", "bzxyy_other": "",
        "brsfzc": "1", "tw": "", "sfcxzz": "", "zdjg": "",
        "zdjg_other": "", "sfgl": "", "gldd": "",
        "gldd_other": "", "glyy": "", "glyy_other": "",
        "gl_start": "", "gl_end": "", "sfmqjc": "",
        "sfzc_14": "1", "sfqw_14": "", "sfqw_14_remark": "",
        "sfzgfx": "", "sfzgfx_remark": "",
        "sfjc_14": "", "sfjc_14_remark": "", "sfjcqz_14": "",
        "sfjcqz_14_remark": "", "sfgtjz_14": "",
        "sfgtjz_14_remark": "", "szsqqz": "", "sfyqk": "",
        "szdd": "1", "area": "",
        "city": "", "province": "",
        "address": "",
        "gwdz": "", "is_move": "", "move_reason": "", "move_remark": "",
        "realname": "", "number": "", "uid": "", "created": "",
        "date": "", "id": ""
    }
    if boarder == "0":
        save_data["sfzs"] = "0"
        save_data["bzxyy"] = not_boarder_reasen
        if not_boarder_reasen == "6":
            save_data["bzxyy_other"] = not_boarder_note
        save_data["area"] = set_area
        save_data["city"] = set_city
        save_data["province"] = set_province
        save_data["address"] = set_address

    else:
        save_data["sfzs"] = "1"
        save_data["area"] = boarder_area
        save_data["city"] = boarder_city
        save_data["province"] = boarder_province
        save_data["address"] = boarder_address

    save_data["realname"] = info_data["d"]["uinfo"]["realname"]
    save_data["number"] = info_data["d"]["uinfo"]["role"]["number"]
    save_data["uid"] = info_data["d"]["info"]["uid"]
    save_data["created"] = info_data["d"]["info"]["created"]
    save_data["date"] = info_data["d"]["info"]["date"]
    save_data["id"] = info_data["d"]["info"]["id"]

    encode_data = encode_formdata(save_data).encode("utf-8")
    req_save = session.post(save_url, headers=header, data=encode_data)

    resp_json = json.loads(req_save.content.decode("utf-8"), parse_int=str)

    # out(str(resp_json))
    out("请求上传成功！ \n\n提示：%s" % (resp_json["m"]))


if __name__ == "__main__":
    check()
    pass
