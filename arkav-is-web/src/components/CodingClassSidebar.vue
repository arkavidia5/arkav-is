<template>
  <v-slide-x-transition>
    <aside v-show="visible">
      <v-list class="transparent">
        <v-list-tile @click="selectTask('register')">
          <v-list-tile-action>
            <v-icon>people</v-icon>
          </v-list-tile-action>
          <v-list-tile-content class="pr-3">
            <v-list-tile-title class="body-2">Registrasi</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>

        <v-list-tile @click="selectTask('quiz')">
          <v-list-tile-action>
            <v-icon>assignment</v-icon>
          </v-list-tile-action>
          <v-list-tile-content class="pr-3">
            <v-list-tile-title class="body-2">Tes Online</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>

         <v-list-tile @click="selectTask('result')">
          <v-list-tile-action>
            <v-icon>announcement</v-icon>
          </v-list-tile-action>
          <v-list-tile-content class="pr-3">
            <v-list-tile-title class="body-2">Hasil</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>


        <!--<v-flex v-for="stage in team.stages" :key="stage.id">-->
          <!--<v-subheader class="text-uppercase">{{stage.name}}</v-subheader>-->
          <!--<v-list-tile v-for="task in stage.tasks" :key="task.id" @click="selectTask(task.id)">-->
            <!--<v-list-tile-action>-->
              <!--<v-icon v-if="!getTaskResponse(task.id)">radio_button_unchecked</v-icon>-->
              <!--<v-flex v-if="resp = getTaskResponse(task.id)">-->
                <!--<v-icon v-if="resp.status == 'completed'" class="green&#45;&#45;text">check_circle</v-icon>-->
                <!--<v-icon v-if="resp.status == 'awaiting_validation'" class="amber&#45;&#45;text">hourglass_full</v-icon>-->
                <!--<v-icon v-if="resp.status == 'rejected'" class="red&#45;&#45;text">error</v-icon>-->
              <!--</v-flex>-->
            <!--</v-list-tile-action>-->
            <!--<v-list-tile-title class="body-2">-->
              <!--{{task.name}}-->
            <!--</v-list-tile-title>-->
          <!--</v-list-tile>-->
        <!--</v-flex>-->
      </v-list>
    </aside>
  </v-slide-x-transition>
</template>

<script>
  export default {
    props: ['visible', 'registrationData'],
    data: () => ({}),
    methods: {
      selectTask: function (task_id) {
        this.$emit('selected', task_id)
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
