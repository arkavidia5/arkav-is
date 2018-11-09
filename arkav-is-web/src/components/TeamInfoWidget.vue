<template>
  <v-flex>
    <h2>Informasi Tim</h2>
    <br />
    <v-form @submit.prevent="editTeam">
      <v-text-field label="Kategori" v-model="category" disabled />
      <v-text-field label="Nama tim" v-model="name" :disabled="loading" />
      <v-text-field label="Asal universitas/sekolah" v-model="institution" :disabled="loading" />
      <v-btn class="ma-0 mt-2" color="primary" type="submit" :loading="loading">Simpan</v-btn>
    </v-form>

    <h2 v-if="team.competition.is_registration_open" class="mt-5">Hapus Tim</h2>
    <p><a href="#" class="body-link" @click="confirmDeleteTeam">Klik disini</a> untuk menghapus tim ini.</p>
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
      loading: state => state.team.saving
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
