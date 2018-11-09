<template>
  <v-layout align-center justify-center>
    <v-flex xs12 sm10 md8>
      <v-card class="elevation-3 pa-3">
        <v-card-text>
          <h1 class="shadowed-heading text-xs-center">Create Team</h1>

          <v-layout row wrap my-4>
            <v-flex class="competition-list" xs6 sm3 v-if="!loading" pa-3 d-flex column v-for="item in competitions" :key="item.id"
              @click="activate(item)" cursor-pointer :active="competition.id==item.id">
              <img :src="item.view_icon" alt="" height="80">
              <div class="competition-name text-xs-center">{{item.name}}</div>
              <div class="max-team-members text-xs-center" v-if="item.min_team_members != item.max_team_members">{{
                  item.min_team_members }}-{{ item.max_team_members }} orang</div>
              <div class="max-team-members text-xs-center" v-else>{{ item.max_team_members }} orang</div>
            </v-flex>
          </v-layout>

          <v-form v-if="competition" @submit.prevent="submit">
            <v-text-field label="Nama tim" :rules="notEmpty" v-model="name"></v-text-field>
            <v-select
              v-if="competition.categories && competition.categories.length > 1"
              label="Kategori"
              :items="competition.categories"
              :rules="notEmpty"
              v-model="category">
            </v-select>
            <v-text-field label="Asal universitas/sekolah" :rules="notEmpty" v-model="institution"></v-text-field>
            <v-alert v-for="error in submitErrors" :key="error" :value="true" type="error" outline>
              {{ error }}
            </v-alert>
            <v-btn class="mt-3" depressed large block color="primary" type="submit" :loading="submitLoading">
              Daftarkan Tim
            </v-btn>
          </v-form>
        </v-card-text>
      </v-card>
    </v-flex>
  </v-layout>

</template>
<script>
import {mapActions, mapState} from 'vuex'
export default {
  data: () => ({
    competition: '',
    name: '',
    category: '',
    institution: '',
    notEmpty: [
      (v) => !!v || 'Harus terisi',
    ],
    emailRules: [
      (v) => !!v || 'E-mail tidak boleh kosong',
      (v) => /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(v) || 'E-mail tidak valid'
    ],
  }),
  computed: {
    ...mapState({
      competitions: state => state.competition.competitions,
      loading: state => state.competition.loading,
      submitLoading: state => state.team.loading,
      submitErrors: state => state.team.errors,
      user: state => state.auth.user
    })
  },
  methods: {
    ...mapActions({
      fetch: 'competition/getCompetitions',
      submitAction: 'team/submitTeam'
    }),
    activate: function (item) {
      this.competition = item
    },
    submit: function () {
      if (this.competition.categories && this.competition.categories.length == 1) {
        this.category = this.competition.categories[0]
      }
      this.submitAction({
        competition_id: this.competition.id,
        name: this.name,
        category: this.category,
        institution: this.institution,
        router: this.$router
      })
    }
  },
  beforeMount: function () {
    this.fetch()
  }
}
</script>

<style scoped>
    .competition-list {
        border-radius: 3px;
    }

    .competition-list.active {
        border: 2px solid #04464F;
        box-shadow: 0px 0px 1px 0px #04464F;
    }

    .competition-list .competition-name {
        font-size: 1rem;
        font-weight: bold;
        line-height: 1.4;
        margin-top: 8px;
    }

    .max-team-members {
        font-size: 0.9rem;
    }
</style>
