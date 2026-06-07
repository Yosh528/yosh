# API 接口文档

## 1. 概述

本文档描述 AI小说转剧本工具的后端 API 接口规范。

### 基础信息

- **基础URL**: `http://localhost:5000/api`
- **内容类型**: `application/json`
- **认证方式**: 用户ID（后续可扩展JWT）

---

## 2. 用户接口

### 2.1 注册

**POST** `/users/register`

请求体：
```json
{
  "username": "string (必填)",
  "email": "string (必填，邮箱格式)",
  "password": "string (必填)"
}
```

成功响应（201）：
```json
{
  "success": true,
  "message": "注册成功",
  "user": {
    "id": "integer",
    "username": "string",
    "email": "string"
  }
}
```

失败响应（400）：
```json
{
  "error": "用户名已存在"
}
```

### 2.2 登录

**POST** `/users/login`

请求体：
```json
{
  "username": "string (必填)",
  "password": "string (必填)"
}
```

成功响应（200）：
```json
{
  "success": true,
  "message": "登录成功",
  "user": {
    "id": "integer",
    "username": "string",
    "email": "string"
  }
}
```

失败响应（401）：
```json
{
  "error": "密码错误"
}
```

### 2.3 获取用户信息

**GET** `/users/{user_id}`

成功响应（200）：
```json
{
  "id": "integer",
  "username": "string",
  "email": "string",
  "created_at": "datetime"
}
```

失败响应（404）：
```json
{
  "error": "用户不存在"
}
```

### 2.4 更新用户信息

**PUT** `/users/{user_id}`

请求体：
```json
{
  "username": "string (可选)",
  "email": "string (可选)"
}
```

成功响应（200）：
```json
{
  "success": true,
  "message": "更新成功",
  "user": {
    "id": "integer",
    "username": "string",
    "email": "string"
  }
}
```

---

## 3. 剧本接口

### 3.1 小说转剧本

**POST** `/scripts/convert`

请求体：
```json
{
  "user_id": "integer (必填)",
  "title": "string (必填)",
  "content": "string (必填，至少100字符)"
}
```

成功响应（200）：
```json
{
  "success": true,
  "message": "转换成功",
  "script": {
    "id": "integer",
    "novel_id": "integer",
    "content": "string (YAML格式)",
    "status": "complete"
  }
}
```

失败响应（500）：
```json
{
  "success": false,
  "message": "转换失败: 错误信息",
  "script": {
    "id": "integer",
    "novel_id": "integer",
    "status": "failed"
  }
}
```

### 3.2 获取剧本详情

**GET** `/scripts/{script_id}`

成功响应（200）：
```json
{
  "id": "integer",
  "user_id": "integer",
  "novel_id": "integer",
  "content": "string (YAML格式)",
  "status": "string (pending/complete/failed)",
  "created_at": "datetime",
  "completed_at": "datetime (可选)"
}
```

失败响应（404）：
```json
{
  "error": "剧本不存在"
}
```

### 3.3 获取用户剧本列表

**GET** `/scripts/user/{user_id}`

成功响应（200）：
```json
{
  "success": true,
  "scripts": [
    {
      "id": "integer",
      "novel_id": "integer",
      "status": "string",
      "created_at": "datetime",
      "completed_at": "datetime (可选)"
    }
  ]
}
```

### 3.4 删除剧本

**DELETE** `/scripts/{script_id}`

成功响应（200）：
```json
{
  "success": true,
  "message": "删除成功"
}
```

失败响应（404）：
```json
{
  "error": "剧本不存在"
}
```

---

## 4. 错误码说明

| 错误码 | 说明 |
|--------|------|
| 400 | 请求参数错误 |
| 401 | 未授权（登录失败） |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

---

## 5. 使用示例

### cURL 示例

```bash
# 注册
curl -X POST http://localhost:5000/api/users/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","password":"123456"}'

# 登录
curl -X POST http://localhost:5000/api/users/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"123456"}'

# 转换小说
curl -X POST http://localhost:5000/api/scripts/convert \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "title": "我的剧本",
    "content": "第一章 初遇\n阳光明媚的早晨，李明走在校园里..."
  }'

# 获取剧本列表
curl http://localhost:5000/api/scripts/user/1

# 获取剧本详情
curl http://localhost:5000/api/scripts/1

# 删除剧本
curl -X DELETE http://localhost:5000/api/scripts/1
```