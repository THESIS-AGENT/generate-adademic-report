from flask import Flask, request, jsonify
import logging
import traceback
import json
from main import generate_academic_report_api

# 配置Flask应用
app = Flask(__name__)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        'status': 'healthy',
        'message': '学术论文生成服务运行正常'
    }), 200

@app.route('/generate_academic_report', methods=['POST'])
def generate():
    """
    生成开题报告和实验设计的主接口
    
    请求体格式:
    {
        "title": "论文标题",
        "details": "研究方案详情", 
        "academicLevel": "本科|硕士|博士",
        "country": "中国|美国|英国|澳大利亚|加拿大|日本|欧洲",
        "materialFiles": ["文件路径1", "文件路径2"]  // 可选
    }
    """
    try:
        # 获取请求数据
        data = request.get_json()
        
        if not data:
            return jsonify({
                'code': 400,
                'message': '请求数据不能为空',
                'data': None
            }), 400
        
        # 提取参数
        title = data.get('title', '').strip()
        details = data.get('details', '').strip()
        academic_level = data.get('academicLevel', '硕士')
        country = data.get('country', '中国')
        material_files = data.get('materialFiles', [])
        
        # 参数验证
        if not title and not details:
            return jsonify({
                'code': 400,
                'message': '请提供论文标题或研究方案',
                'data': None
            }), 400
        
        # 验证学术层次
        valid_levels = ['本科', '硕士', '博士']
        if academic_level not in valid_levels:
            return jsonify({
                'code': 400,
                'message': f'学术层次必须是以下之一: {", ".join(valid_levels)}',
                'data': None
            }), 400
        
        # 验证国家
        valid_countries = ['中国', '美国', '英国', '澳大利亚', '加拿大', '日本', '欧洲']
        if country not in valid_countries:
            return jsonify({
                'code': 400,
                'message': f'国家必须是以下之一: {", ".join(valid_countries)}',
                'data': None
            }), 400
        
        logger.info(f"收到生成请求 - 标题: {title[:50]}..., 学术层次: {academic_level}, 国家: {country}")
        
        # 调用生成函数
        result = generate_academic_report_api(
            title=title,
            details=details,
            academic_level=academic_level,
            country=country,
            material_files=material_files
        )
        
        if result['status'] == 'success':
            response_data = {
                'proposal': result['proposal'],
                'experiment_design': result['experiment_design'],
                'zhihu_research_count': len(result.get('zhihu_research', [])),
                'arxiv_papers_count': len(result.get('arxiv_papers', []))
            }
            
            return jsonify({
                'code': 200,
                'message': '生成成功',
                'data': response_data
            }), 200
        else:
            return jsonify({
                'code': 500,
                'message': result.get('message', '生成失败'),
                'data': None
            }), 500
            
    except Exception as e:
        logger.error(f"生成过程中发生错误: {str(e)}")
        logger.error(traceback.format_exc())
        
        return jsonify({
            'code': 500,
            'message': f'服务器内部错误: {str(e)}',
            'data': None
        }), 500

@app.route('/generate_academic_report_detailed', methods=['POST'])
def generate_detailed():
    """
    生成开题报告和实验设计的详细接口，返回所有中间结果
    """
    try:
        # 获取请求数据
        data = request.get_json()
        
        if not data:
            return jsonify({
                'code': 400,
                'message': '请求数据不能为空',
                'data': None
            }), 400
        
        # 提取参数
        title = data.get('title', '').strip()
        details = data.get('details', '').strip()
        academic_level = data.get('academicLevel', '硕士')
        country = data.get('country', '中国')
        material_files = data.get('materialFiles', [])
        
        # 参数验证（与上面相同）
        if not title and not details:
            return jsonify({
                'code': 400,
                'message': '请提供论文标题或研究方案',
                'data': None
            }), 400
        
        logger.info(f"收到详细生成请求 - 标题: {title[:50]}..., 学术层次: {academic_level}, 国家: {country}")
        
        # 调用生成函数
        result = generate_academic_report_api(
            title=title,
            details=details,
            academic_level=academic_level,
            country=country,
            material_files=material_files
        )
        
        if result['status'] == 'success':
            return jsonify({
                'code': 200,
                'message': '生成成功',
                'data': {
                    'proposal': result['proposal'],
                    'experiment_design': result['experiment_design'],
                    'zhihu_research': result.get('zhihu_research', []),
                    'arxiv_papers': result.get('arxiv_papers', []),
                    'research_sources': {
                        'zhihu_count': len(result.get('zhihu_research', [])),
                        'arxiv_count': len(result.get('arxiv_papers', []))
                    }
                }
            }), 200
        else:
            return jsonify({
                'code': 500,
                'message': result.get('message', '生成失败'),
                'data': None
            }), 500
            
    except Exception as e:
        logger.error(f"详细生成过程中发生错误: {str(e)}")
        logger.error(traceback.format_exc())
        
        return jsonify({
            'code': 500,
            'message': f'服务器内部错误: {str(e)}',
            'data': None
        }), 500

@app.route('/api_info', methods=['GET'])
def api_info():
    """获取API使用说明"""
    info = {
        'service_name': '学术论文智能生成系统',
        'version': '2.0.0-simplified',
        'description': '基于人工智能的学术论文开题报告和实验设计自动生成系统',
        'endpoints': {
            '/health': {
                'method': 'GET',
                'description': '健康检查'
            },
            '/generate_academic_report': {
                'method': 'POST',
                'description': '生成开题报告和实验设计',
                'parameters': {
                    'title': 'string - 论文标题',
                    'details': 'string - 研究方案详情',
                    'academicLevel': 'string - 学术层次（本科/硕士/博士）',
                    'country': 'string - 就读国家',
                    'materialFiles': 'array - 本地文件路径列表（可选）'
                }
            },
            '/generate_academic_report_detailed': {
                'method': 'POST', 
                'description': '生成开题报告和实验设计（详细版，包含所有中间结果）',
                'parameters': '同上'
            }
        },
        'supported_file_formats': ['PDF', 'DOCX', 'DOC'],
        'supported_academic_levels': ['本科', '硕士', '博士'],
        'supported_countries': ['中国', '美国', '英国', '澳大利亚', '加拿大', '日本', '欧洲']
    }
    
    return jsonify(info), 200

@app.errorhandler(404)
def not_found(error):
    """404错误处理"""
    return jsonify({
        'code': 404,
        'message': '接口不存在',
        'data': None
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """405错误处理"""
    return jsonify({
        'code': 405,
        'message': '请求方法不被允许',
        'data': None
    }), 405

@app.errorhandler(500)
def internal_error(error):
    """500错误处理"""
    logger.error(f"内部服务器错误: {str(error)}")
    return jsonify({
        'code': 500,
        'message': '服务器内部错误',
        'data': None
    }), 500

if __name__ == '__main__':
    logger.info("启动学术论文生成服务（简化版）")
    app.run(host='0.0.0.0', port=5000, debug=False) 