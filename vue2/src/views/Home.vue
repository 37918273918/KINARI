<script>

import {defineComponent} from 'vue'
// import MolecularViewer from '@/components/MolecularViewer.vue';

export default defineComponent({

  name: "protein",
  methods: {
    refreshPage() {
      // 刷新页面的方法
      window.location.reload();
    },
  },
})
</script>

<template>

  <div>
    <el-button @click="refreshPage" style="margin-bottom: 3px">Show</el-button>
    <h3>1YCR:</h3>
    <div
        :style="{height: '600px', width: '600px', position: 'relative'}"
        class="viewer_3Dmoljs"
        ref="viewerElement"
        data-pdb="1YCR"
        data-select1="chain:A"
        data-style1="cartoon:color=spectrum"
        data-surface1="opacity:.7;color:white"
        data-select2="chain:B"
        data-style2="stick"
        :data-ui="true"
    ></div>
  </div>

</template>

<style scoped>

</style>