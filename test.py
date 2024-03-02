import hashlib

input_str1 = 'cb065e6279736854e0c884c1ded3584b454dba83e61668a85b906aef5daf0427'
input_str2 = '146f265d860425e994f5668a6e66863c69f0392da3bcdddfc836fcd5ce19f660'
print(hashlib.sha256(input_str1.encode()).hexdigest())
print(hashlib.sha256(input_str2.encode()).hexdigest())
