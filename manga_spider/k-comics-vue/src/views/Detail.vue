<template>
  <div class="detail">
    <div class="nav-box">
      <van-nav-bar
        title="漫画详情"
        left-text="返回"
        left-arrow
        @click-left="back"
      />
    </div>
    <div class="details-box" >
      <!-- <div class="imgBox">
        <img
          :src="`https://images.weserv.nl/?url=${detailsData.horizontal_cover}${imgSuffix}`"
          alt=""
        />
        <p class="img-title">{{ detailsData.title }}</p>
        <p class="img-text">
          <span>{{ getText(detailsData.author_name) }}</span
          ><span>{{ getText(detailsData.styles) }}</span>
        </p>
      </div> -->
      <!-- <div class="collect">
        <div class="starText" @click="sortStar()">
          <img class="star" src="../assets/images/star.svg" alt="" />
          <span>{{ isStar == false ? "追漫" : "已追" }}</span>
        </div>
        <van-button
          class="button"
          round
          width="210px"
          type="info"
          color="#fb7299"
          v-for="(list, index) in sortedList.slice(0, 1)"
          :key="index"
          @click="viewDetail(list.id, list.ord, detailsData.title)"
          >看第{{ list.ord }}话</van-button
        >
      </div> -->
      <div class="detail-box">
        <!-- <p class="dbox-title">
          {{ detailsData.is_finish == 0 ? "连载中" : "已完结" }}
        </p>
        <div class="dbox-evaluate">
          <p>{{ detailsData.evaluate }}</p>
        </div> -->
        <div class="db-total">
          <h4>全部章节({{ detailsData[0].chapter_id }})</h4>
          <div class="total-r" @click="sortList()">
            {{ ascending == true ? "正序" : "倒序" }}
          </div>
        </div>
        <div class="db-item">
          <div
            class="item-box"
            v-for="(list, index) in sortedList.slice(0, 50)"
            :key="index"
            v-if="index < 50"
            @click="viewDetail(list.chapter_id, list.chapter_link, title)"
          >
            <!-- <img
              class="lock"
              v-if="list.pay_mode == 1"
              src="../assets/images/lock.png"
              alt=""
            /> -->
            {{ list.chapter_id }}
          </div>
          <div
            class="item-box"
            v-for="(list, index) in sortedList.slice(50)"
            :key="index + 50"
            v-if="isShowingMore"
            @click="viewDetail(list.chapter_id, list.chapter_link, title)"
          >
            <img
              class="lock"
              v-if="list.pay_mode == 1"
              src="../assets/images/lock.png"
              alt=""
            />
            {{ list.chapter_id }}
          </div>
          <div class="item-box" @click="showMore()" v-if="isShowMore">
            . . .
          </div>
        </div>
      </div>
      <!-- 评论模块 -->
      <!-- <div class="comment-box">
        <h4>全部评论({{ CommentDataPage.acount }})</h4>
        <div class="comment-wrap">
          <div class="comment-container">
            <div class="wrap-box"
              v-for="(replies, index) in CommentDataReplies"
              :key="index"
              v-if="index < 7"
            >
              <div class="user-info">
                <img
                  :src="`https://images.weserv.nl/?url=${replies.member.avatar}${imgSuffix}`"
                  alt=""
                />
                <div class="user-text">
                  <p>{{ replies.member.uname }}</p>
                  <p>{{ replies.reply_control.time_desc }}</p>
                </div>
              </div>
              <div class="comment-info">
                <div class="multi-line-text">{{ replies.content.message }}</div>
              </div>
            </div>
            <div class="wrap-box go-app">
              <p>去App内讨论 ></p>
            </div>
          </div>
        </div>
      </div> -->


      <!-- 猜你喜欢模块 -->
      <!-- <div class="manga-recommendation">
        <div class="section-title">猜你喜欢</div>
        <div class="manga-list">
          <div
            class="list-item"
            v-for="(item, index) in CommentRecommend"
            :key="index"
          >
            <img
              :src="`https://images.weserv.nl/?url=${item.vertical_cover}${imgSuffix}`"
              alt=""
            />
            <div class="manga-title">{{ item.title }}</div>
            <div class="manga-info">
              {{ item.isfinish == 1 ? "完结" : "更新至" }}{{ item.total }}话
            </div>
          </div>
        </div>
      </div> -->
    </div>
  </div>
</template>

