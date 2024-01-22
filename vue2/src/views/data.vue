<script>
import {defineComponent} from 'vue'
/* global $3Dmol*/
export default defineComponent({
  data() {
    return {
      opvalue:100,
      opvalue1:100,
      opvalue2:null,
      opvalue3:null,
      atomColors:{},
      threshold:[5,10,20,50,70,100,200,300,400,500,1000],
      bararray:[],
      hingearray:[],
      bararray_len:0,
      hingearray_len:0,
       isExpanded: false,
        isExpanded1: false,
      isExpanded2: false,
      isExpanded3: false,
      isExpanded4:false,
      isExpanded5: false,
      isExpanded6: false,
      isExpanded7:false,
      isExpanded8:false,
      isExpanded9:false,
      largestBodyID: 0,
      barsVisible:false,
      HingeVisible:false,
      partbarsVisible:false,
      partbarsVisible1:false,
      parthingesVisible:false,
      parthingesVisible1:false,
      surfacesVisible:false,
      atomVisable:false,
      bar_start: null,
      hinge_start:null,
      bar_end: null,
      hinge_end:null,
      bodyId1:null,
      bodyId2:null,
      hin_bodyId1:null,
      hin_bodyId2:null,
      surfacevalue:false,
      surfaceAtoms:[],
      atomvalue1:false,
      allbar_value: false,
      allhinge_value:false,
      partbar_value:false,
      parthinge_value:false,
      partbar_value1:false,
      parthinge_value1:false,
      selectedpointnum: 0,
      viewer: null,
      filename: null,
      selectedValue: 'stick',
      pdbfilename: null,
      showfilename: false,
      fileData: null,
      atomIds: null,
      pdbData: null,
      index: null,
      selectedpdbFile: null,
      selectedFile: null,
      bodyIDs: [],
      AllbodyID:[],
      inputValue: '',
      inputValue1:'',
      showinput: false,
      showload: false,
      flag_t1:false,
      flag_t2:false
    };
  },
  methods: {

    handleFileUpload(event) {
      this.selectedFile = event.target.files[0];
      const reader = new FileReader();

      reader.onload = () => {
        this.fileContent = reader.result;
        this.filename = this.selectedFile.name
      };

      if (this.selectedFile) {
        reader.readAsText(this.selectedFile);
      }
    },
    handlepdbFileUpload(event) {
      this.selectedpdbFile = event.target.files[0];
      const reader = new FileReader();
      reader.onload = () => {
        this.fileContent = reader.result;
        this.pdbfilename = this.selectedpdbFile.name
      };

      if (this.selectedpdbFile) {
        reader.readAsText(this.selectedpdbFile);
      }
    },
    downloadFile() {
      if (!this.fileContent) {
        alert('No file available for download.');
        return;
      }

      const blob = new Blob([this.fileContent], {type: "application/xml"});
      const fileURL = URL.createObjectURL(blob);

      // Create a temporary link and trigger the download
      const tempLink = document.createElement('a');
      tempLink.href = fileURL;
      tempLink.setAttribute('download', this.filename);
      tempLink.setAttribute('style', 'display:none;');
      document.body.appendChild(tempLink);
      tempLink.click();
      document.body.removeChild(tempLink);
    },
    async submitpdbForm() {
      if (this.selectedpdbFile) {
        const formData = new FormData();
        formData.append('file', this.selectedpdbFile, this.selectedpdbFile.name);
        const apiUrl = 'http://localhost:8082/uploadpdb';
        fetch(apiUrl, {
          method: 'POST',
          body: formData,
        }).then(response => response.json())
            .then(data => {
              this.pdbData = data.pdbData;
              this.showPdb(this.pdbData);

            })
            .catch(error => {
              console.error("Error uploading file:", error);
            });
      } else {
        alert("Please choose a PDB file!");
      }
    },
    toggleBars(newValue) {
      if(newValue===false)
      {
        this.allbar_value=false;
        this.allhinge_value=false;
        this.viewer.removeAllShapes();
        this.viewer.render();
      }
      console.log(2);
      this.partbar_value=false;
      this.partbar_value1=false;
      this.parthinge_value=false;
      this.parthinge_value1=false;
      this.atomvalue1=false;
      if(!this.HingeVisible)this.viewer.removeAllShapes();
      this.barsVisible=this.allbar_value;
      if (this.selectedValue === 'stick') this.viewer.setStyle({}, {stick: {hidden: false}});
      if (this.selectedValue === 'line') this.viewer.setStyle({}, {line: {hidden: false}});
      if (this.selectedValue === 'sphere') this.viewer.setStyle({}, {sphere: {hidden: false}});
      if (this.selectedValue === 'cross') this.viewer.setStyle({}, {cross: {hidden: false}});
      if (this.selectedValue === 'cartoon') this.viewer.setStyle({}, {cartoon: {hidden: false}});
      this.addbar();
      },
    toggleHinges(newValue)
    {
      if(newValue===false)
      {
        this.allhinge_value=false;
        this.allbar_value=false;
        this.viewer.removeAllShapes();
        this.viewer.render();
      }
      this.parthinge_value=false;
      this.parthinge_value1=false;
       this.partbar_value=false;
      this.partbar_value1=false;
      this.atomvalue1=false;
      this.viewer.removeAllShapes();
      this.HingeVisible=this.allhinge_value;
      if (this.selectedValue === 'stick') this.viewer.setStyle({}, {stick: {hidden: false}});
      if (this.selectedValue === 'line') this.viewer.setStyle({}, {line: {hidden: false}});
      if (this.selectedValue === 'sphere') this.viewer.setStyle({}, {sphere: {hidden: false}});
      if (this.selectedValue === 'cross') this.viewer.setStyle({}, {cross: {hidden: false}});
      if (this.selectedValue === 'cartoon') this.viewer.setStyle({}, {cartoon: {hidden: false}});
      this.addhinge();
    },
    addbar() {
      if (this.showinput) {
        this.bar_start = this.fileData.bardata_start;
        this.bar_end = this.fileData.bardata_end;
        this.bar_start = this.bar_start.map(num => parseInt(num, 10))
        this.bar_end = this.bar_end.map(num => parseInt(num, 10))
         const model = this.viewer.getModel(); // Get the current viewer model
         const atomList = model.selectedAtoms({});
         console.log(atomList)
        if(this.barsVisible) {
          for (let i = 0; i < this.bar_start.length; i++) {
            const startAtomIndex = this.bar_start[i];
            const endAtomIndex = this.bar_end[i];
            // 假设 atomList 是包含所有原子的数组
            const atom1 = atomList[startAtomIndex];
            const atom2 = atomList[endAtomIndex];
            if (!atom1 || !atom2) continue;
            const stickSpec = {
              start: atom1,
              end: atom2,
              radius: 0.2,
              color: 'lightgreen'
            };
            this.viewer.addCylinder(stickSpec);
          }
        }else {
          this.viewer.removeAllShapes();
        }
        this.viewer.render();
      }
    },
    addhinge()
    {
       if (this.showinput) {
        this.hinge_start = this.fileData.hingedata_start;
        this.hinge_end = this.fileData.hingedata_end;
        this.hinge_start = this.hinge_start.map(num => parseInt(num, 10))
        this.hinge_end = this.hinge_end.map(num => parseInt(num, 10))
         const model = this.viewer.getModel(); // Get the current viewer model
         const atomList = model.selectedAtoms({});
         console.log(atomList)
        if(this.HingeVisible) {
          for (let i = 0; i < this.hinge_start.length; i++) {
            const startAtomIndex = this.hinge_start[i];
            const endAtomIndex = this.hinge_end[i];
            // 假设 atomList 是包含所有原子的数组
            const atom1 = atomList[startAtomIndex];
            const atom2 = atomList[endAtomIndex];
            if (!atom1 || !atom2) continue;
            const stickSpec = {
              start: atom1,
              end: atom2,
              radius: 0.2,
              color: 'purple'
            };
            this.viewer.addCylinder(stickSpec);
          }
        }else {
          this.viewer.removeAllShapes();
        }
        this.viewer.render();
      }
    },
    produce_bararray() {

        this.bar_start = this.fileData.bardata_start;
        this.bar_end = this.fileData.bardata_end;
        this.bodyId1=this.fileData.bardata_body1;
        this.bodyId2=this.fileData.bardata_body2;
        this.bar_start = this.bar_start.map(num => parseInt(num, 10))
        this.bar_end = this.bar_end.map(num => parseInt(num, 10))
        this.bodyId1=this.bodyId1.map(num=>parseInt(num,10))
        this.bodyId2=this.bodyId2.map(num=>parseInt(num,10))
         const model = this.viewer.getModel(); // Get the current viewer model
         const atomList = model.selectedAtoms({});
         console.log(atomList)
          for (let i = 0; i < this.bar_start.length; i++) {
            const startAtomIndex = this.bar_start[i];
            const endAtomIndex = this.bar_end[i];
            const bodyid1=this.bodyId1[i];
            const bodyid2=this.bodyId2[i];
            // 假设 atomList 是包含所有原子的数组
            const atom1 = atomList[startAtomIndex];
            const atom2 = atomList[endAtomIndex];
            if (!atom1 || !atom2) continue;
            this.bararray_len=this.bararray_len+1;
            let bar_ele="#"+this.bararray_len+" -- "+"clusters:"+bodyid1 +","+bodyid2+"  atoms:"+startAtomIndex +","+endAtomIndex;
            this.bararray.push(bar_ele)

        }

    },
    produce_hingearray() {

        this.hinge_start = this.fileData.hingedata_start;

        this.hinge_end = this.fileData.hingedata_end;

        this.hin_bodyId1=this.fileData.hingedata_body1;

        this.hin_bodyId2=this.fileData.hingedata_body2;

        this.hinge_start = this.hinge_start.map(num => parseInt(num, 10))
        this.hinge_end = this.hinge_end.map(num => parseInt(num, 10))
        this.hin_bodyId1=this.hin_bodyId1.map(num=>parseInt(num,10))
        this.hin_bodyId2=this.hin_bodyId2.map(num=>parseInt(num,10))
         const model = this.viewer.getModel(); // Get the current viewer model
         const atomList = model.selectedAtoms({});
         console.log(atomList)
          for (let i = 0; i < this.hinge_start.length; i++) {
            const startAtomIndex = this.hinge_start[i];
            const endAtomIndex = this.hinge_end[i];
            const bodyid1=this.hin_bodyId1[i];
            const bodyid2=this.hin_bodyId2[i];
            // 假设 atomList 是包含所有原子的数组
            const atom1 = atomList[startAtomIndex];
            const atom2 = atomList[endAtomIndex];
            if (!atom1 || !atom2) continue;
            this.hingearray_len=this.hingearray_len+1;
            let bar_ele="#"+this.hingearray_len+" -- "+"bodies:"+bodyid1 +","+bodyid2+"  atoms:"+startAtomIndex +","+endAtomIndex;
            console.log(bar_ele)
            this.hingearray.push(bar_ele)

        }

    },
    toggle_partBars(newValue)
    {
      if(newValue===false)
      {
        this.partbar_value=false;
        this.parthinge_value=false;
        this.parthinge_value1=false;
        this.viewer.removeAllShapes();
        this.viewer.render();
      }

      this.allbar_value=false;
      this.partbar_value1=false;
     this.atomvalue1=false;
      this.viewer.removeAllShapes();
      this.partbarsVisible=this.partbar_value;
      if (this.selectedValue === 'stick') this.viewer.setStyle({}, {stick: {hidden: false}});
      if (this.selectedValue === 'line') this.viewer.setStyle({}, {line: {hidden: false}});
      if (this.selectedValue === 'sphere') this.viewer.setStyle({}, {sphere: {hidden: false}});
      if (this.selectedValue === 'cross') this.viewer.setStyle({}, {cross: {hidden: false}});
      if (this.selectedValue === 'cartoon') this.viewer.setStyle({}, {cartoon: {hidden: false}});
      this.addpartbar();
    },
    toggle_partHinges(newValue)
    {
      if(newValue===false)
      {
        this.parthinge_value=false;
        this.partbar_value=false;
        this.partbar_value1=false;
        this.viewer.removeAllShapes();
        this.viewer.render();
      }
      this.allhinge_value=false;
      this.parthinge_value1=false;
      this.atomvalue1=false;
      this.viewer.removeAllShapes();
      this.parthingesVisible=this.parthinge_value;

      if (this.selectedValue === 'stick') this.viewer.setStyle({}, {stick: {hidden: false}});
      if (this.selectedValue === 'line') this.viewer.setStyle({}, {line: {hidden: false}});
      if (this.selectedValue === 'sphere') this.viewer.setStyle({}, {sphere: {hidden: false}});
      if (this.selectedValue === 'cross') this.viewer.setStyle({}, {cross: {hidden: false}});
      if (this.selectedValue === 'cartoon') this.viewer.setStyle({}, {cartoon: {hidden: false}});
      this.addparthinge();
    },
    toggle_partHinges1(newValue)
    {
        if(newValue===false)
      {
        this.parthinge_value1=false;
        this.partbar_value1=false;
        this.partbar_value=false;
        this.viewer.removeAllShapes();
        this.viewer.render();

      }

      this.allhinge_value=false;
      this.parthinge_value=false;
      this.atomvalue1=false;
       this.viewer.removeAllShapes();
      this.parthingesVisible1=this.parthinge_value1;
      if (this.selectedValue === 'stick') this.viewer.setStyle({}, {stick: {hidden: false}});
      if (this.selectedValue === 'line') this.viewer.setStyle({}, {line: {hidden: false}});
      if (this.selectedValue === 'sphere') this.viewer.setStyle({}, {sphere: {hidden: false}});
      if (this.selectedValue === 'cross') this.viewer.setStyle({}, {cross: {hidden: false}});
      if (this.selectedValue === 'cartoon') this.viewer.setStyle({}, {cartoon: {hidden: false}});
      this.addparthinge1();
    },
    addpartbar()
    {
      if (this.showinput && this.surfacesVisible) { // 仅在显示输入且表面可见时执行操作
    this.bar_start = this.fileData.bardata_start;
    this.bar_end = this.fileData.bardata_end;
    this.bar_start = this.bar_start.map(num => parseInt(num, 10));
    this.bar_end = this.bar_end.map(num => parseInt(num, 10));
    const model = this.viewer.getModel(); // 获取当前查看器模型
    const atomList = model.selectedAtoms({});
    if (this.partbarsVisible) {
      for (let i = 0; i < this.bar_start.length; i++) {
        const startAtomIndex = this.bar_start[i];
        const endAtomIndex = this.bar_end[i];
        // 假设 atomList 包含所有原子的数组
        const atom1 = atomList[startAtomIndex];
        const atom2 = atomList[endAtomIndex];
        if (!atom1 || !atom2) continue;
        // 检查 atom1 和 atom2 是否在已经添加的表面中
        if (this.isAtomInSurface1(atom1)!==-1&&
            this.isAtomInSurface1(atom2)!==-1&&
            this.isAtomInSurface1(atom1)!==this.isAtomInSurface1(atom2)) {

            const stickSpec = {
              start: atom1,
              end: atom2,
              radius: 0.2,
              color: 'lightgreen'
            };
            this.viewer.addCylinder(stickSpec);
            console.log(atom1)
            console.log(atom2)

        }
      }
    } else {
      this.viewer.removeAllShapes();
    }
    this.viewer.render();
  }
    },
    addparthinge()
    {
      if (this.showinput && this.surfacesVisible)
      { // 仅在显示输入且表面可见时执行操作
        this.hinge_start = this.fileData.hingedata_start;
        this.hinge_end = this.fileData.hingedata_end;
        this.hinge_start = this.hinge_start.map(num => parseInt(num, 10))
        this.hinge_end = this.hinge_end.map(num => parseInt(num, 10))
        const model = this.viewer.getModel(); // 获取当前查看器模型
        const atomList = model.selectedAtoms({});
          if (this.parthingesVisible)
          {

            for (let i = 0; i < this.hinge_start.length; i++)
            {
              const startAtomIndex = this.hinge_start[i];
              const endAtomIndex = this.hinge_end[i];
        // 假设 atomList 包含所有原子的数组
              const atom1 = atomList[startAtomIndex];
              const atom2 = atomList[endAtomIndex];
              if (!atom1 || !atom2) continue;
        // 检查 atom1 和 atom2 是否在已经添加的表面中
              if (this.isAtomInSurface1(atom1)!==-1&&
            this.isAtomInSurface1(atom2)!==-1&&
            this.isAtomInSurface1(atom1)!==this.isAtomInSurface1(atom2) )
              {
                console.log(this.isAtomInSurface1(atom1))
                console.log(this.isAtomInSurface1(atom2))
                  const stickSpec = {
                  start: atom1,
                  end: atom2,
                  radius: 0.2,
                  color: 'purple'
                  };
                  this.viewer.addCylinder(stickSpec);

              }
      }
    } else {
      this.viewer.removeAllShapes();
    }
    this.viewer.render();
  }
    },
    toggle_partBars1(newValue)
    {
      if(newValue===false)
      {
        this.partbar_value1=false;
        this.parthinge_value1=false;
        this.parthinge_value=false;
        this.viewer.removeAllShapes();
        this.viewer.render();
      }

      this.allbar_value=false;
      this.partbar_value=false;
     this.atomvalue1=false;
       this.viewer.removeAllShapes();
      this.partbarsVisible1=this.partbar_value1;
      if (this.selectedValue === 'stick') this.viewer.setStyle({}, {stick: {hidden: false}});
      if (this.selectedValue === 'line') this.viewer.setStyle({}, {line: {hidden: false}});
      if (this.selectedValue === 'sphere') this.viewer.setStyle({}, {sphere: {hidden: false}});
      if (this.selectedValue === 'cross') this.viewer.setStyle({}, {cross: {hidden: false}});
      if (this.selectedValue === 'cartoon') this.viewer.setStyle({}, {cartoon: {hidden: false}});
      this.addpartbar1();
    },
     addpartbar1()
    {
      if (this.showinput && this.surfacesVisible) { // 仅在显示输入且表面可见时执行操作
    this.bar_start = this.fileData.bardata_start;
    this.bar_end = this.fileData.bardata_end;
    this.bar_start = this.bar_start.map(num => parseInt(num, 10));
    this.bar_end = this.bar_end.map(num => parseInt(num, 10));
    const model = this.viewer.getModel(); // 获取当前查看器模型
    const atomList = model.selectedAtoms({});
    if (this.partbarsVisible1) {
      for (let i = 0; i < this.bar_start.length; i++) {
        const startAtomIndex = this.bar_start[i];
        const endAtomIndex = this.bar_end[i];
        // 假设 atomList 包含所有原子的数组
        const atom1 = atomList[startAtomIndex];
        const atom2 = atomList[endAtomIndex];
        if (!atom1 || !atom2) continue;

        // 检查 atom1 和 atom2 是否在已经添加的表面中
        if ((this.isAtomInSurface(atom1) &&!this.isAtomInSurface(atom2))||
            (!this.isAtomInSurface(atom1) &&this.isAtomInSurface(atom2))) {

            const stickSpec = {
              start: atom1,
              end: atom2,
              radius: 0.2,
              color: 'lightgreen'
            };
            this.viewer.addCylinder(stickSpec);
            console.log(atom1)
            console.log(atom2)
            }
          }

      }
    } else {
      this.viewer.removeAllShapes();
    }
    this.viewer.render();
  },
    addparthinge1()
    {
       if (this.showinput && this.surfacesVisible) { // 仅在显示输入且表面可见时执行操作
        this.hinge_start = this.fileData.hingedata_start;
        this.hinge_end = this.fileData.hingedata_end;
        this.hinge_start = this.hinge_start.map(num => parseInt(num, 10))
        this.hinge_end = this.hinge_end.map(num => parseInt(num, 10))
    const model = this.viewer.getModel(); // 获取当前查看器模型
    const atomList = model.selectedAtoms({});
    if (this.parthingesVisible1) {
      for (let i = 0; i < this.hinge_start.length; i++) {
        const startAtomIndex = this.hinge_start[i];
        const endAtomIndex = this.hinge_end[i];
        // 假设 atomList 包含所有原子的数组
        const atom1 = atomList[startAtomIndex];
        const atom2 = atomList[endAtomIndex];
        if (!atom1 || !atom2) continue;

        // 检查 atom1 和 atom2 是否在已经添加的表面中
        if ((this.isAtomInSurface(atom1) &&!this.isAtomInSurface(atom2))||
            (!this.isAtomInSurface(atom1) &&this.isAtomInSurface(atom2))) {

            const stickSpec = {
              start: atom1,
              end: atom2,
              radius: 0.2,
              color: 'purple'
            };
            this.viewer.addCylinder(stickSpec);
            console.log(atom1)
            console.log(atom2)
            }
          }

      }
    } else {
      this.viewer.removeAllShapes();
    }
    this.viewer.render();
    },
    isAtomInSurface(atom) {
  if (this.surfaceAtoms) {
    const atomIndex = atom.index; // 原子的索引
    for (let j = 0; j < this.surfaceAtoms.length; j++) {
      for (let i = 0; i < this.surfaceAtoms[j].length; i++) {
        if (this.surfaceAtoms[j][i].toString() === atomIndex.toString())
        {
          return true; // 原子在表面中
        }
      }
    }
  }
  return false; // 原子不在表面中
},
    isAtomInSurface1(atom) {
  if (this.surfaceAtoms) {
    const atomIndex = atom.index; // 原子的索引
    for (let j = 0; j < this.surfaceAtoms.length; j++) {
      for (let i = 0; i < this.surfaceAtoms[j].length; i++) {
        if (this.surfaceAtoms[j][i].toString() === atomIndex.toString())
        {

          return j; // 原子在表面中
        }
      }
    }
    return -1;
  }
  return false; // 原子不在表面中
},
    add_single_bar()
    {
       this.viewer.removeAllShapes();
      const atomPattern = /atoms:(\d+),(\d+)/;
    const atomMatches = this.opvalue2.match(atomPattern);
    const atomindex1=parseInt(atomMatches[1]);
    const atomindex2=parseInt(atomMatches[2]);
    console.log(atomindex1);
    console.log(atomindex2)
    const model = this.viewer.getModel(); // Get the current viewer model
      const atomList = model.selectedAtoms({});
     const atom1 = atomList[atomindex1];
      const atom2 = atomList[atomindex2];
            const stickSpec = {
              start: atom1,
              end: atom2,
              radius: 0.2,
              color: 'lightgreen'
            };
            this.viewer.addCylinder(stickSpec);
             this.viewer.render();
    },
    add_single_hinge()
    {
      this.viewer.removeAllShapes();
      const atomPattern = /atoms:(\d+),(\d+)/;
    const atomMatches = this.opvalue3.match(atomPattern);
    const atomindex1=parseInt(atomMatches[1]);
    const atomindex2=parseInt(atomMatches[2]);
    console.log(atomindex1);
    console.log(atomindex2)
    const model = this.viewer.getModel(); // Get the current viewer model
      const atomList = model.selectedAtoms({});
     const atom1 = atomList[atomindex1];
      const atom2 = atomList[atomindex2];
            const stickSpec = {
              start: atom1,
              end: atom2,
              radius: 0.2,
              color: 'purple'
            };
            this.viewer.addCylinder(stickSpec);
             this.viewer.render();
    },
     toggleMenu() {
      this.isExpanded = !this.isExpanded;
    },
    toggleMenu1() {
      this.isExpanded1 = !this.isExpanded1;
    },
    toggleMenu2() {
      this.isExpanded2 = !this.isExpanded2;
    },
    toggleMenu3() {
      this.isExpanded3 = !this.isExpanded3;
    },
     toggleMenu4() {
      this.isExpanded4 = !this.isExpanded4;
    },
    toggleMenu5() {
      this.isExpanded5 = !this.isExpanded5;
    },
    toggleMenu6() {
      this.isExpanded6= !this.isExpanded6;
    },
    toggleMenu7() {
      this.isExpanded7= !this.isExpanded7;
    },
    toggleMenu8() {
      this.isExpanded8= !this.isExpanded8;
    },
     togglesurfaces() {
      this.viewer.removeAllSurfaces();
      this.viewer.render();
      this.addsurface();
    },

    togglepartatom_incluster()
    {
      if (this.selectedValue === 'stick') this.viewer.setStyle({}, {stick: {hidden: false}});
      if (this.selectedValue === 'line') this.viewer.setStyle({}, {line: {hidden: false}});
      if (this.selectedValue === 'sphere') this.viewer.setStyle({}, {sphere: {hidden: false}});
      if (this.selectedValue === 'cross') this.viewer.setStyle({}, {cross: {hidden: false}});
      if (this.selectedValue === 'cartoon') this.viewer.setStyle({}, {cartoon: {hidden: false}});
      this.viewer.render();
      this.showatomsincluster();

    },
    showatomsincluster()
    {
      if (this.showinput)
      {
         this.viewer.setStyle({}, {sphere: {hidden: true, radius: 1}});
        this.bodyIDs = this.inputValue1.split(',').map(item => parseInt(item.trim(), 10));
        console.log(this.bodyIDs);
        for (const bodyId of this.bodyIDs) {
          this.index = this.fileData.body_index
          this.atomIds = this.fileData.body[this.index[bodyId]]['point_ids']
          this.atomIds = this.atomIds.map(num => parseInt(num, 10))
          console.log(this.atomColors);
          const atomSelection = {serial: this.atomIds};
          const model = this.viewer.getModel(); // Get the current viewer model
          const selectedAtoms = model.selectedAtoms(atomSelection);
         for (let i = 0; i < selectedAtoms.length; i++) {
              // 将选定的原子设置为可见
              if (this.selectedValue === 'stick') this.viewer.setStyle({serial: selectedAtoms[i].serial}, {stick: {hidden: false}});
              if (this.selectedValue === 'line') this.viewer.setStyle({serial: selectedAtoms[i].serial}, {line: {hidden: false}});
              if (this.selectedValue === 'sphere') this.viewer.setStyle({serial: selectedAtoms[i].serial}, {sphere: {hidden: false}});
              if (this.selectedValue === 'cross') this.viewer.setStyle({serial: selectedAtoms[i].serial}, {cross: {hidden: false}});
              if (this.selectedValue === 'cartoon') this.viewer.setStyle({serial: selectedAtoms[i].serial}, {cartoon: {hidden: false}});
            }
        }
         this.viewer.render();
      }
    },
    addsurface()
    {
      if (this.showinput) {
        this.bodyIDs = this.inputValue.split(',').map(item => parseInt(item.trim(), 10));
        console.log(this.bodyIDs);
        this.surfaceAtoms=[];
        for (const bodyId of this.bodyIDs) {
          this.index = this.fileData.body_index
          this.atomIds = this.fileData.body[this.index[bodyId]]['point_ids']
          this.atomIds = this.atomIds.map(num => parseInt(num, 10))

          console.log(this.atomColors);
          this.viewer.setClickable({}, false);
          this.viewer.setClickable({serial: this.atomIds}, true);
          const atomSelection = {serial: this.atomIds};
          const model = this.viewer.getModel(); // Get the current viewer model
          const selectedAtoms = model.selectedAtoms(atomSelection);
          this.surfaceAtoms.push(this.atomIds);
          console.log(selectedAtoms)// Get the selected atoms with specified serial numbers
          if (!this.atomColors[bodyId]) {
          this.atomColors[bodyId] = "#" + ((Math.random() * 0xffffff) << 0).toString(16);
        }
          var randomRadius = Math.random() * (2 - 0.5) + 0.5;
          this.viewer.addSurface($3Dmol.SurfaceType.SAS, {opacity: 0.9, color: this.atomColors[bodyId],radius:randomRadius}, atomSelection);


        }
         this.viewer.render();
      }
    },
    toggleallsurfaces(newValue) {
      if(newValue===false)
      {
        this.surfacevalue=false;
      }
      this.surfacesVisible=this.surfacevalue;
      this.addallsurface();

    },
    Removeandtooglesurfaces(newValue)
    {
      this.viewer.removeAllSurfaces();
      this.viewer.render();
      if(newValue===false)
      {
        this.surfacevalue=false;
      }
      this.surfacesVisible=this.surfacevalue;
      this.addallsurface();
    },
      addallsurface() {
      if (this.showinput && this.surfacesVisible) {
         const model = this.viewer.getModel();
        console.log(this.AllbodyID)
        this.surfaceAtoms=[];
        for (const bodyId of this.AllbodyID) {
           this.index = this.fileData.body_index
          this.atomIds = this.fileData.body[this.index[bodyId]]['point_ids']
          this.atomIds = this.atomIds.map(num => parseInt(num, 10))

          // console.log(this.atomIds);
          const atomSelection = {serial: this.atomIds};

         // Get the current viewer model
          const selectedAtoms = model.selectedAtoms(atomSelection);
          // console.log(selectedAtoms)// Get the selected atoms with specified serial numbers
          if(selectedAtoms.length>this.opvalue) {
            this.surfaceAtoms.push(this.atomIds);
            if (!this.atomColors[bodyId]) {
          this.atomColors[bodyId] = "#" + ((Math.random() * 0xffffff) << 0).toString(16);
        }
            var randomRadius = Math.random() * (2 - 0.5) + 0.5;

            this.viewer.addSurface($3Dmol.SurfaceType.SAS, {
              opacity: 0.9,
              color: this.atomColors[bodyId],
              radius: randomRadius
            }, atomSelection);

          }
        }
        this.viewer.render();
      }
      else
      {
         this.viewer.removeAllSurfaces();
         this.viewer.render();
      }
    },
    togglepartatoms(newValue) {
      if(newValue===false)
      {
        this.atomvalue1=false;
      }
      this.allbar_value=false;
      this.viewer.removeAllShapes();
      this.atomVisable=this.atomvalue1;
      this.showpartatoms();

    },
    showpartatoms()
    {
// 隐藏所有的原子
      if(this.atomVisable) {
        this.viewer.setStyle({}, {sphere: {hidden: true, radius: 1}});
        var model = this.viewer.getModel()

        for (const bodyId of this.AllbodyID) {
          this.index = this.fileData.body_index;
          this.atomIds = this.fileData.body[this.index[bodyId]]['point_ids'];
          this.atomIds = this.atomIds.map(num => parseInt(num, 10));

          const atomSelection = {serial: this.atomIds};

          // Get the current viewer model
          const selectedAtoms = model.selectedAtoms(atomSelection);

          if (selectedAtoms.length > this.opvalue1) {
            for (let i = 0; i < selectedAtoms.length; i++) {
              // 将选定的原子设置为可见
              if (this.selectedValue === 'stick') this.viewer.setStyle({serial: selectedAtoms[i].serial}, {stick: {hidden: false}});
              if (this.selectedValue === 'line') this.viewer.setStyle({serial: selectedAtoms[i].serial}, {line: {hidden: false}});
              if (this.selectedValue === 'sphere') this.viewer.setStyle({serial: selectedAtoms[i].serial}, {sphere: {hidden: false}});
              if (this.selectedValue === 'cross') this.viewer.setStyle({serial: selectedAtoms[i].serial}, {cross: {hidden: false}});
              if (this.selectedValue === 'cartoon') this.viewer.setStyle({serial: selectedAtoms[i].serial}, {cartoon: {hidden: false}});

            }
          }
        }
        this.viewer.render();
      }
      else
      {
              if (this.selectedValue === 'stick') this.viewer.setStyle({}, {stick: {hidden: false}});
              if (this.selectedValue === 'line') this.viewer.setStyle({}, {line: {hidden: false}});
              if (this.selectedValue === 'sphere') this.viewer.setStyle({}, {sphere: {hidden: false}});
              if (this.selectedValue === 'cross') this.viewer.setStyle({}, {cross: {hidden: false}});
              if (this.selectedValue === 'cartoon') this.viewer.setStyle({}, {cartoon: {hidden: false}});
        this.viewer.render();

      }
    },
    // addbar() {
    //   if (this.showinput) {
    //     this.bar_start = this.fileData.bardata_start;
    //     this.bar_end = this.fileData.bardata_end;
    //     this.bar_start = this.bar_start.map(num => parseInt(num, 10))
    //     this.bar_end = this.bar_end.map(num => parseInt(num, 10))
    //      const model = this.viewer.getModel(); // Get the current viewer model
    //      const atomList = model.selectedAtoms({});
    //      console.log(atomList)
    //     if(this.barsVisible) {
    //       for (let i = 0; i < this.bar_start.length; i++) {
    //         const startAtomIndex = this.bar_start[i];
    //         const endAtomIndex = this.bar_end[i];
    //         // 假设 atomList 是包含所有原子的数组
    //         const atom1 = atomList[startAtomIndex];
    //         const atom2 = atomList[endAtomIndex];
    //         if (!atom1 || !atom2) continue;
    //         const stickSpec = {
    //           start: atom1,
    //           end: atom2,
    //           radius: 0.2,
    //           color: 'lightgreen'
    //         };
    //
    //         this.viewer.addCylinder(stickSpec);
    //       }
    //     }else {
    //       this.viewer.removeAllShapes();
    //     }
    //     this.viewer.render();
    //
    //   }
    // },
    showPdb(pdbData) {
      this.viewer = $3Dmol.createViewer(this.$refs.viewer, {backgroundColor: 'white'});
      try {
        this.viewer.addModel(pdbData, "pdb");
        if (this.selectedValue === 'stick') this.viewer.setStyle({}, {stick: {}});
        if (this.selectedValue === 'line') this.viewer.setStyle({}, {line: {}});
        if (this.selectedValue === 'sphere') this.viewer.setStyle({}, {sphere: {}});
        if (this.selectedValue === 'cross') this.viewer.setStyle({}, {cross: {}});
        if (this.selectedValue === 'cartoon') this.viewer.setStyle({}, {cartoon: {}});//sphere, stick, line, cross, cartoon,
        this.viewer.zoomTo();
        this.viewer.render();
        this.showload = true;
        this.allbar_value=false;
        this.partbar_value=false;
        this.partbar_value1=false;
        this.allhinge_value=false;
        this.parthinge_value=false;
        this.partbar_value1=false;
        this.surfacevalue=false;
      } catch (error) {
        console.error("Error rendering PDB data:", error);
      }
    },
    submitxmlForm() {
      const formData = new FormData();
      formData.append('file', this.selectedFile);

      // Change this URL to match your backend route
      const apiUrl = 'http://localhost:8082/upload';

      fetch(apiUrl, {
        method: 'POST',
        body: formData,
      })
          .then(response => response.json())
          .then(data => {
                this.fileData = data;

                this.showfilename = true;
                this.showinput = true
                for (let i = 0; i < this.fileData.body.length; i++) {
                  this.AllbodyID[i] = this.fileData.body[i]['body_id'];

                }
                console.log(this.fileData.body.length);
                this.produce_bararray();
                this.produce_hingearray();
              }
          )
          .catch(error => {
            console.error('Error uploading file:', error);
          });
    },
  }
})
</script>
<template>
  <div id="container">
    <div id="main-content">
      <h2 style="color: #3a8ee6;margin-bottom: 10px">Upload pdb file:</h2>
      <div>
        <form @submit.prevent="submitpdbForm">
          <input class="file-input" ref="fileInput1" type="file" @change="handlepdbFileUpload" accept=".pdb"/>
          <input type="button" class="selbtn" value="select file" @click="$refs.fileInput1.click()"/> {{
            selectedpdbFile ? selectedpdbFile.name : 'no file selected'
          }}
          <button type="submit" class="selbtn"  style="margin-left: 5px">upload</button>
        </form>

        <div ref="viewer" style="min-height: 400px;width: 400px; position: relative;margin-top: 10px"
             :data-ui="true"></div>
        <div v-if="showload">
          <select v-model="selectedValue" class="custom-select" style="margin-top: 10px">
            <option value="stick">stick</option>
            <option value="line">line</option>
            <option value="sphere">sphere</option>
            <option value="cross">cross</option>
            <option value="cartoon">cartoon</option>
          </select>
          <button class="sbtn" @click="showPdb(pdbData)" style="margin-top: 10px;margin-left: 5px">submit</button>
          <button class="restorebtn" @click="showPdb(pdbData)" style="margin-top: 10px;margin-left: 160px">Restore
          </button>
        </div>
          <div style="color: orange" v-if="fileData">Summary:</div>

        <table v-if="fileData" style="margin-top: 10px;margin-left: 70px; border-collapse: collapse;">
          <tr>
            <th style="padding-right: 200px;">Statistics</th>
            <th>Value</th>
          </tr>
          <tr>
            <td>Num of clusters:</td>
            <td>{{ fileData.content[0] }}</td>
          </tr>
          <tr>
            <td>ID of largest cluster:</td>
            <td>{{ fileData.largestbodyID }}</td>
          </tr>
          <tr>
            <td>Size of largest cluster:</td>
            <td>{{ fileData.largestbodysize }}</td>
          </tr>
          <tr>
            <td>Num of hinges:</td>
            <td>{{ fileData.content[3] }}</td>
          </tr>
          <tr>
            <td>Num of bars:</td>
            <td>{{ fileData.content[2] }}</td>
          </tr>
          <tr>
            <td>Num of atoms:</td>
            <td>{{ fileData.content[1] }}</td>
          </tr>
        </table>
      </div>
    </div>


    <div id="right-container">
      <h2 style="color: #3a8ee6;margin-bottom: 10px">Upload xml file:</h2>
      <div>
        <form @submit.prevent="submitxmlForm">
          <div class="file-input-wrapper">
            <input class="file-input" type="file" ref="fileInput" @change="handleFileUpload" id="fileInput"
                   accept=".xml"/>
            <input type="button" class="selbtn" value="select file" @click="$refs.fileInput.click()"/> {{
              selectedFile ? selectedFile.name : 'no file selected'
            }}
          </div>
          <button class="selbtn" type="submit" style="margin-left: 5px">upload</button>
          <div>
            <button class="dlbtn" @click="downloadFile" style="margin-top:8px">Download xml File</button>
          </div>
        </form>
        <!--       <div v-if="showfilename"><h3>{{filename}}:</h3></div>-->
        <!--       <div style="color:orange" v-if="fileData">Summary</div>-->
        <!--    <div style="margin-top: 10px" v-if="fileData">Num of clusters:{{fileData.content[0] }}&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;-->
        <!--      ID of largest cluster{{ fileData.content[1] }}&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Size of largest cluster:{{ fileData.content[2] }} </div>-->
        <!--&lt;!&ndash;    <div style="margin-top: 10px" v-if="fileData"> points</div>&ndash;&gt;-->
        <!--    <div style="margin-top: 10px" v-if="fileData">Num of hinges:{{fileData.content[3] }}&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;-->
        <!--      Num of bars:{{fileData.content[2] }}&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Num of atoms:{{fileData.content[1] }}</div>-->
        <div v-if="showfilename">
          <h3>{{ filename }}:</h3>
        </div>

     <div>
        <div v-if="showinput" @click="toggleMenu" class="expand-button" :data-text="isExpanded ? '-' : '+'" :data-expanded="isExpanded">Clusters</div>

       <div v-show="isExpanded" @click="toggleMenu1" class="expand-button3">{{ isExpanded1 ? '-' : '+' }} Atoms in clusters</div>
       <div v-show="isExpanded1&&isExpanded">
      <div v-if="showinput" style="margin-left: 15px">
         Show atoms only in cluster IDs(separated by ','):
        <input type="text" v-model="inputValue1" placeholder="Please enter body id"
               style="margin-top: 10px;margin-bottom: 10px;width: 23%">
        <button class="selbtn" @click="togglepartatom_incluster" style="margin-left: 5px">Show atoms</button>
        <div>Show/Hide atoms in cluster where atoms more than

            <el-select v-model="opvalue1" filterable placeholder="select" style="width: 100px">
              <el-option
                  v-for="item in threshold"
                  :key="item"
                  :label="item"
                  :value="item"
                  >
              </el-option>

            </el-select>
            <el-button @click="togglepartatoms" class="selbtn" style="margin-left: 5px">update</el-button>

          <div>
          <el-switch v-model="atomvalue1" active-color="#13ce66" inactive-color="#ff4949" @change="togglepartatoms"
                     style="margin-left: 5px"></el-switch>
          </div>
        </div>

      </div>

    </div>
     <div v-show="isExpanded" @click="toggleMenu2" class="expand-button3">{{ isExpanded2 ? '-' : '+' }} Surfaces</div>

    <div v-show="isExpanded2&&isExpanded">
      <div v-if="showinput" style="margin-left: 15px">
         Enter the IDs of clusters(separated by ','):
        <input type="text" v-model="inputValue" placeholder="Please enter body id"
               style="margin-top: 10px;margin-bottom: 10px">
        <button class="selbtn" @click="togglesurfaces" style="margin-left: 5px">Add surface</button>
        <div>Show/Hide surfaces with atomic numbers larger than

            <el-select v-model="opvalue" filterable placeholder="select" style="width: 100px">
              <el-option
                  v-for="item in threshold"
                  :key="item"
                  :label="item"
                  :value="item"
                  >
              </el-option>

            </el-select>
            <el-button @click="Removeandtooglesurfaces" class="selbtn" style="margin-left: 5px">update</el-button>

          <div>
          <el-switch v-model="surfacevalue" active-color="#13ce66" inactive-color="#ff4949" @change="toggleallsurfaces"
                     style="margin-left: 5px"></el-switch>
          </div>
        </div>

      </div>

    </div>
       <div v-if="showinput" @click="toggleMenu3" class="expand-button1" :data-text="isExpanded3 ? '-' : '+'" :data-expanded="isExpanded3">Bars</div>
       <div v-show="isExpanded3" @click="toggleMenu4" class="expand-button4">{{ isExpanded4 ? '-' : '+' }} single</div>
    <div v-show="isExpanded3&&isExpanded4">
     <div v-if="showinput" style="margin-left: 15px">Select bar by IDs:
         <el-select v-model="opvalue2" filterable placeholder="select" style="width: 250px;margin-top: 5px">
              <el-option
                  v-for="item in bararray"
                  :key="item"
                  :label="item"
                  :value="item"
                  >
              </el-option>

            </el-select>
            <el-button @click="add_single_bar" class="selbtn" style="margin-left: 5px">Add bar</el-button>
      </div>
      </div>
        <div v-show="isExpanded3" @click="toggleMenu5" class="expand-button4">{{ isExpanded5 ? '-' : '+' }}multiple</div>
       <div v-show="isExpanded3&&isExpanded5">
          <div v-if="showinput" style="margin-left: 15px">
        <div>Show/Hide all bars:
          <el-switch v-model="allbar_value" active-color="#13ce66" inactive-color="#ff4949" @change="toggleBars"
                     style="margin-left: 5px"></el-switch>
        </div>
        <div>Show/Hide only bars incident to highlighted clusters:
          <el-switch v-model="partbar_value" active-color="#13ce66" inactive-color="#ff4949" @change="toggle_partBars"
                     style="margin-left: 5px"></el-switch>
        </div>
        <div>Show/Hide only bars which span highlighted clusters:
          <el-switch v-model="partbar_value1" active-color="#13ce66" inactive-color="#ff4949" @change="toggle_partBars1"
                     style="margin-left: 5px"></el-switch>
        </div>
          </div>



    </div>
       <div v-if="showinput" @click="toggleMenu6" class="expand-button2" :data-text="isExpanded6 ? '-' : '+'" :data-expanded="isExpanded6"> Hinges</div>
    <div v-show="isExpanded6" @click="toggleMenu7" class="expand-button4">{{ isExpanded7 ? '-' : '+' }} single</div>
    <div v-show="isExpanded6&&isExpanded7">
     <div v-if="showinput" style="margin-left: 15px">Select hinge by IDs:
         <el-select v-model="opvalue3" filterable placeholder="select" style="width: 250px;margin-top: 5px">
              <el-option
                  v-for="item in hingearray"
                  :key="item"
                  :label="item"
                  :value="item"
                  >
              </el-option>

            </el-select>
            <el-button @click="add_single_hinge" class="selbtn" style="margin-left: 5px">Add hinge</el-button>
      </div>
      </div>
        <div v-show="isExpanded6" @click="toggleMenu8" class="expand-button4">{{ isExpanded8 ? '-' : '+' }}multiple</div>
       <div v-show="isExpanded6&&isExpanded8">
          <div v-if="showinput" style="margin-left: 15px">
        <div>Show/Hide all hinges:
          <el-switch v-model="allhinge_value" active-color="#13ce66" inactive-color="#ff4949" @change="toggleHinges"
                     style="margin-left: 5px">
          </el-switch>
        </div>
        <div>Show/Hide only hinges incident to highlighted clusters:
          <el-switch v-model="parthinge_value" active-color="#13ce66" inactive-color="#ff4949" @change="toggle_partHinges"
                     style="margin-left: 5px">
          </el-switch>
        </div>
        <div>Show/Hide only hinges which span highlighted clusters:
          <el-switch v-model="parthinge_value1" active-color="#13ce66" inactive-color="#ff4949" @change="toggle_partHinges1"
                     style="margin-left: 5px"></el-switch>
        </div>
          </div>



    </div>

  </div>

      </div>

    </div>
  </div>

