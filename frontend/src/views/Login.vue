<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <el-icon class="login-icon" size="48" color="#667eea"><Key /></el-icon>
        <h2>欢迎回来</h2>
        <p>登录您的账户开始创作</p>
      </div>
      
      <el-form :model="form" class="login-form" @submit.prevent="login">
        <el-form-item label="用户名" prop="username">
          <el-input 
            v-model="form.username" 
            placeholder="请输入用户名"
            prefix-icon="User"
          />
        </el-form-item>
        
        <el-form-item label="密码" prop="password">
          <el-input 
            v-model="form.password" 
            type="password"
            placeholder="请输入密码"
            prefix-icon="Lock"
          />
        </el-form-item>
        
        <el-form-item>
          <el-button 
            type="primary" 
            size="large" 
            class="login-btn"
            :loading="loading"
            @click="login"
          >
            登录
          </el-button>
        </el-form-item>
      </el-form>
      
      <div class="login-footer">
        <span>还没有账户？</span>
        <el-button type="text" @click="goRegister">立即注册</el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { userApi } from '../utils/api'
import { Key, User, Lock } from '@element-plus/icons-vue'

const router = useRouter()

const form = ref({
  username: '',
  password: ''
})

const loading = ref(false)

const login = async () => {
  if (!form.value.username || !form.value.password) {
    alert('请输入用户名和密码')
    return
  }
  
  loading.value = true
  
  try {
    const response = await userApi.login(form.value)
    
    if (response.success) {
      localStorage.setItem('user', JSON.stringify(response.user))
      router.push('/')
    } else {
      alert(response.message)
    }
  } catch (error) {
    console.error('登录失败:', error)
    alert('登录失败，请检查用户名和密码')
  } finally {
    loading.value = false
  }
}

const goRegister = () => {
  router.push('/register')
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
}

.login-card {
  width: 400px;
  background: white;
  padding: 40px;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.login-icon {
  margin-bottom: 16px;
}

.login-header h2 {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 8px;
}

.login-header p {
  color: #666;
}

.login-form {
  margin-bottom: 24px;
}

.login-btn {
  width: 100%;
}

.login-footer {
  text-align: center;
  color: #666;
}

.login-footer :deep(.el-button) {
  color: #667eea;
  padding: 0;
  margin-left: 8px;
}
</style>