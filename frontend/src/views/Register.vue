<template>
  <div class="register-container">
    <div class="register-card">
      <div class="register-header">
        <el-icon class="register-icon" size="48" color="#667eea"><UserFilled /></el-icon>
        <h2>创建账户</h2>
        <p>开始您的剧本创作之旅</p>
      </div>
      
      <el-form :model="form" class="register-form">
        <el-form-item label="用户名" prop="username">
          <el-input 
            v-model="form.username" 
            placeholder="请输入用户名"
            prefix-icon="User"
          />
        </el-form-item>
        
        <el-form-item label="邮箱" prop="email">
          <el-input 
            v-model="form.email" 
            type="email"
            placeholder="请输入邮箱"
            prefix-icon="Mail"
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
        
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input 
            v-model="form.confirmPassword" 
            type="password"
            placeholder="请再次输入密码"
            prefix-icon="Lock"
          />
        </el-form-item>
        
        <el-form-item>
          <el-button 
            type="primary" 
            size="large" 
            class="register-btn"
            :loading="loading"
            :disabled="!canSubmit"
            @click="register"
          >
            注册
          </el-button>
        </el-form-item>
      </el-form>
      
      <div class="register-footer">
        <span>已有账户？</span>
        <el-button type="text" @click="goLogin">立即登录</el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { userApi } from '../utils/api'
import { UserFilled, User, Message, Lock } from '@element-plus/icons-vue'

const router = useRouter()

const form = ref({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const loading = ref(false)

const canSubmit = computed(() => {
  return form.value.username && 
         form.value.email && 
         form.value.password && 
         form.value.confirmPassword &&
         form.value.password === form.value.confirmPassword
})

const register = async () => {
  if (!canSubmit.value) {
    alert('请填写完整信息并确保密码一致')
    return
  }
  
  loading.value = true
  
  try {
    const response = await userApi.register({
      username: form.value.username,
      email: form.value.email,
      password: form.value.password
    })
    
    if (response.success) {
      alert('注册成功，请登录')
      router.push('/login')
    } else {
      alert(response.message)
    }
  } catch (error) {
    console.error('注册失败:', error)
    alert('注册失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

const goLogin = () => {
  router.push('/login')
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
}

.register-card {
  width: 450px;
  background: white;
  padding: 40px;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.register-header {
  text-align: center;
  margin-bottom: 32px;
}

.register-icon {
  margin-bottom: 16px;
}

.register-header h2 {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 8px;
}

.register-header p {
  color: #666;
}

.register-form {
  margin-bottom: 24px;
}

.register-btn {
  width: 100%;
}

.register-footer {
  text-align: center;
  color: #666;
}

.register-footer :deep(.el-button) {
  color: #667eea;
  padding: 0;
  margin-left: 8px;
}
</style>