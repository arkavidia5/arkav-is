<template>
  <v-card class="elevation-3">
    <header class="task-header px-4 py-3">
      <div>
        <h2 class="display-1 font-weight-bold">Competitions</h2>
      </div>
    </header>
    <div class="task-container">
      <v-container grid-list-md>
        <v-layout row wrap>
          <v-flex v-for="i in competitions.length" :key="`4${i}`" xs3>
            <v-card>
              <v-img src="https://cdn.vuetifyjs.com/images/cards/desert.jpg"></v-img>
              <v-card-title primary-title>
                <div>
                  <h3 class="headline">{{competitions[i-1].name}}</h3>
                </div>
              </v-card-title>
              <v-card-actions>
                <v-btn v-if="competitions[i-1].is_registration_open" flat color="orange">Register</v-btn>
                <v-btn v-if="!competitions[i-1].is_registration_open" flat color="orange" disabled>Coming Soon</v-btn>
              </v-card-actions>
            </v-card>
          </v-flex>
        </v-layout>
      </v-container>
    </div>
    <header class="task-header px-4 py-3">
      <div>
        <h2 class="display-1 font-weight-bold">Teams</h2>
      </div>
    </header>
    <div class="task-container">
      <v-container grid-list-md>
        <v-layout row wrap>
          <v-flex v-for="i in teams.length" :key="`4${i}`" xs3>
            <v-card>
              <v-img src="https://cdn.vuetifyjs.com/images/cards/desert.jpg"></v-img>
              <v-card-text>
                <div class="caption font-weight-bold primary--text">{{teams[i-1].competition.name}}</div>
                <h3 class="headline">{{teams[i-1].name}}</h3>
              </v-card-text>
              <v-card-actions>
                <v-btn flat color="orange">More</v-btn>
              </v-card-actions>
            </v-card>
          </v-flex>
        </v-layout>
      </v-container>
    </div>
  </v-card>
</template>

<script>
  import { mapState, mapActions } from 'vuex'

  export default {
    computed: {
      ...mapState({
        errors: state => state.competition.errors,
        loading: state => state.competition.loading,
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
      this.getCompetitions(),
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
