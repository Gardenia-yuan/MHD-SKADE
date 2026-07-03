import os
from dotenv import load_dotenv

load_dotenv()

# DeepSeek API配置
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "your-api-key-here")
DEEPSEEK_API_BASE = "https://api.deepseek.com/v1"

# 爬虫配置
CRAWLER_CONFIG = {
    "max_pages": 5,
    "delay": 2,  # 请求间隔（秒）
    "timeout": 10,
    "headers": {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
}

# 目标网站配置
JOB_SITES = {
    "linkedin": {
        "url": "https://www.linkedin.com/jobs/search",
        "params": {"keywords": "software engineer", "location": "remote"}
    },
    "indeed": {
        "url": "https://www.indeed.com/jobs",
        "params": {"q": "software engineer", "l": "remote"}
    }
}