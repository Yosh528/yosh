# Novel-to-Script YAML Schema 定义文档
# 版本: 1.0.0
# 更新日期: 2026-06-05

## 概述

本文档定义小说转剧本工具的 YAML 数据结构。该 Schema 旨在：
1. **结构化** - 将非结构化小说文本转换为可计算、可编辑的数据
2. **行业兼容** - 支持导出为 Fountain、Final Draft 等行业标准格式
3. **协作友好** - 支持多人协作、版本追踪、批注评论
4. **AI 友好** - 明确的字段定义便于 AI 模型理解和生成

---

## 分层设计架构

```
┌─────────────────────────────────────────┐
│         版本控制与协作层 (_version)        │  ← 元数据、版本追溯
├─────────────────────────────────────────┤
│          剧本元数据层 (metadata)         │  ← 标题、类型、页数
├─────────────────────────────────────────┤
│           角色库层 (characters)          │  ← 全局角色定义
├─────────────────────────────────────────┤
│          场景列表层 (scenes)             │  ← 剧本主体内容
├─────────────────────────────────────────┤
│          注释层 (notes)                 │  ← 协作批注
└─────────────────────────────────────────┘
```

---

## 字段详解

### 1. _version — 版本控制层

**设计原因**：确保 YAML 输出与 Schema 版本同步，支持工具演进和向后兼容。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `schema_version` | string | 是 | 遵循语义化版本，如 "1.0.0" |
| `schema_url` | string | 否 | Schema 定义文档 URL |
| `last_modified` | string | 否 | 最后修改日期 |
| `compatible_tools` | array[string] | 否 | 兼容工具列表 |

```yaml
_version:
  schema_version: "1.0.0"
  schema_url: "https://github.com/yourname/novel-to-script/blob/main/schema/screenplay-schema.yaml"
  last_modified: "2026-06-05"
  compatible_tools: ["Final Draft 13", "Celtx", "WriterDuet", "Fountain"]
```

---

### 2. _project — 项目信息层

**设计原因**：关联源代码管理，记录生成上下文，便于问题溯源。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `repo_url` | string | 否 | Git 仓库地址 |
| `commit_hash` | string | 否 | 生成时的 Commit SHA |
| `pr_number` | string | 否 | 关联的 PR 编号 |
| `generated_by` | string | 否 | 生成工具/版本 |
| `generation_date` | string | 否 | ISO 8601 日期 |

---

### 3. metadata — 剧本元数据

**设计原因**：剧本的基本属性，用于检索、分类、预览。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `title` | string | 是 | 剧本标题 |
| `original_title` | string | 否 | 原著小说名 |
| `author` | string | 是 | 编剧姓名 |
| `source_author` | string | 否 | 原著作者 |
| `genre` | string | 是 | 类型：爱情/悬疑/科幻/古装/都市/职场 |
| `format` | string | 是 | 格式：短剧/网剧/电影/舞台剧/广播剧 |
| `total_scenes` | integer | 自动 | 自动统计的场景总数 |
| `total_pages` | integer | 自动 | 预估页数（1页≈1分钟） |
| `draft_version` | string | 否 | 版本号，如 "v1.0" |
| `created_at` | string | 是 | ISO 8601 日期 |
| `logline` | string | 是 | 一句话梗概（30字以内） |
| `fountain_compatible` | boolean | 是 | 是否可无损转换为 Fountain |

---

### 4. characters — 角色库

**设计原因**：全局角色定义为两层收益：
- **一致性**：跨章节复用，防止人设崩塌
- **统计分析**：自动追踪角色出场次数、台词数

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | string | 是 | 全局唯一标识，如 "char_001" |
| `name` | string | 是 | 角色中文名 |
| `code_name` | string | 是 | 剧本全大写名称，如 "LI MING" |
| `aliases` | array[string] | 否 | 别名/昵称映射 |
| `age` | integer | 否 | 年龄 |
| `gender` | string | 否 | 男/女/未知 |
| `occupation` | string | 否 | 职业 |
| `traits` | array[string] | 否 | 性格标签（AI 保持人设用） |
| `arc` | string | 否 | 人物弧线简述 |
| `description` | string | 否 | 外貌/标志性特征 |
| `scene_count` | integer | 自动 | 出场场景数 |
| `total_lines` | integer | 自动 | 台词数 |
| `total_words` | integer | 自动 | 台词字数 |
| `first_appearance` | string | 自动 | 首次出场场景 ID |
| `last_appearance` | string | 自动 | 末次出场场景 ID |
| `notes` | string | 否 | 编剧备注 |

---

### 5. scenes — 场景列表（核心）

**设计原因**：场景是剧本的基本单元，每个场景包含完整的戏剧动素。

