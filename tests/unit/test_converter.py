# 测试用例
import pytest
from src.validators.yaml_validator import ScreenplayValidator
from src.utils.fountain import FountainConverter


def test_validator_valid_data():
    """测试有效数据验证"""
    data = {
        "_version": {"schema_version": "1.0.0"},
        "metadata": {
            "title": "测试剧本",
            "author": "张三",
            "genre": "悬疑",
            "format": "短剧",
            "logline": "一个有趣的故事"
        },
        "scenes": [
            {
                "scene_id": "SC001",
                "slugline": {
                    "int_ext": "INT.",
                    "location": "房间",
                    "time": "DAY"
                },
                "content": [
                    {"type": "action", "text": "场景描述"},
                    {"type": "character", "name": "李明", "id": "char_001"},
                    {"type": "dialogue", "text": "你好"}
                ]
            }
        ]
    }

    validator = ScreenplayValidator()
    valid, errors = validator.validate(data)
    assert valid, f"验证失败: {errors}"


def test_validator_missing_meta():
    """测试缺失必填字段"""
    data = {
        "_version": {"schema_version": "1.0.0"},
        "metadata": {},
        "scenes": []
    }

    validator = ScreenplayValidator()
    valid, errors = validator.validate(data)
    assert not valid


def test_fountain_converter():
    """测试 Fountain 转换"""
    data = {
        "metadata": {
            "title": "测试",
            "author": "张三",
            "genre": "爱情",
            "created_at": "2026-06-05"
        },
        "scenes": [
            {
                "scene_id": "SC001",
                "slugline": {"int_ext": "INT.", "location": "咖啡馆", "time": "DAY"},
                "content": [
                    {"type": "action", "text": "阳光透过窗户洒进来。"},
                    {"type": "character", "name": "小红", "id": "char_001"},
                    {"type": "dialogue", "text": "你好。"}
                ]
            }
        ]
    }

    converter = FountainConverter()
    result = converter.to_fountain(data)
    assert "Title: 测试" in result
    assert "INT." in result