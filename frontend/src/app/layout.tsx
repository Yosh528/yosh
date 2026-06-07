import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Novel to Script - AI 小说转剧本工具',
  description: '将小说文本自动转换为结构化剧本',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="zh-CN">
      <body>{children}</body>
    </html>
  )
}