from flask import Blueprint, request, jsonify
from models import Novel, Script, User
from extensions import db
from services.script_generator import ScriptGenerator
from datetime import datetime

script_bp = Blueprint('script', __name__)

@script_bp.route('/convert', methods=['POST'])
def convert_novel_to_script():
    data = request.get_json()
    
    required_fields = ['user_id', 'title', 'content']
    if not all(field in data for field in required_fields):
        return jsonify({'error': '缺少必要字段'}), 400
    
    # 验证用户存在
    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({'error': '用户不存在'}), 404
    
    # 验证小说内容长度
    if len(data['content'].strip()) < 100:
        return jsonify({'error': '小说内容至少需要100字符'}), 400
    
    # 计算章节数（简单按章节标题分割）
    chapters = data['content'].count('第')  # 简单估算
    
    # 保存小说
    novel = Novel(
        user_id=data['user_id'],
        title=data['title'],
        content=data['content'],
        chapters=chapters
    )
    db.session.add(novel)
    db.session.commit()
    
    try:
        # 生成剧本
        generator = ScriptGenerator()
        script_content = generator.generate_script(data['content'])
        
        # 保存剧本
        script = Script(
            user_id=data['user_id'],
            novel_id=novel.id,
            content=script_content,
            status='complete',
            completed_at=datetime.utcnow()
        )
        db.session.add(script)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '转换成功',
            'script': {
                'id': script.id,
                'novel_id': novel.id,
                'content': script_content,
                'status': script.status
            }
        })
        
    except Exception as e:
        # 转换失败
        script = Script(
            user_id=data['user_id'],
            novel_id=novel.id,
            content='',
            status='failed'
        )
        db.session.add(script)
        db.session.commit()
        
        return jsonify({
            'success': False,
            'message': f'转换失败: {str(e)}',
            'script': {
                'id': script.id,
                'novel_id': novel.id,
                'status': 'failed'
            }
        }), 500

@script_bp.route('/<int:script_id>', methods=['GET'])
def get_script(script_id):
    script = Script.query.get(script_id)
    
    if not script:
        return jsonify({'error': '剧本不存在'}), 404
    
    return jsonify({
        'id': script.id,
        'user_id': script.user_id,
        'novel_id': script.novel_id,
        'content': script.content,
        'status': script.status,
        'created_at': script.created_at.isoformat(),
        'completed_at': script.completed_at.isoformat() if script.completed_at else None
    })

@script_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_scripts(user_id):
    scripts = Script.query.filter_by(user_id=user_id).order_by(Script.created_at.desc()).all()
    
    return jsonify({
        'success': True,
        'scripts': [{
            'id': script.id,
            'novel_id': script.novel_id,
            'status': script.status,
            'created_at': script.created_at.isoformat(),
            'completed_at': script.completed_at.isoformat() if script.completed_at else None
        } for script in scripts]
    })

@script_bp.route('/<int:script_id>', methods=['DELETE'])
def delete_script(script_id):
    script = Script.query.get(script_id)
    
    if not script:
        return jsonify({'error': '剧本不存在'}), 404
    
    db.session.delete(script)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': '删除成功'
    })