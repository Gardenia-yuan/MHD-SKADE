import requests
from bs4 import BeautifulSoup
import time
import json
from typing import List, Dict
import pandas as pd
from fake_useragent import UserAgent
import config

class JobCrawler:
    def __init__(self):
        self.ua = UserAgent()
        self.jobs = []
        
    def crawl_indeed(self, query: str, location: str = "remote", max_results: int = 20) -> List[Dict]:
        """爬取Indeed的职位信息"""
        base_url = "https://www.indeed.com/jobs"
        params = {
            "q": query,
            "l": location,
            "limit": 50
        }
        
        for page in range(config.CRAWLER_CONFIG["max_pages"]):
            try:
                params["start"] = page * 10
                headers = {"User-Agent": self.ua.random}
                
                response = requests.get(
                    base_url, 
                    params=params, 
                    headers=headers,
                    timeout=config.CRAWLER_CONFIG["timeout"]
                )
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    job_cards = soup.find_all('div', class_='job_seen_beacon')
                    
                    for card in job_cards:
                        try:
                            title = card.find('h2', class_='jobTitle').get_text(strip=True)
                            company = card.find('span', class_='companyName').get_text(strip=True)
                            location = card.find('div', class_='companyLocation').get_text(strip=True)
                            
                            # 获取职位描述
                            snippet = card.find('div', class_='job-snippet')
                            description = snippet.get_text(strip=True) if snippet else ""
                            
                            job = {
                                "title": title,
                                "company": company,
                                "location": location,
                                "description": description,
                                "source": "indeed",
                                "url": f"https://www.indeed.com/viewjob?jk={card.get('data-jk', '')}"
                            }
                            self.jobs.append(job)
                            
                        except Exception as e:
                            print(f"解析职位卡片出错: {e}")
                            continue
                            
                time.sleep(config.CRAWLER_CONFIG["delay"])
                
            except Exception as e:
                print(f"爬取页面 {page} 出错: {e}")
                continue
                
        return self.jobs
    
    def crawl_linkedin(self, keywords: str, max_results: int = 20) -> List[Dict]:
        """爬取LinkedIn职位（简化版本）"""
        # 注意：LinkedIn通常需要登录，这里提供一个简化的示例
        # 实际使用时建议使用LinkedIn API或Selenium
        print("LinkedIn爬取需要使用API或Selenium进行登录")
        print("这里返回示例数据结构")
        
        sample_jobs = [
            {
                "title": "Python Developer",
                "company": "Tech Corp",
                "location": "Remote",
                "description": "We are looking for a Python developer with experience in Django, Flask, and cloud services...",
                "source": "linkedin"
            }
        ]
        self.jobs.extend(sample_jobs)
        return sample_jobs
    
    def crawl_simulated_jobs(self, keyword: str = "software engineer") -> List[Dict]:
        """提供模拟职位数据用于测试"""
        simulated_jobs = [
            {
                "title": "Senior Python Developer",
                "company": "TechInnovate",
                "location": "Remote",
                "description": """
                We're looking for a Senior Python Developer with 5+ years of experience.
                Required skills: Python, Django, PostgreSQL, AWS, Docker, Microservices.
                Nice to have: Kubernetes, React, Machine Learning experience.
                Responsibilities include building scalable backend systems and mentoring junior developers.
                """,
                "source": "simulated",
                "url": "https://example.com/job1"
            },
            {
                "title": "Full Stack Engineer",
                "company": "StartupXYZ",
                "location": "San Francisco, CA",
                "description": """
                Seeking a Full Stack Engineer proficient in React, Node.js, and Python.
                Must have experience with MongoDB, Express.js, and AWS.
                Knowledge of CI/CD pipelines and Test-Driven Development required.
                """,
                "source": "simulated",
                "url": "https://example.com/job2"
            },
            {
                "title": "Machine Learning Engineer",
                "company": "AI Solutions Inc",
                "location": "Remote",
                "description": """
                Join our ML team! Required: Python, TensorFlow/PyTorch, scikit-learn.
                Experience with NLP, computer vision, or recommendation systems.
                Strong mathematics background and experience with big data technologies.
                """,
                "source": "simulated",
                "url": "https://example.com/job3"
            },
            {
                "title": "DevOps Engineer",
                "company": "CloudTech",
                "location": "New York, NY",
                "description": """
                DevOps Engineer needed with expertise in Kubernetes, Docker, Terraform.
                Experience with AWS/Azure/GCP, CI/CD pipelines (Jenkins, GitLab CI).
                Knowledge of Python scripting and Linux administration.
                """,
                "source": "simulated",
                "url": "https://example.com/job4"
            }
        ]
        self.jobs.extend(simulated_jobs)
        return simulated_jobs
    
    def save_to_file(self, filename: str = "jobs.json"):
        """保存爬取的职位到文件"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.jobs, f, ensure_ascii=False, indent=2)
        print(f"已保存 {len(self.jobs)} 个职位到 {filename}")
    
    def load_from_file(self, filename: str = "jobs.json") -> List[Dict]:
        """从文件加载职位数据"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                self.jobs = json.load(f)
            print(f"从 {filename} 加载了 {len(self.jobs)} 个职位")
        except FileNotFoundError:
            print(f"文件 {filename} 不存在")
        return self.jobs