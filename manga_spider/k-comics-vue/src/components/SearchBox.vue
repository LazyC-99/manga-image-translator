<template>
  <div class="search-box">
    <input type="text" v-model="searchTerm" @input="handleInput" />
    <button @click="handleClick">搜索</button>
  </div>
</template>

<script>
export default {
  name: "SearchBox",
  data() {
    return {
      searchTerm: "",
    };
  },
  methods: {
    handleInput(event) {
      this.searchTerm = event.target.value;
    },
    handleClick() {
      this.$emit("search", this.searchTerm);
    },
  },
};
</script>

<style scoped>
.search-box {
  display: flex;
  align-items: center;
}
.search-box input[type="text"] {
  padding: 8px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
  margin-right: 8px;
}
.search-box button {
  padding: 8px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
</style>
