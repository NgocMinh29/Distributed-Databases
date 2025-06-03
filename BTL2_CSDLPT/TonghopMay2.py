# TẠO BẢNG
import requests
# Thông tin CouchDB
COUCHDB_URL = "http://26.214.245.195:5984"
USERNAME = "Thuy"
PASSWORD = "123"
def create_database(db_name):
    response = requests.put(f"{COUCHDB_URL}/{db_name}", auth=(USERNAME, PASSWORD))
    if response.status_code in [201, 202]:
        print(f"✅ Đã tạo database: {db_name}")
    elif response.status_code == 412:
        print(f"⚠️ Database {db_name} đã tồn tại.")
    else:
        print(f"❌ Lỗi tạo database {db_name}: {response.text}")

# Tạo các database
databases = ["sinhvien", "monhoc", "dangky", "khoa"]
for db in databases:
    create_database(db)
# INSERT DỮ LIỆU

import requests

# Thông tin kết nối CouchDB máy Thúy
COUCHDB_URL = "http://26.214.245.195:5984"  
USERNAME = "Thuy"
PASSWORD = "123"

def insert_document(db_name, document):
    url = f"{COUCHDB_URL}/{db_name}"
    response = requests.post(url, auth=(USERNAME, PASSWORD), json=document)
    if response.status_code in [201, 202]:
        print(f"✅ Đã thêm vào {db_name}: {document['_id']}")
    else:
        print(f"❌ Lỗi thêm {document['_id']} vào {db_name}: {response.text}")

# Dữ liệu mẫu 5 dòng cho mỗi bảng, nối tiếp _id từ máy Ngân

danh_sach_sinhvien = [
   {"_id": "SV006", "type": "sinhvien", "mssv": "SV0006", "hoten": "Lê Thị Thúy A", "makhoa": "DL"},
    {"_id": "SV007", "type": "sinhvien", "mssv": "SV0007", "hoten": "Phạm Văn Thúy B", "makhoa": "KT"},
    {"_id": "SV008", "type": "sinhvien", "mssv": "SV0008", "hoten": "Nguyễn Thúy C", "makhoa": "DL"},
    {"_id": "SV009", "type": "sinhvien", "mssv": "SV0009", "hoten": "Trần Thúy D", "makhoa": "KT"},
    {"_id": "SV010", "type": "sinhvien", "mssv": "SV0010", "hoten": "Hoàng Thúy E", "makhoa": "DL"},
    
  
]

danh_sach_monhoc = [
    {"_id": "MH006", "type": "monhoc", "tenmon": "Kinh tế vi mô", "sotinchi": 3},
    {"_id": "MH007", "type": "monhoc", "tenmon": "Luật kinh doanh", "sotinchi": 3},
    {"_id": "MH008", "type": "monhoc", "tenmon": "Marketing căn bản", "sotinchi": 2},
    {"_id": "MH009", "type": "monhoc", "tenmon": "Quản trị nhân sự", "sotinchi": 3},
    {"_id": "MH010", "type": "monhoc", "tenmon": "Tài chính doanh nghiệp", "sotinchi": 3},
     
]

danh_sach_khoa = [
    {"_id": "DL", "type": "khoa", "tenkhoa": "Du lịch", "sdt": "028.1357.2468"},
    {"_id": "KT", "type": "khoa", "tenkhoa": "Kế toán", "sdt": "028.2468.1357"},
    {"_id": "NV", "type": "khoa", "tenkhoa": "Ngân hàng", "sdt": "028.3333.4444"},
    {"_id": "MK", "type": "khoa", "tenkhoa": "Marketing", "sdt": "028.5555.6666"},
    {"_id": "QL", "type": "khoa", "tenkhoa": "Quản lý", "sdt": "028.7777.8888"},
]

danh_sach_dangky = [
    {"_id": "DK006", "type": "dangky", "mssv": "SV0006", "mamon": "MH006", "hocky": "HK2-2024", "diem": 7.5},
    {"_id": "DK007", "type": "dangky", "mssv": "SV0007", "mamon": "MH007", "hocky": "HK2-2024", "diem": 8.0},
    {"_id": "DK008", "type": "dangky", "mssv": "SV0008", "mamon": "MH008", "hocky": "HK2-2024", "diem": 7.0},
    {"_id": "DK009", "type": "dangky", "mssv": "SV0009", "mamon": "MH009", "hocky": "HK2-2024", "diem": 8.5},
    {"_id": "DK010", "type": "dangky", "mssv": "SV0010", "mamon": "MH010", "hocky": "HK2-2024", "diem": 9.0},
    
]

