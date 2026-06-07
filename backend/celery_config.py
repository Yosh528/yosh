import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

def make_celery(app_name=__name__):
    redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    
    celery = Celery(
        app_name,
        broker=redis_url,
        backend=redis_url
    )
    
    return celery

celery = make_celery()

@celery.task
def generate_script_task(novel_id: int):
    """异步生成剧本任务"""
    from app import create_app
    from models import Novel, Script
    from services.script_generator import ScriptGenerator
    
    app = create_app()
    
    with app.app_context():
        novel = Novel.query.get(novel_id)
        if not novel:
            return {'error': '小说不存在'}
        
        try:
            generator = ScriptGenerator()
            script_content = generator.generate_script(novel.content)
            
            script = Script(
                user_id=novel.user_id,
                novel_id=novel.id,
                content=script_content,
                status='complete',
                completed_at=datetime.utcnow()
            )
            db.session.add(script)
            db.session.commit()
            
            return {'success': True, 'script_id': script.id}
        
        except Exception as e:
            script = Script(
                user_id=novel.user_id,
                novel_id=novel.id,
                content='',
                status='failed'
            )
            db.session.add(script)
            db.session.commit()
            
            return {'success': False, 'error': str(e)}