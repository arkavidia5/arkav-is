<template>
  <v-container fluid fill-height>
    <v-layout align-center justify-center>
      <v-flex xs12 sm8 md4>
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
              <h1 class="text-xs-center">Reset Password</h1>
            </v-flex>

            <v-form class="mt-3" @submit.prevent="tryResetPassword" v-if="messages.length === 0">
              <v-text-field v-model="email" label="Email" autocomplete="username" required></v-text-field>
              <v-alert v-for="error in errors" :key="error" :value="true" type="error" outline>
                {{ error }}
              </v-alert>
              <v-btn
                depressed
                large
                block
                color="primary"
                type="submit"
                :loading="loading"
                :disabled="loading"
                v-if="messages.length === 0"
              >
                Kirim link reset password
              </v-btn>
            </v-form>

            <v-alert v-for="message in messages" :key="message" :value="true" type="success" outline class="mt-3">
              {{ message }}
            </v-alert>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
  import { mapState, mapActions } from 'vuex'

  export default {
    data: () => ({
      email: '',
    }),
    computed: {
      ...mapState({
        errors: state => state.auth.errors,
        messages: state => state.auth.messages,
        loading: state => state.auth.loading
      })
    },
    methods: {
      ...mapActions({
        tryResetPasswordAction: 'auth/tryResetPassword',
        clearErrorAndMessageAction: 'auth/clearErrorAndMessage',
      }),

      tryResetPassword() {
        this.tryResetPasswordAction({
          email: this.email,
          router: this.$router
        })
      }
    },
    beforeRouteLeave(to, from, next) {
      this.clearErrorAndMessageAction()
      next()
    }
  }
</script>
