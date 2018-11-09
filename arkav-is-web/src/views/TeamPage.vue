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
          <TeamMembersWidget :team="team" v-if="activeTask == 'team_members'" />
          <TeamInfoWidget :team="team" v-if="activeTask == 'team_info'" />

          <v-flex v-for="task in getTasks()" v-if="activeTask == task.id" :key="`task-${task.id}`">
            <h2>{{task.name}}</h2>
            <div>
              {{task.widget_parameters}}
            </div>
            <v-flex>
              <Widget :task="task" />
            </v-flex>
            <div v-if="response = getTaskResponse(task.id)">
              <h2>Submission</h2>
              <v-flex v-if="task.widget === 'file_upload'">
                <a :href="`/api/upload/download/${response.response}/`" class="no-decoration" target="_blank">
                  <v-btn color="info">
                    <v-icon>launch</v-icon>
                    Uploaded File
                  </v-btn>
                </a>
                  Submitted: {{getFormattedDate(response.last_submitted_at)}}

              </v-flex>
            </div>
          </v-flex>
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
  import Widget from '../components/Widget.vue'
  import TeamMembersWidget from '../components/TeamMembersWidget.vue'
  import TeamInfoWidget from '../components/TeamInfoWidget.vue'
  import { mapState, mapActions } from 'vuex'
  import moment from 'moment'
  export default {
    components: {
      TaskSidebar,
      Widget,
      TeamMembersWidget,
      TeamInfoWidget,
    },
    data() {
      return {
        sidebarActive: false,
        team_id: this.$route.params.id,
        activeTask: 'team_members',
      }
    },
    computed: {
      shouldCollapseSidebar() {
        return this.$vuetify.breakpoint.smAndDown
      },
      ...mapState({
        loading: state => state.team.loading,
        errors: state => state.team.errors,
        team: state => state.team.team,
      }),
    },
    methods: {
      ...mapActions({
        getTeam: 'team/getTeam',
      }),
      activateTask: function (task) {
        this.activeTask= task
        this.sidebarActive = false
      },
      getTasks: function () {
        let tasks = []
        for (let i = 0; i < this.team.stages.length; i++) {
          let appendee = this.team.stages[i].tasks
          for (let j = 0; j < appendee.length; j++) {
            tasks.push(appendee[j])
          }
        }
        return tasks
      },
      getTaskResponse: function (task_id) {
        return this.team.task_responses.find(obj => { return obj.task_id === task_id })
      },
      getFormattedDate: function(time) {
        return moment(time).format('MMMM Do YYYY, hh:mm:ss');
      }
    },
    mounted() {
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
