import sys
from job_crawler import JobCrawler
from skill_analyzer import SkillAnalyzer
import json

class JobMatcher:
    def __init__(self):
        self.crawler = JobCrawler()
        self.analyzer = SkillAnalyzer()
        
    def load_skills_from_file(self, filename: str = "my_skills.txt") -> str:
        """从文件加载技能描述"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"技能文件 {filename} 不存在，使用默认示例")
            return self.get_sample_skills()
    
    def get_sample_skills(self) -> str:
        """提供示例技能描述"""
        return """
        技术栈：
        - 编程语言：Python（精通），JavaScript（熟练），SQL（熟练）
        - 后端框架：Django（精通），Flask（熟练），FastAPI（了解）
        - 前端技术：HTML/CSS，React（基础），Vue.js（了解）
        - 数据库：PostgreSQL，MySQL，MongoDB
        - 云服务：AWS（EC2, S3, Lambda），Docker
        - 其他工具：Git，Linux，CI/CD（GitHub Actions）
        
        工作经验：
        - 3年Python后端开发经验
        - 2年Django框架使用经验
        - 参与过2个大型Web应用开发
        - 有微服务架构设计经验
        
        软技能：
        - 良好的团队协作能力
        - 较强的问题解决能力
        - 英语读写能力良好
        - 有敏捷开发经验
        """
    
    def save_results(self, analyses: list, report: str, filename: str = "match_results.json"):
        """保存分析结果"""
        results = {
            "analyses": analyses,
            "report": report
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n结果已保存到 {filename}")
    
    def run(self):
        """运行主程序"""
        print("=" * 60)
        print("         职业匹配系统 - AI驱动的工作匹配")
        print("=" * 60)
        
        # 1. 获取职位数据
        print("\n📋 步骤1: 获取职位数据")
        print("-" * 40)
        
        choice = input("选择数据来源:\n1. 使用模拟数据（测试用）\n2. 爬取真实数据\n请输入 (1/2): ")
        
        if choice == "2":
            print("\n正在爬取职位数据...")
            # 这里可以爬取真实数据
            # self.crawler.crawl_indeed("python developer")
            print("提示: 真实爬取需要处理反爬机制，这里使用模拟数据演示")
        
        print("\n使用模拟职位数据...")
        jobs = self.crawler.crawl_simulated_jobs()
        print(f"获取到 {len(jobs)} 个职位")
        
        # 2. 加载技能描述
        print("\n📝 步骤2: 加载技能描述")
        print("-" * 40)
        
        skills = self.load_skills_from_file()
        print("已加载技能描述")
        
        # 3. 分析匹配度
        print("\n🔍 步骤3: AI分析匹配度")
        print("-" * 40)
        
        analyses = self.analyzer.batch_analyze(skills, jobs)
        
        # 4. 显示结果
        print("\n📊 步骤4: 匹配结果")
        print("=" * 60)
        
        for i, analysis in enumerate(analyses, 1):
            print(f"\n🏆 第{i}名: {analysis.get('job_title', 'N/A')}")
            print(f"   公司: {analysis.get('company', 'N/A')}")
            print(f"   匹配度: {analysis.get('score', 0)}/100")
            print(f"   推荐指数: {'⭐' * analysis.get('recommendation', 0)}")
            print(f"   匹配技能: {', '.join(analysis.get('matched_skills', []))}")
            print(f"   缺失技能: {', '.join(analysis.get('missing_skills', []))}")
            print(f"   分析: {analysis.get('fit_analysis', 'N/A')[:100]}...")
        
        # 5. 生成综合报告
        print("\n📄 步骤5: 生成综合报告")
        print("=" * 60)
        
        report = self.analyzer.generate_summary_report(skills, analyses)
        print("\n" + report)
        
        # 6. 保存结果
        self.save_results(analyses, report)
        
        print("\n✅ 分析完成！")

def main():
    matcher = JobMatcher()
    matcher.run()

if __name__ == "__main__":
    main()