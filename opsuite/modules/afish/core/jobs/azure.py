from ._base import Job

class ADClientSecretCredential(Job):
    description: str = "Authenticate with Client ID."
    arguments: dict = {"tenantId": "Tenant ID",
                       "clientId": "Client ID",
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