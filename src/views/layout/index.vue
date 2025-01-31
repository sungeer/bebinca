<template>
  <el-container>
    <el-header style="display:flex;justify-content:space-between;color:#fff;line-height:60px; font-size: 18px;background-color:#545c64">
      <div class="logo"></div>
      <div class="title">核酸采集平台</div>
      <div class="end">
      <span @click="doLogout"><i class="el-icon-switch-button"/>注销</span>
      </div>
    </el-header>
    
    <el-container>

    <el-aside width="200px" style="background-color: #545c64">
      <el-menu
      default-active="2"
      :router="true"
      class="el-menu-vertical-demo"
      background-color="#545c64"
      text-color="#fff"
      active-text-color="#ffd04b">
      <el-menu-item index="1" route="/yuyuecode">
        <i class="el-icon-s-grid"></i>
        <span slot="title">预约二维码</span>
      </el-menu-item>
      <el-menu-item index="2" route="/person">
        <i class="el-icon-menu"></i>
        <span slot="title">预约信息查询</span>
      </el-menu-item>
      <el-menu-item index="3" route="/dengjicode">
        <i class="el-icon-s-grid"></i>
        <span slot="title">登记二维码</span>
      </el-menu-item>
      <el-menu-item index="4" route="/checkin">
        <i class="el-icon-document"></i>
        <span slot="title">登记信息查询</span>
      </el-menu-item>
    </el-menu>
    </el-aside>
    <el-main>
      <router-view />
    </el-main>
    </el-container>
  </el-container>
</template>
<script>
export default {
  name: 'Layout',
  methods:{
    doLogout() {
      window.sessionStorage.removeItem("Authorization")
      this.$router.replace('/login')
    }
  }
}
</script>
<style scoped>
aside {
  height: 100%;
}
.el-container {
  height: 100%;
}
.el-main {
  padding: 10px;
  background: #fefefe;
}
.end {
  font-size:14px;
  cursor: pointer;
}
</style>