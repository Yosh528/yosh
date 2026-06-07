"""Novel-to-Script 核心服务"""
from typing import Dict, Any, Optional
from src.models.screenplay import Screenplay, Metadata, Character, Scene, Slugline, ContentItem


class NovelConverter:
    """小说转剧本转换器"""

    def __init__(self):
        self.characters = {}  # id -> Character
        self.scene_counter = 0

    def convert_novel_to_screenplay(
        self,
        novel_text: str,
        metadata: Dict[str, Any],
        prev_characters: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        将小说文本转换为剧本 YAML 结构

        注意：实际的 AI 转换应该在外部完成，这里提供结构化辅助
        """
        from src.models.screenplay import (
            Version, Project, Metadata as MD, Character as Char,
            Scene, Slugline, ContentItem, Extensions
        )

        # 构建版本信息
        version = Version()
        project = Project(generated_by="novel-to-script v1.0.0")

        # 构建元数据
        meta = MD(
            title=metadata.get("title", "Untitled"),
            author=metadata.get("author", "Anonymous"),
            genre=metadata.get("genre", "未知"),
            format=metadata.get("format", "短剧"),
            logline=metadata.get("logline", "")
        )

        return {
            "_version": version.model_dump(),
            "_project": project.model_dump(),
            "metadata": meta.model_dump(),
            "characters": [],
            "scenes": [],
            "notes": [],
            "extensions": {}
        }

    def extract_characters_from_content(self, content: list) -> Dict[str, Character]:
        """从场景内容中提取角色"""
        char_map = {}

        for item in content:
            if item.get("type") == "character":
                char_id = item.get("id", "")
                char_name = item.get("name", "")
                if char_id and char_name:
                    char_map[char_id] = Character(
                        id=char_id,
                        name=char_name,
                        code_name=char_name.upper().replace(" ", "")
                    )

        return char_map

    def calculate_character_stats(self, scenes: list) -> Dict[str, Dict]:
        """计算角色统计数据"""
        stats = {}

        for scene in scenes:
            chars_present = scene.get("characters_present", [])
            for char_id in chars_present:
                if char_id not in stats:
                    stats[char_id] = {"scenes": 0, "lines": 0, "words": 0}

                stats[char_id]["scenes"] += 1

            for item in scene.get("content", []):
                if item.get("type") == "character":
                    char_id = item.get("id", "")
                    if char_id and char_id in stats:
                        stats[char_id]["lines"] += 1

                elif item.get("type") == "dialogue":
                    text = item.get("text", "")
                    char_id = item.get("id", "")
                    if char_id and char_id in stats:
                        stats[char_id]["words"] += len(text)

        return stats


def batch_convert_chapters(
    chapter_files: list,
    output_dir: str,
    template: str = None
) -> list:
    """批量转换多章节小说"""
    # TODO: 实现批量转��
    raise NotImplementedError("批量转换功能开发中")