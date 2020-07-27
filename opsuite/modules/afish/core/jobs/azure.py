from ._base import Job
import aiohttp


async def fetch(session, url):
    async with session.get(url) as response:
        return await response


class ADClientSecretCredential(Job):
    description: str = "Authenticate with Client ID."
    arguments: dict = {
        "tenantId": "Tenant ID",
        "clientId": "Client ID",
        "clientSecret": "Client Secret",
    }

    async def run(**kwargs):
        """Runs the job"""
        args = kwargs["args"]
        data = {
            "grant_type": "client_credentials",
            "client_id": args["clientId"],
            "client_secret": args["clientSecret"],
            "scope": "https://graph.microsoft.com/.default",
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f'https://login.microsoftonline.com/{args["tenantId"]}/oauth2/token',
                data=data,
            ) as resp:
                output = await resp.json()
                print(output)
                if output.get("access_token"):
                    return "SUCCESS"
                raise Exception(output.get("error_description"))


class ADUserPassCredential(Job):
    description: str = "Authenticate with username and password."
    arguments: dict = {
        "username": "Username of account",
        "password": "Password of account",
    }
    notes: str = "This cannot be used on accounts with MFA."

    async def run(**kwargs):
        """Runs the job"""
        args = kwargs["args"]
        data = {
            "client_id": "1b730954-1685-4b74-9bfd-dac224a7b894",
            "grant_type": "password",
            "username": args["username"],
            "password": args["password"],
            "resource": "https://graph.microsoft.com",
        }

        tenantId = args["username"].split("@")[1]
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"https://login.microsoftonline.com/{tenantId}/oauth2/token", data=data,
            ) as resp:
                output = await resp.json()
                if output.get("access_token"):
                    return "SUCCESS"
                raise Exception(output.get("error_description"))
