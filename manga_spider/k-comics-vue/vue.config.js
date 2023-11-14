const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    allowedHosts: [
      'localhost:7890',
      '8jfahb.natappfree.cc',
    ],
  },
  assetsDir: 'static'
})
