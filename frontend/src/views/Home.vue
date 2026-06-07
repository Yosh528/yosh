<template>
  <div class="home-container">
    <div class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">AI小说转剧本工具</h1>
        <p class="hero-subtitle">让AI帮你将小说自动转换为专业剧本格式</p>
        <div class="hero-buttons">
          <el-button type="primary" size="large" @click="goConvert">开始转换</el-button>
          <el-button size="large" @click="goScripts">查看示例</el-button>
        </div>
      </div>
      <div class="hero-image">
        <el-icon size="120" color="#667eea"><Document /></el-icon>
      </div>
    </div>
    
    <div class="features-section">
      <h2 class="section-title">功能特点</h2>
      <div class="features-grid">
        <div class="feature-card">
          <el-icon size="48" color="#667eea"><StarFilled /></el-icon>
          <h3>智能转换</h3>
          <p>基于先进AI模型，自动分析小说结构，生成专业剧本</p>
        </div>
        <div class="feature-card">
          <el-icon size="48" color="#764ba2"><Notebook /></el-icon>
          <h3>多章节支持</h3>
          <p>支持3章以上长篇小说转换，保持故事完整性</p>
        </div>
        <div class="feature-card">
          <el-icon size="48" color="#f093fb"><Files /></el-icon>
          <h3>YAML格式</h3>
          <p>输出结构化YAML格式剧本，便于编辑和二次创作</p>
        </div>
        <div class="feature-card">
          <el-icon size="48" color="#f5576c"><Lock /></el-icon>
          <h3>隐私保护</h3>
          <p>本地处理，数据安全，保护您的创作成果</p>
        </div>
      </div>
    </div>
    
    <div class="workflow-section">
      <h2 class="section-title">使用流程</h2>
      <div class="workflow-steps">
        <div class="step">
          <div class="step-number">1</div>
          <h3>登录注册</h3>
          <p>创建账户，开始使用</p>
        </div>
        <el-icon class="step-arrow" size="32"><ArrowRight /></el-icon>
        <div class="step">
          <div class="step-number">2</div>
          <h3>上传小说</h3>
          <p>粘贴或上传小说文本</p>
        </div>
        <el-icon class="step-arrow" size="32"><ArrowRight /></el-icon>
        <div class="step">
          <div class="step-number">3</div>
          <h3>AI转换</h3>
          <p>智能生成剧本初稿</p>
        </div>
        <el-icon class="step-arrow" size="32"><ArrowRight /></el-icon>
        <div class="step">
          <div class="step-number">4</div>
          <h3>编辑下载</h3>
          <p>导出剧本继续创作</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { Document, StarFilled, Notebook, Files, Lock, ArrowRight } from '@element-plus/icons-vue'

const router = useRouter()

const goConvert = () => {
  router.push('/convert')
}

const goScripts = () => {
  router.push('/scripts')
}
</script>

<style scoped>
.home-container {
  max-width: 1200px;
  margin: 0 auto;
}

.hero-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 60px 0;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
  border-radius: 16px;
  margin-bottom: 40px;
}

.hero-content {
  flex: 1;
  padding: 0 40px;
}

.hero-title {
  font-size: 42px;
  font-weight: bold;
  color: #333;
  margin-bottom: 16px;
}

.hero-subtitle {
  font-size: 18px;
  color: #666;
  margin-bottom: 24px;
}

.hero-buttons {
  display: flex;
  gap: 12px;
}

.hero-image {
  padding: 40px;
}

.features-section {
  margin-bottom: 40px;
}

.section-title {
  font-size: 28px;
  font-weight: bold;
  text-align: center;
  margin-bottom: 32px;
  color: #333;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.feature-card {
  background: white;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  text-align: center;
}

.feature-card h3 {
  margin: 12px 0;
  color: #333;
}

.feature-card p {
  color: #666;
  font-size: 14px;
}

.workflow-section {
  background: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.workflow-steps {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
}

.step {
  text-align: center;
}

.step-number {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 20px;
  font-weight: bold;
  margin: 0 auto 12px;
}

.step h3 {
  margin-bottom: 8px;
  color: #333;
}

.step p {
  color: #666;
  font-size: 14px;
}

.step-arrow {
  color: #ddd;
}
</style>