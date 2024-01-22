<script>
import {defineComponent} from 'vue'

export default defineComponent({
  name: "Header"
})
</script>

<template>
<div>

    <el-dropdown>
      <i class="el-icon-setting" style="margin-right: 15px"></i>
      <el-dropdown-menu slot="dropdown">
        <el-dropdown-item>find</el-dropdown-item>
        <el-dropdown-item>add</el-dropdown-item>
        <el-dropdown-item>delete</el-dropdown-item>
      </el-dropdown-menu>
    </el-dropdown>
    <span>Shuhan Huang</span>
</div>
</template>

<style scoped>

</style>