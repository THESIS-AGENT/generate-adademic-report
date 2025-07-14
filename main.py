import json
import re
import time
import logging
from typing import List, Dict, Any, Optional
from file_parser import parse_material_files
from api.simple_api import call_llm
from tool.deep_research import search_zhihu
from api.arxiv import query_arxiv

# ================================ 配置日志 ================================

logger = logging.getLogger('generate_academic_report')
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler('generate_academic_report.log', encoding='utf-8')
file_handler.setLevel(logging.INFO)

log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(log_format)
file_handler.setFormatter(log_format)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

# ================================ 辅助函数 ================================


def extract_jsonList_fromStr(content: str) -> List:
    """
    从模型返回的文本内容中提取列表
    
    Args:
        content (str): 模型返回的内容
        
    Returns:
        list: 提取出的列表，解析失败时返回空列表
    """
    if not content:
        return []
        
    # 尝试直接解析
    try:
        keywords = json.loads(content.strip())
        if isinstance(keywords, list):
            return keywords
    except json.JSONDecodeError:
        pass
    
    # 尝试通过正则表达式提取JSON部分
    try:
        # 查找```json ... ```格式
        json_match = re.search(r'```(?:json)?\s*(\[.*?\])\s*```', content, re.DOTALL)
        if json_match:
            extracted_json = json_match.group(1)
            keywords = json.loads(extracted_json.strip())
            if isinstance(keywords, list):
                return keywords
            
        # 查找普通的JSON数组格式 [...]
        json_match = re.search(r'\[(.*?)\]', content, re.DOTALL)
        if json_match:
            extracted_json = "[" + json_match.group(1) + "]"
            keywords = json.loads(extracted_json.strip())
            if isinstance(keywords, list):
                return keywords
            
        # 如果仍然无法解析，尝试分行提取关键词
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        if len(lines) >= 3:
            # 清理引号和可能的其他符号
            keywords = []
            for line in lines[:3]:  # 取前3行
                # 清理可能的序号、引号和其他符号
                cleaned = re.sub(r'^[\d\.\[\]"\']*\s*', '', line)
                cleaned = re.sub(r'[,\.\[\]"\']*$', '', cleaned)
                if cleaned:
                    keywords.append(cleaned)
            
            if len(keywords) > 0:
                return keywords
                
    except Exception as e:
        logger.error(f"JSON解析错误: {str(e)}")

    # 如果所有解析方法都失败，返回一个空列表
    logger.warning("警告：无法从模型响应中提取有效的关键词列表。")
    return []


def extract_markdown_content(text: str) -> str:
    """
    Extract content between markdown or plaintext code blocks.
    If no code block markers are found, return the original text.
    
    Args:
        text (str): Input text potentially containing markdown code blocks
        
    Returns:
        str: Extracted content between code blocks or original text
    """
    pattern = r"```(?:markdown|plaintext)?\s*([\s\S]*?)```"
    match = re.search(pattern, text)
    
    if match:
        return match.group(1)
    else:
        return text
    

# ================================ 主要生成函数 ================================