# Thêm dữ liệu vào CouchDB
for sv in danh_sach_sinhvien:
    insert_document("sinhvien", sv)

for mh in danh_sach_monhoc:
    insert_document("monhoc", mh)

for kh in danh_sach_khoa:
    insert_document("khoa", kh)

for dk in danh_sach_dangky:
    insert_document("dangky", dk)
# CÁC CÂU TRUY VẤN 
#câu  1 ; Lấy danh sách sinh viên thuộc khoa Công nghệ thông tin (CNTT) đã đăng ký môn “Lập trình Java” trong học kỳ HK2-2024 và đạt điểm từ 7 trở lên.
import requests

COUCHDB_URL = "http://26.245.44.25:5984"
AUTH = ("ngan", "12")

def query_database(db_name, mango_query):
    url = f"{COUCHDB_URL}/{db_name}/_find"
    response = requests.post(url, auth=AUTH, json=mango_query)
    if response.status_code == 200:
        return response.json().get("docs", [])
    else:
        print(f"❌ Lỗi truy vấn {db_name}: {response.status_code} - {response.text}")
        return []

# Bước 1: Lấy mã môn "Lập trình Java"
monhoc_docs = query_database("monhoc", {
    "selector": {
        "type": "monhoc",
        "tenmon": "Lập trình Java"
    }
})
if not monhoc_docs:
    print("Không tìm thấy môn học 'Lập trình Java'")
    exit()

mamon = monhoc_docs[0]["_id"]

# Bước 2: Lấy các lượt đăng ký môn đó, điểm >= 7, học kỳ HK2-2024
dangky_docs = query_database("dangky", {
    "selector": {
        "type": "dangky",
        "mamon": mamon,
        "hocky": "HK2-2024",
        "diem": { "$gte": 7.0 }
    }
})
mssv_list = list({dk["mssv"] for dk in dangky_docs})

# Bước 3: Truy sinh viên thuộc khoa CNTT
sinhvien_docs = query_database("sinhvien", {
    "selector": {
        "type": "sinhvien",
        "makhoa": "CNTT",
        "mssv": { "$in": mssv_list }
    }
})
sv_map = {sv["mssv"]: sv["hoten"] for sv in sinhvien_docs}

# Bước 4: Ghép dữ liệu và in
print("\n📋 Danh sách sinh viên khoa CNTT học 'Lập trình Java' đạt điểm >= 7.0 (HK2-2024):\n")
for dk in dangky_docs:
    mssv = dk["mssv"]
    if mssv in sv_map:
        print(f"- MSSV: {mssv} | Họ tên: {sv_map[mssv]} | Điểm: {dk['diem']}")
 

#cau 2 : Lấy danh sách sinh viên thuộc khoa Quản trị kinh doanh (QTKD) đã đăng ký học môn “Hệ điều hành” trong học kỳ HK2-2024.
import requests

COUCHDB_URL = "http://26.245.44.25:5984"
AUTH = ("ngan", "12")

def query_database(db_name, mango_query):
    url = f"{COUCHDB_URL}/{db_name}/_find"
    response = requests.post(url, auth=AUTH, json=mango_query)
    if response.status_code == 200:
        return response.json().get("docs", [])
    else:
        print(f"❌ Lỗi truy vấn {db_name}: {response.status_code} - {response.text}")
        return []
# --- Bước 1: Lấy mã môn học "Hệ điều hành" ---
monhoc_docs = query_database("monhoc", {
    "selector": {
        "type": "monhoc",
        "tenmon": "Hệ điều hành"
    }
})
if not monhoc_docs:
    print("Không tìm thấy môn học 'Hệ điều hành'")
    exit()

mamon = monhoc_docs[0]["_id"]

# --- Bước 2: Lấy danh sách MSSV đã đăng ký môn đó trong HK2-2024 ---
dangky_docs = query_database("dangky", {
    "selector": {
        "type": "dangky",
        "mamon": mamon,
        "hocky": "HK2-2024"
    }
})
mssv_list = list({dk["mssv"] for dk in dangky_docs})

# --- Bước 3: Truy vấn sinh viên thuộc khoa QTKD có trong danh sách mssv ---
sinhvien_docs = query_database("sinhvien", {
    "selector": {
        "type": "sinhvien",
        "makhoa": "QTKD",
        "mssv": { "$in": mssv_list }
    }
})
sv_map = {sv["mssv"]: sv["hoten"] for sv in sinhvien_docs}

