<template>
  <div class="home">
    <div class="home-title"></div>
    <!-- 轮播图 -->
    <!-- <van-swipe class="my-swipe" :autoplay="3000" indicator-color="white">
      <van-swipe-item v-for="(item, index) in imgData" :key="index">
        <img
          :src="`https://images.weserv.nl/?url=${item.img}${imgSuffix}`"
          alt=""
        />
      </van-swipe-item>
    </van-swipe> -->

    <!-- 推荐 -->
    <div class="cards">
      <div class="cards-box" v-for="(item, index) in reData" :key="index" @click="viewDetail(item.name,item.detail_link)"> 
        <img
          :src="`${item.img}`"
          alt=""
        />
        <div >
          <p class="title">
            <span>{{ item.name }}</span
            ><van-tag v-for="style in item.styles" :key="style.id"
              class="tag"
              color="rgba(192, 192, 192, 0.16)"
              text-color="rgb(144, 149, 155)"
              >{{ style }}</van-tag
            >
          </p>
          <div class="cb-bottom">
            <span class="chapter">{{ item.sub_title }}</span>
            <!-- <span class="commentTotal">{{
              item.comment_total | kFormatter
            }}</span> -->
            <!-- <img src="../assets/images/pl.png" alt="" /> -->
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Home",
  data() {
    return {
      //商品类型
      imgData: [],
      imgSuffix: "@760w_380h.jpg",
      reData: [],
    };
  },
  created() {
    this.getType();
    this.getRecommend();
  },
  filters: {
    kFormatter(value) {
      if (value >= 10000) {
        let newValue = value / 1000;
        newValue = Math.round(newValue) / 10;
        return newValue + "W";
      } else {
        return value;
      }
    },
  },
  methods: {
    getType() {
      this.axios({
        method: "get",
        url: "https://apis.netstart.cn/mbcomic/Banner",
      })
        .then((res) => {
          console.log("获取商品类型 res ==> ", res);
          this.imgData = res.data.data;
          console.log(this.imgData);
        })
        .catch((err) => {
          console.log("获取商品类型 err ==> ", err);
        });
    },
    getRecommend() {
      this.axios({
        method: "get",
        //url: "https://apis.netstart.cn/mbcomic/HomeRecommend?seed=1&drag=1&page_num=1",
        url: this.$api+"/pop",
      })
        .then((res) => {
          console.log("获取商品类型 res ==> ", res);
          //this.reData = res.data.data.list;
          this.reData = res.data;
          console.log(this.reData);
        })
        .catch((err) => {
          console.log("获取商品类型 err ==> ", err);
        });
    },
    viewDetail(name,detail_link) {
      this.$router.push({ name: "Detail", params: { name,detail_link } });
      console.log(pid);
    },
  },
};
</script>

<style lang="scss" scoped>
.my-swipe .van-swipe-item {
  color: #fff;
  font-size: 20px;
  // line-height: 150px;
  text-align: center;
  // background-color: #39a9ed;
  margin-top: 10px;
}
.my-swipe .van-swipe-item img {
  border-radius: 10px;
  width: 340px;
  height: 170px;
}
.cards {
  margin-top: 10px;
  padding-bottom: 50px;
}
.cards-box {
  width: 350px;
  height: 270px;
  margin: 10px auto;
  // background-color: pink;
}
.cards-box img {
  width: 350px;
  height: 200px;
  border-radius: 10px;
}
.cards-box .title {
  margin: 0;
  text-align: start;
  font-size: 20px;
  height: 27px;
}
.cards-box .tag {
  margin-left: 5px;
}
.cb-bottom {
  height: 20px;
  line-height: 20px;
  margin-top: 3px;
}
.cb-bottom span {
  font-size: 14px;
  color: #999999;
}
.commentTotal {
  float: right;
}
.cb-bottom img {
  float: right;
  width: 16px;
  height: 16px;
}
</style>