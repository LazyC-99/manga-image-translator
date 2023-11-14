<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<style lang="scss">
body{
  margin: 0;
  // background-color: #f5f5f5;
  font-size: 14px !important;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

.auto-img{
  width: 100%;
  display: block;
}
</style>
<script>
export default {
  created() {
    this.$router.push({
      path: "/",
    });
  },
  destroyed() {
    sessionStorage.clear();
  },
};
</script>
