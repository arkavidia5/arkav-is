<template>
  <v-app>
    <router-view />
  </v-app>
</template>

<script>

export default {
  name: 'App',
  data () {
    return {
      title: 'Arkavidia 5'
    }
  }
}
</script>

<style>
.application a {
  color: inherit;
  text-decoration: none;
  position: relative;
}

.application a::before{
  content: '';
  border-bottom: 6px solid;
  border-bottom-color: var(--v-primary-base, #1976d2);
  position: absolute;
  opacity: 0.25;
  left: 0;
  bottom: 0;
  width: 100%;
}

.application a:hover::before{
  opacity: 0.4;
  transition: 0.2s;
}

</style>