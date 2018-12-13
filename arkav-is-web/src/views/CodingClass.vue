<template>
  <v-card class="elevation-3" v-if="true">
    <header class="task-header px-4 py-3">
      <v-btn flat icon color="gray" class="ma-0 mr-3" v-show="shouldCollapseSidebar" @click.native="sidebarActive = !sidebarActive">
        <v-icon>menu</v-icon>
      </v-btn>
      <v-layout row align-center>
        <img src="../assets/codingclass-02.svg" alt="" height="50" class="mr-3" v-show="!shouldCollapseSidebar">
        <div>
          <h2 class="display-1 font-weight-bold">Coding Class</h2>
          <div class="caption font-weight-bold primary--text">SMA/Sederajat</div>
        </div>
      </v-layout>
    </header>

    <div class="task-container">
      <!-- TODO: when any of the menu items in task sidebar is pressed, set sidebarActive = false-->
      <CodingClassSidebar
        class="task-sidebar grey lighten-4 px-2"
        :visible="!shouldCollapseSidebar || sidebarActive"
        style="min-height:400px"
        @selected="activateTask"
        :registration-data="registrationData"
      />

      <v-slide-x-transition>
        <section class="task-content px-4 py-3" v-show="!shouldCollapseSidebar || !sidebarActive">

          <CodingClassRegistrationForm v-if="activeTaskId === 'register'" :registration-data="registrationData"/>
          <CodingClassOnlineTest v-if="activeTaskId === 'quiz'" :registration-data="registrationData"/>
          <CodingClassResult v-if="activeTaskId === 'result'" :registration-data="registrationData"/>

        </section>
      </v-slide-x-transition>
    </div>

  </v-card>
  <v-layout v-else-if="loading" row justify-center>
     <v-progress-circular
      indeterminate
      color="primary"
    ></v-progress-circular>
  </v-layout>
  <v-layout v-else-if="errors">
      <v-alert v-for="error in errors" :key="error" :value="true" type="error" outline>
        {{error}}
      </v-alert>
  </v-layout>
</template>

<script>
  import CodingClassSidebar from '../components/CodingClassSidebar.vue'
  import CodingClassRegistrationForm from '../components/CodingClassRegistrationForm'
  import CodingClassOnlineTest from '../components/CodingClassOnlineTest'
  import CodingClassResult from '../components/CodingClassResult'
  import { mapState, mapActions } from 'vuex'
  export default {
    components: {
      CodingClassSidebar,
      CodingClassRegistrationForm,
      CodingClassOnlineTest,
      CodingClassResult
    },
    data() {
      return {
        sidebarActive: false,
        activeTaskId: 'register',
      }
    },
    computed: {
      ...mapState({
        loading: state => state.codinclass.loading,
        errors: state => state.codinclass.errors,
        registrationData: state => state.codingclass.registrationData,
      }),
      shouldCollapseSidebar() {
        return this.$vuetify.breakpoint.smAndDown
      },
    },
    methods: {
      ...mapActions({
        getRegistrationOpen: 'codingclass/getRegistrationOpen',
        getRegistrationData: 'codingclass/getRegistrationData'
      }),
      activateTask: function (taskId) {
        this.activeTaskId = taskId
        this.sidebarActive = false
      },
    },
    beforeMount: function () {
        this.getRegistrationOpen()
        this.getRegistrationData();
    }

  }
</script>

<style scoped>
  .task-header {
    border-bottom: solid 1px #eee;
    display: flex;
    align-items: center;
  }    bg</v-flex>bg

  .task-sidebar {
    z-index: 99;
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

  .task-sidebar .v-list__tile__action,
  .task-sidebar .v-list__tile__avatar {
    min-width: 36px;
  }
</style>
