<template>
  <div id="app" style = "margin: -1% -0.6%">
    <div style="width: 100%;height: 100%;">
      <el-backtop :bottom="60">UP</el-backtop>
    </div>
    <el-menu :default-active="activeIndex"
      class="el-menu-demo"
      mode="horizontal"
      router
      @select="handleSelect"
      background-color="#000000"
      text-color="#ffffff"
    >
      <el-menu-item index="1" style = "width: 10%">
        <img src = "../assets/LOGO.png" width = 120% align = "left" style = "margin-top: 8px">
      </el-menu-item>
      <el-menu-item index="/" style="margin-left: 400px">Classification</el-menu-item>
      <el-menu-item index="/image">Watermark</el-menu-item>
      <el-menu-item index="/similarity">Similarity</el-menu-item>
    </el-menu>
    <el-carousel :interval="5000" style = "height: 350%; margin: 0 0; background-color: #e9eef3">
      <el-carousel-item v-for="item in bannerList" :key="item">
        <a href="#">
          <img :src=item.url style="width: 100%">
        </a>
      </el-carousel-item>
    </el-carousel>
    <el-tabs v-model="activeName" @tab-click="handleSelect" style = "justify-content: center; display: flex; text-align: center; background-color: #e9eef3">
      <el-tab-pane label="Soft Music" name="first"></el-tab-pane>
      <el-tab-pane label="Noisy Music" name="second"></el-tab-pane>
      <el-tab-pane label="Crawled Music" name="third"></el-tab-pane>
    </el-tabs>
    <div style = "background-color: #e9eef3">
      <el-input
        placeholder="请输入爬取的歌手名或歌曲名"
        v-model="input"
        style = "width: 18%; padding-top: 1%; padding-bottom: 2%"
        @keyup.enter.native="get_crawl"
        clearable>
      </el-input>
    </div>
    <div v-if = "softmusic.length === 0" style = "background-color: #e9eef3; padding-bottom: 3%">
      <span>暂无歌曲</span>
    </div>
    <div style = "background-color: #e9eef3">
      <el-row style = "margin-left: 120px; margin-right: 120px">
        <el-col :span="6" v-for="(item, index) in softmusic" style = "margin: 2% auto">
          <div class="img_div" style="height: 230px; padding: 20px">
            <div>
              <div style="padding-bottom: 15px">
                <span style="font-size: 18px !important">{{softtxt[index]}}</span>
              </div>
              <img :src="require('../assets/crawl/'+softimage[index])" style="width: 100%; height: 200px; border-radius:10px 10px;">
            </div>
            <audio controls="controls" style="width: 300px">
              <source :src="require('../assets/crawl/'+softmusic[index])">
            </audio>
          </div>
        </el-col>
      </el-row>
      <el-dialog
        title="详细信息"
        :visible.sync="dialog"
        width="30%"
        :before-close="handleClose">
        <span>{{text}}</span>
        <span slot="footer" class="dialog-footer">
          <el-button type="danger" @click="dialog = false">关闭</el-button>
        </span>
      </el-dialog>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MainPage',
  data () {
    return {
      activeIndex: '/',
      activeName: 'third',
      showall: false,
      input: '',
      softmusic: [],
      softimage: [],
      softtxt: [],
      text: '',
      dialog: false,
      mark: 0,
      bannerList: [{url: require('../assets/ad1.jpg'), id: 0}, {url: require('../assets/ad2.jpg'), id: 1}, {url: require('../assets/ad3.jpg'), id: 2}, {url: require('../assets/ad4.jpg'), id: 3}, {url: require('../assets/ad5.jpg'), id: 4}],
      flat: false,
      media: true,
      loading: false,
      actions: true,
      outlined: false,
      elevation: undefined,
      raised: false,
      width: 344,
      height: undefined,
      currentDate: new Date()
    }
  },
  methods: {
    handleSelect (key, keyPath) {
      if (key.name === 'first') {
        this.$router.push({ path: './' })
      }
      else if (key.name === 'second') {
        this.$router.push({ path: './noisy' })
      }
      //console.log("111", key.name, keyPath)
    },
    handleClose (done) {
      this.$confirm('确认关闭？')
        .then(_ => {
          done()
        })
        .catch(_ => {})
    },
    autoPlay () {
      this.mark++
      if (this.mark === 5) {
        this.mark = 0
      }
    },
    play () {
      setInterval(this.autoPlay, 2500)
    },
    change (i) {
      this.mark = i
    },
    GetSoftMusicUrl () {
      this.$api.post('/get_crawl_music').then(response => {
        this.softmusic = response.data
        console.log(this.softmusic)
      })
    },
    GetSoftImageUrl () {
      this.$api.post('/get_crawl_image').then(response => {
        this.softimage = response.data
        //console.log(this.softimage)
      })
    },
    GetSoftTxt () {
      this.$api.post('/get_crawl_txt').then(response => {
        this.softtxt = response.data
      })
    },
    show (index) {
      this.text = this.softtxt[index]
    },
    get_crawl () {
      console.log(this.input)
      this.$api.post('/get_crawl', {input: this.input}).then(response => {
        this.$message.success('爬取成功！');
      })
    }
  },
  mounted () {
    this.GetSoftTxt()
    this.GetSoftMusicUrl()
    this.GetSoftImageUrl()
  },
  created () {
    this.play()
  },
  filters: {

  }
}
</script>

<style>
  .el-menu-item {
    font-size: 18px;
    font-weight: bold;
    font-family: SimSun;
    padding-top: 0.4%;
  }
  .el-link {
    text-weight: bold !important;
    align: right !important;
  }
  .el-collapse-item__header {
    color: #409eff;
    text-align: center;
  }
  .el-carousel__container {
    position: relative;
    height: 700px;
  }
  .el-carousel__indicators--horizontal {
    bottom: 20px !important;
  }
  .image {
    width: 100%;
    display: block;
  }
  .clearfix:before,
  .clearfix:after {
      display: table;
      content: "";
  }
  .clearfix:after {
      clear: both
  }
  html {
    background-color: #e9eef3;
  }
  .el-menu--horizontal>.el-menu-item.is-active {
    color: #54ff00 !important;
  }
  .el-card__body {
    padding: 0px;
  }
  .el-tabs__item {
    padding: 50px 20px;
    font-weight: bold;
    font-size: 20px;
  }
</style>
