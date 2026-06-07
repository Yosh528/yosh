<template>
  <div class="convert-container">
    <div class="convert-header">
      <h2>小说转剧本</h2>
      <p>请输入至少3个章节的小说文本，AI将自动转换为剧本格式</p>
    </div>
    
    <el-form :model="form" class="convert-form">
      <el-form-item label="剧本标题" prop="title">
        <el-input 
          v-model="form.title" 
          placeholder="请输入剧本标题"
          class="title-input"
        />
      </el-form-item>
      
      <el-form-item label="小说内容" prop="content">
        <textarea 
          v-model="form.content" 
          placeholder="请粘贴小说文本（至少100字符）"
          rows="15"
          class="content-textarea"
        ></textarea>
        <div class="char-count">{{ form.content.length }} 字符</div>
      </el-form-item>
      
      <el-form-item>
        <el-button 
          type="primary" 
          size="large" 
          class="convert-btn"
          :loading="loading"
          :disabled="!canConvert"
          @click="convert"
        >
          <el-icon><MagicStick /></el-icon>
          AI转换
        </el-button>
      </el-form-item>
    </el-form>
    
    <!-- 转换结果 -->
    <div v-if="result" class="result-section">
      <div class="result-header">
        <h3>转换结果</h3>
        <div class="result-actions">
          <el-button type="primary" @click="copyResult">
            <el-icon><CopyDocument /></el-icon>
            复制
          </el-button>
          <el-button @click="downloadResult">
            <el-icon><Download /></el-icon>
            下载
          </el-button>
        </div>
      </div>
      <pre class="result-content">{{ result }}</pre>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { scriptApi } from '../utils/api'
import { MagicStick, CopyDocument, Download } from '@element-plus/icons-vue'

const router = useRouter()

const form = ref({
  title: '',
  content: ''
})

const loading = ref(false)
const result = ref('')

const canConvert = computed(() => {
  const user = localStorage.getItem('user')
  return user && form.value.title.trim() && form.value.content.trim().length >= 100
})

const convert = async () => {
  const user = JSON.parse(localStorage.getItem('user'))
  
  if (!user) {
    router.push('/login')
    return
  }
  
  loading.value = true
  
  try {
    const response = await scriptApi.convert({
      user_id: user.id,
      title: form.value.title,
      content: form.value.content
    })
    
    if (response.success) {
      result.value = response.script.content
    } else {
      alert(response.message)
    }
  } catch (error) {
    console.error('转换失败:', error)
    alert('转换失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

const copyResult = async () => {
  try {
    await navigator.clipboard.writeText(result.value)
    alert('已复制到剪贴板')
  } catch (error) {
    console.error('复制失败:', error)
  }
}

const downloadResult = () => {
  const blob = new Blob([result.value], { type: 'text/yaml' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${form.value.title}.yaml`
  a.click()
  URL.revokeObjectURL(url)
}
</script>

<style scoped>
.convert-container {
  max-width: 800px;
  margin: 0 auto;
}

.convert-header {
  text-align: center;
  margin-bottom: 32px;
}

.convert-header h2 {
  font-size: 28px;
  font-weight: bold;
  color: #333;
  margin-bottom: 8px;
}

.convert-header p {
  color: #666;
}

.convert-form {
  background: white;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.title-input {
  width: 100%;
}

.content-textarea {
  width: 100%;
  font-family: 'Monaco', 'Menlo', monospace;
  pointer-events: auto !important;
  cursor: text !important;
  opacity: 1 !important;
}

.char-count {
  text-align: right;
  font-size: 12px;
  color: #999;
  margin-top: 8px;
}

.convert-btn {
  width: 100%;
}

.result-section {
  margin-top: 32px;
  background: white;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.result-header h3 {
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.result-actions {
  display: flex;
  gap: 12px;
}

.result-content {
  background: #f8f9fa;
  padding: 16px;
  border-radius: 8px;
  max-height: 500px;
  overflow-y: auto;
  font-family: 'Monaco', 'Menlo', monospace;
  font-size: 14px;
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-all;
}
</style>