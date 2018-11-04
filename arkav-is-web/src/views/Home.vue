<template>
  <v-app class="app">
    <Navbar />
    <v-container fluid main-container>
      <v-container>
      <router-view />
      </v-container>
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
    background: url('https://static.arkavidia.id/5/images/landing-bg-2.svg');
    background-repeat: no-repeat;
    background-position: bottom;
    background-size: 102%;
  }
  .app {
  }
</style>


