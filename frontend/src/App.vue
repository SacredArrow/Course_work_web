<template>
  <div id="app">
    <figure class="image container is-256x256">
  <img alt="RNA" src="./assets/rna3.png">
</figure>
    <!-- <img alt="Vue logo" src="./assets/rna2.png"> -->
    <Example> </Example>
  </div>
</template>

<script>
import Example from './components/Example.vue'
export default {
  name: 'app',
  components: {
  Example
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
