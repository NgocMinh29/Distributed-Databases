# Kết nối đến máy 2
import requests 

# Thông tin kết nối CouchDB máy  

COUCHDB_URL = "http:// 26.214.245.195:5984"  

USERNAME = "thuy" 

PASSWORD = "34"  

#Câu 1: Lấy danh sách sinh viên thuộc khoa Du lịch (DL) có điểm môn học >= 8.0 

import requests 

COUCHDB_URL_THUY = "http://26.214.245.195:5984" 
AUTH_THUY = ("Thuy", "123") 

def query_dangky_diem_cao(): 
    url = f"{COUCHDB_URL_THUY}/dangky/_find" 
    selector = { 
        "selector": { 
            "diem": {"$gte": 8.0} 
        } 
    } 
    response = requests.post(url, auth=AUTH_THUY, json=selector) 
    if response.status_code == 200: 
        return response.json()["docs"] 
    else: 
        print("Lỗi truy vấn dangky:", response.text) 
        return [] 
    
def query_sinhvien_dulich(mssv_list): 
    url = f"{COUCHDB_URL_THUY}/sinhvien/_find" 
    selector = { 
        "selector": { 
            "makhoa": "DL", 
            "mssv": {"$in": mssv_list} 
        } 
    } 
    response = requests.post(url, auth=AUTH_THUY, json=selector) 
    if response.status_code == 200: 
        return response.json()["docs"] 
    else: 
        print("Lỗi truy vấn sinhvien:", response.text) 
        return [] 

dangky_docs = query_dangky_diem_cao() 
mssv_list = list(set([doc["mssv"] for doc in dangky_docs])) 
sinhvien_docs = query_sinhvien_dulich(mssv_list) 
sv_map = {sv["mssv"]: sv["hoten"] for sv in sinhvien_docs} 

for dk in dangky_docs: 
    if dk["mssv"] in sv_map: 
        print(f"MSSV: {dk['mssv']}, Họ tên: {sv_map[dk['mssv']]}, Môn: {dk['mamon']}, Điểm: {dk['diem']}")  
#Câu 2: Tìm sinh viên có điểm lớn hơn 8 
 
import requests 

url = "http://26.214.245.195:5984/dangky/_find" 

payload = { 
    "selector": { 
        "diem": { "$gt": 8 } 
    } 
} 
res = requests.post(url, auth=("Thuy", "123"), json=payload) 
data = res.json() 
if data.get("docs") and len(data["docs"]) > 0: 
    for doc in data["docs"]: 
        print(doc) 
else: 
    print("Không có")     

#Câu 3: Lấy danh sách sinh viên khoa "KT" và mã sinh viên lớn hơn "SV0007" 

import requests 
url = "http://26.214.245.195:5984/sinhvien/_find" 

payload = { 
    "selector": { 
        "$and": [ 
            {"makhoa": "KT"}, 
            {"mssv": {"$gt": "SV0007"}} 
        ] 
    } 
} 

res = requests.post(url, auth=("Thuy", "123"), json=payload) 
data = res.json() 
if data.get("docs") and len(data["docs"]) > 0: 
    for doc in data["docs"]: 
        print(doc) 
else: 
    print("Không có")     

#Câu 4:  Lấy danh sách sinh viên có điểm đăng ký từ 7.5 trở lên trong học kỳ "HK2-2024", kèm theo họ tên và thông tin môn học đã đăng ký. 
 
import requests 

COUCHDB_URL_THUY = "http://26.214.245.195:5984" 
AUTH_THUY = ("Thuy", "123") 

def query_dangky(diem_min, hocky): 
    url = f"{COUCHDB_URL_THUY}/dangky/_find" 
    selector = { 
        "selector": { 
            "diem": {"$gte": diem_min}, 
            "hocky": {"$eq": hocky} 
        } 
    } 
    response = requests.post(url, auth=AUTH_THUY, json=selector) 
    if response.status_code == 200: 
        return response.json()["docs"] 
    else: 
        print("Lỗi truy vấn dangky:", response.text) 
        return [] 

def query_sinhvien(mssv_list): 
    url = f"{COUCHDB_URL_THUY}/sinhvien/_find" 
    selector = { 
        "selector": { 
            "mssv": {"$in": mssv_list} 
        } 
    } 
    response = requests.post(url, auth=AUTH_THUY, json=selector) 
    if response.status_code == 200: 
        return response.json()["docs"] 
    else: 
        print("Lỗi truy vấn sinhvien:", response.text) 
        return [] 

dangky_docs = query_dangky(7.5, "HK2-2024") 
mssv_list = list(set([doc["mssv"] for doc in dangky_docs])) 
sinhvien_docs = query_sinhvien(mssv_list) 
sinhvien_map = {sv["mssv"]: sv for sv in sinhvien_docs} 

for dk in dangky_docs: 
    sv = sinhvien_map.get(dk["mssv"], {}) 
    hoten = sv.get("hoten", "Không rõ") 
    print(f"MSSV: {dk['mssv']}, Họ tên: {hoten}, Môn: {dk['mamon']}, Điểm: {dk['diem']}, Học kỳ: {dk['hocky']}") 

#Câu 5: Tổng tín chỉ đã đăng ký mỗi sinh viên     
 
import requests 
from collections import defaultdict 

# Thông tin kết nối đến CouchDB máy Thúy 

COUCHDB_URL = "http://26.214.245.195:5984" 
USERNAME = "Thuy" 
PASSWORD = "123" 
def get_all_docs(db_name): 
    url = f"{COUCHDB_URL}/{db_name}/_all_docs?include_docs=true" 
    res = requests.get(url, auth=(USERNAME, PASSWORD)) 
    if res.status_code == 200: 
        return [row['doc'] for row in res.json()['rows']] 
    else: 
        print(f"Lỗi lấy dữ liệu từ {db_name}: {res.text}") 
        return [] 
    
mon = {m["_id"]: m.get("sotinchi", 0) for m in get_all_docs("monhoc")} 
dk_list = get_all_docs("dangky") 
tinchi_dict = defaultdict(int) 

for dk in dk_list: 
    mssv = dk.get("mssv") 
    mamon = dk.get("mamon") 
    sotinchi = mon.get(mamon, 0) 
    tinchi_dict[mssv] += sotinchi 
    
print("TỔNG TÍN CHỈ ĐÃ ĐĂNG KÝ:") 

for mssv, tong in tinchi_dict.items(): 
    print(f"- {mssv}: {tong} tín chỉ")     
    
