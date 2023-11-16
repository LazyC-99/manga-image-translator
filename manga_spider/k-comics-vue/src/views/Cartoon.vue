<template>
  <div class="cartoon">
    <div class="nav-box">
      <div class="nav-title">
        <img src="../assets/images/back.png" class="btn" @click="back" />
        <p class="nav-text">{{this.name}}</p>
        <p class="nav-id">第{{this.chapter_id}}话</p>
      </div>
      <div v-for="(item, i) in imgArr" :key="i" class="photo">
        <img :src="item" alt="" />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Cartoon",

  data() {
    return {
      chapter_link: "",

      chapter_id: "",

      name: "",

      detailsData: [],

      ImageData: [],

      imgArr:[],
    };
  },

  created() {
    this.chapter_link = this.$route.params.chapter_link;
    this.chapter_id = this.$route.params.chapter_id;
    console.log(this.chapter_id); 
    this.name = this.$route.params.name;
    console.log(this.name);
    this.getImgArr()
    // this.getCartoonDetail();
    // this.getImageDetail();
    // this.getData()
  },

  methods: {
    back() {
      this.$router.back();
    },
    getImgArr() {
       
       console.log("传参数 res ==> ", this.chapter_link);
      this.axios({
        method: "get",
        url: this.$api+"/chapter?",
        params: {
          url: this.chapter_link,
        },
      })
        .then((res) => {
          console.log("获图片详情 res ==> ", res);
          this.imgArr = res.data
          console.log(this.imgArr)
        })
        .catch((err) => {});
    },
    getCartoonDetail() {
      this.axios({
        method: "get",
        url: "https://apis.netstart.cn/mbcomic/GetImageIndex?",
        params: {
          ep_id: this.cid,
        },
      })
        .then((res) => {
          console.log("获取漫画详情 res ==> ", res);
          this.detailsData = res.data.data.images;
          console.log(this.detailsData);
        })
        .catch((err) => {});
    },

    getImageDetail() {
      this.axios({
        method: "get",
        url: "https://apis.netstart.cn/mbcomic/ImageToken?",
        params: {
          urls: this.detailsData,
        },
      })
        .then((res) => {
          console.log("获取漫画详情 res ==> ", res);
          this.ImageData = res.data.data;
          console.log(this.ImageData);
        })
        .catch((err) => {});
    },
    getData() {
      this.axios({
        method: "get",
        url: "/GetImageIndex",
        params: {
          ep_id: this.cid,
        },
      })
        .then((res) => {
          // console.log(this.$route.query.index);
          // this.$root.index = this.$route.query.index
          //   console.log(this.$route);
          //   console.log("replies ==>", res);
          //   console.log(this.$route.query.ep_id);
          this.data = res.data.data;
          this.arr = [];
          res.data.data.images.forEach((item) => {
            this.arr.push(item.path + "@660w.webp");
          });
          this.axios({
            method: "get",
            url: "/ImageToken",
            params: {
              urls: JSON.stringify(this.arr),
            },
          })
            .then((res) => {
              //   console.log(this.$route.params);
              //   console.log(" ==>", res);
              this.imgArr = [];
              res.data.data.forEach((item) => {
                this.imgArr.push(item.url + "?token=" + item.token);
              });
              this.isLoad = false; //   console.log("this.imgArr ==>", this.imgArr);
              console.log('图片数组',this.imgArr);
            })
            .catch((err) => {
              console.log("err ==> ", err);
            }); //   console.log("this.arr ==>", this.arr);
        })
        .catch((err) => {
          console.log("err ==> ", err);
        });
    },
  },
};
</script>

<style lang="scss" scoped>
.nav-title {
  width: 100%;
  height: 48px;
  padding: 0 17px;
  background-color: #1e212c;
  color: #fff;
  box-sizing: border-box;
  line-height: 48px;
  z-index: 101;
  position: fixed;
  top:0;
  left:0;
  display: flex;
  .btn {
    width: 24px;
    height: 24px;
    margin-top: 12px;
  }
  .nav-text{
    display: inline-block;
    font-size: 16px;
    margin: 0;
  }
  .nav-id{
    display: inline-block;
    font-size: 12px;
    // margin-left: 10px;
    color: #bcbdc0;
    margin: 0 0 0 10px;
  }
}
.photo{
  margin-top:0px;
  font-size: 0px;
  width:100%;
  img{
    width:100%;
  }
}
</style>