#### 5.1 场景级元数据

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `scene_id` | string | 是 | 场景编号，如 "SC001" |
| `act` | string | 否 | 幕结构：第一幕/第二幕/第三幕/尾声 |
| `sequence` | string | 否 | 叙事节拍：铺垫/冲突/上升/高潮/转折/结局 |
| `slugline.int_ext` | string | 是 | INT./EXT. 或者 INT./EXT. |
| `slugline.location` | string | 是 | 地点名称 |
| `slugline.time` | string | 是 | DAY/NIGHT/DAWN/DUSK/MORNING/EVENING |
| `full_slugline` | string | 是 | 完整场景标题 |
| `mood` | string | 否 | 氛围基调 |
| `characters_present` | array[string] | 自动 | 本场景出场角色 ID |
| `estimated_duration` | string | 否 | 预估时长 |
| `pages` | integer | 否 | 预估页数 |

#### 5.2 content — 场景内容数组

场景内容按时间顺序排列，支持以下元素类型：

| 类型 (type) | 字段 | 说明 |
|-------------|------|------|
| `scene_heading` | `text` | 场景标题 |
| `action` | `text`, `notes` | 动作描写（视觉化、可拍摄） |
| `character` | `name`, `id`, `extension` | 角色名（居中） |
| `parenthetical` | `text`, `emotion` | 括号提示 |
| `dialogue` | `text`, `emotion`, `delivery`, `parenthetical`, `offscreen`, `voiceover` | 对话内容 |
| `transition` | `text` | 转场标记 |
| `shot` | `shot_type`, `description` | 镜头提示 |
| `sound` | `description`, `source` | 音效提示 |

**各类型详细设计**：

##### action（动作描写）
```
转换规则：
- 心理描写 → 动作或表情
- 环境氛围 → 视觉+听觉
- 省略过渡 → 时间跳跃标记

示例：
小说："他很紧张，手心出汗"
剧本：action: "他搓着手，视线游移"
```

##### dialogue（对话）
```
扩展字段：
- emotion: 情绪标签（开心/悲伤/愤怒/紧张）
- delivery: 表演方式（低声/激动/冷漠/嘲讽）
- parenthetical: 内联括号提示
- offscreen: 是否画外音
- voiceover: 是否旁白
```

##### transition（转场）
```
支持值：
CUT TO: / DISSOLVE TO: / FADE IN: / FADE OUT.
SMASH CUT TO: / MATCH CUT TO: / JUMP CUT TO: / WIPE TO:
```

---

### 6. notes — 注释层

**设计原因**：支持协作评审，追踪修改意见。

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `scene_id` | string | 否 | 关联场景 ID |
| `type` | string | 是 | 注释类型 |
| `author` | string | 是 | 注释作者 |
| `text` | string | 是 | 注释内容 |
| `created_at` | string | 是 | ISO 日期 |
| `pr_reference` | string | 否 | 关联的 PR 编号 |

**type 可选值**：
- `待修改` - 需要修改的内容
- `AI提示` - AI 转换时的处理说明
- `导演备注` - 导演特定要求
- `编剧备忘` - 编剧内部备注
- `技术备注` - 技术可行性备注
- `审核意见` - 审核反馈
- `PR关联` - 关联变更请求

---

### 7. extensions — 扩展字段

**设计原因**：预留扩展性，支持未来功能。

| 字段 | 类型 | 说明 |
|------|------|------|
| `custom_fields` | object | 用户自定义字段 |
| `production_notes` | object | 制片备注（预算/场地/道具） |
| `scheduling_info` | object | 拍摄排期信息 |
| `git_history` | array | 生成历史记录 |

---

## 转换规则摘要

### 小说 → 剧本的核心映射

| 小说元素 | 剧本处理方式 |
|----------|-------------|
| 心理描写 | 转化为动作或表情 |
| 环境氛围 | 场景标题 + 动作描写 |
| 间接引语 | 转为直接对话 |
| 内心独白 | 转为旁白 (V.O.) |
| 回忆插叙 | 转为闪回场景 |
| 时间跳跃 | 添加转场标记 |

---

## 使用示例

### 输入：小说片段
```
夜深了，李明独自走在回家的路上。他想着今天发生的事，心里越来越不安。他的手机突然响了...
```

### 输出：YAML 剧本
```yaml
scenes:
  - scene_id: "SC001"
    slugline:
      int_ext: "EXT."
      location: "街道 - 夜景"
      time: "NIGHT"
    full_slugline: "EXT. 街道 - NIGHT"
    mood: "紧张不安"
    content:
      - type: "action"
        text: "深夜的街道寂静无声。李明独自走着，步伐缓慢而沉重。"
      - type: "character"
        name: "李明"
        id: "char_001"
      - type: "dialogue"
        text: "（自语）今天到底是怎么回事..."
        voiceover: true
```

---

## 设计决策记录

| 决策 | 原因 | 替代方案 considered |
|------|------|-------------------|
| 分层设计 | 清晰的数据关注点分离 | 扁平结构（被拒绝：难以扩展） |
| 独立 character 库 | 跨章节一致性 | 内联角色定义（被拒绝：无法追踪） |
| content 数组顺序 | 时间顺序是剧本核心 | 按类型分组（被拒绝：不直观） |
| 扩展字段预留 | 未来制片功能 | 无扩展（被拒绝：不灵活） |
| Fountain 兼容性 | 行业工具导入 | 仅 YAML 输出（被拒绝：限制用户） |

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-06-05 | 初始版本 |