# --- Bước 4: Ghép kết quả và in ---
print("\n📋 Danh sách sinh viên khoa QTKD học 'Hệ điều hành' trong HK2-2024:\n")
for dk in dangky_docs:
    mssv = dk["mssv"]
    if mssv in sv_map:
        print(f"- MSSV: {mssv} | Họ tên: {sv_map[mssv]} | Điểm: {dk['diem']}")
#câu 3 ; Liệt kê tất cả sinh viên đã đăng ký học kỳ HK2-2024, kèm theo tên môn học, điểm số, họ tên sinh viên và tên khoa tương ứng.

# --- Bước 1: Lấy danh sách đăng ký học kỳ HK2-2024 ---
import requests

COUCHDB_URL = "http://26.245.44.25:5984"
AUTH = ("ngan", "12")

def query_database(db_name, mango_query):
    url = f"{COUCHDB_URL}/{db_name}/_find"
    response = requests.post(url, auth=AUTH, json=mango_query)
    if response.status_code == 200:
        return response.json().get("docs", [])
    else:
        print(f"❌ Lỗi truy vấn {db_name}: {response.status_code} - {response.text}")
        return []
dangky_docs = query_database("dangky", {
    "selector": {
        "type": "dangky",
        "hocky": "HK2-2024"
    }
})

mssv_set = {dk["mssv"] for dk in dangky_docs}
mamon_set = {dk["mamon"] for dk in dangky_docs}

# --- Bước 2: Lấy sinh viên theo mssv ---
sinhvien_docs = query_database("sinhvien", {
    "selector": {
        "type": "sinhvien",
        "mssv": { "$in": list(mssv_set) }
    }
})
sv_map = {sv["mssv"]: (sv["hoten"], sv["makhoa"]) for sv in sinhvien_docs}

# --- Bước 3: Lấy môn học theo mamon ---
monhoc_docs = query_database("monhoc", {
    "selector": {
        "type": "monhoc",
        "_id": { "$in": list(mamon_set) }
    }
})
mh_map = {mh["_id"]: mh["tenmon"] for mh in monhoc_docs}

# --- Bước 4: In kết quả ---
print("\n📋 Danh sách đăng ký học kỳ HK2-2024 kèm đầy đủ thông tin:\n")
for dk in dangky_docs:
    mssv = dk["mssv"]
    mamon = dk["mamon"]
    if mssv in sv_map and mamon in mh_map:
        hoten, makhoa = sv_map[mssv]
        tenmon = mh_map[mamon]
        print(f"- MSSV: {mssv} | Họ tên: {hoten} | Khoa: {makhoa} | Môn: {tenmon} | Điểm: {dk['diem']}")
# Cau 4: Liệt kê danh sách sinh viên đã đăng ký bất kỳ môn học nào có số tín chỉ từ 3 trở lên trong học kỳ HK2-2024, kèm theo tên môn, số tín chỉ, họ tên và điểm
import requests
COUCHDB_URL = "http://26.245.44.25:5984"
AUTH = ("ngan", "12")

def query_database(db_name, mango_query):
    url = f"{COUCHDB_URL}/{db_name}/_find"
    response = requests.post(url, auth=AUTH, json=mango_query)
    if response.status_code == 200:
        return response.json().get("docs", [])
    else:
        print(f"❌ Lỗi truy vấn {db_name}: {response.status_code} - {response.text}")
        return []
# Bước 1: Lấy danh sách môn học có số tín chỉ >= 3
monhoc_docs = query_database("monhoc", {
    "selector": {
        "type": "monhoc",
        "sotinchi": { "$gte": 3 }
    }
})
ds_mamon = [mh["_id"] for mh in monhoc_docs]
mh_map = {mh["_id"]: (mh["tenmon"], mh["sotinchi"]) for mh in monhoc_docs}

# Bước 2: Lấy các đăng ký liên quan
dangky_docs = query_database("dangky", {
    "selector": {
        "type": "dangky",
        "hocky": "HK2-2024",
        "mamon": { "$in": ds_mamon }
    }
})
ds_mssv = list({dk["mssv"] for dk in dangky_docs})

# Bước 3: Lấy sinh viên liên quan
sinhvien_docs = query_database("sinhvien", {
    "selector": {
        "type": "sinhvien",
        "mssv": { "$in": ds_mssv }
    }
})
sv_map = {sv["mssv"]: sv["hoten"] for sv in sinhvien_docs}

