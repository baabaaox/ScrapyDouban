import hashlib


def shorturl(url):
    chars = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    _hex = 0x7FFFFFF & int(str(hashlib.md5(url.encode()).hexdigest()), 16)
    code = ""
    for i in range(9):
        index = 0x0000003D & _hex
        code += chars[index]
        _hex = _hex >> 3
    return code
