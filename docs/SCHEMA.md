# 剧本 YAML Schema 设计文档

## 1. 概述

本项目使用 YAML 格式作为剧本输出格式，旨在提供结构化、可读性强且易于编辑的剧本初稿。YAML 的层次结构天然适合表示剧本的场景、角色和对话关系。

## 2. Schema 定义

### 2.1 顶层结构

```yaml
# 剧本元数据
title: string                    # 剧本标题
author: string                  # 作者（可选）
created_at: datetime            # 创建时间（可选）
version: string                 # 版本号（可选）

# 场景列表
scenes:
  - scene_number: integer       # 场景编号
    scene_title: string         # 场景标题
    description: string         # 场景描述
    location: string            # 场景地点（可选）
    time_of_day: string         # 时间（可选）
    characters:                 # 角色列表
      - string
    dialogues:                  # 对话列表
      - character: string       # 角色名
        line: string            # 台词
        action: string          # 动作描述（可选）
        emotion: string         # 情绪（可选）
```

### 2.2 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| title | string | 是 | 剧本的标题，通常与小说同名 |
| author | string | 否 | 作者信息 |
| created_at | datetime | 否 | 生成时间 |
| version | string | 否 | 版本号，便于迭代管理 |
| scenes | array | 是 | 场景列表，按顺序排列 |
| scenes[].scene_number | integer | 是 | 场景序号，从1开始 |
| scenes[].scene_title | string | 是 | 场景小标题 |
| scenes[].description | string | 是 | 场景的环境描述 |
| scenes[].location | string | 否 | 具体地点 |
| scenes[].time_of_day | string | 否 | 时间描述（如：早晨、傍晚） |
| scenes[].characters | array | 是 | 出场角色列表 |
| scenes[].dialogues | array | 是 | 对话列表 |
| scenes[].dialogues[].character | string | 是 | 说话角色 |
| scenes[].dialogues[].line | string | 是 | 台词内容 |
| scenes[].dialogues[].action | string | 否 | 角色动作 |
| scenes[].dialogues[].emotion | string | 否 | 情绪状态 |

## 3. 设计原因

### 3.1 为什么选择 YAML？

1. **可读性强**：YAML 使用缩进表示层级，直观易懂
2. **结构灵活**：支持复杂的嵌套结构，适合剧本的场景-角色-对话关系
3. **易于编辑**：文本格式，可使用任何文本编辑器修改
4. **易于解析**：Python、JavaScript 等主流语言都有成熟的 YAML 解析库
5. **版本控制友好**：纯文本格式便于 Git 版本管理

### 3.2 Schema 设计考量

1. **场景化结构**：剧本天然按场景划分，使用 `scenes` 数组符合剧本写作习惯
2. **角色管理**：每个场景独立定义角色列表，便于理解场景中的人物关系
3. **对话扩展**：`action` 和 `emotion` 字段为后续剧本细化提供空间
4. **元数据支持**：`author`、`version` 等字段便于剧本管理和协作

## 4. 示例输出

```yaml
title: "月光下的秘密"
author: "佚名"
created_at: "2024-01-15T10:30:00Z"
version: "1.0"

scenes:
  - scene_number: 1
    scene_title: "第一章：神秘来信"
    description: "一间昏暗的书房，窗外月光洒落。男主角坐在书桌前，手中拿着一封泛黄的信。"
    location: "男主角书房"
    time_of_day: "深夜"
    characters:
      - 陈风
      - 神秘人（画外音）
    dialogues:
      - character: 陈风
        line: "这封信...到底是谁寄来的？"
        action: 手指轻轻摩挲着信封上的蜡封
        emotion: "疑惑"
      - character: 神秘人（画外音）
        line: "陈先生，您想知道十年前的真相吗？"
        emotion: "神秘"

  - scene_number: 2
    scene_title: "第二章：雨夜探访"
    description: "雨夜，陈风撑着伞来到一处废弃的老宅前。门吱呀一声开了。"
    location: "城郊老宅"
    time_of_day: "雨夜"
    characters:
      - 陈风
      - 老管家
    dialogues:
      - character: 老管家
        line: "您终于来了，陈先生。"
        action: 打开门，雨水打湿了他的肩膀
      - character: 陈风
        line: "你知道我会来？"
        emotion: "警惕"
```

## 5. 扩展说明

本 Schema 为基础版本，可根据需求扩展以下字段：

- **场景类型**：添加 `scene_type` 字段（内景/外景）
- **场景时长**：添加 `duration` 字段
- **镜头描述**：添加 `camera` 字段描述镜头角度
- **音效描述**：添加 `sound_effects` 字段

---

## 附录：JSON Schema 规范

如需程序验证，可使用以下 JSON Schema：

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["title", "scenes"],
  "properties": {
    "title": { "type": "string" },
    "author": { "type": "string" },
    "created_at": { "type": "string", "format": "date-time" },
    "version": { "type": "string" },
    "scenes": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["scene_number", "scene_title", "description", "characters", "dialogues"],
        "properties": {
          "scene_number": { "type": "integer", "minimum": 1 },
          "scene_title": { "type": "string" },
          "description": { "type": "string" },
          "location": { "type": "string" },
          "time_of_day": { "type": "string" },
          "characters": {
            "type": "array",
            "items": { "type": "string" },
            "minItems": 1
          },
          "dialogues": {
            "type": "array",
            "items": {
              "type": "object",
              "required": ["character", "line"],
              "properties": {
                "character": { "type": "string" },
                "line": { "type": "string" },
                "action": { "type": "string" },
                "emotion": { "type": "string" }
              }
            }
          }
        }
      }
    }
  }
}
```