# Bước 4: In kết quả
print("\n📋 Danh sách sinh viên đăng ký các môn >=3 tín chỉ trong HK2-2024:\n")
for dk in dangky_docs:
    mamon = dk["mamon"]
    mssv = dk["mssv"]
    if mamon in mh_map and mssv in sv_map:
        tenmon, tc = mh_map[mamon]
        print(f"- MSSV: {mssv} | Họ tên: {sv_map[mssv]} | Môn: {tenmon} | Tín chỉ: {tc} | Điểm: {dk['diem']}")
#Cau 5 : Lấy danh sách sinh viên đã đăng ký ít nhất 2 môn trong học kỳ HK2-2024 nhưng có điểm trung bình dưới 7.0, nhằm phát hiện các trường hợp quá tải học phần có thể ảnh hưởng đến kết quả học tập.
import requests
from collections import defaultdict
COUCHDB_URL = "http://26.245.44.25:5984"
AUTH = ("ngan", "12")

def query_database(db_name, mango_query):
    url = f"{COUCHDB_URL}/{db_name}/_find"
    response = requests.post(url, auth=AUTH, json=mango_query)
    if response.status_code == 200:
        return response.json().get("docs", [])
    else:
        print(f"❌ Lỗi truy vấn {db_name}: {response.status_code} - {response.text}")
        return []
# Bước 1: Lấy tất cả lượt đăng ký trong HK2-2024
dangky_docs = query_database("dangky", {
    "selector": {
        "type": "dangky",
        "hocky": "HK2-2024"
    }
})

# Bước 2: Gom nhóm theo MSSV
diem_map = defaultdict(list)
for dk in dangky_docs:
    diem_map[dk["mssv"]].append(dk["diem"])

# Bước 3: Tìm MSSV có >= 2 môn và điểm TB < 7.0
mssv_can_canh_bao = []
for mssv, diem_list in diem_map.items():
    if len(diem_list) >= 2:
        avg = sum(diem_list) / len(diem_list)
        if avg < 7.0:
            mssv_can_canh_bao.append((mssv, avg, len(diem_list)))

# Bước 4: Truy sinh viên để lấy tên
if mssv_can_canh_bao:
    mssv_only = [item[0] for item in mssv_can_canh_bao]
    sinhvien_docs = query_database("sinhvien", {
        "selector": {
            "type": "sinhvien",
            "mssv": { "$in": mssv_only }
        }
    })
    sv_map = {sv["mssv"]: sv for sv in sinhvien_docs}

    # Bước 5: In kết quả
    print("\n⚠️ Danh sách sinh viên học ≥ 2 môn nhưng điểm trung bình < 7.0 trong HK2-2024:\n")
    for mssv, avg, sl in mssv_can_canh_bao:
        sv = sv_map.get(mssv)
        if sv:
            print(f"- MSSV: {mssv} | Họ tên: {sv['hoten']} | Khoa: {sv['makhoa']}")
            print(f"  Số môn: {sl} | Điểm TB: {avg:.2f}")
            print("-" * 60)
else:
    print("✅ Không có sinh viên nào rơi vào nhóm điểm thấp này (ít nhất là theo dữ liệu hiện tại).")

# CÁC THAO TÁC CREATE - READ -UPDATE- DELETE

#   THAO TÁC READ (MÁY NGÂN)

import requests

local_db = {
    "name": "Máy Ngân",
    "ip": "26.245.44.25",
    "user": "ngan",
    "password": "12",
    "db": "monhoc"
}

def build_all_docs_url(db_info):
    return f"http://{db_info['user']}:{db_info['password']}@{db_info['ip']}:5984/{db_info['db']}/_all_docs?include_docs=true"

def get_all_documents(db_info):
    url = build_all_docs_url(db_info)
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        docs = [row['doc'] for row in data['rows']]
        return docs
    else:
        print("❌ Lỗi khi lấy dữ liệu:", res.status_code, res.text)
        return []

if __name__ == "__main__":
    all_docs = get_all_documents(local_db)
    print(f"✅ Tổng số môn học: {len(all_docs)}")
    for doc in all_docs:
        print(doc)
import requests

# Cấu hình CouchDB sau khi thay IP và tài khoản
local_db = {
    "name": "Máy Thúy",
    "ip": "26.214.245.195",
    "user": "Thuy",
    "password": "123",
    "db": "sinhvien"
}

remote_db = {
    "name": "Máy Ngân",
    "ip": "26.245.44.25",
    "user": "ngan",
    "password": "12",
    "db": "sinhvien"
}

