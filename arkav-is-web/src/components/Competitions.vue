<template>
  <div v-if="teams.length > 0">
    <h1 class="mb-3 shadowed-heading text-xs-center text-md-left">Your Teams</h1>
      <v-card class="row elevation-2 pa-4">
        <v-layout row wrap>
          <v-flex md2 sm4 xs12 pa-3 ma-1 elevation-1 v-for="item in teams" :key="`teams-${item.id}`">
            <router-link class="no-decoration" :to="`/teams/${item.id}`">
              <v-layout row justify-center>
                <img :src="item.competition.view_icon" alt="" height=60>
              </v-layout>
              <v-layout row justify-center class="mt-3" style="line-height: 1.2">
                <h2 class="text-xs-center">{{item.name}}</h2>
              </v-layout>
            </router-link>
          </v-flex>

        </v-layout>
    </v-card>
  </div>
</template>

<script>
  import { mapState, mapActions } from 'vuex'

  export default {
    name: "Competitions",
    computed: {
      ...mapState({
        competitions: state => state.competition.competitions,
        teams: state => state.competition.teams,
      })
    },
    methods: {
      ...mapActions({
        getCompetitions: 'competition/getCompetitions',
        getTeams: 'competition/getTeams'
      }),
    },
    beforeMount() {
      this.getTeams()
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
