import os
import time
from aes import CTR


key = os.urandom(16)
iv = os.urandom(16)

message = b'This is a sample test message'
start_time = time.time()
encrypted = CTR(key).encrypt_ctr(message, iv)
print(CTR(key).decrypt_ctr(encrypted, iv))

print("--- %s seconds ---" % (time.time() - start_time))