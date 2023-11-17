const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    allowedHosts: [
      'localhost:7890',
      'n6g45s.natappfree.cc',
    ],
  },
  assetsDir: 'static'
})
