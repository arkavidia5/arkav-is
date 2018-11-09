<template>
  <v-slide-x-transition>
    <aside v-show="visible">
      <v-list class="transparent">
        <v-subheader class="text-uppercase">Tim</v-subheader>

        <v-list-tile @click="selectTask('team_info')">
          <v-list-tile-action>
            <v-icon>description</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title class="body-2">Informasi Tim</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>

        <v-list-tile @click="selectTask('team_members')">
          <v-list-tile-action>
            <v-icon>people</v-icon>
          </v-list-tile-action>
          <v-list-tile-content class="pr-3">
            <v-list-tile-title class="body-2">Anggota Tim</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>


        <v-flex v-for="stage in team.stages" :key="stage.id">
          <v-subheader class="text-uppercase">{{stage.name}}</v-subheader>
          <v-list-tile v-for="task in stage.tasks" @click="selectTask(task.id)">
            <v-list-tile-action>
              <v-icon v-if="!getTaskResponse(task.id)">radio_button_unchecked</v-icon>
              <v-flex v-if="resp = getTaskResponse(task.id)">
                <v-icon v-if="resp.status == 'completed'" class="green--text">check_circle</v-icon>
                <v-icon v-if="resp.status == 'awaiting_validation'" class="amber--text">hourglass_full</v-icon>
                <v-icon v-if="resp.status == 'rejected'" class="red--text">error</v-icon>
              </v-flex>
            </v-list-tile-action>
            <v-list-tile-title class="body-2">
              {{task.name}}
            </v-list-tile-title>
          </v-list-tile>
        </v-flex>
      </v-list>
    </aside>
  </v-slide-x-transition>
</template>

<script>
  export default {
    props: ['visible', 'team'],
    data: () => ({}),
    methods: {
      selectTask: function (task_id) {
        this.$emit('selected', task_id)
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
    },
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
