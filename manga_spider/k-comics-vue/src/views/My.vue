<template>
  <div class="my">
    <div class="my-title">个人中心</div>
    <div class="my-box">
      <div class="box-item">
        <div class="head"></div>
        <div class="name">{{ this.name }}</div>
      </div>
      <div class="list">
        <p>个人信息  ></p>
        <p>安全中心  ></p>
      </div>
    </div>
    <div class="bookshelf">
      <div class="bookshelf-title">我的书架</div>
      <div class="bookshelf-item" >
        <div class="item" v-for="(item,i) in cartoonName" :key="i" @click="viewDetail(item.id)">
        <img :src="`https://images.weserv.nl/?url=${item.vertical_cover}`" alt="">
          <p>{{item.title}}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "My",

  data() {
    return {
      name: [],
      cartoonName:{

      },
    };
  },
  created() {
    this.getName();
  },
  methods: {
    viewDetail(pid) {
      this.$router.push({ name: "Detail", params: { pid } });
      console.log(pid);
    },
    getName() {
      let num = sessionStorage.getItem("token");
      let Carname = sessionStorage.getItem("cartoon");
      console.log(num);
      const obj = JSON.parse(num);
      this.name = obj.name;
      // const object = JSON.parse(Carname);
      this.cartoonName = JSON.parse(Carname);
    },
  },
};
</script>

<style lang="scss" scoped>
.my {
  .my-title {
    width: 100%;
    height: 30px;
    line-height: 30px;
    text-align: center;
    border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  }
  .my-box {
    width: 90%;
    height: 180px;
    border-radius: 10px;
    margin: 20px auto;
    background-color: aliceblue;
    padding-top: 10px;
    .box-item {
      height: 90px;
      line-height: 90px;
      display: flex;
      .head {
        width: 80px;
        height: 80px;
        background-color: darkgray;
        border: 5px solid white;
        border-radius: 50%;
        display: inline-block;
        margin-left: 20px;
      }
      .name {
        display: inline-block;
        font-size: 20px;
        color: skyblue;
        margin-left: 20px;
      }
    }
    .list{
      margin-left: 30px;
      // color: white;
    }
  }
  .bookshelf{
    width: 90%;
    min-width: 80px;
    margin: 30px auto 100px;
    
    .bookshelf-title{
      font-size: 16px;
    }
    .bookshelf-item{
      margin: 20px 0;
      display: flex;
      flex-wrap: wrap;
      // justify-content: space-evenly;

      .item{
        width: 40%;
        height: 180px;
        border: 1px solid rgba(0, 0, 0, 0.1);
             margin: 20px 20px 20px 10px;

        img{
          vertical-align: middle;
          width: 100%;
          height: 100%;
        }
        p{
          padding: 0;
          margin: 10px 0 0;
        }
      }
    }
  }
}
</style>