def generate_academic_report(
    title: str, 
    details: str, 
    academic_level: str, 
    country: str, 
    material_file_paths: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    学术报告生成函数：生成开题报告和实验设计
    
    Args:
        title (str): 论文标题
        details (str): 初步研究方案
        academic_level (str): 学术层次（本科/硕士/博士）
        country (str): 就读国家
        material_file_paths (Optional[List[str]]): 材料文件路径列表
    
    Returns:
        Dict[str, Any]: 生成结果，包含开题报告和实验设计
    """
    logger.info("开始生成论文开题报告和实验设计")
    
    result = {
        "proposal": "",
        "experiment_design": "",
        "zhihu_research": [],
        "arxiv_papers": [],
        "status": "success",
        "message": ""
    }
    
    try:
        input_dict = {"学术层次": academic_level, "就读国家": country}
        
        # ================================ 解析上传文件 ================================
        
        parsed_files = []
        if material_file_paths:
            logger.info(f"开始解析 {len(material_file_paths)} 个本地文件")
            parsed_files = parse_material_files(material_file_paths)
            logger.info(f"成功解析 {len(parsed_files)} 个文件")
        
        # 分类解析的文件
        proposal_files = [f for f in parsed_files if f.get('fileBizType') == 1]
        experiment_files = [f for f in parsed_files if f.get('fileBizType') == 2]
        paper_files = [f for f in parsed_files if f.get('fileBizType') == 4]

        # ================================ 搜索补充材料 ================================
        
        logger.info("开始搜索知乎补充材料")
        zhihu_result = []
        
        if title and details:
            input_dict["学位论文标题"] = title
            input_dict["初步研究方案"] = details
            
            # 生成搜索关键词
            prompt_search_keywords = f"""
根据以下信息生成3个最适合在知乎搜索的关键词，用于收集相关技术资料：

论文标题：{title}
研究方案：{details}
学术层次：{academic_level}

要求：
1. 关键词要精确指向研究主题
2. 避免过于宽泛的术语
3. 每个关键词不超过10个字

请只返回JSON格式的关键词列表：
["关键词1", "关键词2", "关键词3"]
"""
            
            try:
                keywords_response = call_llm(prompt_search_keywords, "auto", 60)
                keywords = extract_jsonList_fromStr(keywords_response)
                
                if keywords:
                    logger.info(f"生成的搜索关键词: {keywords}")
                    zhihu_result = search_zhihu(keywords, 3)  # 每个关键词搜索3个结果
                    result["zhihu_research"] = zhihu_result
                    logger.info(f"知乎搜索完成，获得 {len(zhihu_result)} 条结果")
            except Exception as e:
                logger.error(f"知乎搜索失败: {str(e)}")
        
        # ================================ 搜索参考文献 ================================
        
        logger.info("开始搜索arXiv参考文献")
        paper_info = []
        
        if not paper_files and title and details:
            # 生成论文搜索关键词组合
            prompt_paper_keywords = f"""
根据以下信息生成2组英文关键词组合，用于在arXiv搜索相关论文：

论文标题：{title}
研究方案：{details}

要求：
1. 每组包含1-2个核心英文学术术语
2. 术语要精确且具有专业性
3. 能够定位到高度相关的研究文献

请只返回JSON格式：
[["keyword1", "keyword2"], ["keyword3", "keyword4"]]
"""
            
            try:
                paper_keywords_response = call_llm(prompt_paper_keywords, "auto", 60)
                paper_keywords = extract_jsonList_fromStr(paper_keywords_response)
                
                if paper_keywords:
                    logger.info(f"生成的论文搜索关键词: {paper_keywords}")
                    
                    for keyword_group in paper_keywords:
                        try:
                            arxiv_result = query_arxiv(keyword_group)
                            if arxiv_result and "entries" in arxiv_result:
                                paper_info.extend(arxiv_result["entries"])
                                time.sleep(2)  # 避免频繁请求
                        except Exception as e:
                            logger.warning(f"arXiv搜索失败: {str(e)}")
                    
                    result["arxiv_papers"] = paper_info
                    logger.info(f"arXiv搜索完成，获得 {len(paper_info)} 篇论文")
            except Exception as e:
                logger.error(f"arXiv搜索失败: {str(e)}")
        else:
            # 使用上传的论文文件
            paper_info = paper_files
    
        # ================================ 生成开题报告 ================================
        
        logger.info("开始生成开题报告")
        
        # 准备输入数据
        input_dict_str = json.dumps(input_dict, ensure_ascii=False, indent=4)
        paper_info_str = json.dumps(paper_info, ensure_ascii=False, indent=4)
        zhihu_result_str = json.dumps(zhihu_result, ensure_ascii=False, indent=4)
        
        if proposal_files:
            # 如果有上传的开题报告，进行润色优化
            proposal_str = json.dumps(proposal_files, ensure_ascii=False, indent=None)
            
            prompt_proposal = f"""
请基于以下信息，对现有开题报告进行专业润色和完善：

学术背景：{input_dict_str}
参考文献：{paper_info_str}
现有开题报告：{proposal_str}

要求：
1. 保持原有核心思想和研究方向
2. 提升学术表达的专业性和严谨性
3. 根据{academic_level}学位要求调整内容深度
4. 体现{country}学术规范
5. 输出完整的Markdown格式开题报告

请直接输出润色后的开题报告，无需解释过程。
"""
        else:
            # 从头生成开题报告
            prompt_proposal = f"""
请基于以下信息生成一份专业的学术开题报告：

学术背景：{input_dict_str}
参考文献：{paper_info_str}
知乎技术资料：{zhihu_result_str}

要求：
1. 符合{academic_level}学位论文标准
2. 体现{country}学术规范和写作风格
3. 结构完整，包含研究背景、文献综述、研究目标、方法、预期成果等
4. 合理融入知乎技术内容中的实践见解
5. 输出Markdown格式

请直接输出完整的开题报告。
"""
        
        try:
            proposal_response = call_llm(prompt_proposal, "auto", 120)
            proposal = extract_markdown_content(proposal_response)
            result["proposal"] = proposal
            logger.info("开题报告生成完成")
        except Exception as e:
            logger.error(f"开题报告生成失败: {str(e)}")
            result["status"] = "error"
            result["message"] = f"开题报告生成失败: {str(e)}"
            return result
        
        # ================================ 生成实验设计 ================================
        
        logger.info("开始生成实验设计")
        
        if experiment_files:
            # 如果有上传的实验设计，进行优化
            experiment_str = json.dumps(experiment_files, ensure_ascii=False, indent=None)
            
            prompt_experiment = f"""
请基于以下开题报告和现有实验设计，进行优化和完善：

开题报告：{proposal}
现有实验设计：{experiment_str}

要求：
1. 确保实验设计与开题报告高度一致
2. 完善实验步骤和数据分析方法
3. 提高实验的可操作性和科学性
4. 输出Markdown格式

请直接输出优化后的实验设计。
"""
        else:
            # 从头生成实验设计
            prompt_experiment = f"""
请基于以下开题报告生成详细的实验设计方案：

开题报告：{proposal}
知乎技术资料：{zhihu_result_str}

要求：
1. 与开题报告的研究目标和方法完全对应
2. 包含具体的实验步骤、数据收集、分析方法
3. 考虑实验的可行性和可重复性
4. 融入实践经验和技术方案
5. 输出Markdown格式

请直接输出完整的实验设计方案。
"""
        
        try:
            experiment_response = call_llm(prompt_experiment, "auto", 120)
            experiment_design = extract_markdown_content(experiment_response)
            result["experiment_design"] = experiment_design
            logger.info("实验设计生成完成")
        except Exception as e:
            logger.error(f"实验设计生成失败: {str(e)}")
            result["status"] = "error"
            result["message"] = f"实验设计生成失败: {str(e)}"
            return result
        
        logger.info("论文生成流程全部完成")
        return result
        
    except Exception as e:
        logger.error(f"生成过程中出现错误: {str(e)}")
        result["status"] = "error"
        result["message"] = f"生成失败: {str(e)}"
        return result

# ================================ 简化的API接口函数 ================================

def generate_academic_report_api(
    title: str = "", 
    details: str = "", 
    academic_level: str = "硕士", 
    country: str = "中国",
    material_files: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    学术报告生成API接口函数
    
    Args:
        title (str): 论文标题
        details (str): 初步研究方案  
        academic_level (str): 学术层次
        country (str): 就读国家
        material_files (Optional[List[str]]): 本地文件路径列表
        
    Returns:
        Dict[str, Any]: 生成结果
    """
    if not title and not details:
        return {
            "status": "error",
            "message": "请提供论文标题或研究方案",
            "proposal": "",
            "experiment_design": ""
        }
    
    return generate_academic_report(title, details, academic_level, country, material_files)

if __name__ == "__main__":
    # 测试函数
    test_result = generate_academic_report_api(
        title="基于深度学习的智能问答系统研究",
        details="研究如何利用大语言模型构建更准确、更自然的智能问答系统，重点解决多轮对话和知识推理问题。",
        academic_level="硕士",
        country="中国"
    )
    
    print("开题报告:")
    print(test_result["proposal"])
    print("\n" + "="*50 + "\n")
    print("实验设计:")
    print(test_result["experiment_design"])
