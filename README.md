# Novel-to-Script

AI 小说转剧本工具 - 将小说文本自动转换为结构化剧本（YAML 格式）。

## 功能特性

- [x] 小说文本解析与场景分割
- [x] 角色提取与一致性追踪
- [x] 剧本元素转换（动作、对话、转场）
- [x] YAML Schema 验证
- [x] Fountain 格式双向转换
- [x] REST API 接口

## 快速开始

### 后端安装

```bash
pip install -r requirements.txt
```

### 后端运行

```bash
# CLI 模式
python src/main.py --input novel.txt --output script.yaml

# API 模式
uvicorn src.api:app --reload --port 8000
```

### 前端运行

```bash
cd frontend
npm install
npm run dev
```

## 项目结构

```
ai-novel-to-script/
├── docs/                    # 文档
│   └── YAML_SCHEMA.md       # YAML Schema 定义
├── schema/                  # Schema 参考
│   └── screenplay-schema.yaml
├── src/                     # 核心源码
│   ├── api.py              # FastAPI 入口
│   ├── main.py            # CLI 入口
│   ├── models/           # 数据模型
│   ├── services/        # 转换服务
│   ├── validators/     # 验证器
│   └── utils/          # 工具函数
├── templates/              # 模板
│   └── system-prompt.txt
├── tests/                 # 测试
└── frontend/             # Next.js 前端
```

## API 文档

访问 http://localhost:8000/docs 查看完整 API 文档。

## 许可证

MIT License