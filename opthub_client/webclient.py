from urllib.parse import urljoin


class WebClient:
    def __urljoin(self, path: str) -> str:
        return urljoin(self.__web_service_host, path)

    def __create_headers(self) -> str:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.__access_token}",
            "correlation-id": "DEV_CORRELATION_ID",
        }

    def login(self, user_name: str, password: str) -> dict:
        body = json.dumps({"email": user_name, "password": password})
        response = requests.post(
            self.__urljoin("/v1/users/login"), data=body, headers=self.__create_headers_without_token()
        )
        result = json.loads(response.text)
        result["refresh"] = response.cookies.get("refresh")
        return result

    @classmethod
    def save_credentials(
        cls, credentials: Credentials, credentials_filepath: str = DEFAULT_CREDENTIALS_FILEPATH
    ) -> Credentials:
        os.makedirs(os.path.dirname(DEFAULT_CREDENTIALS_FILEPATH), exist_ok=True)
        with open(credentials_filepath, "w+") as credentials_file:
            credentials_rawjson = json.dumps(credentials.__dict__, indent=4)
            credentials_file.write(credentials_rawjson)
        return credentials
