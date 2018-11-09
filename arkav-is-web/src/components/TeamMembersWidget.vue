<template>
  <v-flex>
    <h2>Anggota Tim</h2>

    <v-list v-for="member in team.team_members">
      <v-list-tile-content>
        <v-list-tile-title>{{member.name}}</v-list-tile-title>
        <v-list-tile-sub-title>{{member.email}}</v-list-tile-sub-title>
      </v-list-tile-content>
    </v-list>
  </v-flex>
</template>

<script>
import { mapState, mapActions } from 'vuex'
export default {
    name: 'TeamMembersWidget',
    props: ['team'],
    data: () => ({

    }),
    computed: {
      ...mapState({
          saving: state => state.team.saving
      })
    },
    methods: {
      ...mapActions({
          submit: 'team/submitTask'
      }),
      fileChange: function(e, f){
          this.taskData = f[0]
      },
      submitTask: function() {
          this.submit({
              task: this.task,
              data: this.taskData
          })
      },
    }
}
</script>
