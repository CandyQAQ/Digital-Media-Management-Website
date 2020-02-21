<template>
  <div id="app">
    <img src="../assets/001.png">
    <audio controls="controls">
      <source src="../assets/001.mp3">
    </audio>
    <el-button type="success">按钮</el-button>
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'MainPage',
  data () {
    return {}
  },
  methods: {
  },
  filters: {

  }
}
</script>

<style>

</style>
