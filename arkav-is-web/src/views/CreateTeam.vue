<template>
    <v-card class="elevation-2">
        <h1 class="pa-3 headline"><b>Create Team</b></h1>
        <hr class="mx-1">
        <v-layout row wrap justify-center mt-1 pa-2>
            <v-flex md8 sm10 xs10 v-if="loading">
              <v-progress-linear :indeterminate="true" ></v-progress-linear>
            </v-flex>
            <v-flex sm2 xs6 v-else pa-2 v-for="item in competitions" :key="`comp-${item.id}`" d-flex column competition-list @click="activate(item)" cursor-pointer :active="competition.id==item.id">
                <img :src="item.view_icon" alt="" height="80">
                <h3 class="text-xs-center">{{item.name}}</h3>
            </v-flex>
        </v-layout>
        <v-layout row wrap>
            <v-flex pa-2>
                <h3>Competiton: {{competition.name}}</h3>
                <h3>Maks. Jumlah Anggota: {{competition.max_team_members}}</h3>
            </v-flex>
            
        </v-layout>
        
    </v-card>
    
</template>
<script>
import {mapActions, mapState} from 'vuex'
export default {
    data: () => ({
        competition: '',
    }),
    computed: {
      ...mapState({
        competitions: state => state.competition.competitions,
        loading: state => state.competition.loading
      })
    },
    methods: {
        ...mapActions({
            fetch: 'competition/getCompetitions'
        }),
        activate: function(item) {
            this.competition = item
        }
    }, 
    beforeMount: function() {
        this.fetch()
    }
}
</script>
<style scoped>
    .competition-list {
        border-radius: 3px;
    }
    .competition-list.active {
        border: 1px solid #04464F;
        box-shadow: 0px 0px 1px 0px #04464F;
    }
</style>
