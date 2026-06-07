'use client'

import { useState, useCallback } from 'react'
import Editor from '@monaco-editor/react'
import { motion, AnimatePresence } from 'framer-motion'

interface ConversionResult {
  yaml_output: string
  scenes: number
  characters: number
}

export default function Home() {
  const [novelText, setNovelText] = useState('')
  const [title, setTitle] = useState('')
  const [author, setAuthor] = useState('')
  const [genre, setGenre] = useState('爱情')
  const [format, setFormat] = useState('短剧')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<ConversionResult | null>(null)
  const [activeTab, setActiveTab] = useState<'input' | 'yaml' | 'fountain'>('input')

  const handleConvert = useCallback(async () => {
    if (!novelText.trim()) return

    setLoading(true)
    try {
      const response = await fetch('/api/v1/convert', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text: novelText,
          title,
          author,
          genre,
          format,
        }),
      })

      const data = await response.json()
      setResult(data)
      setActiveTab('yaml')
    } catch (error) {
      console.error('转换失败:', error)
    } finally {
      setLoading(false)
    }
  }, [novelText, title, author, genre, format])

  const handleDownloadYaml = () => {
    if (!result?.yaml_output) return
    const blob = new Blob([result.yaml_output], { type: 'text/yaml' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${title || 'script'}.yaml`
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <main className="cyber-bg grid-pattern min-h-screen">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-50 glass px-6 py-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-primary to-accent-purple flex items-center justify-center">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <div>
              <h1 className="text-xl font-bold bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">
                Novel to Script
              </h1>
              <p className="text-xs text-gray-500">AI 小说转剧本工具</p>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <span className="text-xs text-gray-500">v1.0.0</span>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="pt-24 pb-12 px-6 max-w-7xl mx-auto">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Panel - Input */}
          <div className="lg:col-span-1 space-y-4">
            <div className="glass rounded-xl p-5 neon-border">
              <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-primary animate-pulse" />
                基本信息
              </h2>

              <div className="space-y-4">
                <div>
                  <label className="text-sm text-gray-400 block mb-1.5">剧本标题</label>
                  <input
                    type="text"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    placeholder="输入剧本标题"
                    className="w-full bg-dark-bg border border-dark-border rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-primary transition-colors"
                  />
                </div>

                <div>
                  <label className="text-sm text-gray-400 block mb-1.5">作者</label>
                  <input
                    type="text"
                    value={author}
                    onChange={(e) => setAuthor(e.target.value)}
                    placeholder="编剧姓名"
                    className="w-full bg-dark-bg border border-dark-border rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-primary transition-colors"
                  />
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="text-sm text-gray-400 block mb-1.5">类型</label>
                    <select
                      value={genre}
                      onChange={(e) => setGenre(e.target.value)}
                      className="w-full bg-dark-bg border border-dark-border rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:border-primary"
                    >
                      <option value="爱情">爱情</option>
                      <option value="悬疑">悬疑</option>
                      <option value="科幻">科幻</option>
                      <option value="古装">古装</option>
                      <option value="都市">都市</option>
                      <option value="职场">职场</option>
                    </select>
                  </div>
                  <div>
                    <label className="text-sm text-gray-400 block mb-1.5">格式</label>
                    <select
                      value={format}
                      onChange={(e) => setFormat(e.target.value)}
                      className="w-full bg-dark-bg border border-dark-border rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:border-primary"
                    >
                      <option value="短剧">短剧</option>
                      <option value="网剧">网剧</option>
                      <option value="电影">电影</option>
                      <option value="舞台剧">舞台剧</option>
                      <option value="广播剧">广播剧</option>
                    </select>
                  </div>
                </div>
              </div>
            </div>

            {/* Convert Button */}
            <motion.button
              onClick={handleConvert}
              disabled={loading || !novelText.trim()}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="w-full btn-glow py-4 rounded-xl font-semibold text-white disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <svg className="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                  转换中...
                </span>
              ) : (
                '开始转换'
              )}
            </motion.button>
          </div>

          {/* Right Panel - Editor */}
          <div className="lg:col-span-2">
            <div className="glass rounded-xl overflow-hidden">
              {/* Tabs */}
              <div className="flex border-b border-dark-border">
                {(['input', 'yaml', 'fountain'] as const).map((tab) => (
                  <button
                    key={tab}
                    onClick={() => setActiveTab(tab)}
                    className={`px-5 py-3 text-sm font-medium transition-colors ${
                      activeTab === tab
                        ? 'text-primary border-b-2 border-primary bg-primary/5'
                        : 'text-gray-400 hover:text-white'
                    }`}
                  >
                    {tab === 'input' ? '小说输入' : tab === 'yaml' ? 'YAML 输出' : 'Fountain 格式'}
                  </button>
                ))}
              </div>

              {/* Content */}
              <div className="h-[600px]">
                <AnimatePresence mode="wait">
                  {activeTab === 'input' && (
                    <motion.div
                      key="input"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      exit={{ opacity: 0 }}
                      className="h-full"
                    >
                      <Editor
                        height="100%"
                        defaultLanguage="markdown"
                        theme="vs-dark"
                        value={novelText}
                        onChange={(value) => setNovelText(value || '')}
                        options={{
                          minimap: { enabled: false },
                          fontSize: 14,
                          lineNumbers: 'off',
                          wordWrap: 'on',
                          padding: { top: 20 },
                          scrollBeyondLastLine: false,
                        }}
                      />
                    </motion.div>
                  )}

                  {activeTab === 'yaml' && (
                    <motion.div
                      key="yaml"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      exit={{ opacity: 0 }}
                      className="h-full relative"
                    >
                      {result?.yaml_output ? (
                        <>
                          <Editor
                            height="100%"
                            defaultLanguage="yaml"
                            theme="vs-dark"
                            value={result.yaml_output}
                            options={{
                              readOnly: true,
                              minimap: { enabled: false },
                              fontSize: 13,
                              lineNumbers: 'on',
                              padding: { top: 20 },
                            }}
                          />
                          <button
                            onClick={handleDownloadYaml}
                            className="absolute top-4 right-4 z-10 px-3 py-1.5 bg-primary/80 hover:bg-primary rounded-lg text-sm transition-colors"
                          >
                            下载 YAML
                          </button>
                        </>
                      ) : (
                        <div className="h-full flex items-center justify-center text-gray-500">
                          点击"开始转换"查看输出结果
                        </div>
                      )}
                    </motion.div>
                  )}

                  {activeTab === 'fountain' && (
                    <motion.div
                      key="fountain"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      exit={{ opacity: 0 }}
                      className="h-full p-4 overflow-auto"
                    >
                      {result?.yaml_output ? (
                        <pre className="font-mono text-sm text-gray-300 whitespace-pre-wrap">
                          {result.yaml_output.slice(0, 500)}...
                        </pre>
                      ) : (
                        <div className="h-full flex items-center justify-center text-gray-500">
                          暂无 Fountain 输出
                        </div>
                      )}
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            </div>

            {/* Stats */}
            {result && (
              <div className="grid grid-cols-3 gap-4 mt-4">
                <div className="glass rounded-xl p-4 text-center">
                  <div className="text-2xl font-bold text-primary">{result.scenes}</div>
                  <div className="text-xs text-gray-500 mt-1">场景数</div>
                </div>
                <div className="glass rounded-xl p-4 text-center">
                  <div className="text-2xl font-bold text-accent-purple">{result.characters}</div>
                  <div className="text-xs text-gray-500 mt-1">角色数</div>
                </div>
                <div className="glass rounded-xl p-4 text-center">
                  <div className="text-2xl font-bold text-accent-cyan">OK</div>
                  <div className="text-xs text-gray-500 mt-1">状态</div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </main>
  )
}