"""YAML 验证器"""
import yaml
from pathlib import Path
from typing import Dict, Any, List, Tuple


class ValidationError(Exception):
    """验证错误异常"""
    def __init__(self, errors: List[str]):
        self.errors = errors
        super().__init__("\n".join(errors))


class ScreenplayValidator:
    """剧本 YAML 验证器"""

    REQUIRED_FIELDS = {
        "_version": ["schema_version"],
        "metadata": ["title", "author", "genre", "format", "logline"],
    }

    CONTENT_TYPES = {
        "scene_heading", "action", "character", "parenthetical",
        "dialogue", "transition", "shot", "sound"
    }

    VALID_INT_EXT = {"INT.", "EXT.", "INT./EXT.", "EXT./INT."}
    VALID_TIME = {
        "DAY", "NIGHT", "DAWN", "DUSK", "MORNING", "EVENING",
        "LATER", "CONTINUOUS", "AM", "PM"
    }

    def __init__(self, strict: bool = True):
        self.strict = strict
        self.errors: List[str] = []

    def validate(self, data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """验证 YAML 数据的完整性和正确性"""
        self.errors = []

        self._validate_top_level(data)
        self._validate_metadata(data.get("metadata", {}))
        self._validate_characters(data.get("characters", []))
        self._validate_scenes(data.get("scenes", []))

        if self.errors:
            return False, self.errors
        return True, []

    def _add_error(self, path: str, message: str):
        """添加错误信息"""
        self.errors.append(f"[{path}] {message}")

    def _validate_top_level(self, data: Dict):
        """验证顶层结构"""
        if "_version" not in data:
            self._add_error("root", "缺少 _version 字段")

        if "metadata" not in data:
            self._add_error("root", "缺少 metadata 字段")

    def _validate_metadata(self, meta: Dict):
        """验证元数据"""
        if not meta:
            self._add_error("metadata", "为空对象")
            return

        required = ["title", "author", "genre", "format", "logline"]
        for field in required:
            if field not in meta or not meta[field]:
                self._add_error("metadata", f"缺少必填字段: {field}")

    def _validate_characters(self, characters: List):
        """验证角色库"""
        if not characters:
            return

        ids = set()
        code_names = set()

        for i, char in enumerate(characters):
            char_id = char.get("id", "")
            code_name = char.get("code_name", "")

            if not char_id:
                self._add_error(f"characters[{i}]", "缺少 id 字段")
            elif char_id in ids:
                self._add_error(f"characters[{i}]", f"重复的角色 id: {char_id}")
            else:
                ids.add(char_id)

            if not code_name:
                self._add_error(f"characters[{i}]", "缺少 code_name 字段")
            elif code_name.upper() != code_name:
                self._add_error(f"characters[{i}]", f"code_name 必须全大写: {code_name}")
            elif code_name in code_names:
                self._add_error(f"characters[{i}]", f"重复的 code_name: {code_name}")
            else:
                code_names.add(code_name)

    def _validate_scenes(self, scenes: List):
        """验证场景列表"""
        if not scenes:
            self._add_error("scenes", "场景列表为空")
            return

        scene_ids = set()
        prev_scene_id = None

        for i, scene in enumerate(scenes):
            self._validate_single_scene(scene, i, scene_ids)

            # 检查 scene_id 连续性
            scene_id = scene.get("scene_id", "")
            if scene_id and prev_scene_id:
                expected_num = self._extract_scene_number(prev_scene_id) + 1
                actual_num = self._extract_scene_number(scene_id)
                if actual_num != expected_num and self.strict:
                    pass  # 警告但不阻断

            prev_scene_id = scene_id

    def _validate_single_scene(self, scene: Dict, index: int, scene_ids: set):
        """验证单个场景"""
        scene_path = f"scenes[{index}]"

        # 必需字段
        if "scene_id" not in scene:
            self._add_error(scene_path, "缺少 scene_id")

        scene_id = scene.get("scene_id", "")
        if scene_id in scene_ids:
            self._add_error(scene_path, f"重复的 scene_id: {scene_id}")
        else:
            scene_ids.add(scene_id)

        # slugline 验证
        slugline = scene.get("slugline", {})
        if not slugline:
            self._add_error(scene_path, "缺少 slugline")
        else:
            int_ext = slugline.get("int_ext", "")
            if int_ext not in self.VALID_INT_EXT:
                self._add_error(f"{scene_path}.slugline.int_ext",
                           f"无效值: {int_ext}，应为 {self.VALID_INT_EXT}")

            time_val = slugline.get("time", "")
            if time_val not in self.VALID_TIME:
                self._add_error(f"{scene_path}.slugline.time",
                           f"无效值: {time_val}，应为 {self.VALID_TIME}")

        # content 验证
        content = scene.get("content", [])
        if not content:
            self._add_error(f"{scene_path}.content", "场景内容为空")

        for j, item in enumerate(content):
            item_type = item.get("type", "")
            if item_type not in self.CONTENT_TYPES:
                self._add_error(f"{scene_path}.content[{j}]",
                             f"未知的 type: {item_type}")

    def _extract_scene_number(self, scene_id: str) -> int:
        """提取场景编号数字"""
        import re
        match = re.search(r'\d+', scene_id)
        return int(match.group()) if match else 0

    def validate_file(self, file_path: str) -> Tuple[bool, List[str]]:
        """验证 YAML 文件"""
        path = Path(file_path)

        if not path.exists():
            return False, [f"文件不存在: {file_path}"]

        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            return False, [f"YAML 解析错误: {e}"]

        return self.validate(data)


def validate_screenplay(file_path: str, strict: bool = True) -> Tuple[bool, List[str]]:
    """便捷验证函数"""
    validator = ScreenplayValidator(strict=strict)
    return validator.validate_file(file_path)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("用法: python yaml_validator.py <file.yaml>")
        sys.exit(1)

    valid, errors = validate_screenplay(sys.argv[1])

    if valid:
        print("✓ 验证通过")
    else:
        print("✗ 验证失败:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)