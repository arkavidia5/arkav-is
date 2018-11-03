<template>
  <v-app>
    <Navbar />
    <v-container main-container>
      <router-view />
    </v-container>
  </v-app>
</template>

<script>
  import Navbar from '../components/Navbar.vue';

  export default {
    components: {
      Navbar
    },
    data() {
      return {
        
      }
    }
  }
</script>
<style>
  .main-container {
    margin-top: 50px;
  }
</style>


