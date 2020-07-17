from ._base import Job

class ADClientSecretCredential(Job):
    description: str = "Authenticate with Client ID."
    arguments: dict = {"tenantId": "Tenant ID",
                       "clientId": "Client ID",
                       "clientId3": "Client ID",
                       "clientId4": "Client ID",
                       "clientId5": "Client ID",
                       "clientId6": "Client ID",
                       "clientId7": "Client ID",
                       "clientId8": "Client ID",
                       "clientId9": "Client ID",
                       "clientId11": "Client ID",
                       "clientId12": "Client ID",
                       "clientId13": "Client ID",
                       "clientId14": "Client ID",
                       "clientSecret": "Client Secret"}

    def run(cls, *args, **kwargs):
        """Runs the job"""
        pass

class ADUserPassCredential(Job):
    description: str = "Authenticate with username and password."
    arguments: dict = {"username": "Username of account",
                       "password": "Password of account"}
    notes: str = "This cannot be used on accounts with MFA."
    
    def run(cls, *args, **kwargs):
        """Runs the job"""
        pass