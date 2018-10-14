<template>
  <v-card class="elevation-3">
    <header class="task-header px-4 py-3">
      <h2 class="display-1 font-weight-bold">GituKanYa</h2>
      <div class="caption font-weight-bold primary--text">Data Mining</div>
    </header>

    <div class="task-container">
      <TaskSidebar class="task-sidebar grey lighten-4 px-2 hidden-sm-and-down" />

      <section class="task-content px-4 py-3">
        <h2 class="headline font-weight-bold">Kode Tim</h2>
        <br /><br /><br /><br /><br /><br /><br /><br />
        <br /><br /><br /><br /><br /><br /><br /><br />
      </section>
    </div>


  </v-card>
</template>

<script>
  import TaskSidebar from '../components/TaskSidebar.vue';

  export default {
    components: {
      TaskSidebar
    },
    data() {
      return {

      }
    }
  }
</script>

<style scoped>
  .task-header {
    border-bottom: solid 1px #eee;
  }

  .task-container {
    display: flex;
  }

  .task-content {
    flex: 1;
  }
</style>
