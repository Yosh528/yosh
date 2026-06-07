<template>
  <div class="app-container">
    <el-header class="app-header">
      <div class="header-content">
        <div class="logo" @click="goHome">
          <el-icon class="logo-icon" size="32"><Notebook /></el-icon>
          <span class="logo-text">AI小说转剧本</span>
        </div>
        <el-menu :default-active="activeMenu" mode="horizontal" class="nav-menu">
          <el-menu-item index="/" @click="navigate('/')">首页</el-menu-item>
          <el-menu-item index="/convert" @click="navigate('/convert')">转换工具</el-menu-item>
          <el-menu-item index="/scripts" @click="navigate('/scripts')">我的剧本</el-menu-item>
        </el-menu>
        <div class="user-info">
          <template v-if="currentUser">
            <span>{{ currentUser.username }}</span>
            <el-button type="text" @click="logout">退出登录</el-button>
          </template>
          <template v-else>
            <el-button type="text" @click="navigate('/login')">登录</el-button>
            <el-button type="primary" @click="navigate('/register')">注册</el-button>
          </template>
        </div>
      </div>
    </el-header>
    <el-main class="app-main">
      <router-view />
    </el-main>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Notebook } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()

const currentUser = ref(null)
const activeMenu = ref('/')

// 监听路由变化
watch(() => route.path, (newPath) => {
  activeMenu.value = newPath
})

// 初始化用户信息
const initUser = () => {
  const user = localStorage.getItem('user')
  if (user) {
    currentUser.value = JSON.parse(user)
  }
}

initUser()

const goHome = () => {
  router.push('/')
}

const navigate = (path) => {
  router.push(path)
}

const logout = () => {
  localStorage.removeItem('user')
  currentUser.value = null
  router.push('/login')
}
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 0 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 60px;
}

.logo {
  display: flex;
  align-items: center;
  cursor: pointer;
  color: white;
}

.logo-icon {
  margin-right: 8px;
}

.logo-text {
  font-size: 18px;
  font-weight: bold;
}

.nav-menu {
  flex: 1;
  justify-content: center;
}

.nav-menu :deep(.el-menu-item) {
  color: white;
}

.nav-menu :deep(.el-menu-item:hover) {
  background-color: rgba(255, 255, 255, 0.2);
}

.nav-menu :deep(.el-menu-item.is-active) {
  background-color: rgba(255, 255, 255, 0.3);
}

.user-info {
  display: flex;
  align-items: center;
  color: white;
}

.user-info span {
  margin-right: 16px;
}

.user-info :deep(.el-button) {
  color: white;
}

.user-info :deep(.el-button--primary) {
  background-color: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.3);
}

.app-main {
  flex: 1;
  padding: 20px;
}
</style>