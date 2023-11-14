<template>
  <div class="classify">
    <div class="classify-title">分类</div>
    <div class="classify-box">
      <div class="label-list">
        <!-- 漫画类型 -->
        <div class="label-row">
          <div
            class="first-label"
            type="-1"
            @click="highlight1(0, -1)"
            :class="{ active: currentIndex === 0 }"
          >
            全部
          </div>
          <div
            class="classify-label"
            v-for="(style, index) in stylesData"
            :key="index"
            @click="highlight1(index + 1, style.id)"
            :class="{ active: currentIndex === index + 1 }"
          >
            {{ style.name }}
          </div>
        </div>
        <!-- 地区 -->
        <div class="label-row" v-show="visible">
          <div
            class="first-label"
            type="-1"
            @click="highlight2(0, -1)"
            :class="{ active: areasIndex === 0 }"
          >
            全部
          </div>
          <div
            class="classify-label"
            v-for="(area, index) in areasData"
            :key="index"
            @click="highlight2(index + 1, area.id)"
            :class="{ active: areasIndex === index + 1 }"
          >
            {{ area.name }}
          </div>
        </div>
        <!-- 是否完结 -->
        <div class="label-row" v-show="visible">
          <div
            class="first-label"
            type="-1"
            @click="highlight3(0, -1)"
            :class="{ active: statusIndex === 0 }"
          >
            全部
          </div>
          <div
            class="classify-label"
            v-for="(statu, index) in statusData"
            :key="index"
            @click="highlight3(index + 1, statu.id)"
            :class="{ active: statusIndex === index + 1 }"
          >
            {{ statu.name }}
          </div>
        </div>
        <!-- 是否付费 -->
        <div class="label-row" v-show="visible">
          <div
            class="first-label"
            type="-1"
            @click="highlight4(0, 0)"
            :class="{ active: pricesIndex === 0 }"
          >
            全部
          </div>
          <div
            class="classify-label"
            v-for="(price, index) in pricesData"
            :key="index"
            @click="highlight4(index + 1, price.id)"
            :class="{ active: pricesIndex === index + 1 }"
          >
            {{ price.name }}
          </div>
        </div>
        <!-- 时间分类 -->
        <div class="label-row">
          <div
            class="first-label"
            type="-1"
            @click="highlight5(0, -1)"
            :class="{ active: ordersIndex === 0 }"
          >
            全部
          </div>
          <div
            class="classify-label"
            v-for="(order, index) in ordersData"
            :key="index"
            @click="highlight5(index + 1, order.id)"
            :class="{ active: ordersIndex === index + 1 }"
          >
            {{ order.name }}
          </div>
        </div>
        <!-- 筛选 -->
        <div class="v-middle" v-on:click="toggle">筛选</div>
      </div>
    </div>
    <div class="list-data">
      <div class="list-item" v-for="(item, index) in imageData" :key="index" @click="viewDetail(item.season_id)">
        <img
          :src="`https://images.weserv.nl/?url=${item.vertical_cover}${imgSuffix}`"
          alt=""
        />
        <div class="list-title">{{ item.title }}</div>
        <div class="list-info">
          {{ item.isfinish == 1 ? "[完结] 共" : "[更新] 至"
          }}{{ item.total }} 话
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Classify",
  data() {
    return {
      imgSuffix: "@760w_380h.jpg",
      stylesData: [],
      ordersData: [],
      pricesData: [],
      statusData: [],
      areasData: [],
      imageData: [],
      visible: false,
      currentIndex: 0,
      statusIndex: 0,
      pricesIndex: 0,
      ordersIndex: 0,
      areasIndex: 0,
      obj: {
        style_id: -1,
        area_id: -1,
        is_finish: -1,
        order: 0,
        is_free: -1,
      },
    };
  },
  created() {
    this.getType();
    this.getClassify();
  },
  methods: {
    viewDetail(pid) {
      this.$router.push({ name: "Detail", params: { pid } });
      console.log(pid);
    },
    highlight1(index, styles) {
      this.currentIndex = index;
      this.obj.style_id = styles;
      this.getClassify(styles);
    },
    highlight2(index, areas) {
      this.areasIndex = index;
      this.obj.area_id = areas;
      this.getClassify(areas);
    },
    highlight3(index, statu) {
      this.statusIndex = index;
      this.obj.is_finish = statu;
      this.getClassify(statu);
    },
    highlight4(index, prices) {
      this.pricesIndex = index;
      this.obj.is_free = prices;
      this.getClassify(prices);
    },
    highlight5(index, orders) {
      this.ordersIndex = index;
      this.obj.order = orders;
      this.getClassify(orders);
    },
    toggle() {
      this.visible = !this.visible;
    },
    //获取商品类型
    getType() {
      this.axios({
        method: "get",
        url: "https://apis.netstart.cn/mbcomic/AllLabel",
      })

        .then((res) => {
          console.log("获取分类筛选条件 res ==> ", res);
          this.stylesData = res.data.data.styles;
          this.ordersData = res.data.data.orders;
          this.pricesData = res.data.data.prices;
          this.statusData = res.data.data.status;
          this.areasData = res.data.data.areas;
          // console.log(this.stylesData);
        })
        .catch((err) => {
          console.log("获取分类筛选条件 err ==> ", err);
        });
    },
    getClassify() {
      // console.log(styles, areas, statu, orders, prices);
      this.axios({
        method: "get",
        url: "https://apis.netstart.cn/mbcomic/ClassPage",
        params: {
          ...this.obj,
        },
      })

        .then((res) => {
          console.log("获取分类筛选条件 res ==> ", res);
          if (res.data.code === 0) {
            this.imageData = res.data.data;
            console.log(this.imageData);
            console.log(this.obj);
          }
        })
        .catch((err) => {
          console.log("获取分类筛选条件 err ==> ", err);
        });
    },
  },
};
</script>

<style lang="scss" scoped>
.classify {
  color: #6c727e;
  .classify-title {
    width: 100%;
    height: 30px;
    line-height: 30px;
    text-align: center;
    border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  }
  .classify-box {
    width: 100%;
    .label-list {
      padding: 10px 16px 0 16px;
      position: relative;
      .label-row {
        .first-label,
        .classify-label {
          font-size: 12px;
          display: inline-block;
          padding: 2px 10px 2px 10px;
          margin: 6px 0;
        }
      }
      .label-row:first-child {
        border-bottom: 1px solid rgba(0, 0, 0, 0.1);
      }
      .v-middle {
        display: inline-block;
        position: absolute;
        bottom: 9px;
        right: 15px;
        color: #6c727e;
        font-size: 12px;
      }
    }
  }
  .list-data {
    box-sizing: border-box;
    padding: 0px 8px 50px 8px;
    .list-item {
      width: 33.3%;
      padding: 8px;
      display: inline-block;
      box-sizing: border-box;
      img {
        width: 100px;
        height: 140px;
      }
      .list-title {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        font-size: 14px;
        color: black;
      }
      .list-info {
        font-size: 12px;
      }
    }
  }
}
.active {
  color: #fb7299;
}
</style>