# Tạo URL kết nối CouchDB
def build_url(db_info, doc_id=None):
    base = f"http://{db_info['user']}:{db_info['password']}@{db_info['ip']}:5984/{db_info['db']}"
    return f"{base}/{doc_id}" if doc_id else base

# Kiểm tra document có tồn tại không
def document_exists(db_info, doc_id):
    res = requests.get(build_url(db_info, doc_id))
    return res.status_code == 200

# Thêm document
def create_document(db_info, doc):
    res = requests.post(build_url(db_info), json=doc)
    return res.status_code == 201, res.json()

# === CHƯƠNG TRÌNH CHÍNH ===
if __name__ == '__main__':
    print("🔸 Nhập thông tin sinh viên:")
    doc_id = input("Nhập _id (ví dụ: SV001): ").strip()
    mssv = input("Mã số sinh viên (mssv): ").strip()
    hoten = input("Họ tên: ").strip()
    makhoa = input("Mã khoa: ").strip()

    sinhvien_doc = {
        "_id": doc_id,
        "type": "sinhvien",
        "mssv": mssv,
        "hoten": hoten,
        "makhoa": makhoa
    }

    if document_exists(remote_db, doc_id):
        print("❌ _id đã tồn tại ở máy Ngân.")
    elif document_exists(local_db, doc_id):
        print("❌ _id đã tồn tại ở máy Thúy.")
    else:
        success, response = create_document(remote_db, sinhvien_doc)
        if success:
            print("✅ Đã thêm sinh viên vào máy Ngân.")
        else:
            print("❌ Lỗi khi thêm vào máy Ngân:", response)
import requests
remote_db = {
    "name": "Máy Ngân",
    "ip": "26.245.44.25",
    "user": "ngan",
    "password": "12",
    "db": "sinhvien"
}

def build_url(db_info, doc_id=None):
    base = f"http://{db_info['user']}:{db_info['password']}@{db_info['ip']}:5984/{db_info['db']}"
    return f"{base}/{doc_id}" if doc_id else base

def get_document(db_info, doc_id):
    res = requests.get(build_url(db_info, doc_id))
    if res.status_code == 200:
        return res.json()
    else:
        print(f"❌ Document {doc_id} không tồn tại trên {db_info['name']}.")
        return None

def update_document(db_info, doc_id, updated_fields):
    doc = get_document(db_info, doc_id)
    if not doc:
        return False
    doc.update(updated_fields)
    res = requests.put(build_url(db_info, doc_id), json=doc)
    if res.status_code == 201:
        print(f"✅ Đã cập nhật document {doc_id} trên {db_info['name']}.")
        return True
    else:
        print(f"❌ Lỗi khi cập nhật document {doc_id}:", res.json())
        return False

if __name__ == "__main__":
    doc_id = input("Nhập _id sinh viên muốn cập nhật trên máy Ngân: ").strip()
    field = input("Nhập tên trường muốn cập nhật (ví dụ: hoten): ").strip()
    value = input("Nhập giá trị mới: ").strip()
    update_document(remote_db, doc_id, {field: value})
# THAO TÁC DELETE
import requests
thuy_db = {
    "name": "Máy Thúy",
    "ip": "26.214.245.195",
    "user": "Thuy",
    "password": "123",
    "db": "sinhvien"
}

ngan_db = {
    "name": "Máy Ngân",
    "ip": "26.245.44.25",
    "user": "ngan",
    "password": "12",
    "db": "sinhvien"
}

def build_url(db_info, doc_id=None):
    base = f"http://{db_info['user']}:{db_info['password']}@{db_info['ip']}:5984/{db_info['db']}"
    return f"{base}/{doc_id}" if doc_id else base

def get_document(db_info, doc_id):
    res = requests.get(build_url(db_info, doc_id))
    if res.status_code == 200:
        return res.json()
    else:
        print(f"❌ Document {doc_id} không tồn tại trên {db_info['name']}.")
        return None

def delete_document(db_info, doc_id):
    doc = get_document(db_info, doc_id)
    if not doc:
        return False
    rev = doc["_rev"]
    res = requests.delete(build_url(db_info, doc_id) + f"?rev={rev}")
    if res.status_code == 200:
        print(f"✅ Đã xóa document {doc_id} trên {db_info['name']}.")
        return True
    else:
        print(f"❌ Lỗi khi xóa document {doc_id}:", res.json())
        return False

if __name__ == "__main__":
    doc_id = input("Nhập _id sinh viên muốn xóa trên máy Ngân: ").strip()
    delete_document(ngan_db, doc_id)
