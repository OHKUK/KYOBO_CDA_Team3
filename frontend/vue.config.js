module.exports = {
  // Webpack 관련 설정
  configureWebpack: {
    resolve: {
      alias: {
        'vue$': 'vue/dist/vue.esm.js'
      }
    }
  },

  // 개발 서버 설정 (프록시 등)
  devServer: {
    proxy: {
      '/api': {
        target: 'http://192.168.56.1:5000',
        changeOrigin: true,
        pathRewrite: { '^/api': '/api' }
      }
    }
  }
}

