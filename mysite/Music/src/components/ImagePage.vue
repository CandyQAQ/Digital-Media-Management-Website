<template>
  <div id="app" style = "margin: -1% -0.6%">
    <div style="width: 100%;height: 100%">
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
    <div style = "padding-top: 50px; padding-bottom: 10px; font-weight: bold; font-size: 20px">
      <span>请上传PNG格式原图</span>
    </div>
    <div class="UploadDIV">
      <div class="UploadInnerDIV">
        <el-upload
          action="http://127.0.0.1:8000/upload_image1"
          list-type="picture-card"
          :on-preview="handlePictureCardPreview1"
          :on-remove="handleRemove"
          style = "padding: 2%">
          <i class="el-icon-plus"></i>
        </el-upload>
      </div>
    </div>
    <div style = "padding-top: 50px; padding-bottom: 10px; font-weight: bold; font-size: 20px">
      <span>请上传PNG格式水印图</span>
    </div>
    <div class="UploadDIV">
      <div class="UploadInnerDIV">
        <el-upload
          action="http://127.0.0.1:8000/upload_image2"
          list-type="picture-card"
          :on-preview="handlePictureCardPreview1"
          :on-remove="handleRemove"
          style = "padding: 2%">
          <i class="el-icon-plus"></i>
        </el-upload>
      </div>
    </div>
    <div style = "padding-top: 50px">
      <el-button type="primary" @click="add">添加水印</el-button>
    </div>
    <div style = "padding-top: 50px; padding-bottom: 10px; font-weight: bold; font-size: 20px">
      <span>添加水印后的图片</span>
    </div>
    <div>
      <img src = "../assets/Image/new.png" style = "width: 30%; padding: 2%">
    </div>
    <div style = "padding-top: 50px; padding-bottom: 10px; font-weight: bold; font-size: 20px">
      <span>提取的水印</span>
    </div>
    <div>
      <img src = "../assets/Image/wm.png" style = "width: 30%; padding: 2%">
    </div>
  </div>
</template>

<script>
export default {
  name: 'MainPage',
  data () {
    return {
      image: false,
      watermark: false,
      activeIndex: '/image',
      dialogImageUrl1: '',
      dialogImageUrl2: '',
      dialogVisible1: false,
      dialogVisible2: false
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
    handleRemove(file, fileList) {
      console.log(file, file.url);
    },
    handlePictureCardPreview1 (file) {
      console.log(file.url)
      this.dialogImageUrl1 = file.url;
      this.dialogVisible1 = true;
    },
    handlePictureCardPreview2 (file) {
      this.dialogImageUrl2 = file.url;
      this.dialogVisible2 = true;
    },
    add () {
      this.$api.post('/add_watermark').then(response => {
        this.image = true;
        this.$message.success('添加成功！');
      })
    }
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

  .UploadDIV {
    border-radius: 6px;
    min-height: 155px;
    max-width: 32em;
    background: rgba(152, 152, 152, 0.1);
    margin-left: 525px;
    margin-right: 5em;
    margin-top: 20px;
    position: relative;
    -webkit-box-flex: 1;
    -webkit-flex: 1;
    -ms-flex: 1;
    flex: 1;
    display: flex;
  }

  .UploadDIV:hover {
    background: rgba(102, 102, 102, 0.4);
    box-shadow: inset 0 0 0 1px rgba(122, 122, 122, 0.25), 0 0 0.5em 0 #FF6382;
  }

  .UploadInnerDIV {
    display: flex;
    -webkit-box-align: center;
    -webkit-align-items: center;
    -ms-flex-align: center;
    align-items: center;
    margin: 45px 0;
  }
  .el-upload--picture-card {
    background-color: #f2f8fd;
    height: 148px;
    width: 148px;
    margin-left: 20px;
  }
</style>
