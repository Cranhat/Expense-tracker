import hashlib

def hash_password(password):
    encoded_password = password.encode('utf-8')
    
    hash_object = hashlib.sha256(encoded_password)
    
    hashed_password = hash_object.hexdigest()
    
    return hashed_password


def verify_password(entered_password, stored_hash):
    computed_hash = hash_password(entered_password)
    
    return computed_hash == stored_hash