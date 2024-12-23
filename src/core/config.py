from pydantic_settings import BaseSettings

class Settings (): 
    PROJECT_NAME: str = "beca2"
    PROJECT_VERSION: str= "0.0.1"
    DATABASE_URL: str


    class Config:
        env_file = '.env'

settings = Settings() 

