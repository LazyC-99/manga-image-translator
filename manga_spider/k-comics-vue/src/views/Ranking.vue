<template>
  <div class="ranking">
    <div class="ranking-title">排行</div>
    <div class="ranking-box">
      <div class="ranking-left">
        <van-sidebar v-model="activeKey">
          <van-sidebar-item
            v-for="(item, index) in rankingData"
            :key="index"
            @click="toggleType(item.type)"
          >
            <template #title>
              <span :class="{ active: activeKey === index }">{{
                item.title
              }}</span>
            </template>
          </van-sidebar-item>
        </van-sidebar>
      </div>
      <div class="ranking-right">
        <van-sticky>
          <p class="illustrate">前7日综合指标最高的三个月内上线漫画作品排行</p>
        </van-sticky>
        <div class="product-list">
          <div
            class="product-item"
            v-for="(item, index) in typeData"
            :key="index" @click="viewDetail(item.comic_id)"
          >
            <img
              :src="`https://images.weserv.nl/?url=${item.vertical_cover}${imgSuffix}`"
              alt=""
            />
            <div class="title">{{ item.title }}</div>
            <p class="author">{{ getText(item.author) }}</p>
            <p class="styles" v-for="styles in item.styles" :key="styles.id">
              {{ styles.name }}
            </p>
            <div v-if="item.is_finish === 1">
              <p class="lastShort">共{{ item.last_ord }}话</p>
            </div>
            <div v-else>
              <p class="lastShort">更新至{{ item.last_short_title }}话</p>
            </div>
            <div class="rank">{{ item.last_rank }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Ranking",
  data() {
    return {
      activeKey: 0,

      imgSuffix: "@760w_380h.jpg",

      rankingData: [
        {
          title: "日漫榜",
          type: 3,
        },
        {
          title: "国漫榜",
          type: 4,
        },
        {
          title: "免费榜",
          type: 1,
        },
      ],

      //商品类型
      typeData: [],
    };
  },
  created() {
    this.getType();
  },
  methods: {
    viewDetail(pid) {
      this.$router.push({ name: "Detail", params: { pid } });
      console.log(pid);
    },
    toggleType(type) {
      // console.log('type ==> ', type);
      this.getType(type);
    },
    //获取商品类型
    getType(type) {
      console.log("type ==> ", type);
      this.axios({
        method: "get",
        url: "https://apis.netstart.cn/mbcomic/HomeHot?",
        params: {
          type: type,
        },
      })
        .then((res) => {
          console.log("获取漫画分类 res ==> ", res);

          this.typeData = res.data.data;
          console.log(this.typeData);
        })
        .catch((err) => {
          console.log("获取漫画分类 err ==> ", err);
        });
    },
    getText(str) {
      // console.log(str);
      // 在这里对传入的文本进行处理
      return str.toString().replace(/\,/g, " ");
    },
  },
};
</script>

<style lang="scss" scoped>
.ranking {
  .ranking-title {
    width: 100%;
    height: 29px;
    line-height: 29px;
    text-align: center;
    border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  }
  .product-list {
    margin-top: 50px;
    display: flex;
    flex-wrap: wrap;
    padding: 5px;
    .product-item {
      width: 100%;
      height: 140px;
      background-color: #fff;
      margin-right: 10px;
      margin-bottom: 20px;
      position: relative;
      img {
        height: 140px;
      }
      .title {
        position: absolute;
        width: 185px;
        max-height: 46.8px;
        overflow: hidden;
        text-overflow: ellipsis;
        top: 0;
        left: 115px;
        font-size: 18px;
      }
      .author {
        width: 185px;
        position: absolute;
        bottom: 50px;
        font-size: 12px;
        color: #90959b;
        left: 115px;
        margin: 0;
      }
      .styles {
        width: 185px;
        position: absolute;
        bottom: 23px;
        font-size: 12px;
        color: #90959b;
        left: 115px;
        margin: 0;
      }
      .lastShort {
        width: 185px;
        font-size: 12px;
        color: #90959b;
        position: absolute;
        left: 115px;
        bottom: 0px;
        margin: 0;
      }
      .rank {
        position: absolute;
        top: 0;
        width: 38px;
        height: 50px;
        color: rgb(246, 160, 99);
        font-weight: 600;
        line-height: 50px;
        font-size: 50px;
      }
      &:nth-child(2n) {
        margin-right: 0;
      }
    }
  }
  .active {
    color: #0c34ba;
  }
  .ranking-box {
    position: fixed;
    top: 30px;
    bottom: 50px;
    left: 0;
    right: 0;
    display: flex;
  }
  .ranking-left {
    width: 65px;
    overflow-y: auto;
    background-color: #f7f8fa;
  }
  .ranking-right {
    width: calc(100% - 65px);
    overflow-y: auto;
    position: relative;
    // background-color: #ddd;
    .illustrate {
      font-size: 8px;
      width: 100%;
      margin-left: 16px;
      height: 60px;
      line-height: 60px;
      color: #999999;
      background-color: white;
      position: fixed;
      top: 29.5px;
      left: 69px;
      padding-left: 10px;
      right: 0;
      margin: 0;
    }
  }
}
</style>