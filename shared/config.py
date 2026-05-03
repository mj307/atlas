from pydantic_settings import BaseSettings, SettingsConfigDict
# static information

# config has the code that reads the env file (or some file) and then set the values of those needed vars

class Settings(BaseSettings):
    # open router
    openrouter_api_key: str
    openrouter_model: str
    openai_api_base: str 
    # mcp auth
    mcp_secret_key: str 
    
    calculator_url: str
    knowledge_base_url: str
    task_manager_url: str
    agent_url: str
    
    log_level: str = "INFO"
  
    
    model_config = SettingsConfigDict(env_file='.env')
    

    
settings = Settings()