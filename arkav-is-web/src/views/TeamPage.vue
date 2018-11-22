<template>
  <v-card class="elevation-3" v-if="team">
    <header class="task-header px-4 py-3">
      <v-btn flat icon color="gray" class="ma-0 mr-3" v-show="shouldCollapseSidebar" @click.native="sidebarActive = !sidebarActive">
        <v-icon>menu</v-icon>
      </v-btn>
      <v-layout row align-center>
        <img :src="team.competition.view_icon" alt="" height="50" class="mr-3" v-show="!shouldCollapseSidebar">
        <div>
          <h2 class="display-1 font-weight-bold">{{team.name}}</h2>
          <div class="caption font-weight-bold primary--text">{{team.competition.name}}</div>
        </div>
      </v-layout>
    </header>

    <div class="task-container">
      <!-- TODO: when any of the menu items in task sidebar is pressed, set sidebarActive = false-->
      <TaskSidebar
        class="task-sidebar grey lighten-4 px-2"
        :visible="!shouldCollapseSidebar || sidebarActive"
        style="min-height:400px"
        :team="team"
        @selected="activateTask"
      />

      <v-slide-x-transition>
        <section class="task-content px-4 py-3" v-show="!shouldCollapseSidebar || !sidebarActive">
          <TeamMembersWidget :team="team" v-if="activeTaskId == 'team_members'" />
          <TeamInfoWidget :team="team" v-if="activeTaskId === 'team_info'" />
          <FileUploadWidget
            :team="team"
            :task="activeTask"
            :taskResponse="activeTaskResponse"
            v-if="activeTask && activeTask.widget === 'file_upload'"
          />
          <TextInputWidget
            :team="team"
            :task="activeTask"
            :taskResponse="activeTaskResponse"
            v-else-if="activeTask && activeTask.widget === 'text_input'"
            />
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
  import TaskSidebar from '../components/TaskSidebar.vue'
  import TeamMembersWidget from '../components/TeamMembersWidget.vue'
  import TeamInfoWidget from '../components/TeamInfoWidget.vue'
  import FileUploadWidget from '../components/FileUploadWidget.vue'
  import TextInputWidget from '../components/TextInputWidget.vue'
  import { mapState, mapActions } from 'vuex'
  import moment from 'moment'
  export default {
    components: {
      TaskSidebar,
      TeamMembersWidget,
      TeamInfoWidget,
      FileUploadWidget,
      TextInputWidget,
    },
    data() {
      return {
        sidebarActive: false,
        team_id: this.$route.params.id,
        activeTaskId: 'team_members',
      }
    },
    computed: {
      ...mapState({
        loading: state => state.team.loading,
        errors: state => state.team.errors,
        team: state => state.team.team,
      }),
      shouldCollapseSidebar() {
        return this.$vuetify.breakpoint.smAndDown
      },
      activeTask() {
        let tasks = [];
        for (let i = 0; i < this.team.stages.length; i++) {
          tasks = tasks.concat(this.team.stages[i].tasks)
        }
        return tasks.find(task => task && task.id === this.activeTaskId)
      },
      activeTaskResponse() {
        return this.team.task_responses.find(taskResponse => taskResponse.task_id === this.activeTaskId)
      },
    },
    methods: {
      ...mapActions({
        getTeam: 'team/getTeam',
      }),
      activateTask: function (taskId) {
        this.activeTaskId = taskId
        this.sidebarActive = false
      },
      getFormattedDate: function(time) {
        return moment(time).format('D MMMM YYYY, hh:mm:ss');
      }
    },
    mounted: function () {
      this.getTeam({
        team_id: this.team_id
      })
    }
  }
</script>

<style scoped>
  .task-header {
    border-bottom: solid 1px #eee;
    display: flex;
    align-items: center;
  }

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
