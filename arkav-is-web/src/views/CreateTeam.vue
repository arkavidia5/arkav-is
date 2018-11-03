<template>
    <v-card class="elevation-2 pa-4">
        <h1 class="pa-3 headline"><b>Create Team</b></h1>
        <hr class="mx-1">
        <v-layout row wrap justify-center mt-1 pa-2>
            <v-flex md8 sm10 xs10 v-if="loading">
              <v-progress-linear :indeterminate="true" ></v-progress-linear>
            </v-flex>
            <v-flex xs6 md2 sm4 v-else pa-2 v-for="item in competitions" :key="`comp-${item.id}`" d-flex column competition-list @click="activate(item)" cursor-pointer :active="competition.id==item.id">
                <img :src="item.view_icon" alt="" height="80">
                <h3 class="text-xs-center">{{item.name}}</h3>
            </v-flex>
        </v-layout>
        <v-container v-if="competition">
            <v-layout row wrap >
                <v-flex xs12 sm8 md8>
                    <h2 class="text-xs-center text-sm-left">{{competition.name}}</h2>
                </v-flex>
                <v-flex xs12 sm4 md4 d-flex justify-end align-center v-if="competition" text-xs-center text-sm-right>
                    <span v-if="competition.min_team_members != competition.max_team_members">Anggota Tim: {{competition.min_team_members}} - {{competition.max_team_members}} orang</span>
                    <span v-else>Anggota Tim: {{competition.max_team_members}} orang</span>
                </v-flex>
            </v-layout>
            <h3 class="mt-4">Detil Tim</h3>
            <v-layout row wrap pa-2>
                <v-flex xs12 sm10 md8>
                    <v-text-field label="Nama Tim"></v-text-field>
                    <v-select  label="Kategori" :items="competition.categories.map(a => a.name)"></v-select>
                    <v-text-field label="Asal Universitas/Sekolah"></v-text-field>
                </v-flex>
            </v-layout>
            <h3>Peserta</h3>

            <v-layout row wrap v-for="i in members.length" :key="`member-${i}`">
                <v-flex xs12 md6 px-1>
                    <v-text-field :label="`Nama Lengkap Peserta ${i}`" v-model="members[i-1].name"></v-text-field>
                </v-flex>
                <v-flex xs12 md6 px-1>
                    <v-text-field :label="`Email Peserta ${i}`" v-model="members[i-1].email"></v-text-field>
                </v-flex>
            </v-layout>

            <v-layout row>
                <v-btn  color='success' @click="addMember"><i class="material-icons">add</i> Tambah</v-btn>
                <v-btn color='error' @click="removeMember"><i class="material-icons">delete</i>Kurang</v-btn>
            </v-layout>
        </v-container>
        
    </v-card>
    
</template>
<script>
import {mapActions, mapState} from 'vuex'
export default {
    data: () => ({
        competition: '',
        members: [],
        team_name: '',
        team_category: '',
        team_
    }),
    computed: {
      ...mapState({
        competitions: state => state.competition.competitions,
        loading: state => state.competition.loading,
        user: state => state.auth.user
      })
    },
    methods: {
        ...mapActions({
            fetch: 'competition/getCompetitions'
        }),
        activate: function(item) {
            this.competition = item
            while(this.members.length < this.competition.min_team_members) {
                this.members.push({})
            }
            while(this.members.length > this.competition.max_team_members) {
                this.members.pop()
            }
        },
        addMember: function() {
            if (this.members.length < this.competition.max_team_members) {
                this.members.push({})
            }

        },
        removeMember: function() {
            if (this.members.length > this.competition.min_team_members) {
                this.members.pop()
            }
        }
    }, 
    beforeMount: function() {
        this.fetch()
        this.members.push({'name': this.user.full_name, 'email': this.user.email})
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
