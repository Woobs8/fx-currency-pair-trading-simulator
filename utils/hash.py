import hashlib

def hash_objects(objects: list) -> str:
    md5 = hashlib.md5()
    for item in objects:
        md5.update(repr(item).encode('utf-8'))
    return md5.hexdigest()