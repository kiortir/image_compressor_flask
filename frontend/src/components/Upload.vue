<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios'
import 'element-plus/es/components/upload/style/css'
import { Loading, UploadFilled } from '@element-plus/icons-vue'
import { useDropzone } from "vue3-dropzone";

const emits = defineEmits(['next'])
const project_id = ref(null)

const files = ref([

])

const saveFiles = (f_s) => {
    const formData = new FormData(); // pass data as a form
    for (var x = 0; x < f_s.length; x++) {
        console.log(f_s[x])
        // append files as array to the form, feel free to change the array name
        formData.append("images[]", f_s[x]);
    }
    formData.append('project_id', project_id.value)
    // post the formData to your backend where storage is processed. In the backend, you will need to loop through the array and save each file through the loop.

    axios
        .post('/api', formData, {
            headers: {
                "Content-Type": "multipart/form-data",
            },
        })
        .then((response) => {
            console.log({ response: response.data, files: files.value })
            files.value = files.value.concat(response.data)
        })
        .catch((err) => {
            console.error(err);
        });
};



const showdrop = ref(true)
const loading = ref(false)

function onDrop(acceptFiles: object, rejectReasons: object) {
    saveFiles(acceptFiles)
    // files.value = files.value.concat(acceptFiles)
    loading.value = true
    showdrop.value = false
}

const sendPhotos = new Promise((resolve, reject) => {
    setTimeout(function () { resolve('Успех') }, 3000);


})

const { getRootProps, getInputProps, isDragActive, ...rest } = useDropzone({ onDrop });

</script>

<template>
    {{ project_id }}
    <div class="el-upload  is-drag ">
        <button class="el-upload-dragger mb-3 w-full" :class="[isDragActive ? 'is-dragover' : '']"
            v-bind="getRootProps()">

            <input v-bind="getInputProps()" />
            <!-- <el-upload v-if="files.length" action="https://jsonplaceholder.typicode.com/posts/" list-type="picture-card"
                :file-list="files">
                <el-icon>
                    <Plus />
                </el-icon>
            </el-upload> -->
            <div class="el-upload__text">
                <el-icon class="el-icon el-icon--upload">
                    <upload-filled />
                </el-icon>
                <p v-if="isDragActive">Отпустите для магии!</p>
                <p v-else>Перетащите фото сюда, или <em>нажмите, чтобы выбрать</em></p>
            </div>
        </button>
    </div>
    <div class="pictures grid gap-2 fixed-grid--between">

        <div v-for="image in files" class="w-fit hover:brightness-50">
            <el-image style="width: 150px; height: 150px" :src="image.url" :initial-index="4" fit="cover" />
        </div>


    </div>
    <!-- <div v-else-if="loading"></div> -->

    <!-- <el-upload class="upload-demo w-full" drag action="https://jsonplaceholder.typicode.com/posts/" multiple>
        <el-icon class="el-icon--upload">
            <upload-filled />
        </el-icon>
        <div class="el-upload__text">
            Перетащите фото сюда <em>нажмите, чтобы выбрать</em>
        </div>
        <template #tip>
            <div class="el-upload__tip">
                jpg/png, не более 3mb
            </div>
        </template>
    </el-upload> -->
</template>

<style>
/* for space-around style */
/* for space-around style */
.fixed-grid--around {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    justify-items: center;
}

/* for space-between style*/
.fixed-grid--between {
    grid-template-columns: repeat(auto-fit, 150px);
    justify-content: space-between;
}

/* both should run fixed width elements equal to the declared in the container */
.grid-element {
    width: 150px;
}
</style>