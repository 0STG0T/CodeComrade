from dataclasses import dataclass

@dataclass
class Config:
    openai_api_key: str 
    bot_api_key: str
    cache_dir: str
    
config = Config('', '', '')