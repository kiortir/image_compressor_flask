<script setup lang="ts">
import NavigationVue from './components/Navigation.vue';
</script>

<template>
  <el-container>
    <el-header>
      <navigation-vue></navigation-vue>
    </el-header>
    <el-main>
      <div class="container mx-auto">
        <router-view></router-view>
      </div>
    </el-main>
    <el-footer></el-footer>
  </el-container>
</template>

<style>
</style>
