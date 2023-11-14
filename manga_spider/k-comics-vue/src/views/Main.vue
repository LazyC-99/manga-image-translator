<template>
  <div class="main">
    

    <div>
      <router-view></router-view>
    </div>
    
    <van-tabbar v-model="active" active-color="#0C34BA" inactive-color="#646566" route>

      <van-tabbar-item v-for="(item, index) in tabbarData" :key="index" :to="{name: item.name}">
        <span>{{item.title}}</span>
        <template #icon="props">
          <img :src="props.active ? item.activeIcon : item.inactiveIcon" alt="">
        </template>
      </van-tabbar-item>

    </van-tabbar>
  </div>
</template>

<script>
  export default {
    name: 'Main',
    data() {
      return {
        //选项卡的默认高亮下标
        active: 0,

        tabbarData: [
          {
            title: '首页',
            activeIcon: require('../assets/images/home_active.png'),
            inactiveIcon: require('../assets/images/home.png'),
            name: 'Home'
          },
           {
            title: '排行',
            activeIcon: require('../assets/images/Ranking_active.png'),
            inactiveIcon: require('../assets/images/Ranking.png'),
            name: 'Ranking'
          },
           {
            title: '分类',
            activeIcon: require('../assets/images/classify_active.png'),
            inactiveIcon: require('../assets/images/classify.png'),
            name: 'Classify'
          },
           {
            title: '我的',
            activeIcon: require('../assets/images/My_active.png'),
            inactiveIcon: require('../assets/images/My.png'),
            name: 'My'
          }
        ]
      }
    }
  }
</script>

<style lang="scss" scoped>
.navigation{
  height: 50px;
}
</style>