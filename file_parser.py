import os
import logging
from typing import List, Dict, Any
import zipfile
import xml.etree.ElementTree as ET

logger = logging.getLogger('file_parser')

def extract_text_from_pdf(file_path: str) -> str:
    """
    从PDF文件中提取文本内容
    
    Args:
        file_path (str): PDF文件路径
        
    Returns:
        str: 提取的文本内容
    """
    try:
        import PyPDF2
        
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
                
        return text.strip()
    except ImportError:
        logger.error("PyPDF2 not installed. Please install it with: pip install PyPDF2")
        return ""
    except Exception as e:
        logger.error(f"Error reading PDF file {file_path}: {str(e)}")
        return ""

def extract_text_from_docx(file_path: str) -> str:
    """
    从DOCX文件中提取文本内容
    
    Args:
        file_path (str): DOCX文件路径
        
    Returns:
        str: 提取的文本内容
    """
    try:
        import docx
        
        doc = docx.Document(file_path)
        text = ""
        
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
            
        return text.strip()
    except ImportError:
        logger.error("python-docx not installed. Please install it with: pip install python-docx")
        return ""
    except Exception as e:
        logger.error(f"Error reading DOCX file {file_path}: {str(e)}")
        return ""

def extract_text_from_doc(file_path: str) -> str:
    """
    从DOC文件中提取文本内容（使用python-docx2txt作为备选方案）
    
    Args:
        file_path (str): DOC文件路径
        
    Returns:
        str: 提取的文本内容
    """
    try:
        import docx2txt
        text = docx2txt.process(file_path)
        return text.strip() if text else ""
    except ImportError:
        logger.error("docx2txt not installed. Please install it with: pip install docx2txt")
        return ""
    except Exception as e:
        logger.error(f"Error reading DOC file {file_path}: {str(e)}")
        return ""

def parse_local_file(file_path: str, file_type: int) -> Dict[str, Any]:
    """
    解析本地文件
    
    Args:
        file_path (str): 文件路径
        file_type (int): 文件类型 1-开题报告 2-实验设计 3-论文模板 4-论文材料
        
    Returns:
        Dict[str, Any]: 解析结果
    """
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return {}
    
    file_extension = os.path.splitext(file_path)[1].lower()
    text_content = ""
    
    if file_extension == '.pdf':
        text_content = extract_text_from_pdf(file_path)
    elif file_extension == '.docx':
        text_content = extract_text_from_docx(file_path)
    elif file_extension == '.doc':
        text_content = extract_text_from_doc(file_path)
    else:
        logger.error(f"Unsupported file format: {file_extension}")
        return {}
    
    if not text_content:
        logger.warning(f"No text content extracted from {file_path}")
        return {}
    
    result = {
        'fileName': os.path.basename(file_path),
        'fileBizType': file_type,
        'fileContent': text_content
    }
    
    # 对于论文材料，尝试提取标题和摘要
    if file_type == 4:  # 论文材料
        title, abstract = extract_paper_metadata(text_content)
        result.update({
            'paper_title': title,
            'paper_abstract': abstract,
            'citationInfo': ''  # 本地解析暂不提供引用信息
        })
    
    return result

def extract_paper_metadata(text: str) -> tuple:
    """
    从论文文本中提取标题和摘要
    
    Args:
        text (str): 论文文本
        
    Returns:
        tuple: (标题, 摘要)
    """
    lines = text.split('\n')
    title = ""
    abstract = ""
    
    # 简单的标题提取：取前几行中最长的非空行作为标题
    for i, line in enumerate(lines[:10]):
        line = line.strip()
        if line and len(line) > len(title) and len(line) < 200:
            title = line
    
    # 简单的摘要提取：查找包含"abstract"的段落
    abstract_keywords = ['abstract', 'Abstract', 'ABSTRACT', '摘要', '摘　要']
    for i, line in enumerate(lines):
        if any(keyword in line for keyword in abstract_keywords):
            # 从这一行开始，取后续几行作为摘要
            abstract_lines = []
            for j in range(i+1, min(i+20, len(lines))):
                next_line = lines[j].strip()
                if next_line and not any(stop_word in next_line.lower() for stop_word in ['introduction', 'keywords', '关键词', '1.', '一、']):
                    abstract_lines.append(next_line)
                elif len(abstract_lines) > 0:
                    break
            abstract = ' '.join(abstract_lines)
            break
    
    return title[:200], abstract[:500]  # 限制长度

def parse_material_files(file_paths: List[str]) -> List[Dict[str, Any]]:
    """
    批量解析材料文件
    
    Args:
        file_paths (List[str]): 文件路径列表
        
    Returns:
        List[Dict[str, Any]]: 解析结果列表
    """
    results = []
    
    for file_path in file_paths:
        if isinstance(file_path, dict):
            # 如果传入的是文件信息字典
            path = file_path.get('filePath', file_path.get('fileKey', ''))
            file_type = file_path.get('fileBizType', 4)  # 默认为论文材料
        else:
            # 如果传入的是文件路径字符串
            path = file_path
            # 根据文件名推断类型
            filename = os.path.basename(path).lower()
            if '开题' in filename or 'proposal' in filename:
                file_type = 1
            elif '实验' in filename or 'experiment' in filename:
                file_type = 2
            else:
                file_type = 4  # 默认为论文材料
        
        if path:
            result = parse_local_file(path, file_type)
            if result:
                results.append(result)
    
    return results 