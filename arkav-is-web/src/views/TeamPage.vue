<template>
  <v-card class="elevation-3" v-if="team">
    <header class="task-header px-4 py-3">
      <v-btn flat icon color="gray" class="ma-0 mr-3" v-show="shouldCollapseSidebar" @click.native="sidebarActive = !sidebarActive">
        <v-icon>menu</v-icon>
      </v-btn>
      <v-layout row align-center>
        <img :src="team.competition.view_icon" alt="" height="50">
        <div class="ml-2">
        <h2 class="display-1 font-weight-bold">{{team.name}}</h2>
        <div class="caption font-weight-bold primary--text">{{team.competition.name}}</div>
        </div>
      </v-layout>
    </header>

    <div class="task-container">
      <!-- TODO: when any of the menu items in task sidebar is pressed, set sidebarActive = false-->
      <TaskSidebar class="task-sidebar grey lighten-4 px-2" :visible="!shouldCollapseSidebar || sidebarActive"  style="min-height:400px">
          <v-list class="transparent">
        <v-subheader class="text-uppercase">Informasi Tim</v-subheader>
    
        <v-list-tile @click="activateTask('member')">
          <v-list-tile-action>
            <v-icon class="green--text">check_circle</v-icon>
          </v-list-tile-action>
          <v-list-tile-content class="pr-3">
            <v-list-tile-title class="body-2">Anggota Tim</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
        <v-flex v-for="stage in team.stages" :key="`stage-${stage.name}`">
          <v-subheader class="text-uppercase">
            {{stage.name}}
          </v-subheader>
          <v-list-tile v-for="task in stage.tasks" @click="activateTask(task.id)">
            <v-list-tile-action>
              <v-icon>radio_button_unchecked</v-icon>
            </v-list-tile-action>
            <v-list-tile-title class="body-2">
              {{task.name}}
            </v-list-tile-title>
          </v-list-tile>
        </v-flex>    
      </v-list>
      </TaskSidebar>
      <v-slide-x-transition>
        <section class="task-content px-4 py-3" v-show="!shouldCollapseSidebar || !sidebarActive">
          <v-flex v-if="activeTask == 'member'">
            <h2>Anggota Tim</h2>
            <v-list v-for="member in team.team_members">
                <v-list-tile-content>
                  <v-list-tile-title>
                    {{member.name}}
                  </v-list-tile-title>
                  <v-list-tile-sub-title>{{member.email}}</v-list-tile-sub-title>

                </v-list-tile-content>
            </v-list>
          </v-flex>
          <v-flex v-for="task in getTasks()" v-if="activeTask == task.id">
            <h2>{{task.name}}</h2>
            <div>
              {{task.widget_parameters}}
            </div>
            <v-flex>
              <Widget :task="task" />
            </v-flex>
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
  import {mapState, mapActions} from 'vuex'
  export default {
    components: {
      TaskSidebar,
      Widget
    },
    data() {
      return {
        sidebarActive: false,
        team_id: this.$route.params.id,
        activeTask: 'member',
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
      activateTask: function(task) {
        this.activeTask= task
        this.sidebarActive = false
      },
      getTasks: function() {
        let tasks = []
        for(let i=0; i < this.team.stages.length; i++) {
          let appendee = this.team.stages[i].tasks
          for(let j=0;j < appendee.length; j++) {
            tasks.push(appendee[j])
          }
        }
        return tasks
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
