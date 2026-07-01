from pydantic_settings import BaseSettings,SettingsConfigDict
import os
from pydantic import  computed_field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # Use top level .env file (one level above ./backend/)
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )
    API_V1_STR: str = "/api"
    APP_NAME: str = "新闻头条"
    APP_VERSION: str = "0.1.0"
    # ===== JWT 鉴权参数 =====
    JWT_SECRET_KEY:str = "your-secret-key"    # 用于签名的密钥，部署时必须替换
    JWT_algorithm:str = "HS256" # JWT 签名算法
    JWT_EXPIRE_MINUTES: int = 60 * 24 * 1  # Token 过期时间：7 天
    # =================数据库连接参数=================
    DB_USER: str = "root"
    DB_PASSWORD: str = "123456"
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_NAME: str = "news_app"
    DB_CHARSET: str = "utf8mb4"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD:str = "123456"
    DECODE_RESPONSE:bool=True #是否将字节数据解码为字符串

    @computed_field
    @property  # Python 的内置装饰器，用于将方法转换为只读属性。它的核心作用是让你可以在不改变调用方式的前提下，在属性访问时添加逻辑。
    def database_url(self) -> str:
        return (
            f"mysql+asyncmy://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?charset={self.DB_CHARSET}"
        )

    @computed_field
    @property
    def redis_client(self) ->  dict:
        return {"host": self.REDIS_HOST, "port": self.REDIS_PORT, "db": self.REDIS_DB, "decode_responses": self.DECODE_RESPONSE,"password": self.REDIS_PASSWORD}


# 模块级全局单例：其他模块直接 `from .config import settings` 即可使用
settings = Settings()