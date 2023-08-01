import json
import requests, uuid
import signing



class Reddit:

    def __init__(self):
        self.session = requests.Session()
        self.device_id = str(uuid.uuid4())
        self.adversary_id = str(uuid.uuid4())
        self.x_reddit_loid = ""
        self.x_reddit_session = ""
        self.user_agent = 'Reddit/Version 2023.29.0/Build 1059855/Android 12'
        self.session.verify = False



        self.get_basic_access_token()
        self.verify_token()

    def register(self, e_mail : str, username : str, password : str):

        json_data = {
          "username": username,
          "password": password,
          "email": e_mail,
          "newsletter_subscribe": False
        }

        body = json.dumps(json_data)

        epoch = signing.current_epoch()

        hmac_header = signing.get_hmac_header(epoch, body, self.user_agent, self.device_id)

        register_response = self.session.post(
            "https://accounts.reddit.com/api/register",
            headers= {
                'accept-encoding': 'gzip',
                'client-vendor-id': self.device_id,
                'connection': 'Keep-Alive',
                'content-type': 'application/json; charset=UTF-8',
                'host': 'accounts.reddit.com',
                'user-agent': self.user_agent,
                'x-hmac-signed-body': hmac_header.hmac_signed_body,
                'x-hmac-signed-result': hmac_header.hmac_signed_result,
                'x-reddit-compression': '1',
                'x-reddit-loid': self.x_reddit_loid,
                'x-reddit-media-codecs': 'available-codecs=video/avc, video/x-vnd.on2.vp9',
                'x-reddit-qos': 'down-rate-mbps=3.200',
                'x-reddit-retry': 'algo=no-retries',
            },
            data = body
        )
        assert register_response.ok, f"{self.__class__.__name__}.register(): {register_response.json().get('error', {}).get('explanation')}"

    def verify_token(self):
        verify_token_response = self.session.get(
            "https://oauth.reddit.com/api/v1/me?raw_json=1&feature=link_preview&sr_detail=true&expand_srs=true&from_detail=true&api_type=json&raw_json=1&always_show_media=1",
            headers= {
                'accept-encoding': 'gzip',
                'accept-language': 'en,en;q=0.9',
                'authorization': self.token,
                'client-vendor-id': self.device_id,
                'connection': 'Keep-Alive',
                'device-name': 'Google;sdk_gphone64_x86_64',
                'host': 'oauth.reddit.com',
                'user-agent': self.user_agent,
                'x-dev-ad-id': self.adversary_id,
                'x-reddit-compression': '1',
                'x-reddit-device-id': self.device_id,
                'x-reddit-dpr': '2.625',
                'x-reddit-loid': self.x_reddit_loid,
                'x-reddit-media-codecs': 'available-codecs=video/avc, video/x-vnd.on2.vp9',
                'x-reddit-qos': 'down-rate-mbps=3.200',
                'x-reddit-retry': 'attempt=0, max=3, algo=full-jitter',
                'x-reddit-width': '1080',
            }
        )

        assert verify_token_response.ok, f"{self.__class__.__name__}.verify_token()"
        self.x_reddit_session = verify_token_response.headers.get("x-reddit-session", self.x_reddit_session)

    def get_basic_access_token(self) -> str:
        access_token_response = self.session.post(
            "https://accounts.reddit.com/api/access_token",
            headers = {
                'accept-encoding': 'gzip',
                'authorization': 'Basic b2hYcG9xclpZdWIxa2c6',
                'client-vendor-id': self.device_id,
                'connection': 'Keep-Alive',
                'content-type': 'application/json; charset=UTF-8',
                'host': 'accounts.reddit.com',
                'user-agent': self.user_agent,
                'x-reddit-compression': '1',
                'x-reddit-media-codecs': 'available-codecs=video/avc, video/x-vnd.on2.vp9',
                'x-reddit-qos': 'down-rate-mbps=3.200',
                'x-reddit-retry': 'algo=no-retries',
            },
            json = {
                "scopes": [
                    "*",
                    "email",
                    "pii"
              ]
            }
        )
        assert access_token_response.status_code == 200, access_token_response.text
        self.x_reddit_loid = access_token_response.headers.get("x-reddit-loid", self.x_reddit_loid)
        self.token = f"{access_token_response.json().get('token_type').title()} {access_token_response.json().get('access_token')}"
        return self.token

reddit = Reddit()
reddit.register("email@gmail.com", "username", "124124wrqrqwr")
print(reddit.get_basic_access_token())
