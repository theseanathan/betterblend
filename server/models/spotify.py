

class Spotify():
    auth_token = None
    refresh_token = None

    req_header = {'Authorization': 'Bearer {token}'}

    def __init__(self, token):
        self.auth_token = token
