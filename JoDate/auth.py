import bcrypt
import requests
from requests.exceptions import ConnectTimeout

def create_password(raw):
    # 使用bcrypt加密
    raw = raw.encode('utf-8')
    hashed = bcrypt.hashpw(raw, bcrypt.gensalt(10))
    # save hashed as a string in database
    hashed = hashed.decode('utf-8')
    return hashed

def compare_password(check,hashed):
    check = check.encode('utf-8')
    hashed = hashed.encode('utf-8')
    if bcrypt.checkpw(check, hashed):
        return True
    else:
        return False
    
def email_validation(email: str)->bool:
    # 要檢查的email
    url = "https://emailvalidation.abstractapi.com/v1/?api_key=898e021c3538404191affd53881b9bfd&email="+email
    try:     
        response = requests.get(url,timeout=10)
        json_dict = response.json()
        # 檢查email格式
        is_valid_format = json_dict["is_valid_format"]["value"]
        # email SMTP check 
        is_smtp_valid = json_dict["is_smtp_valid"]["value"]
    # 如果連線時間過長 則回傳未通過
    except ConnectTimeout:
        return False
    return is_valid_format and is_smtp_valid