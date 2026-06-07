"""FastAPI 路由定义"""
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional, List
from pydantic import BaseModel
from src.services.converter import NovelConverter


router = APIRouter(prefix="/api/v1", tags=["novel-to-script"])
converter = NovelConverter()


class ConvertRequest(BaseModel):
    """转换请求"""
    title: str
    author: str
    genre: str = "未知"
    format: str = "短剧"
    logline: str


class ConvertResponse(BaseModel):
    """转换响应"""
    success: bool
    yaml_content: Optional[str] = None
    error: Optional[str] = None
    scene_count: int = 0
    character_count: int = 0


@router.post("/convert", response_model=ConvertResponse)
async def convert_novel(
    file: UploadFile = File(...),
    title: str = Form(...),
    author: str = Form(...),
    genre: str = Form("未知"),
    format: str = Form("短剧"),
    logline: str = Form("")
):
    """转换小说文本为剧本"""
    # 读取上传的文件
    try:
        content = await file.read()
        novel_text = content.decode("utf-8")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"文件读取失败: {e}")

    if not novel_text.strip():
        raise HTTPException(status_code=400, detail="小说文本为空")

    # 构建元数据
    metadata = {
        "title": title,
        "author": author,
        "genre": genre,
        "format": format,
        "logline": logline
    }

    # 转换（注：实际 AI 转换需要在外部调用 Claude API）
    # 这里返回结构化模板，实际转换由 AI 完成
    result = converter.convert_novel_to_screenplay(novel_text, metadata)

    import yaml
    yaml_content = yaml.dump(result, allow_unicode=True, default_flow_style=False)

    return ConvertResponse(
        success=True,
        yaml_content=yaml_content,
        scene_count=len(result.get("scenes", [])),
        character_count=len(result.get("characters", []))
    )


@router.post("/validate")
async def validate_yaml(yaml_content: str):
    """验证剧本 YAML"""
    import yaml
    from src.validators.yaml_validator import ScreenplayValidator

    try:
        data = yaml.safe_load(yaml_content)
    except yaml.YAMLError as e:
        raise HTTPException(status_code=400, detail=f"YAML 解析错误: {e}")

    validator = ScreenplayValidator()
    valid, errors = validator.validate(data)

    return {
        "valid": valid,
        "errors": errors
    }


@router.post("/to-fountain")
async def convert_to_fountain(yaml_content: str):
    """转换为 Fountain 格式"""
    import yaml
    from src.utils.fountain import FountainConverter

    try:
        data = yaml.safe_load(yaml_content)
    except yaml.YAMLError as e:
        raise HTTPException(status_code=400, detail=f"YAML 解析错误: {e}")

    converter = FountainConverter()
    fountain_text = converter.to_fountain(data)

    return {
        "success": True,
        "fountain": fountain_text
    }


@router.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "ok", "service": "novel-to-script"}