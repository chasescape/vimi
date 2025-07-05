import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true
      }
    }
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    // 生成静态资源的存放路径
    assetsInlineLimit: 4096,
    // 小于此阈值的导入或引用资源将内联为 base64 编码
    cssCodeSplit: true,
    // 启用/禁用 CSS 代码拆分
    sourcemap: false,
    // 构建后是否生成 source map 文件
    rollupOptions: {
      output: {
        manualChunks: {
          // 将第三方库单独打包
          vendor: ['vue', 'vue-router']
        }
      }
    }
  }
})
