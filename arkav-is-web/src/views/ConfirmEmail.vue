<template>
  <v-container fluid fill-height>
    <v-layout align-center justify-center>
      <v-flex xs12 sm10 md4>
        <v-flex d-flex align-center justify-center mb-4>
          <v-flex text-xs-right>
            <img src="https://static.arkavidia.id/5/images/logo.svg" height=50 >
          </v-flex>
          <h1 class="ml-3 futura-bt bold primary--text">
            ARKAVIDIA 5.0
          </h1>
        </v-flex>
        <v-card class="elevation-3 pa-3">
          <v-card-text>
            <v-flex d-flex align-center justify-center>
              <h1 class="text-xs-center">Konfirmasi Pendaftaran</h1>
            </v-flex>
            <v-alert class="mt-3" :value="true" type="success" outline v-for="message in messages" :key="message">
              {{ message }}
            </v-alert>
            <v-alert class="mt-3" :value="true" type="error" outline v-for="error in errors" :key="error">
              {{ error }}
            </v-alert>
            <v-btn to="/login" block color="primary" class="mt-3">Login</v-btn>
            <div class="text-xs-center" v-if="loading">
              <v-progress-circular class="mt-3" indeterminate></v-progress-circular>
            </div>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
  import { mapState, mapActions } from 'vuex'

  export default {
    data: () => ({ }),
    computed: {
      ...mapState({
        errors: state => state.auth.errors,
        messages: state => state.auth.messages,
        loading: state => state.auth.loading
      })
    },
    methods: {
      ...mapActions({
        resetPasswordAction: 'auth/resetPassword',
        confirmEmailAction: 'auth/confirmEmail',
        clearErrorAndMessageAction: 'auth/clearErrorAndMessage',
      }),
    },
    beforeMount() {
      this.confirmEmailAction({
        token: this.$route.params.token,
        router: this.router,
      })
    },
    beforeRouteLeave(to, from, next) {
      this.clearErrorAndMessageAction()
      next()
    }
  }
</script>
