<template>
  <div class="script-detail-container">
    <div v-if="loading" class="loading">
      <el-spinner size="large" />
    </div>
    
    <div v-else class="script-content">
      <div class="script-header">
        <div class="script-info">
          <h2>剧本详情</h2>
          <el-tag :type="getStatusType(script.status)">
            {{ getStatusText(script.status) }}
          </el-tag>
        </div>
        <div class="script-actions">
          <el-button type="primary" @click="copyContent">
            <el-icon><CopyDocument /></el-icon>
            复制
          </el-button>
          <el-button @click="downloadContent">
            <el-icon><Download /></el-icon>
            下载
          </el-button>
          <el-button @click="goBack">
            <el-icon><ArrowLeft /></el-icon>
            返回
          </el-button>
        </div>
      </div>
      
      <div class="script-meta">
        <span>创建时间: {{ formatDate(script.created_at) }}</span>
        <span v-if="script.completed_at">完成时间: {{ formatDate(script.completed_at) }}</span>
      </div>
      
      <div class="script-body">
        <pre>{{ script.content }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { scriptApi } from '../utils/api'
import { CopyDocument, Download, ArrowLeft } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()

const loading = ref(true)
const script = ref({
  id: 0,
  content: '',
  status: 'pending',
  created_at: '',
  completed_at: ''
})

onMounted(() => {
  loadScript()
})

const loadScript = async () => {
  const id = route.params.id
  
  try {
    const response = await scriptApi.getScript(id)
    script.value = response
  } catch (error) {
    console.error('加载剧本失败:', error)
    alert('加载剧本失败')
  } finally {
    loading.value = false
  }
}

const getStatusType = (status) => {
  switch (status) {
    case 'complete': return 'success'
    case 'pending': return 'warning'
    case 'failed': return 'danger'
    default: return 'info'
  }
}

const getStatusText = (status) => {
  switch (status) {
    case 'complete': return '已完成'
    case 'pending': return '处理中'
    case 'failed': return '失败'
    default: return status
  }
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN')
}

const copyContent = async () => {
  try {
    await navigator.clipboard.writeText(script.value.content)
    alert('已复制到剪贴板')
  } catch (error) {
    console.error('复制失败:', error)
  }
}

const downloadContent = () => {
  const blob = new Blob([script.value.content], { type: 'text/yaml' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `script_${script.value.id}.yaml`
  a.click()
  URL.revokeObjectURL(url)
}

const goBack = () => {
  router.push('/scripts')
}
</script>

<style scoped>
.script-detail-container {
  max-width: 900px;
  margin: 0 auto;
}

.loading {
  display: flex;
  justify-content: center;
  padding: 40px;
}

.script-content {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.script-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.script-info h2 {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 8px;
}

.script-actions {
  display: flex;
  gap: 12px;
}

.script-meta {
  display: flex;
  gap: 24px;
  margin-bottom: 24px;
  color: #666;
  font-size: 14px;
}

.script-body {
  background: #f8f9fa;
  padding: 24px;
  border-radius: 8px;
  max-height: 600px;
  overflow-y: auto;
}

.script-body pre {
  font-family: 'Monaco', 'Menlo', monospace;
  font-size: 14px;
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-all;
  margin: 0;
}
</style>