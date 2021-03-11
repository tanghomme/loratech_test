import hashlib
from datetime import datetime
import json

CONFIG_TOKEN_VALIDITY_IN_SECOND = 300


class ApiCredentials:
    def __init__(self, apikey, hash_token, unix_timestamp):
        self.apikey = apikey
        self.hash_token = hash_token
        self.unix_timestamp = unix_timestamp

    def getSharedSecret(self):
        # todo: connect user database to get the shared secret by apikey
        # below is the sample of reading from file apiusers.json
        result = ""
        with open("apiusers.json", "r") as read_file:
            data = json.load(read_file)
            for x in data:
                if x['apikey'] == self.apikey:
                    print(x['shared_secret'])
                    result = x['shared_secret']
                    break
        return result

    def verifyToken(self):
        try:
            diff_in_second = (
                datetime.now()-datetime.fromtimestamp(int(self.unix_timestamp))).total_seconds()
            print(diff_in_second)
            if diff_in_second > CONFIG_TOKEN_VALIDITY_IN_SECOND:
                return False
            else:
                m = hashlib.sha512()

                data = self.apikey + self.getSharedSecret() + self.unix_timestamp
                m.update(data.encode("utf-8"))
                hashkey = m.hexdigest()
                if hashkey != self.hash_token:
                    return False
                else:
                    return True
        except:
            return False


def getApiCredentials(value):
    apikey = ""
    signature = ""
    timestamp = ""
    x = value.split(",")
    for item in x:
        if 'apikey' in item:
            apikey = item.split("=", 1)[1]
        if 'signature' in item:
            signature = item.split("=", 1)[1]
        if 'timestamp' in item:
            timestamp = item.split("=", 1)[1]

    apiCredentials = ApiCredentials(apikey, signature, timestamp)
    return apiCredentials


def validToken(value):
    apiCredentials = getApiCredentials(value)
    return apiCredentials.verifyToken()
