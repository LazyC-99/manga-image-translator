<template>
  <div class="cartoon">
    <div class="nav-box">
      <div class="nav-title">
        <img src="../assets/images/back.png" class="btn" @click="back" />
        <p class="nav-text">{{this.name}}</p>
        <p class="nav-id">第{{chapter_list[index].chapter_id}}话</p>
        <van-button @click="toggleTranslate()"  size="small" :type="showTranslate ? 'warning' : 'info'">{{showTranslate ? '关闭翻译' : '开启翻译'}}</van-button>
      </div>
      <div v-for="(item, i) in imgArr" :key="i" class="photo">
        <img :src="item" alt="" />
        <div v-if="showTranslate" class="overlay">
          <img :src="tranImgArr[i]" alt="Overlay Image">
        </div>
      </div>
      <div class="page">
        <van-button @click="turnPage(index-=1)" type="default" >上一章</van-button>
        <van-button @click="turnPage(index+=1)" type="default" >下一章</van-button>
      </div>
    </div>
  </div>
</template>

<script>
import { Toast } from 'vant';
export default {
  name: "Cartoon",

  data() {
    return {
      tranBtnType: "info",

      showTranslate: false,

      chapter_list: "",

      index: 0,

      name: "",

      detailsData: [],

      ImageData: [],

      imgArr:[],

      tranImgArr: [],
    };
  },

  created() {
    this.chapter_list = this.$route.params.sortedList;
    this.index = this.$route.params.index;
    this.name = this.$route.params.name;
    this.getImgArr()

    // this.getCartoonDetail();
    // this.getImageDetail();
    // this.getData()
  },

  methods: {
    back() {
      this.$router.back();
    },
    scrollToTop() {
      window.scrollTo({
        top: 0,
        behavior: "smooth" // 添加这个选项可以实现平滑滚动效果
      });
    },
    toggleTranslate() {
      this.showTranslate = !this.showTranslate
    },
    turnPage(index){
      console.log("翻页：",index)
      if(index<0){
        Toast.success("前面没有了")
        this.index = 0
      }else{
        this.index = index
        this.getImgArr()
        this.scrollToTop()
      }
      
    },
    getImgArr() {
      var link = this.chapter_list[this.index].chapter_link
      console.log("第"+(this.index+1)+"话 chapter?url= ",link );
      this.axios({
        method: "get",
        url: this.$api+"/chapter?",
        params: {
          url: link,
        },
      })
        .then((res) => {
          this.imgArr = res.data.imgs
          console.log("图片详情 res ==> ", this.imgArr);
          
          var newArray = res.data.trans_imgs.map(element=> {
              return this.$api + element;
          });
          console.log("翻译详情 res ==> ", newArray);
          this.tranImgArr = newArray
          
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
  }
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
  position: relative;
  img{
    width:100%;
  }
  .overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 1; /* 调整这个值以确定覆盖的层级关系 */
    }
}
.page{
  float: right;
}
</style>