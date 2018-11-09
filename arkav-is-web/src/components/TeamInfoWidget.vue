<template>
  <v-flex>
    <h2>Informasi Tim</h2>
    <br />
    <v-form @submit.prevent="editTeam">
      <v-text-field label="Kategori" v-model="category" disabled />
      <v-text-field label="Nama tim" v-model="name" :disabled="loading || !team.competition.is_registration_open" />
      <v-text-field label="Asal universitas/sekolah" v-model="institution" :disabled="loading || !team.competition.is_registration_open" />
      <v-btn
        class="ma-0 mt-2"
        color="primary"
        type="submit"
        :loading="loading"
        v-if="team.competition.is_registration_open"
      >Simpan</v-btn>
    </v-form>

    <template v-if="team.competition.is_registration_open">
      <h3 class="mt-5">Hapus Tim</h3>
      <p><a href="#" class="body-link" @click="confirmDeleteTeam">Klik disini</a> untuk menghapus tim ini.</p>
    </template>
  </v-flex>
</template>

<script>
import { mapState, mapActions } from 'vuex'
export default {
  name: 'TeamInfoWidget',
  props: ['team'],
  data: function () {
    return {
      name: this.team.name,
      institution: this.team.institution,
      category: this.team.category,
    }
  },
  computed: {
    ...mapState({
      loading: state => state.team.loading
    })
  },
  methods: {
    ...mapActions({
      editTeamAction: 'team/editTeam',
      deleteTeamAction: 'team/deleteTeam',
    }),
    editTeam: function () {
      this.editTeamAction({
        team_id: this.team.id,
        name: this.name,
        institution: this.institution,
      })
    },
    confirmDeleteTeam: function () {
      if (confirm('Apakah Anda yakin ingin menghapus tim ' + this.team.name + '?\nTim akan dihapus secara permanen.')) {
        this.deleteTeamAction({
          team_id: this.team.id,
          router: this.$router,
        })
      }
    },
  }
}
</script>
