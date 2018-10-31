<template>
  <div>
    <h1 class="mb-3 futura-bt primary--text">Competition</h1>
    <v-card class="row elevation-2 pa-2" style="max-width: 900px;">
        <header class="text-header pa-2">
          <h1>Your Teams</h1>
        </header>
        <v-layout row wrap>
          <v-flex md3 sm4 xs12 pa-4 ma-1 elevation-1 v-for="item in teams" :key="`teams-${item.id}`">
            <router-link class="no-decoration" :to="`/team/${item.id}`">
              <v-layout row justify-center>
                <img :src="item.competition.view_icon" alt="" height=60>
              </v-layout>
              <v-layout row justify-center>
                <h2 class="text-xs-center">{{item.name}}</h2>
              </v-layout>
            </router-link>
          </v-flex>
          <v-flex md3 sm4 xs12 pa-4 ma-1 elevation-1 v-if="teams.length < 2">
            <router-link class="no-decoration" to="/create-team">
              <v-layout row justify-center>
                <i class="material-icons" style="font-size: 4.5rem;">add_circle</i>
              </v-layout>
              <v-layout row justify-center>
                <h2 class="text-xs-center">Create a Team</h2>
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
      this.getCompetitions()
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
