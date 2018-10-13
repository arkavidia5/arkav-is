<template>
  <v-app>
    <v-container>
      <Navbar />
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