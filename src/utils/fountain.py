"""Fountain 格式转换器"""
from typing import Dict, Any, List


class FountainConverter:
    """YAML 剧本转 Fountain 格式"""

    def __init__(self):
        self.indent_action = ""
        self.indent_dialogue = "                "

    def to_fountain(self, data: Dict[str, Any]) -> str:
        """将 YAML 剧本转换为 Fountain 格式"""
        lines = []
        lines.append(f"Title: {data.get('metadata', {}).get('title', 'UNTITLED')}")
        lines.append(f"Credit: Written by")
        lines.append(f"Author: {data.get('metadata', {}).get('author', 'Anonymous')}")
        lines.append(f"Genre: {data.get('metadata', {}).get('genre', '')}")
        lines.append(f"Draft date: {data.get('metadata', {}).get('created_at', '')}")
        lines.append("")

        # Characters
        characters = data.get("characters", [])
        if characters:
            lines.append("== Characters ==")
            for char in characters:
                lines.append(f"{char.get('name', '')}")
            lines.append("")

        # Scenes
        scenes = data.get("scenes", [])
        for scene in scenes:
            lines.extend(self._format_scene(scene))

        return "\n".join(lines)

    def _format_scene(self, scene: Dict) -> List[str]:
        """格式化单个场景"""
        lines = []
        scene_id = scene.get("scene_id", "")

        # Scene Heading
        slugline = scene.get("slugline", {})
        int_ext = slugline.get("int_ext", "")
        location = slugline.get("location", "")
        time = slugline.get("time", "")

        lines.append(f"{int_ext}. {location} - {time}")
        if scene.get("mood"):
            lines.append(f"// Mood: {scene['mood']}")
        lines.append("")

        # Content
        content = scene.get("content", [])
        for item in content:
            item_type = item.get("type", "")
            text = item.get("text", "")

            if item_type == "action":
                lines.append(text)
                lines.append("")

            elif item_type == "character":
                name = item.get("name", "")
                ext = item.get("extension", "")
                if ext:
                    lines.append(f"{name} ({ext})")
                else:
                    lines.append(name)
                lines.append("")

            elif item_type == "parenthetical":
                para = item.get("text", "")
                lines.append(f"({para})")
                lines.append("")

            elif item_type == "dialogue":
                dialogue = item.get("text", "")
                voiceover = item.get("voiceover", False)
                offscreen = item.get("offscreen", False)

                if voiceover:
                    dialogue = f"(V.O.) {dialogue}"
                elif offscreen:
                    dialogue = f"(O.S.) {dialogue}"

                lines.append(dialogue)
                lines.append("")

            elif item_type == "transition":
                trans = item.get("text", "")
                lines.append(f"{trans}")
                lines.append("")

            elif item_type == "shot":
                shot_type = item.get("shot_type", "")
                desc = item.get("description", "")
                lines.append(f"[{shot_type}: {desc}]")
                lines.append("")

            elif item_type == "sound":
                desc = item.get("description", "")
                lines.append(f"SOUND: {desc}")
                lines.append("")

        return lines

    def from_fountain(self, fountain_text: str) -> Dict[str, Any]:
        """从 Fountain 格式解析（简化版）"""
        # TODO: 实现 Fountain 到 YAML 的反向转换
        raise NotImplementedError("Fountain 到 YAML 的转换尚未实现")


def convert_to_fountain(yaml_file: str, output_file: str = None):
    """便捷转换函数"""
    import yaml
    from pathlib import Path

    path = Path(yaml_file)
    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {yaml_file}")

    with open(path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    converter = FountainConverter()
    fountain_text = converter.to_fountain(data)

    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(fountain_text)
    else:
        output_path = path.with_suffix('.fountain')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(fountain_text)

    return fountain_text


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("用法: python fountain_converter.py <input.yaml> [output.fountain]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        result = convert_to_fountain(input_file, output_file)
        if output_file:
            print(f"已转换到: {output_file}")
        else:
            print(result)
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)