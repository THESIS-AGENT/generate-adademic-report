# 学术论文智能生成系统 (Academic Report Generator)

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-supported-blue.svg)](https://www.docker.com/)

**语言切换 / Language Switch:** [中文](README.md) | [English](README_EN.md)

一个基于人工智能的学术论文开题报告和实验设计自动生成工具，旨在帮助研究者进行空白研究领域的挖掘和初步方案设计。

## ⚠️ 学术诚信声明

**重要提醒：**
- 本工具仅用于**研究启发和参考**，不应直接用于正式的学术提交
- 生成的内容需要经过**人工审查、验证和大幅修改**
- 使用者需要确保最终成果的**原创性和学术诚信**
- 本工具不能替代**独立思考和深入研究**
- 请遵守所在机构的学术规范和伦理要求

## 🎯 项目简介

本项目是一个用于**空白研究挖掘**的demo工具，通过整合多个AI模型和学术资源，帮助研究者：

- 🔍 **发现研究空白**：基于现有文献分析，识别潜在的研究机会
- 📝 **生成开题报告**：提供结构化的研究方案框架
- 🧪 **设计实验方案**：生成初步的实验设计思路
- 📚 **整合学术资源**：自动检索相关的arXiv论文和知乎讨论

## ✨ 主要功能

### 🔬 智能内容生成
- **开题报告生成**：包含研究背景、问题陈述、方法论等完整结构
- **实验设计方案**：提供实验流程、评估指标、预期结果等
- **多学术层次支持**：适配本科、硕士、博士不同层次的要求

### 🌍 多元化内容源
- **arXiv论文检索**：获取最新的学术研究动态
- **知乎内容分析**：了解实际应用场景和讨论热点
- **本地文件解析**：支持PDF、DOCX、DOC格式的参考资料

### 🤖 多模型AI支持
- **OpenAI GPT**：GPT-3.5/4系列模型
- **Google Gemini**：Gemini 1.5 Flash/Pro
- **Claude**：Anthropic Claude 3系列
- **阿里通义千问**：Qwen Max
- **SiliconFlow**：多种开源模型

## 🚀 快速开始

### 环境要求

- Python 3.8或更高版本
- 至少一个可用的AI模型API密钥
- 稳定的网络连接

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/yourusername/generate-academic-report.git
cd generate-academic-report
```

2. **安装依赖**
```bash
# 推荐使用虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

3. **配置API密钥**

创建 `.env` 文件：
```bash
cp .env.example .env
```

编辑 `.env` 文件，配置至少一个API密钥：
```env
# 请参考 .env.example 文件中的详细配置说明
# 配置您需要使用的API密钥
OPENAI_API_KEY=sk-your_actual_openai_api_key_here
GEMINI_API_KEY=your_actual_gemini_api_key_here
# ... 其他API密钥
```

**注意**：请确保将 `your_actual_xxx_api_key_here` 替换为您的真实API密钥。

4. **启动服务**
```bash
# 使用启动脚本
./start.sh

# 或直接运行
python app.py
```

服务默认在 `http://localhost:5000` 启动。

### Docker 部署

```bash
# 构建并启动
docker-compose up --build

# 后台运行
docker-compose up -d
```

## 📖 使用指南

### API调用示例

**基础生成接口**

```bash
curl -X POST http://localhost:5000/generate_academic_report \
  -H "Content-Type: application/json" \
  -d '{
    "title": "基于深度学习的智能问答系统研究",
    "details": "研究如何利用大语言模型构建更准确的问答系统...",
    "academicLevel": "硕士",
    "country": "中国",
    "materialFiles": ["./docs/reference.pdf"]
  }'
```

**Python调用示例**

```python
import requests

data = {
    "title": "人工智能在医疗诊断中的应用",
    "details": "探索AI技术在医学影像分析中的创新应用...",
    "academicLevel": "博士",
    "country": "中国",
    "materialFiles": [
        "./materials/medical_ai_survey.pdf",
        "./materials/diagnosis_methods.docx"
    ]
}

response = requests.post(
    "http://localhost:5000/generate_academic_report",
    json=data
)

result = response.json()
if result["code"] == 200:
    print("开题报告:")
    print(result["data"]["proposal"])
    print("\n实验设计:")
    print(result["data"]["experiment_design"])
```

### 支持的参数

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `title` | string | 是 | 研究题目 |
| `details` | string | 是 | 研究详情和背景 |
| `academicLevel` | string | 是 | 学术层次：本科/硕士/博士 |
| `country` | string | 是 | 国家/地区：中国/美国/英国等 |
| `materialFiles` | array | 否 | 参考文件路径列表 |

### 支持的文件格式

- **PDF文件**：`.pdf`
- **Word文档**：`.docx`、`.doc`

## 🔧 配置说明

### API优先级

系统会按以下顺序自动尝试不同的API：
1. Google Gemini（推荐，性价比高）
2. OpenAI
3. SiliconFlow
4. 阿里通义千问
5. Claude

### 自定义配置

通过环境变量配置：
- API密钥：在 `.env` 文件中设置
- 模型参数：可在代码中调整（temperature、max_tokens等）
- 重试策略：可在API调用模块中自定义
- 超时设置：可在代码中配置

## 🧪 开发和测试

### 运行测试

```bash
# 运行完整测试套件
python test_simplified.py

# 检查服务状态
curl http://localhost:5000/health
```

### 项目结构

```
├── app.py                      # Flask应用入口
├── main.py                     # 核心业务逻辑
├── simple_api.py               # AI模型调用封装
├── file_parser.py              # 文件解析工具
├── requirements.txt            # 依赖列表
├── docker-compose.yml          # Docker配置
├── start.sh                    # 启动脚本
├── config/
│   ├── api_config.py           # API配置
│   └── api_keys.py             # API密钥池
├── tool/
│   └── deep_research.py        # 知乎搜索工具
└── api/
    └── arxiv.py                # arXiv搜索接口
```

## 🤝 贡献指南

我们欢迎各种形式的贡献：

### 贡献类型
- 🐛 Bug修复
- ✨ 新功能开发
- 📚 文档改进
- 🧪 测试增强
- 🌍 国际化支持

### 开发流程

1. **Fork项目**
2. **创建功能分支**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **提交更改**
   ```bash
   git commit -m "Add: 新功能描述"
   ```
4. **推送分支**
   ```bash
   git push origin feature/your-feature-name
   ```
5. **创建Pull Request**

### 代码规范

- 遵循PEP8代码风格
- 添加适当的注释和文档字符串
- 确保测试通过
- 保持向后兼容性

## ⚠️ 使用限制

### 学术使用规范
- 本工具仅用于**研究启发和初步探索**
- 生成内容需要**人工验证和大幅修改**
- 不得直接用于**正式学术提交**
- 使用者需承担**学术诚信责任**

### 技术限制
- 依赖外部API服务，需要稳定网络连接
- 文件解析能力有限，复杂格式可能解析不完整
- AI生成内容存在不确定性，需要人工审核

## 📄 许可证

本项目采用 [MIT License](LICENSE) 许可证。

## 🆘 获取帮助

- 📋 [提交Issue](https://github.com/yourusername/generate-academic-report/issues)
- 📧 邮箱支持: your.email@example.com
- 📖 [项目Wiki](https://github.com/yourusername/generate-academic-report/wiki)

## 🙏 致谢

感谢以下开源项目和服务：
- [OpenAI](https://openai.com/) - GPT模型支持
- [Google](https://ai.google.dev/) - Gemini模型支持
- [Anthropic](https://www.anthropic.com/) - Claude模型支持
- [阿里云](https://dashscope.aliyun.com/) - 通义千问支持
- [SiliconFlow](https://siliconflow.cn/) - 开源模型支持

## ⭐ Star History

如果这个项目对您有帮助，请给我们一个⭐️！

---

**声明**：本工具仅用于学术研究的启发和参考，使用者需确保遵守学术诚信和相关法律法规。 