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
  .application--wrap {
    background-color: #FFFFF2;
    background-image: url('./assets/bg_pattern.png');
    background-size: 80%;
    background-position: top left;
    background-repeat: repeat;
  }
  .application a.body-link {
    color: inherit;
    text-decoration: none;
    position: relative;
  }

  .application a.body-link::before {
    content: '';
    border-bottom: 6px solid;
    border-bottom-color: var(--v-primary-base, #1976d2);
    position: absolute;
    opacity: 0.25;
    left: 0;
    bottom: 0;
    width: 100%;
  }

  .application a.body-link:hover::before {
    opacity: 0.4;
    transition: 0.2s;
  }

  .application a.body-link.hover-only::before {
    border-bottom: 0px solid;
  }

  .application a.body-link.hover-only:hover::before {
    transition: 0.2;
    border-bottom: 6px solid;
    border-bottom-color: var(--v-primary-base, #1976d2);
  }
  .futura-bt {
    font-family: 'Futura Md BT Bold'
  }
  .futura-bt.bold {
    font-family: 'Futura Md BT Bold';
  }
  .futura-lt.bold {
    font-family: 'FuturaLT'
  }
  .futura-lt.bold {
    font-family: 'FuturaLT-Bold'
  }
  .text-right {
    text-align: right;
  }
</style>