</template>

<style scoped>
.psbtn {
  background: #349cd9;
  background-image: -webkit-linear-gradient(top, #349cd9, #2c33b8);
  background-image: -moz-linear-gradient(top, #349cd9, #2c33b8);
  background-image: -ms-linear-gradient(top, #349cd9, #2c33b8);
  background-image: -o-linear-gradient(top, #349cd9, #2c33b8);
  background-image: linear-gradient(to bottom, #349cd9, #2c33b8);
  -webkit-border-radius: 2;
  border: solid #204a8a 2px;
  -moz-border-radius: 2;
  border-radius: 2px;
  text-shadow: 0px 1px 3px #666666;
  -webkit-box-shadow: 0px 1px 3px #666666;
  -moz-box-shadow: 0px 1px 3px #666666;
  box-shadow: 0px 1px 3px #666666;
  font-family: Arial;
  color: #ffffff;
  font-size: 1px;
  padding: 5px 5px 5px 5px;
  text-decoration: none;
  border: none;
}

.psbtn:hover {
  background: #3cb0fd;
  background-image: -webkit-linear-gradient(top, #3cb0fd, #3498db);
  background-image: -moz-linear-gradient(top, #3cb0fd, #3498db);
  background-image: -ms-linear-gradient(top, #3cb0fd, #3498db);
  background-image: -o-linear-gradient(top, #3cb0fd, #3498db);
  background-image: linear-gradient(to bottom, #3cb0fd, #3498db);
  text-decoration: none;
}

.selbtn {
  background: #3498db;
  background-image: -webkit-linear-gradient(top, #3498db, #2980b9);
  background-image: -moz-linear-gradient(top, #3498db, #2980b9);
  background-image: -ms-linear-gradient(top, #3498db, #2980b9);
  background-image: -o-linear-gradient(top, #3498db, #2980b9);
  background-image: linear-gradient(to bottom, #3498db, #2980b9);
  -webkit-border-radius: 4;
  -moz-border-radius: 4;
  border-radius: 4px;
  font-family: Arial;
  color: #ffffff;
  font-size: 12px;
  padding: 8px 8px 8px 10px;
  text-decoration: none;
  border:none;
}

.selbtn:hover {
   background: #3cb0fd;
  background-image: -webkit-linear-gradient(top, #3cb0fd, #3498db);
  background-image: -moz-linear-gradient(top, #3cb0fd, #3498db);
  background-image: -ms-linear-gradient(top, #3cb0fd, #3498db);
  background-image: -o-linear-gradient(top, #3cb0fd, #3498db);
  background-image: linear-gradient(to bottom, #3cb0fd, #3498db);
  text-decoration: none;
  border:none;
}

.dlbtn {
  background: #34d9b2;
  background-image: -webkit-linear-gradient(top, #34d9b2, #a02bb8);
  background-image: -moz-linear-gradient(top, #34d9b2, #a02bb8);
  background-image: -ms-linear-gradient(top, #34d9b2, #a02bb8);
  background-image: -o-linear-gradient(top, #34d9b2, #a02bb8);
  background-image: linear-gradient(to bottom, #34d9b2, #a02bb8);
  -webkit-border-radius: 28;
  -moz-border-radius: 28;
  border-radius: 28px;
  border: solid #218a54 2px;
  text-shadow: 0px 1px 3px #666666;
  font-family: Arial;
  color: #ffffff;
  font-size:12px;
  padding: 10px 20px 10px 20px;
  text-decoration: none;
  border: none;
}

.sbtn {
  background: #d97034;
  background-image: -webkit-linear-gradient(top, #d97034, #b8632b);
  background-image: -moz-linear-gradient(top, #d97034, #b8632b);
  background-image: -ms-linear-gradient(top, #d97034, #b8632b);
  background-image: -o-linear-gradient(top, #d97034, #b8632b);
  background-image: linear-gradient(to bottom, #d97034, #b8632b);
  -webkit-border-radius: 0;
  -moz-border-radius: 0;
  border-radius: 0px;
  font-family: Arial;
  color: #ffffff;
  font-size: 18px;
  padding: 6px 6px 6px 6px;
  text-decoration: none;
  border: none;
}

.sbtn:hover {
  background: #3cb0fd;
  background-image: -webkit-linear-gradient(top, #3cb0fd, #3498db);
  background-image: -moz-linear-gradient(top, #3cb0fd, #3498db);
  background-image: -ms-linear-gradient(top, #3cb0fd, #3498db);
  background-image: -o-linear-gradient(top, #3cb0fd, #3498db);
  background-image: linear-gradient(to bottom, #3cb0fd, #3498db);
  text-decoration: none;
}

.dlbtn:hover {
  background: #3cb0fd;
  background-image: -webkit-linear-gradient(top, #3cb0fd, #3498db);
  background-image: -moz-linear-gradient(top, #3cb0fd, #3498db);
  background-image: -ms-linear-gradient(top, #3cb0fd, #3498db);
  background-image: -o-linear-gradient(top, #3cb0fd, #3498db);
  background-image: linear-gradient(to bottom, #3cb0fd, #3498db);
  text-decoration: none;
}

.restorebtn {
  background: #34d9aa;
  background-image: -webkit-linear-gradient(top, #34d9aa, #2980b9);
  background-image: -moz-linear-gradient(top, #34d9aa, #2980b9);
  background-image: -ms-linear-gradient(top, #34d9aa, #2980b9);
  background-image: -o-linear-gradient(top, #34d9aa, #2980b9);
  background-image: linear-gradient(to bottom, #34d9aa, #2980b9);
  -webkit-border-radius: 21;
  -moz-border-radius: 21;
  border-radius: 21px;
  font-family: Arial;
  border: solid #1f8c7a 2px;
  color: #ffffff;
  font-size: 14px;
  padding: 10px 20px 10px 20px;
  text-decoration: none;
  border: none;
}

.restorebtn:hover {
  background: #6cfc3c;
  background-image: -webkit-linear-gradient(top, #6cfc3c, #34d994);
  background-image: -moz-linear-gradient(top, #6cfc3c, #34d994);
  background-image: -ms-linear-gradient(top, #6cfc3c, #34d994);
  background-image: -o-linear-gradient(top, #6cfc3c, #34d994);
  background-image: linear-gradient(to bottom, #6cfc3c, #34d994);
  text-decoration: none;
}

.custom-select {
  margin-top: 10px;
  padding: 5px;
  font-size: 16px;
  border: 2px solid #ccc;
  /* 添加其他样式规则 */
}

.smbtn {
  background: #34d9b2;
  background-image: -webkit-linear-gradient(top, #34d9b2, #7bb82c);
  background-image: -moz-linear-gradient(top, #34d9b2, #7bb82c);
  background-image: -ms-linear-gradient(top, #34d9b2, #7bb82c);
  background-image: -o-linear-gradient(top, #34d9b2, #7bb82c);
  background-image: linear-gradient(to bottom, #34d9b2, #7bb82c);
  -webkit-border-radius: 28;
  -moz-border-radius: 28;
  border-radius: 28px;
  text-shadow: 0px 1px 3px #666666;
  font-family: Arial;
  color: #ffffff;
  font-size: 8px;
  padding: 10px 20px 10px 20px;
  text-decoration: none;
}

.smbtn:hover {
  background: #3cb0fd;
  background-image: -webkit-linear-gradient(top, #3cb0fd, #3498db);
  background-image: -moz-linear-gradient(top, #3cb0fd, #3498db);
  background-image: -ms-linear-gradient(top, #3cb0fd, #3498db);
  background-image: -o-linear-gradient(top, #3cb0fd, #3498db);
  background-image: linear-gradient(to bottom, #3cb0fd, #3498db);
  text-decoration: none;
}

.rebtn {
  background: #3439d9;
  background-image: -webkit-linear-gradient(top, #3439d9, #2b92b8);
  background-image: -moz-linear-gradient(top, #3439d9, #2b92b8);
  background-image: -ms-linear-gradient(top, #3439d9, #2b92b8);
  background-image: -o-linear-gradient(top, #3439d9, #2b92b8);
  background-image: linear-gradient(to bottom, #3439d9, #2b92b8);
  -webkit-border-radius: 28;
  -moz-border-radius: 28;
  border-radius: 28px;
  font-family: Arial;
  border: solid #21648a 2px;
  color: #ffffff;
  font-size: 14px;
  padding: 10px 20px 10px 20px;
  text-decoration: none;
  border: none;
}

.rebtn:hover {
  background: #b63cfc;
  background-image: -webkit-linear-gradient(top, #b63cfc, #3473d9);
  background-image: -moz-linear-gradient(top, #b63cfc, #3473d9);
  background-image: -ms-linear-gradient(top, #b63cfc, #3473d9);
  background-image: -o-linear-gradient(top, #b63cfc, #3473d9);
  background-image: linear-gradient(to bottom, #b63cfc, #3473d9);
  text-decoration: none;
}

#container {
  display: flex;
}

#main-content {
  flex: 1;
}

#right-container {
  width: 50%;
}

.file-input-wrapper {
  display: inline-block;
  position: relative;
}

.file-input {
  display: none;
}

input[type='button'] {
  /* Add your custom styles for the button here */
}
.expand-button {
  background-color: green; /* 设置背景颜色 */
  color: #fff; /* 设置文字颜色 */
  border: none;
  cursor: pointer;
  outline: none;
  font-size: 18px; /* 增大字体大小 */
  padding: 10px 20px; /* 增加内边距，使按钮更大 */
  margin-right: 10px;
  margin-top: 10px;
  border-radius: 5px; /* 添加圆角边框 */
  transition: background-color 0.3s ease; /* 添加渐变动画效果 */
}

/* 鼠标悬停时的样式 */
.expand-button:hover {
  background-color: lightgreen; /* 悬停时的背景颜色 */
}

/* 展开按钮的 "-" 和 "+" 样式 */
.expand-button::before {
  content: attr(data-text); /* 使用data-text属性作为内容，根据isExpanded显示"+"或"-" */
  font-weight: bold;
  margin-right: 10px;
}

/* 如果按钮已展开，更改内容显示 "-" */
.expand-button[data-expanded="true"]::before {
  content: "-";
}
.expand-button1 {
  background-color: blue; /* 设置背景颜色 */
  color: #fff; /* 设置文字颜色 */
  border: none;
  cursor: pointer;
  outline: none;
  font-size: 18px; /* 增大字体大小 */
  padding: 10px 20px; /* 增加内边距，使按钮更大 */
  margin-right: 10px;
  margin-top: 10px;
  border-radius: 5px; /* 添加圆角边框 */
  transition: background-color 0.3s ease; /* 添加渐变动画效果 */
}

/* 鼠标悬停时的样式 */
.expand-button1:hover {
  background-color: cornflowerblue; /* 悬停时的背景颜色 */
}

/* 展开按钮的 "-" 和 "+" 样式 */
.expand-button1::before {
  content: attr(data-text); /* 使用data-text属性作为内容，根据isExpanded显示"+"或"-" */
  font-weight: bold;
  margin-right: 10px;
}

/* 如果按钮已展开，更改内容显示 "-" */
.expand-button1[data-expanded="true"]::before {
  content: "-";
}

.expand-button2 {
  background-color: orange; /* 设置背景颜色 */
  color: #fff; /* 设置文字颜色 */
  border: none;
  cursor: pointer;
  outline: none;
  font-size: 18px; /* 增大字体大小 */
  padding: 10px 20px; /* 增加内边距，使按钮更大 */
  margin-right: 10px;
  margin-top: 10px;
  border-radius: 5px; /* 添加圆角边框 */
  transition: background-color 0.3s ease; /* 添加渐变动画效果 */
}

/* 鼠标悬停时的样式 */
.expand-button2:hover {
  background-color: coral; /* 悬停时的背景颜色 */
}

/* 展开按钮的 "-" 和 "+" 样式 */
.expand-button2::before {
  content: attr(data-text); /* 使用data-text属性作为内容，根据isExpanded显示"+"或"-" */
  font-weight: bold;
  margin-right: 10px;
}

/* 如果按钮已展开，更改内容显示 "-" */
.expand-button2[data-expanded="true"]::before {
  content: "-";
}

.expand-button3 {
  background-color: darkseagreen; /* 设置背景颜色 */
  color: #fff; /* 设置文字颜色 */
  border: none;
  cursor: pointer;
  outline: none;
  font-size: 14px; /* 增大字体大小 */
  padding: 5px 7px; /* 增加内边距，使按钮更大 */
  margin-left: 15px;
  margin-top: 10px;
  border-radius: 5px; /* 添加圆角边框 */
  width:50%;
  transition: background-color 0.3s ease; /* 添加渐变动画效果 */
}

/* 鼠标悬停时的样式 */
.expand-button3:hover {
  background-color: lightseagreen; /* 悬停时的背景颜色 */
}

/* 展开按钮的 "-" 和 "+" 样式 */
.expand-button3::before {
  content: attr(data-text); /* 使用data-text属性作为内容，根据isExpanded显示"+"或"-" */
  font-weight: bold;
  margin-right: 10px;
}

/* 如果按钮已展开，更改内容显示 "-" */
.expand-button3[data-expanded="true"]::before {
  content: "-";
}
.expand-button4{
  background-color:cornflowerblue; /* 设置背景颜色 */
  color: #fff; /* 设置文字颜色 */
  border: none;
  cursor: pointer;
  outline: none;
  font-size: 14px; /* 增大字体大小 */
  padding: 5px 7px; /* 增加内边距，使按钮更大 */
  margin-left: 15px;
  margin-top: 10px;
  border-radius: 5px; /* 添加圆角边框 */
  width:50%;
  transition: background-color 0.3s ease; /* 添加渐变动画效果 */
}

/* 鼠标悬停时的样式 */
.expand-button4:hover {
  background-color:deepskyblue; /* 悬停时的背景颜色 */
}

/* 展开按钮的 "-" 和 "+" 样式 */
.expand-button4::before {
  content: attr(data-text); /* 使用data-text属性作为内容，根据isExpanded显示"+"或"-" */
  font-weight: bold;
  margin-right: 10px;
}

/* 如果按钮已展开，更改内容显示 "-" */
.expand-button4[data-expanded="true"]::before {
  content: "-";
}
/*.custom-select  {
  width: 100px !important; !* 调整为您希望的宽度 *!
}*/
</style>


<!--<script>-->
<!--import {defineComponent} from 'vue'-->

<!--/* global $3Dmol*/-->
<!--export default defineComponent({-->
<!-- data() {-->
<!--    return {-->
<!--      viewer:null,-->
<!--      filename:null,-->
<!--      pdbfilename:null,-->
<!--      showfilename:false,-->
<!--      fileData: null,-->
<!--      atomIds:null,-->
<!--      pdbData:null,-->
<!--      index:null,-->
<!--      selectedpdbFile:null,-->
<!--      selectedFile: null,-->
<!--      bodyId: 0,-->
<!--      inputValue: '',-->
<!--      showinput:false,-->
<!--      showload:false-->
<!--    };-->
<!--  },-->
<!--  methods: {-->
<!--    handleFileUpload(event) {-->
<!--      this.selectedFile = event.target.files[0];-->
<!--      const reader = new FileReader();-->

<!--      reader.onload = () => {-->
<!--        this.fileContent = reader.result;-->
<!--        this.filename=this.selectedFile.name-->
<!--      };-->

<!--      if (this.selectedFile) {-->
<!--        reader.readAsText(this.selectedFile);-->

<!--      }-->
<!--    },-->
<!--     handlepdbFileUpload(event) {-->
<!--      this.selectedpdbFile = event.target.files[0];-->
<!--      const reader = new FileReader();-->

<!--      reader.onload = () => {-->
<!--        this.fileContent = reader.result;-->
<!--        this.pdbfilename=this.selectedpdbFile.name-->
<!--      };-->

<!--      if (this.selectedpdbFile) {-->
<!--        reader.readAsText(this.selectedpdbFile);-->

<!--      }-->
<!--    },-->
<!--    downloadFile() {-->
<!--       if (!this.fileContent) {-->
<!--      alert('No file available for download.');-->
<!--      return;-->
<!--    }-->

<!--    const blob = new Blob([this.fileContent], { type: "application/xml" });-->
<!--    const fileURL = URL.createObjectURL(blob);-->
<!--    // Create a temporary link and trigger the download-->
<!--    const tempLink = document.createElement('a');-->
<!--    tempLink.href = fileURL;-->
<!--    tempLink.setAttribute('download',this.filename );-->
<!--    tempLink.setAttribute('style', 'display:none;');-->
<!--    document.body.appendChild(tempLink);-->
<!--    tempLink.click();-->
<!--    document.body.removeChild(tempLink);-->
<!--    },-->
<!--     async submitpdbForm() {-->
<!--      if (this.selectedpdbFile) {-->
<!--        const formData = new FormData();-->
<!--        formData.append('file', this.selectedpdbFile, this.selectedpdbFile.name);-->
<!--        const apiUrl = 'http://localhost:8082/uploadpdb';-->
<!--        fetch(apiUrl, {-->
<!--        method: 'POST',-->
<!--        body: formData,-->
<!--      })-->
<!--      .then(response => response.json())-->
<!--      .then(data => {-->
<!--        this.pdbData = data.pdbData;-->
<!--        this.showPdb(this.pdbData);-->
<!--      })-->
<!--      .catch(error => {-->
<!--        console.error("Error uploading file:", error);-->
<!--      });-->
<!--      } else {-->
<!--        alert("Please choose a PDB file!");-->
<!--      }-->
<!--    },-->
<!--  //   addsurface()-->
<!--  //   {-->
<!--  //     if(this.showinput) {-->
<!--  //       this.index = this.fileData.body_index-->
<!--  //       this.atomIds = this.fileData.body[this.index[this.bodyId]]['point_ids']-->
<!--  //-->
<!--  //       this.atomIds = this.atomIds.map(num => parseInt(num, 10))-->
<!--  //       console.log(this.atomIds);-->
<!--  //        const atomSelection = { serial: this.atomIds };-->
<!--  //          const model = this.viewer.getModel(); // Get the current viewer model-->
<!--  //          const selectedAtoms = model.selectedAtoms(atomSelection); // Get the selected atoms with specified serial numbers-->
<!--  //          for (const atom of selectedAtoms) {-->
<!--  //   atom.clickable = true;-->
<!--  //   atom.callback = function (pickedAtom) {-->
<!--  //     console.log(pickedAtom); // Output atom information-->
<!--  //     // Perform further actions based on atom properties, e.g., change style, display popup, etc.-->
<!--  //   };-->
<!--  //   // Add a red dot to the atom-->
<!--  //   this.viewer.addStyle(atom, {-->
<!--  //     sphere: {-->
<!--  //       radius: 5, // Set the radius of the sphere based on desired dot size-->
<!--  //       color: "yellow",-->
<!--  //     }-->
<!--  //   });-->
<!--  // }-->
<!--  //       this.viewer.addSurface($3Dmol.SurfaceType.SAS, { opacity: 0.9, color: "lightblue" }, atomSelection);-->
<!--  //     }-->
<!--  //     this.viewer.render();-->
<!--  //   },-->
<!--     showPdb(pdbData)-->
<!--    {-->
<!--      this.viewer=$3Dmol.createViewer(this.$refs.viewer,{ backgroundColor: 'black' });-->
<!--      try {-->
<!--        this.viewer.addModel(pdbData, "pdb");-->
<!--        this.viewer.setStyle({}, { line: {} });-->
<!--        this.viewer.zoomTo();-->
<!--         if(this.showinput) {-->
<!--        this.index = this.fileData.body_index-->
<!--        this.atomIds = this.fileData.body[this.index[this.bodyId]]['point_ids']-->

<!--        this.atomIds = this.atomIds.map(num => parseInt(num, 10))-->
<!--        console.log(this.atomIds);-->
<!--         const atomSelection = { serial: this.atomIds };-->
<!--           const model = this.viewer.getModel(); // Get the current viewer model-->
<!--           const selectedAtoms = model.selectedAtoms(atomSelection); // Get the selected atoms with specified serial numbers-->
<!--           for (const atom of selectedAtoms) {-->
<!--    atom.clickable = true;-->
<!--    atom.callback = function (pickedAtom) {-->
<!--      console.log(pickedAtom); // Output atom information-->
<!--      // Perform further actions based on atom properties, e.g., change style, display popup, etc.-->
<!--    };-->
<!--    // Add a red dot to the atom-->
<!--    this.viewer.addStyle(atom, {-->
<!--      sphere: {-->
<!--        radius: 5, // Set the radius of the sphere based on desired dot size-->
<!--        color: "yellow",-->
<!--      }-->
<!--    });-->
<!--  }-->
<!--        this.viewer.addSurface($3Dmol.SurfaceType.SAS, { opacity: 0.9, color: "lightblue" }, atomSelection);-->
<!--      }-->
<!--      this.viewer.render();-->
<!--        this.showload=true;-->
<!--      } catch (error) {-->
<!--        console.error("Error rendering PDB data:", error);-->
<!--      }-->
<!--    },-->
<!--    updateBodyId() {-->
<!--        this.bodyId = this.inputValue;-->
<!--        alert("Sumit successfully!Please press 'reload' button!")-->

<!--      },-->

<!--    submitxmlForm() {-->
<!--      const formData = new FormData();-->
<!--      formData.append('file', this.selectedFile);-->

<!--      // Change this URL to match your backend route-->
<!--      const apiUrl = 'http://localhost:8082/upload';-->

<!--      fetch(apiUrl, {-->
<!--        method: 'POST',-->
<!--        body: formData,-->
<!--      })-->
<!--      .then(response => response.json())-->
<!--      .then(data => {-->
<!--        this.fileData = data;-->
<!--        this.showfilename=true;-->
<!--        this.showinput=true-->
<!--      })-->
<!--      .catch(error => {-->
<!--        console.error('Error uploading file:', error);-->
<!--      });-->
<!--    },-->
<!--  }-->
<!--})-->
<!--</script>-->
<!--<template>-->


<!--  <div id="container">-->
<!--  <div id="main-content">-->
<!--    <h2 style="color: #3a8ee6;margin-bottom: 10px">Parse pdb file:</h2>-->
<!--  <div>-->
<!--    <form @submit.prevent="submitpdbForm">-->
<!--      <input class="file-input"  ref="fileInput1" type="file" @change="handlepdbFileUpload" accept=".pdb" />-->
<!--      <input type="button" class="selbtn" value="select file" @click="$refs.fileInput1.click()" /> {{-->
<!--        selectedpdbFile ? selectedpdbFile.name : 'no file selected'-->
<!--      }}-->
<!--      <button type="submit" class="psbtn" style="margin-left: 5px">parse</button>-->
<!--    </form>-->

<!--    <div ref="viewer" style="min-height: 400px;width: 400px; position: relative;margin-top: 10px" :data-ui="true"></div>-->
<!--    <div v-if="showload">-->
<!--      <button class="rebtn" @click="showPdb(pdbData)" style="margin-top: 10px">Reload</button>-->
<!--&lt;!&ndash;      <button class="rebtn" @click="showPdb(pdbData)" style="margin-top: 10px">Restore</button>&ndash;&gt;-->
<!--    </div>-->
<!--    <div v-if="showinput">-->
<!--    <input type="text" v-model="inputValue" placeholder="Please enter body id" style="margin-top: 10px;margin-bottom: 10px">-->
<!--    <button class="psbtn" @click="updateBodyId" style="margin-left: 5px">submit</button>-->


<!--  </div>-->
<!--  </div>-->
<!--  </div>-->


<!--  <div id="right-container">-->
<!--    <h2 style="color: #3a8ee6;margin-bottom: 10px">Parse xml file:</h2>-->
<!--     <div>-->
<!--    <form @submit.prevent="submitxmlForm">-->
<!--    <div class="file-input-wrapper">-->
<!--      <input class="file-input" type="file" ref="fileInput" @change="handleFileUpload" id="fileInput" accept=".xml" />-->
<!--      <input type="button" class="selbtn" value="select file" @click="$refs.fileInput.click()" /> {{-->
<!--        selectedFile ? selectedFile.name : 'no file selected'-->
<!--      }}-->
<!--    </div>-->
<!--    <button class="psbtn" type="submit" style="margin-left: 5px">parse</button>-->
<!--     <div> <button class="dlbtn" @click="downloadFile" style="margin-top:8px">Download xml File</button></div>-->
<!--    </form>-->
<!--       <div v-if="showfilename"><h3>{{filename}}:</h3></div>-->
<!--    <div style="margin-top: 10px" v-if="fileData">The protein contains {{ fileData.content[0] }} bodies</div>-->
<!--    <div style="margin-top: 10px" v-if="fileData">The protein contains {{ fileData.content[1] }} points</div>-->
<!--    <div style="margin-top: 10px" v-if="fileData">The protein contains {{ fileData.content[2] }} bars</div>-->
<!--    <div style="margin-top: 10px" v-if="fileData">The protein contains {{ fileData.content[3] }} hinges</div>-->
<!--  </div>-->

<!--  </div>-->
<!--</div>-->

<!--</template>-->

<!--<style scoped>-->
<!--.psbtn {-->
<!--  background: #349cd9;-->
<!--  background-image: -webkit-linear-gradient(top, #349cd9, #2c33b8);-->
<!--  background-image: -moz-linear-gradient(top, #349cd9, #2c33b8);-->
<!--  background-image: -ms-linear-gradient(top, #349cd9, #2c33b8);-->
<!--  background-image: -o-linear-gradient(top, #349cd9, #2c33b8);-->
<!--  background-image: linear-gradient(to bottom, #349cd9, #2c33b8);-->
<!--  -webkit-border-radius: 2;-->
<!--  -moz-border-radius: 2;-->
<!--  border-radius: 2px;-->
<!--  text-shadow: 0px 1px 3px #666666;-->
<!--  -webkit-box-shadow: 0px 1px 3px #666666;-->
<!--  -moz-box-shadow: 0px 1px 3px #666666;-->
<!--  box-shadow: 0px 1px 3px #666666;-->
<!--  font-family: Arial;-->
<!--  color: #ffffff;-->
<!--  font-size: 1px;-->
<!--  padding: 5px 5px 5px 5px;-->
<!--  text-decoration: none;-->
<!--}-->

<!--.psbtn:hover {-->
<!--  background: #3cb0fd;-->
<!--  background-image: -webkit-linear-gradient(top, #3cb0fd, #3498db);-->
<!--  background-image: -moz-linear-gradient(top, #3cb0fd, #3498db);-->
<!--  background-image: -ms-linear-gradient(top, #3cb0fd, #3498db);-->
<!--  background-image: -o-linear-gradient(top, #3cb0fd, #3498db);-->
<!--  background-image: linear-gradient(to bottom, #3cb0fd, #3498db);-->
<!--  text-decoration: none;-->
<!--}-->
<!--.selbtn {-->
<!--  background: #349cd9;-->
<!--  background-image: -webkit-linear-gradient(top, #349cd9, #2c33b8);-->
<!--  background-image: -moz-linear-gradient(top, #349cd9, #2c33b8);-->
<!--  background-image: -ms-linear-gradient(top, #349cd9, #2c33b8);-->
<!--  background-image: -o-linear-gradient(top, #349cd9, #2c33b8);-->
<!--  background-image: linear-gradient(to bottom, #349cd9, #2c33b8);-->
<!--  -webkit-border-radius: 2;-->
<!--  -moz-border-radius: 2;-->
<!--  border-radius: 2px;-->
<!--  text-shadow: 0px 1px 3px #666666;-->
<!--  -webkit-box-shadow: 0px 1px 3px #666666;-->
<!--  -moz-box-shadow: 0px 1px 3px #666666;-->
<!--  box-shadow: 0px 1px 3px #666666;-->
<!--  font-family: Arial;-->
<!--  color: #ffffff;-->
<!--  font-size: 1px;-->
<!--  padding: 5px 5px 5px 5px;-->
<!--  text-decoration: none;-->
<!--}-->

<!--.selbtn:hover {-->
<!--  background: #3cb0fd;-->
<!--  background-image: -webkit-linear-gradient(top, #3cb0fd, #3498db);-->
<!--  background-image: -moz-linear-gradient(top, #3cb0fd, #3498db);-->
<!--  background-image: -ms-linear-gradient(top, #3cb0fd, #3498db);-->
<!--  background-image: -o-linear-gradient(top, #3cb0fd, #3498db);-->
<!--  background-image: linear-gradient(to bottom, #3cb0fd, #3498db);-->
<!--  text-decoration: none;-->
<!--}-->
<!--.dlbtn {-->
<!--  background: #34d9b2;-->
<!--  background-image: -webkit-linear-gradient(top, #34d9b2, #a02bb8);-->
<!--  background-image: -moz-linear-gradient(top, #34d9b2, #a02bb8);-->
<!--  background-image: -ms-linear-gradient(top, #34d9b2, #a02bb8);-->
<!--  background-image: -o-linear-gradient(top, #34d9b2, #a02bb8);-->
<!--  background-image: linear-gradient(to bottom, #34d9b2, #a02bb8);-->
<!--  -webkit-border-radius: 28;-->
<!--  -moz-border-radius: 28;-->
<!--  border-radius: 28px;-->
<!--  text-shadow: 0px 1px 3px #666666;-->
<!--  font-family: Arial;-->
<!--  color: #ffffff;-->
<!--  font-size: 8px;-->
<!--  padding: 10px 20px 10px 20px;-->
<!--  text-decoration: none;-->
<!--}-->

<!--.dlbtn:hover {-->
<!--  background: #3cb0fd;-->
<!--  background-image: -webkit-linear-gradient(top, #3cb0fd, #3498db);-->
<!--  background-image: -moz-linear-gradient(top, #3cb0fd, #3498db);-->
<!--  background-image: -ms-linear-gradient(top, #3cb0fd, #3498db);-->
<!--  background-image: -o-linear-gradient(top, #3cb0fd, #3498db);-->
<!--  background-image: linear-gradient(to bottom, #3cb0fd, #3498db);-->
<!--  text-decoration: none;-->
<!--}-->
<!--.smbtn {-->
<!--  background: #34d9b2;-->
<!--  background-image: -webkit-linear-gradient(top, #34d9b2, #7bb82c);-->
<!--  background-image: -moz-linear-gradient(top, #34d9b2, #7bb82c);-->
<!--  background-image: -ms-linear-gradient(top, #34d9b2, #7bb82c);-->
<!--  background-image: -o-linear-gradient(top, #34d9b2, #7bb82c);-->
<!--  background-image: linear-gradient(to bottom, #34d9b2, #7bb82c);-->
<!--  -webkit-border-radius: 28;-->
<!--  -moz-border-radius: 28;-->
<!--  border-radius: 28px;-->
<!--  text-shadow: 0px 1px 3px #666666;-->
<!--  font-family: Arial;-->
<!--  color: #ffffff;-->
<!--  font-size: 8px;-->
<!--  padding: 10px 20px 10px 20px;-->
<!--  text-decoration: none;-->
<!--}-->

<!--.smbtn:hover {-->
<!--  background: #3cb0fd;-->
<!--  background-image: -webkit-linear-gradient(top, #3cb0fd, #3498db);-->
<!--  background-image: -moz-linear-gradient(top, #3cb0fd, #3498db);-->
<!--  background-image: -ms-linear-gradient(top, #3cb0fd, #3498db);-->
<!--  background-image: -o-linear-gradient(top, #3cb0fd, #3498db);-->
<!--  background-image: linear-gradient(to bottom, #3cb0fd, #3498db);-->
<!--  text-decoration: none;-->
<!--}-->
<!--.rebtn {-->
<!--  background: #3439d9;-->
<!--  background-image: -webkit-linear-gradient(top, #3439d9, #2b92b8);-->
<!--  background-image: -moz-linear-gradient(top, #3439d9, #2b92b8);-->
<!--  background-image: -ms-linear-gradient(top, #3439d9, #2b92b8);-->
<!--  background-image: -o-linear-gradient(top, #3439d9, #2b92b8);-->
<!--  background-image: linear-gradient(to bottom, #3439d9, #2b92b8);-->
<!--  -webkit-border-radius: 28;-->
<!--  -moz-border-radius: 28;-->
<!--  border-radius: 28px;-->
<!--  font-family: Arial;-->
<!--  color: #ffffff;-->
<!--  font-size: 14px;-->
<!--  padding: 10px 20px 10px 20px;-->
<!--  text-decoration: none;-->
<!--}-->

<!--.rebtn:hover {-->
<!--  background: #b63cfc;-->
<!--  background-image: -webkit-linear-gradient(top, #b63cfc, #3473d9);-->
<!--  background-image: -moz-linear-gradient(top, #b63cfc, #3473d9);-->
<!--  background-image: -ms-linear-gradient(top, #b63cfc, #3473d9);-->
<!--  background-image: -o-linear-gradient(top, #b63cfc, #3473d9);-->
<!--  background-image: linear-gradient(to bottom, #b63cfc, #3473d9);-->
<!--  text-decoration: none;-->
<!--}-->
<!--#container {-->
<!--  display: flex;-->
<!--}-->

<!--#main-content {-->
<!--  flex: 1;-->
<!--}-->

<!--#right-container {-->
<!--  width: 50%;-->
<!--}-->
<!--.file-input-wrapper {-->
<!--  display: inline-block;-->
<!--  position: relative;-->
<!--}-->

<!--.file-input {-->
<!--  display: none;-->
<!--}-->

<!--input[type='button'] {-->
<!--  /* Add your custom styles for the button here */-->
<!--}-->
<!--</style>-->
