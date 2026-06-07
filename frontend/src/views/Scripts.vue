<template>
  <div class="scripts-container">
    <div class="scripts-header">
      <h2>我的剧本</h2>
      <el-button type="primary" @click="goConvert">
        <el-icon><Plus /></el-icon>
        新建转换
      </el-button>
    </div>
    
    <div v-if="loading" class="loading">
      <el-spinner size="large" />
    </div>
    
    <div v-else-if="scripts.length === 0" class="empty-state">
      <el-icon size="64" color="#ccc"><Document /></el-icon>
      <p>暂无剧本记录</p>
      <el-button type="primary" @click="goConvert">开始转换</el-button>
    </div>
    
    <div v-else class="scripts-list">
      <el-table :data="scripts" border>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="title" label="剧本标题" />
        <el-table-column prop="status" label="状态" width="120">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button type="text" @click="viewScript(scope.row.id)">查看</el-button>
            <el-button type="text" @click="downloadScript(scope.row)">下载</el-button>
            <el-button type="text" danger @click="deleteScript(scope.row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { scriptApi } from '../utils/api'
import { Plus, Document } from '@element-plus/icons-vue'

const router = useRouter()

const loading = ref(true)
const scripts = ref([])

onMounted(() => {
  loadScripts()
})

const loadScripts = async () => {
  const user = localStorage.getItem('user')
  if (!user) {
    router.push('/login')
    return
  }
  
  const userId = JSON.parse(user).id
  
  try {
    const response = await scriptApi.getUserScripts(userId)
    if (response.success) {
      scripts.value = response.scripts
    }
  } catch (error) {
    console.error('加载剧本失败:', error)
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

const viewScript = (id) => {
  router.push(`/script/${id}`)
}

const downloadScript = async (script) => {
  try {
    const response = await scriptApi.getScript(script.id)
    const blob = new Blob([response.content], { type: 'text/yaml' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `script_${script.id}.yaml`
    a.click()
    URL.revokeObjectURL(url)
  } catch (error) {
    console.error('下载失败:', error)
    alert('下载失败')
  }
}

const deleteScript = async (id) => {
  if (!confirm('确定要删除这个剧本吗？')) {
    return
  }
  
  try {
    const response = await scriptApi.deleteScript(id)
    if (response.success) {
      scripts.value = scripts.value.filter(s => s.id !== id)
      alert('删除成功')
    }
  } catch (error) {
    console.error('删除失败:', error)
    alert('删除失败')
  }
}

const goConvert = () => {
  router.push('/convert')
}
</script>

<style scoped>
.scripts-container {
  max-width: 1000px;
  margin: 0 auto;
}

.scripts-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.scripts-header h2 {
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.loading {
  display: flex;
  justify-content: center;
  padding: 40px;
}

.empty-state {
  text-align: center;
  padding: 60px;
  background: white;
  border-radius: 12px;
}

.empty-state p {
  margin: 16px 0;
  color: #666;
}

.scripts-list {
  background: white;
  border-radius: 12px;
}
</style>