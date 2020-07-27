from pydantic import BaseSettings
from pydantic.networks import IPvAnyAddress, PostgresDsn
from pydantic.types import SecretStr


class OpSuiteConfig(BaseSettings):
    host: IPvAnyAddress
    port: int
    debug: bool
    workers: int
    pg_user: str
    pg_password: SecretStr
    pg_host: str
    pg_port: int
    opsuite_pg_conn: PostgresDsn


class AfishConfig(BaseSettings):
    sched_max_instances: int
    sched_coalesce: bool
    sched_timezone: str
    afish_pg_conn: PostgresDsn
