<script>
import {defineComponent} from 'vue'

/* global $3Dmol*/
export default defineComponent({
 data() {
    return {
      viewer:null,
      filename:null,
      pdbfilename:null,
      showfilename:false,
      fileData: null,
      atomIds:null,
      pdbData:null,
      index:null,
      selectedpdbFile:null,
      selectedFile: null,
      bodyId: 0,
      inputValue: '',
      showinput:false,
      showload:false
    };
  },
  methods: {
    handleFileUpload(event) {
      this.selectedFile = event.target.files[0];
      const reader = new FileReader();

      reader.onload = () => {
        this.fileContent = reader.result;
        this.filename=this.selectedFile.name
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
        this.pdbfilename=this.selectedpdbFile.name
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

    const blob = new Blob([this.fileContent], { type: "application/xml" });
    const fileURL = URL.createObjectURL(blob);

    // Create a temporary link and trigger the download
    const tempLink = document.createElement('a');
    tempLink.href = fileURL;
    tempLink.setAttribute('download',this.filename );
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
      })
      .then(response => response.json())
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
  //   addsurface()
  //   {
  //     if(this.showinput) {
  //       this.index = this.fileData.body_index
  //       this.atomIds = this.fileData.body[this.index[this.bodyId]]['point_ids']
  //
  //       this.atomIds = this.atomIds.map(num => parseInt(num, 10))
  //       console.log(this.atomIds);
  //        const atomSelection = { serial: this.atomIds };
  //          const model = this.viewer.getModel(); // Get the current viewer model
  //          const selectedAtoms = model.selectedAtoms(atomSelection); // Get the selected atoms with specified serial numbers
  //          for (const atom of selectedAtoms) {
  //   atom.clickable = true;
  //   atom.callback = function (pickedAtom) {
  //     console.log(pickedAtom); // Output atom information
  //     // Perform further actions based on atom properties, e.g., change style, display popup, etc.
  //   };
  //   // Add a red dot to the atom
  //   this.viewer.addStyle(atom, {
  //     sphere: {
  //       radius: 5, // Set the radius of the sphere based on desired dot size
  //       color: "yellow",
  //     }
  //   });
  // }
  //       this.viewer.addSurface($3Dmol.SurfaceType.SAS, { opacity: 0.9, color: "lightblue" }, atomSelection);
  //     }
  //     this.viewer.render();
  //   },
     showPdb(pdbData)
    {
      this.viewer=$3Dmol.createViewer(this.$refs.viewer,{ backgroundColor: 'black' });
      try {
        this.viewer.addModel(pdbData, "pdb");
        this.viewer.setStyle({}, { line: {} });
        this.viewer.zoomTo();
         if(this.showinput) {
        this.index = this.fileData.body_index
        this.atomIds = this.fileData.body[this.index[this.bodyId]]['point_ids']

        this.atomIds = this.atomIds.map(num => parseInt(num, 10))
        console.log(this.atomIds);
         const atomSelection = { serial: this.atomIds };
           const model = this.viewer.getModel(); // Get the current viewer model
           const selectedAtoms = model.selectedAtoms(atomSelection); // Get the selected atoms with specified serial numbers
           for (const atom of selectedAtoms) {
    atom.clickable = true;
    atom.callback = function (pickedAtom) {
      console.log(pickedAtom); // Output atom information
      // Perform further actions based on atom properties, e.g., change style, display popup, etc.
    };
    // Add a red dot to the atom
    this.viewer.addStyle(atom, {
      sphere: {
        radius: 5, // Set the radius of the sphere based on desired dot size
        color: "yellow",
      }
    });
  }
        this.viewer.addSurface($3Dmol.SurfaceType.SAS, { opacity: 0.9, color: "lightblue" }, atomSelection);
      }
      this.viewer.render();
        this.showload=true;

      } catch (error) {
        console.error("Error rendering PDB data:", error);
      }
    },
    updateBodyId() {
        this.bodyId = this.inputValue;
        alert("Sumit successfully!Please press 'reload' button!")

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
        this.showfilename=true;
        this.showinput=true
      })
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
    <h2 style="color: #3a8ee6;margin-bottom: 10px">Parse pdb file:</h2>
  <div>
    <form @submit.prevent="submitpdbForm">
      <input class="file-input"  ref="fileInput1" type="file" @change="handlepdbFileUpload" accept=".pdb" />
      <input type="button" class="selbtn" value="select file" @click="$refs.fileInput1.click()" /> {{
        selectedpdbFile ? selectedpdbFile.name : 'no file selected'
      }}
      <button type="submit" class="psbtn" style="margin-left: 5px">parse</button>
    </form>

    <div ref="viewer" style="min-height: 400px;width: 400px; position: relative;margin-top: 10px" :data-ui="true"></div>
    <div v-if="showload">
      <button class="rebtn" @click="showPdb(pdbData)" style="margin-top: 10px">Reload</button>
<!--      <button class="rebtn" @click="showPdb(pdbData)" style="margin-top: 10px">Restore</button>-->
    </div>
    <div v-if="showinput">
    <input type="text" v-model="inputValue" placeholder="Please enter body id" style="margin-top: 10px;margin-bottom: 10px">
    <button class="psbtn" @click="updateBodyId" style="margin-left: 5px">submit</button>


  </div>
  </div>
  </div>




  <div id="right-container">
    <h2 style="color: #3a8ee6;margin-bottom: 10px">Parse xml file:</h2>
     <div>
    <form @submit.prevent="submitxmlForm">
    <div class="file-input-wrapper">
      <input class="file-input" type="file" ref="fileInput" @change="handleFileUpload" id="fileInput" accept=".xml" />
      <input type="button" class="selbtn" value="select file" @click="$refs.fileInput.click()" /> {{
        selectedFile ? selectedFile.name : 'no file selected'
      }}
    </div>
    <button class="psbtn" type="submit" style="margin-left: 5px">parse</button>
     <div> <button class="dlbtn" @click="downloadFile" style="margin-top:8px">Download xml File</button></div>
    </form>
       <div v-if="showfilename"><h3>{{filename}}:</h3></div>
    <div style="margin-top: 10px" v-if="fileData">The protein contains {{ fileData.content[0] }} bodies</div>
    <div style="margin-top: 10px" v-if="fileData">The protein contains {{ fileData.content[1] }} points</div>
    <div style="margin-top: 10px" v-if="fileData">The protein contains {{ fileData.content[2] }} bars</div>
    <div style="margin-top: 10px" v-if="fileData">The protein contains {{ fileData.content[3] }} hinges</div>
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
  background: #349cd9;
  background-image: -webkit-linear-gradient(top, #349cd9, #2c33b8);
  background-image: -moz-linear-gradient(top, #349cd9, #2c33b8);
  background-image: -ms-linear-gradient(top, #349cd9, #2c33b8);
  background-image: -o-linear-gradient(top, #349cd9, #2c33b8);
  background-image: linear-gradient(to bottom, #349cd9, #2c33b8);
  -webkit-border-radius: 2;
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
}

.selbtn:hover {
  background: #3cb0fd;
  background-image: -webkit-linear-gradient(top, #3cb0fd, #3498db);
  background-image: -moz-linear-gradient(top, #3cb0fd, #3498db);
  background-image: -ms-linear-gradient(top, #3cb0fd, #3498db);
  background-image: -o-linear-gradient(top, #3cb0fd, #3498db);
  background-image: linear-gradient(to bottom, #3cb0fd, #3498db);
  text-decoration: none;
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
  text-shadow: 0px 1px 3px #666666;
  font-family: Arial;
  color: #ffffff;
  font-size: 8px;
  padding: 10px 20px 10px 20px;
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
  color: #ffffff;
  font-size: 14px;
  padding: 10px 20px 10px 20px;
  text-decoration: none;
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
</style>
