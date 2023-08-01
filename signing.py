import time, hmac, hashlib
from dataclasses import dataclass
# These are extracted from libreddit-ndk.so and used to create SIGNING_KEY, I didn't spend my time to reverse engineer it so I hardcoded the SIGNING_KEY.
# MAP = b'\xd1\t\xcbc\x164#\xe6\xcf\x90\xf1\x18-\xb9\x0f,\xb5\x00\x8a\x1d\xf2\x06\x9bQ\xd6\xa4e>\xd5\xac\x07Tn\xadvi@\x88r\x95\x98\x1f\xf8Y\xeaoP\xa3\x12U\x87p\xc2\xd4\x01x\x10a\x84]\xd0\x82L\x03\x17\xc0\xf5\xf3_\xa5B\x971*\xa8G\\M\x93\x02$d0\x8d!\xc1+\xe8S\x83\x85I\xa2\x117\xbeH\xb6\xf6\x9e&5\x04\x0egk\xc3\xd9\xdd\x9f\xeb\x14~\xbas\x80\xb8\xbd\xfa\xcaw\xd7\xc8u\xe2\xbb\xe3\x1c\x966\xa9\r\xaa?\xc7\xb1b8\x0b\xfc\xa0\'{\xb2\xe5\xfb\xc9\x15q\xf4\x1b\xfeD.Zy\xa7\x19\xfd;\x8b"\xa1\xec\xdffJ\xed \x86=l^\x99C\xaf\xe1\n\xef\xd3\x13\xde\x94h\xb4\xcdj\xdc\xff<}\xe7\x91)%\xc53mz9\xe4:O\x1e\xdbAVN\x9c\x81\xe9\xb7\xbf\xe0\x9aR\xc4\x8c\x7f\x0cW/\xabt\x1a\x92EF\xceK\xbc\xf0\x89\xf9\xb0\xb3\xd2X\x08\xcc\xd8\xc6\xda2\xa6(\xee[\x8f\x05\xae\x9d`\x8e\xf7|'
# KEY = b'\x89\x03^9\x8899e\xa5\xc7Re\xa5^R\x05RR\x03\x89H\x88\xa5\xc49H9HRH\x1a^e\xa5^\xf3HRHR\x05\x88H\xc7\xc7H\xa5R\x03Qe\xf3\x05R99\x89R\x03\x05Q\xc7\xc7Q\x11'

SIGNING_KEY = b'8c7abaa5f905f70400c81bf3a1a101e75f7210104b1991f0cd5240aa80c4d99d'

@dataclass
class HMACHeader:
    hmac_signed_body: str
    hmac_signed_result: str
    epoch: int


def current_epoch():
    milliseconds = int(round(time.time() * 1000))
    return milliseconds // 1000

def hash(key, data):
    mac = hmac.new(key, data, hashlib.sha256)
    do_final = mac.digest()
    return do_final.hex()

def format_epoch_body(epoch: int, body: str):
    return f"Epoch:{epoch}|Body:{body}"

def format_epoch_useragent_client_vendor_id(epoch, useragent, client_vendor_id):
    return f"Epoch:{epoch}|User-Agent:{useragent}|Client-Vendor-ID:{client_vendor_id}"

def format_hash_as_header(hash, epoch):
    return f"1:android:2:{epoch}:{hash}"


def get_hmac_header(epoch:int, body: str, user_agent: str, device_id: str):
    hmac_signed_body = format_hash_as_header(hash(SIGNING_KEY, format_epoch_body(epoch, body).encode()),
                                             epoch)
    hmac_signed_result = format_hash_as_header(
        hash(SIGNING_KEY, format_epoch_useragent_client_vendor_id(epoch, user_agent, device_id).encode()),
        epoch)
    return HMACHeader(hmac_signed_body, hmac_signed_result, epoch)



