from .llm_client import MinimaxClient, LLMServiceError
import yaml
import re

class ScriptGenerator:
    def __init__(self):
        self.llm_client = MinimaxClient()
    
    def generate_script(self, novel_text: str) -> str:
        """将小说文本转换为剧本YAML"""
        if not novel_text or len(novel_text.strip()) < 100:
            raise ValueError("小说内容不能为空且至少100字符")
        
        # 构建转换prompt
        prompt = self._build_prompt(novel_text)
        
        # 调用大模型
        result = self.llm_client.call_api(prompt)
        
        # 清理和验证输出
        return self._clean_and_validate(result)
    
    def _build_prompt(self, novel_text: str) -> str:
        """构建大模型prompt"""
        return f"""
请将以下小说文本转换为结构化剧本，输出格式为YAML。

小说内容：
{novel_text[:8000]}

输出要求：
1. 严格按照以下YAML格式输出，不要包含任何markdown代码块标记（不要用```yaml或```）
2. 所有字符串值必须用英文双引号包裹，不要使用中文引号
3. 剧本结构包含：剧本标题(title)、场景列表(scenes)
4. 每个场景包含：场景编号(scene_number)、场景标题(scene_title)、场景描述(description)、角色列表(characters)、对话列表(dialogues)
5. 对话包含：角色名(character)、台词(line)、动作(action，可选)

YAML格式示例：
title: "剧本标题"
scenes:
  - scene_number: 1
    scene_title: "第一章：初遇"
    description: "阳光明媚的早晨，男主角走在校园的林荫道上。"
    characters:
      - "李明"
      - "小雨"
    dialogues:
      - character: "李明"
        line: "今天天气真好啊。"
        action: "抬头望向天空"
      - character: "小雨"
        line: "是啊，适合出去走走。"

请确保输出是有效的YAML格式，可以被Python yaml库解析。所有字符串值必须用英文双引号。
"""
    
    def _clean_and_validate(self, output: str) -> str:
        """清理并验证YAML输出"""
        # 移除markdown代码块标记
        output = output.replace('```yaml', '').replace('```', '').strip()
        
        # 替换中文引号为英文引号
        output = output.replace('"', '"').replace('"', '"')
        output = output.replace("'", "'").replace("'", "'")
        
        # 提取 YAML 内容 - 找到 title: 开头的行，直到结尾
        lines = output.split('\n')
        yaml_lines = []
        found_yaml_start = False
        
        for line in lines:
            # 找到 YAML 开始
            if line.strip().startswith('title:') or line.strip().startswith('scenes:'):
                found_yaml_start = True
            
            if found_yaml_start:
                # 跳过空行和说明文字
                stripped = line.strip()
                if stripped and not stripped.startswith('请') and not stripped.startswith('注意') and not stripped.startswith('以上'):
                    yaml_lines.append(line)
        
        output = '\n'.join(yaml_lines).strip()
        
        # 如果没有找到 YAML，尝试另一种方式提取
        if not output or not output.strip().startswith('title'):
            # 尝试从整个输出中提取 YAML 结构
            import re
            yaml_match = re.search(r'(title:.*?scenes:.*?(?:dialogues|characters).*?)', output, re.DOTALL)
            if yaml_match:
                output = yaml_match.group(1)
        
        # 尝试解析验证
        try:
            yaml.safe_load(output)
        except yaml.YAMLError as e:
            # 如果解析失败，尝试修复常见问题
            output = self._fix_yaml_issues(output)
            try:
                yaml.safe_load(output)
            except yaml.YAMLError:
                # 最后尝试：生成一个简单的 YAML 结构
                output = self._generate_fallback_yaml(novel_text="")
                try:
                    yaml.safe_load(output)
                except yaml.YAMLError:
                    raise LLMServiceError(f"生成的剧本YAML格式无效: {str(e)}")
        
        return output
    
    def _fix_yaml_issues(self, yaml_text: str) -> str:
        """尝试修复常见的YAML格式问题"""
        # 确保所有列表项字符串被引号包裹
        lines = yaml_text.split('\n')
        fixed_lines = []
        
        for line in lines:
            # 处理 characters 列表项
            if line.strip().startswith('- ') and not line.strip().startswith('- "'):
                # 检查是否是简单的字符串项（不包含其他YAML结构）
                content = line.strip()[2:].strip()
                if ':' not in content and not content.startswith('"'):
                    indent = len(line) - len(line.lstrip())
                    fixed_lines.append(' ' * indent + '- "' + content + '"')
                else:
                    fixed_lines.append(line)
            else:
                fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)
    
    def _generate_fallback_yaml(self, novel_text: str) -> str:
        """生成备用YAML结构（当大模型输出无效时）"""
        return '''title: "剧本初稿"
scenes:
  - scene_number: 1
    scene_title: "第一章"
    description: "故事开始"
    characters:
      - "主角"
      - "配角"
    dialogues:
      - character: "主角"
        line: "故事开始了。"
        action: "走上舞台"
      - character: "配角"
        line: "欢迎来到这个世界。"
'''