<script>
export default {
  name: "Detail",

  data() {
    return {
      detail_link: "",

      title: "",

      detailsData: [],

      listData: [],

      CommentDataPage: [],

      CommentDataReplies: [],

      CommentRecommend: [],

      nameArr: [],

      imgSuffix: "@600w.jpg",

      isShowingMore: false,

      isShowMore: true,

      ascending: true,

      isStar: false,

      ord: [],
    };
  },

  created() {
    this.title = this.$route.params.name;
    this.detail_link = this.$route.params.detail_link;
    this.getComicDetail();
    //this.getCommentDetail();
    //this.getRecommendDetail();
    // this.sortedList();
    //this.isStars();
  },

  computed: {
    sortedList() {
      const newList = [...this.detailsData];
      if (this.ascending == true) {
        newList.sort((a, b) => a.chapter_id - b.chapter_id);
        this.ascending == false;
      } else {
        newList.sort((a, b) => b.chapter_id - a.chapter_id);
      }
      console.log(newList);
      return newList;
    },
  },

  methods: {
    sortList() {
      this.ascending = !this.ascending;
    },

    isStars() {
      console.log(this.pid);

      let components = sessionStorage.getItem("cartoon");

      let nameArr = JSON.parse(components) || [];
      // console.log(nameArr);
      const found = nameArr.some((item) => item.id === this.pid);
      // console.log(found);
      if (found) {
        this.isStar = true;
        console.log(1);
      } else {
        this.isStar = false;
      }
      // if (this.pid == nameArr.id) {
      //   this.isStar = !this.isStar;
      // }
    },

    sortStar() {
      this.isStar = !this.isStar;
      // let Carname = sessionStorage.getItem("cartoon");
      // 将更新后的数据保存回存储
      // console.log(nameArr);
      let { title, vertical_cover, id } = this.detailsData;
      let obj = {};
      obj.title = title;
      obj.vertical_cover = vertical_cover;
      obj.id = id;
      console.log("obj", obj);

      let components = sessionStorage.getItem("cartoon");

      let nameArr = JSON.parse(components) || [];
      // console.log(nameArr);
      nameArr.push(obj);
      console.log(nameArr);
      // let newArr = [...new Set(nameArr)];
      let arr = [...new Set(nameArr.map((item) => JSON.stringify(item)))].map(
        (item) => JSON.parse(item)
      );
      // sessionStorage.setItem("cartoon", JSON.stringify(newArr));
      sessionStorage.setItem("cartoon", JSON.stringify(arr));
      console.log("1.0", nameArr);

      // let components = JSON.parse(sessionStorage.getItem("cartoon")) || [];
      // console.log(components);
      // components.push(nameArr);
      // sessionStorage.setItem("cartoon", JSON.stringify(components));
      // sessionStorage.setItem(
      //   "cartoon",
      //   JSON.stringify({
      //     name:name
      //   })
      // );
    },

    viewDetail(chapter_id, chapter_link, name) {
      console.log("传参",chapter_id, chapter_link, name)
      this.$router.push({ name: "Cartoon", params: { chapter_id, chapter_link, name } });
      // this.$router.push({ name: "Cartoon", params: { id } });
      // this.$router.push({ name: "Cartoon", params: { name } });
      // console.log(cid);
      // console.log(titleName);
    },

    showMore() {
      this.isShowingMore = !this.isShowingMore;
      this.isShowMore = !this.isShowMore;
    },

    back() {
      this.$router.back();
    },

    getText(str) {
      // console.log(str);
      // 在这里对传入的文本进行处理
      return str?.toString().replace(/\,/g, " ");
    },

    getComicDetail() {
       
       console.log("传参数 res ==> ", this.detail_link);
      this.axios({
        method: "get",
        url: this.$api+"/detail?",
        params: {
          url: this.detail_link,
        },
      })
        .then((res) => {
          console.log("获取章节详情 res ==> ", res);
          this.detailsData = res.data
          console.log(this.detailsData)
          // this.detailsData = res.data.data;
          // this.listData = res.data.data.ep_list;
          // console.log(this.detailsData);
          // console.log(this.listData);
        })
        .catch((err) => {});
    },

    getCommentDetail() {
      this.axios({
        method: "get",
        url: "https://apis.netstart.cn/mbcomic/reply?",
        params: {
          oid: this.pid,
        },
      })
        .then((res) => {
          console.log("获取漫画评论 res ==> ", res);
          this.CommentDataPage = res.data.data.page;
          this.CommentDataReplies = res.data.data.replies;
          console.log(this.CommentData);
          console.log(this.CommentDataReplies);
        })
        .catch((err) => {});
    },

    getRecommendDetail() {
      this.axios({
        method: "get",
        url: "https://apis.netstart.cn/mbcomic/Recommend?",
        params: {
          comic_id: this.pid,
        },
      })
        .then((res) => {
          console.log("获取漫画评论 res ==> ", res);
          this.CommentRecommend = res.data.data;
          console.log(this.CommentRecommend);
        })
        .catch((err) => {});
    },
  },
};
</script>

