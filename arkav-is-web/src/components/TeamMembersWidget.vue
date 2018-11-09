<template>
  <v-flex>
    <h2>Anggota Tim</h2>
    <p>
      Jumlah peserta tim maksimal untuk {{ team.competition.name }}
      adalah {{team.competition.max_team_members}} orang.
    </p>
    <v-list two-line>
      <v-divider></v-divider>
      <template v-for="member in team.team_members">
        <v-list-tile :key="member.email" profile>
          <v-list-tile-avatar>
            <template v-if="member.is_team_leader">
              <v-tooltip bottom>
                <v-icon slot="activator" color="accent">account_circle</v-icon>
                <span>Ketua tim</span>
              </v-tooltip>
            </template>
            <template v-else-if="team.competition.is_registration_open && member.has_account">
              <v-tooltip bottom>
                <v-btn slot="activator" icon ripple @click="setTeamLeader(member)">
                  <v-icon>person</v-icon>
                </v-btn>
                <span>Jadikan ketua tim</span>
              </v-tooltip>
            </template>
            <template v-else>
              <v-tooltip bottom>
                <v-icon slot="activator">person</v-icon>
                <span>Anggota tim</span>
              </v-tooltip>
            </template>
          </v-list-tile-avatar>
          <v-list-tile-content>
            <v-list-tile-title>{{member.full_name}}</v-list-tile-title>
            <v-list-tile-sub-title v-if="member.is_team_leader">{{member.email}} - Ketua tim</v-list-tile-sub-title>
            <v-list-tile-sub-title v-else>{{member.email}} - {{member.has_account ? 'Akun teraktivasi' : 'Email undangan terkirim'}}</v-list-tile-sub-title>
          </v-list-tile-content>
          <v-list-tile-action>
            <v-tooltip bottom>
              <v-btn
                slot="activator"
                icon
                ripple
                @click="confirmDeleteTeamMember(member)"
                v-if="currentUserEmail !== member.email && !member.is_team_leader && team.competition.is_registration_open"
              >
                <v-icon color="red">close</v-icon>
              </v-btn>
              <span>Hapus anggota tim</span>
            </v-tooltip>
          </v-list-tile-action>
        </v-list-tile>
        <v-divider></v-divider>
      </template>
    </v-list>
    <br />

    <template v-if="team.competition.is_registration_open && team.team_members.length < team.competition.max_team_members">
      <h3>Tambah Anggota Tim</h3>
      <v-form @submit.prevent="addTeamMember">
        <v-text-field label="Nama lengkap" v-model="invitation_full_name" :disabled="loading" />
        <v-text-field label="Email" v-model="invitation_email" :disabled="loading" />
        <v-btn class="ma-0 mt-2" color="primary" type="submit" :loading="loading">Tambahkan Anggota</v-btn>
      </v-form>
    </template>
  </v-flex>
</template>

<script>
import { mapState, mapActions } from 'vuex'
export default {
    name: 'TeamMembersWidget',
    props: ['team'],
    data: function () {
      return {
        invitation_full_name: '',
        invitation_email: '',
      }
    },
    computed: {
      ...mapState({
        loading: state => state.team.loading,
        currentUserEmail: state => state.auth.user.email,
      })
    },
    methods: {
      ...mapActions({
        setTeamLeaderAction: 'team/setTeamLeader',
        addTeamMemberAction: 'team/addTeamMember',
        removeTeamMemberAction: 'team/removeTeamMember',
      }),
      setTeamLeader: function (teamMember) {
        this.setTeamLeaderAction({
          team_id: this.team.id,
          email: teamMember.email,
        })
      },
      addTeamMember: function () {
        this.addTeamMemberAction({
          team_id: this.team.id,
          full_name: this.invitation_full_name,
          email: this.invitation_email,
        })
      },
      confirmDeleteTeamMember: function (teamMember) {
        if (confirm('Apakah Anda yakin ingin menghapus ' + teamMember.full_name + ' dari tim?')) {
          this.removeTeamMemberAction({
            team_id: this.team.id,
            team_member_id: teamMember.id,
          })
        }
      },
    }
}
</script>
