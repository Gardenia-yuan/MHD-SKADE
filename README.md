# MHD-SKADE
Multi-Source Heterogeneous Data-Driven Construction and Dynamic Evolution Analysis of Skill-Knowledge Capability Landscapes

# 🎯 Job Matcher - AI驱动的职位匹配系统

一个基于DeepSeek AI的智能职位匹配系统，能够自动爬取网上的职位描述，并根据你的技能进行智能匹配分析。

## ✨ 功能特点

- 🤖 **AI智能分析**：使用DeepSeek API进行深度技能匹配分析
- 🕷️ **多源爬虫**：支持从Indeed、LinkedIn等平台爬取职位信息
- 📊 **详细报告**：生成包含匹配度、技能差距、改进建议的综合报告
- 🔄 **批量处理**：支持同时分析多个职位，自动排序推荐
- 💾 **数据持久化**：自动保存爬取数据和分析结果
- 📝 **灵活配置**：支持自定义爬取规则和分析参数

## 🚀 快速开始

### 前置要求

- Python 3.8+
- DeepSeek API密钥（[获取地址](https://platform.deepseek.com/)）

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/yourusername/job-matcher.git
cd job-matcher
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置环境变量**

创建 `.env` 文件并添加你的API密钥：
```bash
DEEPSEEK_API_KEY=sk-your-actual-api-key-here
```

4. **准备技能描述**

编辑 `my_skills.txt` 文件，填入你的技能信息：
```txt
技术栈：
- 编程语言：Python（精通），JavaScript（熟练）
- 框架：Django，Flask，React
- 数据库：PostgreSQL，MongoDB
...

工作经验：
- 3年Python后端开发
- 参与过大型项目开发
...

软技能：
- 团队协作
- 问题解决
...
```

5. **运行程序**
```bash
python main.py
```

## 📖 使用指南

### 基本使用

1. **选择数据源**
   - 选项1：使用模拟数据（快速测试）
   - 选项2：爬取真实职位数据

2. **查看匹配结果**
   - 系统会显示按匹配度排序的职位列表
   - 每个职位包含详细的匹配分析

3. **获取综合报告**
   - AI生成的职业发展建议
   - 技能提升方向指导

### 命令行参数

```bash
# 运行主程序
python main.py

# 仅爬取职位数据
python job_crawler.py

# 仅运行技能分析
python skill_analyzer.py
```

### 配置文件说明

`config.py` 中可以调整：

```python
# 爬虫配置
CRAWLER_CONFIG = {
    "max_pages": 5,        # 最大爬取页数
    "delay": 2,            # 请求间隔（秒）
    "timeout": 10,         # 请求超时时间
}

# 目标网站
JOB_SITES = {
    "linkedin": {
        "url": "https://www.linkedin.com/jobs/search",
        "params": {"keywords": "python developer"}
    },
    # 添加更多网站...
}
```

## 📁 项目结构

```
job-matcher/
├── README.md              # 项目说明文档
├── requirements.txt       # Python依赖包
├── .env                   # 环境变量（需自行创建）
├── config.py             # 配置文件
├── main.py               # 主程序入口
├── job_crawler.py        # 职位爬虫模块
├── skill_analyzer.py     # AI技能分析模块
├── my_skills.txt         # 个人技能描述
├── jobs.json            # 爬取的职位数据
└── match_results.json   # 匹配分析结果
```

## 🔧 模块说明

### 1. JobCrawler (job_crawler.py)

职位爬虫模块，支持多种数据源：

- **Indeed爬虫**：爬取Indeed网站的职位信息
- **LinkedIn爬虫**：通过API或Selenium获取LinkedIn职位
- **模拟数据**：用于测试的示例职位数据

```python
from job_crawler import JobCrawler

crawler = JobCrawler()
# 爬取Indeed职位
jobs = crawler.crawl_indeed("python developer", "remote")
# 使用模拟数据
jobs = crawler.crawl_simulated_jobs()
```

### 2. SkillAnalyzer (skill_analyzer.py)

AI分析模块，使用DeepSeek进行智能匹配：

```python
from skill_analyzer import SkillAnalyzer

analyzer = SkillAnalyzer()
# 分析单个职位
result = analyzer.analyze_match(my_skills, job)
# 批量分析
results = analyzer.batch_analyze(my_skills, jobs, top_n=10)
# 生成综合报告
report = analyzer.generate_summary_report(my_skills, results)
```

## 📊 输出示例

### 匹配结果
```
🏆 第1名: Senior Python Developer
   公司: TechInnovate
   匹配度: 85/100
   推荐指数: ⭐⭐⭐⭐
   匹配技能: Python, Django, PostgreSQL, AWS
   缺失技能: Kubernetes, React
   分析: 整体匹配度较高，技术栈重合度约70%...
```

### 综合报告
```
📄 职业匹配综合报告
================================

1. 总体匹配概况
   - 分析了4个职位，平均匹配度75%
   - 你的Python和Django技能最受欢迎
   
2. 最匹配职位
   - Senior Python Developer (85%)
   - Backend Engineer (78%)
   
3. 核心竞争力
   - 深厚的Python后端开发经验
   - Django框架专精
   ...
```

## ⚙️ 高级配置

### 添加新的职位来源

编辑 `config.py`：
```python
JOB_SITES["glassdoor"] = {
    "url": "https://www.glassdoor.com/Job/jobs.htm",
    "params": {"suggestCount": 0, "suggestChosen": False}
}
```

在 `job_crawler.py` 中添加对应的爬虫方法。

### 自定义分析维度

修改 `skill_analyzer.py` 中的分析提示词，添加更多分析维度：
- 薪资匹配度
- 文化契合度
- 职业发展空间
- 工作地点偏好

### 设置定时爬取

使用crontab或任务调度器：
```bash
# 每天上午9点自动运行
0 9 * * * cd /path/to/job-matcher && python main.py
```

## 🛠️ 常见问题

### Q: API调用失败怎么办？
检查：
- API密钥是否正确设置
- 网络连接是否正常
- API额度是否用完

### Q: 爬虫无法获取数据？
可能原因：
- 网站反爬机制更新
- 需要更新User-Agent
- 请求频率过高被限制

解决方案：
- 增加请求延迟
- 使用代理IP
- 更新爬虫选择器

### Q: 分析结果不准确？
优化建议：
- 完善技能描述，添加更多细节
- 调整API temperature参数
- 优化分析提示词

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开Pull Request

## 📝 更新日志

### v1.0.0 (2024-01)
- ✅ 初始版本发布
- ✅ 支持Indeed职位爬取
- ✅ DeepSeek AI分析集成
- ✅ 批量职位匹配
- ✅ 综合报告生成

### 计划中的功能
- [ ] Web界面（Flask/FastAPI）
- [ ] 更多数据源支持
- [ ] 邮件通知功能
- [ ] 职位收藏和历史记录
- [ ] 数据可视化仪表板

## ⚠️ 免责声明

- 本工具仅供学习和个人使用
- 爬取数据时请遵守目标网站的robots.txt和使用条款
- API调用产生的费用由用户自行承担
- 分析结果仅供参考，不构成职业建议

## 📄 许可证

MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.

## 🎉 致谢

- [DeepSeek](https://deepseek.com/) - 提供强大的AI API支持
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) - HTML解析库
- [OpenAI](https://openai.com/) - API接口标准

## 📮 联系方式

- 项目Issue: [GitHub Issues](https://github.com/yourusername/job-matcher/issues)
- 邮箱: your.email@example.com

---

⭐ 如果这个项目对你有帮助，请给个Star！
