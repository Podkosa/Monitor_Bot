<template>
  <div class="grid-container">
    <NavBar />
    <RouterView/>
  </div>
</template>

<script lang="ts">
import { RouterView } from 'vue-router'

export default {
  data() {
    return {
      a: 'a'
    }
  }
}
</script>

<style>
.grid-container {
  display: grid;
  height: 100%;
  grid-template-columns: minmax(50px, 5%) auto;
}
</style>
