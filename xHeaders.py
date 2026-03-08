import requests, os, psutil, sys, jwt, pickle, json, binascii, time, urllib3, base64, datetime, re, socket, threading, ssl
from protobuf_decoder.protobuf_decoder import Parser
from xC4 import *
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from Pb2 import MajoRLoGinrEq_pb2, MajoRLoGinrEs_pb2, PorTs_pb2

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

Hr = {
    "Accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0"
}

def GeTToK():  
    try:
        with open("token.txt") as f: return f.read().strip()
    except: return ""

def equie_emote(JWT, url):
    url = f"{url}/ChooseEmote"
    headers = Hr.copy()
    headers["Authorization"] = f"Bearer {JWT}"
    headers["ReleaseVersion"] = "OB51"
    headers["X-GA"] = "v1 1"
    data = bytes.fromhex("CA F6 83 22 2A 25 C7 BE FE B5 1F 59 54 4D B3 13")
    try: requests.post(url, headers=headers, data=data, verify=False)
    except: pass

def MajorLogin(payload):
    urls = [
        "https://loginbp.ggblueshark.com/MajorLogin",
        "https://clientbp.ggblueshark.com/MajorLogin",
        "https://login.freefiremobile.com/MajorLogin"
    ]
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; G011A Build/PI)",
        "X-Unity-Version": "2018.4.11f1",
        "ReleaseVersion": "OB51",
        "X-GA": "v1 1",
        "Connection": "Keep-Alive"
    }
    for url in urls:
        try:
            print(f"DEBUG: Trying MajorLogin at {url}...")
            response = requests.post(url, data=payload, headers=headers, verify=False, timeout=15)
            if response.status_code == 200:
                return response.content
            print(f"DEBUG: MajorLogin at {url} failed with status_code={response.status_code}")
        except Exception as e:
            print(f"DEBUG: MajorLogin at {url} exception={e}")
    return None
def GetLoginData(base_url, payload, token):
    url = f"{base_url}/GetLoginData"
    headers = Hr.copy()
    headers['Authorization'] = f"Bearer {token}"
    try:
        response = requests.post(url, data=payload, headers=headers, verify=False, timeout=15)
        if response.status_code == 200:
            return response.content
        return None
    except: return None

def DecRypTMajoRLoGin(MajoRLoGinResPonsE):
    proto = MajoRLoGinrEs_pb2.MajorLoginRes()
    proto.ParseFromString(MajoRLoGinResPonsE)
    return proto

def DecRypTLoGinDaTa(LoGinDaTa):
    proto = PorTs_pb2.GetLoginData()
    proto.ParseFromString(LoGinDaTa)
    return proto

def GeNeRaTeAccEss(uid, password):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    data = {
        "uid": uid,
        "password": password,
        "response_type": "token",
        "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067"
    }
    try:
        response = requests.post(url, data=data, verify=False, timeout=15)
        if response.status_code == 200:
            res = response.json()
            return res.get("open_id"), res.get("access_token")
        return None, None
    except: return None, None

def EncRypTMajoRLoGin(open_id, access_token):
    major_login = MajoRLoGinrEq_pb2.MajorLogin()
    major_login.event_time = str(datetime.now())[:-7]
    major_login.game_name = "free fire"
    major_login.platform_id = 1
    major_login.client_version = "1.110.1"
    major_login.system_software = "Android OS 11"
    major_login.client_version_code = "2023070101"
    major_login.graphics_api = "OpenGLES3"
    major_login.is_vpn = 0
    major_login.network_type = "WIFI"
    major_login.telecom_operator = "T-Mobile"
    major_login.screen_width = 1920
    major_login.screen_height = 1080
    major_login.screen_dpi = "440"
    major_login.processor_details = "Qualcomm Snapdragon 8 Gen 1"
    major_login.memory = 5900
    major_login.gpu_renderer = "Adreno (TM) 730"
    major_login.gpu_version = "OpenGL ES 3.2"
    major_login.unique_device_id = "Google|a8b9c0d1-e2f3-4a4b-5c6d-7e8f9a0b1c2d"
    major_login.client_ip = "202.81.106.16"
    major_login.language = "en"
    major_login.open_id = open_id
    major_login.open_id_type = "4"
    major_login.device_type = "Handheld"
    major_login.access_token = access_token
    major_login.platform_sdk_id = 1
    major_login.login_by = 3
    major_login.channel_type = 3
    major_login.is_64bit = 1
    major_login.os_type = 1
    major_login.device_model = "SM-G981B"
    major_login.bundle_id = "com.dts.freefireth"
    major_login.is_emulator = 0
    major_login.os_api_level = 29
    major_login.manufacturer = "Samsung"
    major_login.app_id = "com.dts.freefireth"
    major_login.android_id = "34a7dcdf"
    major_login.mac_address = "02:00:00:00:00:00"
    major_login.device_brand = "Samsung"
    major_login.google_aid = "34a7dcdf-a7d5-4cb6-8d7e-3b0e448a0c57"

    
    # Try different client versions or device IDs if login fails
    # major_login.client_version = "1.111.1" 
    
    return encrypted_proto(major_login.SerializeToString())