<style lang="scss" scoped>
.details-box {
  .imgBox {
    position: relative;
    height: 210px;
    img {
      position: absolute;
      width: 375px;
      height: 210px;
      z-index: -1;
    }
    .img-title {
      z-index: 1;
      position: absolute;
      font-size: 20px;
      color: white;
      text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
      top: 135px;
      left: 15px;
    }
    .img-text {
      position: absolute;
      color: white;
      text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
      font-size: 12px;
      top: 175px;
      left: 10px;
      span:last-child {
        margin-left: 10px;
      }
    }
  }
  .collect {
    display: flex;
    justify-content: space-between;
    width: 93%;
    height: 44px;
    margin: 0.5333rem auto 0.3rem;
    line-height: 44px;
    .starText {
      min-width: 74px;
      padding: 6px 6px 6px 0;
      font-size: 18px;
      line-height: 30px;
      .star {
        width: 32px;
        height: 32px;
        vertical-align: middle;
      }
    }
    .button {
      width: 210px;
    }
  }
  .detail-box {
    width: 345px;
    margin: 0 auto;
    padding-top: 16px;
    padding-bottom: 15px;
    .dbox-title {
      margin: 0;
      font-size: 16px;
      padding-bottom: 8px;
    }
    .dbox-evaluate {
      color: #999;
      font-size: 12px;
      height: 33px;
      overflow: hidden;
      text-overflow: ellipsis;
      p {
        height: 33px;
        margin: 0;
      }
    }
    .db-total {
      margin-top: 23px;
      margin-bottom: 8px;
      h4 {
        font-weight: normal;
        font-size: 16px;
        margin: 0;
        display: inline-block;
      }
      .total-r {
        display: block;
        float: right;
      }
    }
    .db-item {
      .item-box {
        border-radius: 3px;
        border: 1px solid #ccc;
        display: inline-block;
        width: 23%;
        margin: 3px;
        overflow: hidden;
        font-size: 14px;
        color: #212121;
        text-align: center;
        line-height: 36px;
        box-sizing: border-box;
        position: relative;
        .lock {
          position: absolute;
          top: 0;
          right: 0;
          width: 16px;
          height: 16px;
        }
      }
    }
  }
  .comment-box {
    width: 345px;
    margin: 0 auto;
    h4 {
      font-size: 16px;
      font-weight: normal;
    }
    .comment-wrap {
      overflow-y: scroll;
      height: 120px;
    }
    .comment-container {
      white-space: nowrap;
      width: auto;
      .wrap-box {
        width: 225px;
        height: 95px;
        border: 1px solid #eee;
        padding: 11px;
        margin: 0 12px 0 0;
        overflow: hidden;
        display: inline-block;
      }
      .go-app{
        width: 158px;
        height: 95px;
        color: #fb7299;
        font-size: 14px;
        background: #f5f7f8;
        text-align: center;
        line-height: 65px;
        p{
          display: inline-block;
        }
      }
      .user-info {
        height: 35px;
        img {
          width: 32px;
          border-radius: 32px;
          margin: 0 6px 0 0;
        }
        .user-text {
          display: inline-block;
          p {
            margin: 0;
            color: #757575;
            font-size: 12px;
          }
        }
      }
      .comment-info {
        max-height: 54px;
        padding-right: 10px;
        overflow: hidden;
        .multi-line-text {
          text-align: justify;
          overflow: hidden;
          white-space: normal;
        }
      }
    }
  }
  .manga-recommendation {
    margin: 16px;
    .section-title {
      font-size: 16px;
      color: #212121;
      line-height: 40px;
    }
    .manga-list {
      .list-item {
        width: 28%;
        padding: 8px;
        display: inline-block;
        img {
          width: 98px;
        }
        .manga-info {
          font-size: 12px;
          color: #999;
        }
      }
    }
  }
}
</style>