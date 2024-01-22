<template>
  <div>
    <div
        style="height: 400px; width: 400px; position: relative"
        :data-ui="true"
        ref="viewerElement"
    ></div>
  </div>
</template>

<script>
/*global $3Dmol*/
export default {
  mounted() {
    this.loadMolecule();
  },
  methods: {
    loadMolecule() {
      const options = {
        ui: true,
      };
      const viewerElement = this.$refs.viewerElement;
      const viewer = $3Dmol.createViewer(viewerElement,options);

      $3Dmol.download("pdb:1BNA", viewer, {}, function() {
        viewer.setStyle({chain: 'A'}, {cartoon: {color: 'spectrum'}});
        viewer.setStyle({chain: 'B'}, {stick: {}});

        viewer.addSurface($3Dmol.SurfaceType.VDW, {opacity:0.7, color:'white'}, {chain: 'A'});

        viewer.render();
      });
    },
  },
};
</script>
