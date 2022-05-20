<script setup lang="ts">
import { computed, ref } from 'vue';
import UploadVue from './Upload.vue'
import { breakpointsTailwind, useBreakpoints } from '@vueuse/core'

const breakpoints = useBreakpoints(breakpointsTailwind)

const steps = [
    {
        title: "Выберите фотографии",
        component: UploadVue,
        form_key: 'images'
    },
    {
        title: "Укажите настройки",
        component: "",
        form_key: 'images'

    },
    {
        title: "Дождитесь результат",
        component: "",
        form_key: 'images'
    }
]

const form = ref(<{ [key: string]: object }>{})

const current_step = ref(0)

const next_step = (key: string, data: object) => {
    console.log({ data })
    form.value[key] = data
    if (current_step.value++ < steps.length - 1) {

    }
}

</script>

<template>
    <div class="mt-10 flex flex-col lg:flex-row gap-5 justify-between">
        <div class="main flex-grow order-1">
            <component :is="steps[current_step].component"
                @next="(data: object) => next_step(steps[current_step].form_key, data)" />
        </div>
        <div class="hidden sm:flex flex-grow md:flex-grow-0 lg:basis-2/12 lg:pl-5 lg:order-2">
            <el-steps class="w-full" :active="current_step" align-center
                :direction="breakpoints.lg.value ? 'vertical' : 'horizontal'" finish-status="success">
                <el-step v-for="step in steps" :title="step.title" />
            </el-steps>
        </div>
    </div>
</template>