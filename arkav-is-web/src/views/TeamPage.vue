<template>
  <v-card class="elevation-3">
    <header class="task-header px-4 py-3">
      <v-btn flat icon color="gray" class="ma-0 mr-3" v-show="shouldCollapseSidebar" @click.native="sidebarActive = !sidebarActive">
        <v-icon>menu</v-icon>
      </v-btn>
      <div>
        <h2 class="display-1 font-weight-bold">GituKanYa</h2>
        <div class="caption font-weight-bold primary--text">Data Mining</div>
      </div>
    </header>

    <div class="task-container">
      <!-- TODO: when any of the menu items in task sidebar is pressed, set sidebarActive = false-->
      <TaskSidebar class="task-sidebar grey lighten-4 px-2" :visible="!shouldCollapseSidebar || sidebarActive" />
      <v-slide-x-transition>
        <section class="task-content px-4 py-3" v-show="!shouldCollapseSidebar || !sidebarActive">
          <h2 class="headline font-weight-bold">
            Kode Tim
          </h2>

          <br /><br /><br /><br /><br /><br /><br /><br />
          <br /><br /><br /><br /><br /><br /><br /><br />
        </section>
      </v-slide-x-transition>
    </div>


  </v-card>
</template>

<script>
  import TaskSidebar from '../components/TaskSidebar.vue'

  export default {
    components: {
      TaskSidebar
    },
    computed: {
      shouldCollapseSidebar() {
        return this.$vuetify.breakpoint.smAndDown
      }
    },
    data() {
      return {
        sidebarActive: false
      }
    },
  }
</script>

<style scoped>
  .task-header {
    border-bottom: solid 1px #eee;
    display: flex;
    align-items: center;
  }

  .task-sidebar {
    z-index: 9999;
    flex: 1;
  }

  .task-container {
    display: flex;
    flex: 1
  }

  .task-content {
    flex: 3;
  }

  .task-content.slide-x-transition-leave-active {
    position: absolute;
  }
</style>
