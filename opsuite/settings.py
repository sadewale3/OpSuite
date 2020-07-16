from pydantic import BaseSettings
from pydantic.networks import IPvAnyAddress

class OpSuiteSettings(BaseSettings):
    host: IPvAnyAddress
    port: int
    debug: bool
    workers: int
    