# Academic Report Generator (学术论文智能生成系统)

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-supported-blue.svg)](https://www.docker.com/)

**Language Switch / 语言切换:** [中文](README.md) | [English](README_EN.md)

An AI-powered academic paper proposal and experimental design generation tool designed to help researchers explore blank research areas and design preliminary research plans.

## ⚠️ Academic Integrity Statement

**Important Notice:**
- This tool is for **research inspiration and reference only**, not for direct academic submission
- Generated content requires **human review, verification, and substantial modification**
- Users must ensure **originality and academic integrity** of final work
- This tool cannot replace **independent thinking and in-depth research**
- Please comply with academic norms and ethical requirements of your institution

## 🎯 Project Overview

This project is a demo tool for **blank research exploration** that integrates multiple AI models and academic resources to help researchers:

- 🔍 **Discover Research Gaps**: Identify potential research opportunities based on existing literature analysis
- 📝 **Generate Proposals**: Provide structured research proposal frameworks
- 🧪 **Design Experiments**: Generate preliminary experimental design ideas
- 📚 **Integrate Academic Resources**: Automatically retrieve relevant arXiv papers and Zhihu discussions

## ✨ Key Features

### 🔬 Intelligent Content Generation
- **Proposal Generation**: Complete structure including research background, problem statement, methodology, etc.
- **Experimental Design**: Provides experimental procedures, evaluation metrics, expected results, etc.
- **Multi-Academic Level Support**: Adapts to different requirements for undergraduate, master's, and doctoral levels

### 🌍 Diverse Content Sources
- **arXiv Paper Search**: Access latest academic research developments
- **Zhihu Content Analysis**: Understand practical application scenarios and discussion hotspots
- **Local File Parsing**: Support PDF, DOCX, DOC format reference materials

### 🤖 Multi-Model AI Support
- **OpenAI GPT**: GPT-3.5/4 series models
- **Google Gemini**: Gemini 1.5 Flash/Pro
- **Claude**: Anthropic Claude 3 series
- **Alibaba Qwen**: Qwen Max
- **SiliconFlow**: Various open-source models

## 🚀 Quick Start

### Requirements

- Python 3.8 or higher
- At least one available AI model API key
- Stable internet connection

### Installation Steps

1. **Clone the project**
```bash
git clone https://github.com/yourusername/generate-academic-report.git
cd generate-academic-report
```

2. **Install dependencies**
```bash
# Recommended to use virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

3. **Configure API keys**

Create `.env` file:
```bash
cp .env.example .env
```

Edit `.env` file and configure at least one API key:
```env
# Please refer to .env.example for detailed configuration instructions
# Configure the API keys you need to use
OPENAI_API_KEY=sk-your_actual_openai_api_key_here
GEMINI_API_KEY=your_actual_gemini_api_key_here
# ... other API keys
```

**Note**: Please ensure to replace `your_actual_xxx_api_key_here` with your actual API keys.

4. **Start the service**
```bash
# Use startup script
./start.sh

# Or run directly
python app.py
```

The service runs on `http://localhost:5000` by default.

### Docker Deployment

```bash
# Build and start
docker-compose up --build

# Run in background
docker-compose up -d
```

## 📖 Usage Guide

### API Usage Examples

**Basic Generation Endpoint**

```bash
curl -X POST http://localhost:5000/generate_academic_report \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Research on Intelligent Q&A System Based on Deep Learning",
    "details": "Research on how to use large language models to build more accurate Q&A systems...",
    "academicLevel": "Master",
    "country": "China",
    "materialFiles": ["./docs/reference.pdf"]
  }'
```

**Python Usage Example**

```python
import requests

data = {
    "title": "Application of Artificial Intelligence in Medical Diagnosis",
    "details": "Exploring innovative applications of AI technology in medical image analysis...",
    "academicLevel": "PhD",
    "country": "China",
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
    print("Proposal:")
    print(result["data"]["proposal"])
    print("\nExperimental Design:")
    print(result["data"]["experiment_design"])
```

### Supported Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `title` | string | Yes | Research title |
| `details` | string | Yes | Research details and background |
| `academicLevel` | string | Yes | Academic level: Bachelor/Master/PhD |
| `country` | string | Yes | Country/Region: China/USA/UK etc. |
| `materialFiles` | array | No | Reference file path list |

### Supported File Formats

- **PDF files**: `.pdf`
- **Word documents**: `.docx`, `.doc`

## 🔧 Configuration

### API Priority

The system automatically tries different APIs in the following order:
1. Google Gemini (recommended, cost-effective)
2. OpenAI
3. SiliconFlow
4. Alibaba Qwen
5. Claude

### Custom Configuration

Configuration via environment variables:
- API keys: Set in `.env` file
- Model parameters: Can be adjusted in code (temperature, max_tokens, etc.)
- Retry strategy: Can be customized in API call modules
- Timeout settings: Can be configured in code

## 🧪 Development and Testing

### Run Tests

```bash
# Run complete test suite
python test_simplified.py

# Check service status
curl http://localhost:5000/health
```

### Project Structure

```
├── app.py                      # Flask application entry
├── main.py                     # Core business logic
├── simple_api.py               # AI model call wrapper
├── file_parser.py              # File parsing utility
├── requirements.txt            # Dependencies list
├── docker-compose.yml          # Docker configuration
├── start.sh                    # Startup script
├── config/
│   ├── api_config.py           # API configuration
│   └── api_keys.py             # API key pool
├── tool/
│   └── deep_research.py        # Zhihu search tool
└── api/
    └── arxiv.py                # arXiv search interface
```

## 🤝 Contributing

We welcome contributions in various forms:

### Contribution Types
- 🐛 Bug fixes
- ✨ New feature development
- 📚 Documentation improvements
- 🧪 Test enhancements
- 🌍 Internationalization support

### Development Process

1. **Fork the project**
2. **Create feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Commit changes**
   ```bash
   git commit -m "Add: new feature description"
   ```
4. **Push branch**
   ```bash
   git push origin feature/your-feature-name
   ```
5. **Create Pull Request**

### Code Standards

- Follow PEP8 code style
- Add appropriate comments and docstrings
- Ensure tests pass
- Maintain backward compatibility

## ⚠️ Usage Limitations

### Academic Use Guidelines
- This tool is for **research inspiration and preliminary exploration only**
- Generated content requires **human verification and substantial modification**
- Should not be used directly for **formal academic submission**
- Users bear **academic integrity responsibility**

### Technical Limitations
- Depends on external API services, requires stable internet connection
- Limited file parsing capabilities, complex formats may not be parsed completely
- AI-generated content has uncertainty, requires human review

## 📄 License

This project is licensed under [MIT License](LICENSE).

## 📄 License

This project is licensed under the MIT License.

## 🆘 Getting Help

- 📋 [Submit Issue](https://github.com/THESIS-AGENT/generate-adademic-report/issues)
- 📧 Email Support: service@thesisagent.ai

## 🙏 Acknowledgments

Thanks to the following open source projects and services:
- [OpenAI](https://platform.openai.com/docs/models) - GPT Model Support
- [Google](https://ai.google.dev/gemini-api/docs/models) - Gemini Model Support
- [Anthropic](https://docs.anthropic.com/en/docs/about-claude/models/overview) - Claude Model Support
- [Alibaba Cloud](https://help.aliyun.com/zh/model-studio/models) - Tongyi Qianwen Support
- [SiliconFlow](https://www.siliconflow.com/models) - Open Source Model Support

## ⭐ Star History

If this project has been helpful to you, please give us a ⭐️!

---

**Disclaimer**: This tool is only for academic research inspiration and reference. Users must ensure compliance with academic integrity and relevant laws and regulations.
