import openai
from typing import List, Dict, Tuple
import json
import config

class SkillAnalyzer:
    def __init__(self):
        self.client = openai.OpenAI(
            api_key=config.DEEPSEEK_API_KEY,
            base_url=config.DEEPSEEK_API_BASE
        )
        
    def analyze_match(self, my_skills: str, job: Dict) -> Dict:
        """分析单个职位与个人技能的匹配度"""
        prompt = f"""
        你是一个专业的职业顾问和技能分析专家。请分析以下职位描述与候选人技能的匹配程度。

        候选人的技能描述：
        {my_skills}

        职位信息：
        职位名称：{job.get('title', 'N/A')}
        公司：{job.get('company', 'N/A')}
        职位描述：{job.get('description', 'N/A')}

        请提供以下分析：
        1. 匹配度评分（0-100分）
        2. 匹配的技能列表
        3. 缺失的技能列表
        4. 优势分析
        5. 建议提升的方向
        6. 综合推荐指数（1-5星）

        请以JSON格式返回结果：
        {{
            "score": 85,
            "matched_skills": ["Python", "Django"],
            "missing_skills": ["Kubernetes", "React"],
            "strengths": "你的Python后端开发经验非常匹配...",
            "improvements": "建议学习Kubernetes和容器化技术...",
            "recommendation": 4,
            "fit_analysis": "整体匹配度较高，技术栈重合度约70%..."
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "你是一个专业的职业匹配分析助手。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            result = response.choices[0].message.content
            # 尝试解析JSON
            try:
                analysis = json.loads(result)
            except json.JSONDecodeError:
                # 如果返回的不是纯JSON，尝试提取JSON部分
                start = result.find('{')
                end = result.rfind('}') + 1
                if start != -1 and end > start:
                    analysis = json.loads(result[start:end])
                else:
                    analysis = {"error": "无法解析分析结果", "raw_response": result}
            
            analysis['job_title'] = job.get('title', 'N/A')
            analysis['company'] = job.get('company', 'N/A')
            return analysis
            
        except Exception as e:
            print(f"分析职位时出错: {e}")
            return {"error": str(e)}
    
    def batch_analyze(self, my_skills: str, jobs: List[Dict], top_n: int = 10) -> List[Dict]:
        """批量分析多个职位"""
        results = []
        print(f"开始分析 {len(jobs)} 个职位...")
        
        for i, job in enumerate(jobs, 1):
            print(f"正在分析第 {i}/{len(jobs)} 个职位: {job.get('title', 'N/A')}")
            analysis = self.analyze_match(my_skills, job)
            results.append(analysis)
            
        # 按匹配度排序
        results.sort(key=lambda x: x.get('score', 0), reverse=True)
        
        # 返回前N个结果
        return results[:top_n]
    
    def generate_summary_report(self, my_skills: str, analyses: List[Dict]) -> str:
        """生成综合报告"""
        if not analyses:
            return "没有可分析的数据"
        
        prompt = f"""
        基于以下分析结果，生成一份综合的职业匹配报告。

        候选人技能：{my_skills}

        分析结果：
        {json.dumps(analyses, ensure_ascii=False, indent=2)}

        请生成一份报告，包括：
        1. 总体匹配概况
        2. 最匹配的3个职位及其原因
        3. 候选人的核心竞争力
        4. 技能缺口分析
        5. 职业发展建议
        6. 下一步行动计划

        请用中文生成，格式清晰。
        """
        
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "你是一个资深的职业规划顾问。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"生成报告时出错: {e}"