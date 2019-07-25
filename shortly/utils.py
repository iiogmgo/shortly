def get_random_shortly_name():
    import os
    import binascii

    return binascii.hexlify(os.urandom(3)).decode('ascii')
