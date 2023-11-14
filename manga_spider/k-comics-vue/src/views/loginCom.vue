<template>
  <div class="myInfo">
    <div class="header">
      <img src="../assets/images/login.jpg" alt="" />
    </div>
    <div class="myInfo-con">
      <div class="myInfo-title">
        <ul>
          <li
            :class="index == i ? 'active' : ''"
            v-for="(item, i) in arr"
            :key="i"
            @click="changeInfo(i)"
          >
            {{ item.title }}
          </li>
          <!-- <li>注册</li> -->
        </ul>
      </div>
      <div class="login-con" v-if="index == 0 ? 'isShow' : ''">
        <div class="inp">
          <input
            type="text"
            placeholder="请输入昵称"
            v-model="loginName"
            @keydown.enter="getLogin()"
          />
          <input
            type="password"
            placeholder="请输入密码"
            v-model="loginPass"
            @keydown.enter="getLogin()"
          />
        </div>
        <div class="check"><input type="checkbox" /><span>记住我</span></div>
        <div class="btn">
          <button @click="goHome">登录</button>
          <button @click="goback()">返回</button>
        </div>
      </div>
      <div class="register-con" v-if="index == 1 ? '!isShow' : ''">
        <div class="inp">
          <input
            type="text"
            placeholder="填写常用手机号"
            v-model="phone"
            @keydown.enter="getInfo()"
          />
          <input
            type="text"
            placeholder="昵称"
            v-model="uname"
            @keydown.enter="getInfo()"
          />
          <input
            type="password"
            placeholder="请输入密码"
            v-model="pass"
            @keydown.enter="getInfo()"
          />
        </div>
        <div class="check">
          <input type="checkbox" /><span
            >我已同意<span class="word">《扒啦扒啦漫画用户使用协议》</span
            >和<span class="word">《扒啦扒啦漫画隐私政策》</span></span
          >
        </div>
        <button class="btn" @click="goLogin()">注册</button>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: "MyLogin",
  data() {
    return {
      uname: "",
      loginName: "",
      pass: "",
      loginPass: "",
      phone: "",
      index: 0,
      isShow: true,
      num: null,
      arr: [
        {
          title: "登录",
        },
        {
          title: "注册",
        },
      ],
    };
  },
  methods: {
    getInfo() {
      let v1 = this.uname;
      let v2 = this.pass;
      let v3 = this.phone;
    },
    goback() {
      this.$router.go(-1);
    },
    getLogin() {
      this.loginName;
      this.loginPass;
    },
    goHome() {
      this.num = JSON.parse(sessionStorage.getItem("token"));
      if (this.num == null) {
        if (confirm("您还没有注册,是否前往注册")) {
          this.isShow = true;
          this.index = 1;
        }
        return;
      }
      if (this.loginName.length == 0 && this.loginPass.length == 0) {
        alert("您还没输入好信息");
      } else if (
        this.loginName != this.num.name &&
        this.loginPass != this.num.pass
      ) {
        alert("信息错误");
      } else {
        // location.href = "/";
        alert("登陆成功,即将跳转");
        location.href = "/";
      }
    },
    goLogin() {
      if (
        this.uname.length == 0 &&
        this.pass.length == 0 &&
        this.phone.length == 0
      ) {
        alert("您还没输入好信息");
        return;
      } else if (this.uname.length == 0 && this.phone.length == 0) {
        alert("你还没有输入昵称和手机号码");
      } else if (this.uname.length == 0 && this.pass.length == 0) {
        alert("你还没有输入昵称和密码");
      } else if (this.pass.length == 0 && this.phone.length == 0) {
        alert("你还没有输入密码和手机号码");
      } else if (this.uname.length == 0) {
        alert("你还没有输入昵称");
      } else if (this.pass.length == 0) {
        alert("你还没有输入密码");
      } else if (this.phone.length == 0) {
        alert("你还没有输入手机号码");
      } else {
        // location.href = "/";
        sessionStorage.setItem(
          "token",
          JSON.stringify({
            name: this.uname,
            pass: this.pass,
            phone: this.phone,
          })
        );
        this.isShow = true;
        this.index = 0;
      }
    },
    changeInfo(value) {
      this.index = value;
      this.isShow = !this.isShow;
    },
  },
  created() {
    this.num = JSON.parse(sessionStorage.getItem("token"));
  },
};
</script>
<style lang="scss">
html{
  // font-size: 0;
  .myInfo {
  position: relative;
  width: 90%;
  height: 400px;
  margin: 128px auto 0;
  // background-color: pink;
  border: 1px solid #ccc;
  border-radius: 15px;
  .header {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 2.6667px;
    img {
      width: 100%;
      border-top-left-radius: 15px;
      border-top-right-radius: 15px;
    }
  }
  .myInfo-con {
    position: absolute;
    top: 35px;
    left: 20px;
    z-index: 10000;
    display: flex;
    flex-direction: column;
    width: 90%;
    height: 293px;
    .myInfo-title {
      ul {
        display: flex;
        li {
          font-size: 18px;
          padding: 0.4px 0.5px;
          // color: skyblue;
          border-bottom: 4px solid #ccc;
          &.active {
            border-bottom: 4px solid #00a1d6;
            color: #2db2dd;
            transition: all 0.5s;
          }
        }
      }
    }
    .login-con {
      width: 272px;
      .inp {
        margin-top: 1.2px;
        width: 272px;
        input {
          display: block;
          width: 272px;
          height: 44px;
          margin-top: 16px;
          padding-left: 9.6px;
          font-size: 12px;
        }
      }
      .check {
        margin-top: 1px;
        font-size: 12px;
        font-size: #ccc;
        // display: flex;
        input {
          vertical-align: middle;
        }
        span {
          font-size: 8px;
        }
      }
      .btn {
        margin: 13px auto;
        width: 272px;
        // display: flex;
        button {
          display: inline-block;
          width: 60px;
          height: 38px;
          background-color: skyblue;
          color: #fff;
          margin-left: 60px;
          border: 0;
        }
      }
    }
    .register-con {
      .inp {
        margin-top: 1.2px;
        input {
          display: block;
          width: 272px;
          height: 44px;
          margin-top: 10px;
          padding-left: 0.6px;
          font-size: 12px;
        }
      }
      .check {
        margin-top: 1px;
        font-size: 12px;
        font-size: #ccc;
        display: flex;
        input {
          vertical-align: middle;
        }
        span {
          font-size: 8px;
        }
        .word {
          color: #00a1d6;
          line-height: 1.8;
        }
      }
      .btn {
        display: block;
        width: 270px;
        height: 38px;
        margin: 10px auto 0;
        border: 0;
        background-color: skyblue;
        color: #fff;
      }
    }
  }
}
}
</style>
