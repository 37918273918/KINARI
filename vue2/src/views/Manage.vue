<template>
    <el-container style="height: 100vh; border: 1px solid #eee">
  <el-aside width="200px" style="background-color: rgb(238, 241, 246)" height="100%" >
    <Aside/><!-- 侧边栏  -->
  </el-aside>
  
  <el-container>
    <el-header style="text-align: right; font-size: 12px;border-bottom: 1px solid #ccc; line-height:60px" >
     <Header/><!-- 头部  -->
    </el-header>

    <el-main>
<!--      表示当前页面的子路由会在<router-view/>中展示-->
        <router-view/>
    </el-main>
  </el-container>
</el-container>

</template>

<script>
// @ is an alias to /src


import Aside from "@/components/Aside.vue";
import Header from "@/components/Header.vue";


export default {
  data()
  {
    return {
      tableData:[],
      mutipleSelection:[],
      total:0,
      username:"",
      msg:"hsh",
      form: {},
      pageNum: 1,
      pageSize:2,
      email:"",
      address:"",
      dialogFormVisible:false

    }
  },
  components: {Aside,Header},

}
</script>
<style>
.headerbg
{
  background:#ccc!important;
}
</style>