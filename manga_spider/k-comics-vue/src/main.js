import Vue from 'vue'

import axios from 'axios'

import VueAxios from 'vue-axios'

import { 
  Tabbar, 
  TabbarItem,
  Search,
  Sidebar, 
  SidebarItem,
  Grid, 
  GridItem,
  Swipe,
  SwipeItem,
  Tag,
  Sticky,
  DropdownMenu,
  DropdownItem,
  NavBar,
  Button,
  Toast,
} from 'vant';

import App from './App.vue'
import router from './router'
import api from "./index" 
import 'lib-flexible/flexible'

Vue.use(Tabbar)
.use(TabbarItem)
.use(Search)
.use(Sidebar)
.use(SidebarItem)
.use(Grid)
.use(GridItem)
.use(Swipe)
.use(SwipeItem)
.use(Tag)
.use(Sticky)
.use(DropdownMenu)
.use(DropdownItem)
.use(NavBar)
.use(Button)

Vue.prototype.$axios = axios
Vue.prototype.$api = api.commonUrl
Vue.config.productionTip = false

Vue.use(VueAxios, axios);

router.beforeEach((to, from, next) => {
  let num = sessionStorage.getItem("token");

  console.log(num);
  if ( to.name == 'My') {
    if (num != null) {
      next()
    } else {

      next({
        name: 'MyLogin'
      })
    }
  } else {
    next()
  }
})

//设置请求基础路劲
axios.defaults.baseURL = 'https://apis.netstart.cn/mbcomic';

// 添加请求拦截器
axios.interceptors.request.use(
  function (config) {
    // 在发送请求之前做些什么
    // console.log('发送请求之前触发');

    // let appkey = 'U2FsdGVkX19WSQ59Cg+Fj9jNZPxRC5y0xB1iV06BeNA=';

    //处理参数
    // console.log('config ==> ', config);
    //如果时get请求, 参数则保存在params
    // if (config.method === 'get') {
    //     config.params = config.params || {};
    //     config.params.appkey = appkey;
    // }

    //启动加载提示
    Toast({
      type: 'loading',
      message: '加载中...',
      forbidClick: true,
      duration: 0,
    });

    return config;
  },
  function (error) {
    // 对请求错误做些什么
    //关闭加载提示
    Toast.clear();
    return Promise.reject(error);
  }
);

// 添加响应拦截器
axios.interceptors.response.use(
  function (response) {
    // 对响应数据做点什么
    //关闭加载提示
    Toast.clear();

    return response;
  },
  function (error) {
    // 对响应错误做点什么
    //关闭加载提示
    Toast.clear();

    return Promise.reject(error);
  }
);



new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
