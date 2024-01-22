<script>
import {defineComponent} from 'vue'

export default defineComponent({
  name: "Aside",
  props: {

  },

})
</script>

<template>
  <el-menu :default-openeds="['1', '3']" style="min-height: 100%;overflow-x:hidden"
           background-color="rgb(88,20,108)"
           text-color="#fff"
           active-text-color="#ffd04b"
           :collapse-transition="false"
           router
  >
    <el-menu-item index="/home">
      <template slot="title"><i class="el-icon-house"></i>Home</template>
    </el-menu-item>

      <el-menu-item index="/data">
      <template slot="title"><i class="el-icon-house"></i>Data analysis</template>
    </el-menu-item>
  </el-menu>
</template>

<style scoped>

</style>