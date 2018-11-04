<template>
  <v-slide-x-transition>
    <aside v-show="visible">
      <slot></slot>
    </aside>
  </v-slide-x-transition>
</template>

<script>
  export default {
    props: ['visible', ''],
    data: () => ({})
  }
</script>

<style scoped>
  .task-sidebar.slide-x-transition-leave-active {
    position: absolute;
  }

  .task-sidebar .v-list__tile__action,
  .task-sidebar .v-list__tile__avatar {
    min-width: 36px;
  } 
</style>
