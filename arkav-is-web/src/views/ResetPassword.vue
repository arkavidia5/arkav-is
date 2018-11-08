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
              <h1 class="text-xs-center">Reset Password</h1>
            </v-flex>
            <v-alert class="mt-3" :value="true" type="success" outline v-if="messages.length > 0">
              Password Anda berhasil di-reset.
              <router-link to="/login" class="body-link">
                Klik disini untuk login.
              </router-link>
            </v-alert>
            <v-form class="mt-3" @submit.prevent="resetPassword" v-if="messages.length === 0" :key="true">
              <v-text-field v-model="password" label="Password" type="password" required></v-text-field>
              <v-text-field v-model="confirm_password" label="Confirm Password" type="password" required :rules="[(v) => !!v || 'Confirm Password cannot be empty', (v) => v === password || 'Password does not match']"></v-text-field>
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
              >
                Reset
              </v-btn>
            </v-form>
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
      password: '',
      confirm_password: '',
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
        resetPasswordAction: 'auth/resetPassword',
        clearErrorAndMessageAction: 'auth/clearErrorAndMessage',
      }),

      resetPassword() {
        this.resetPasswordAction({
          token: this.$route.params.token,
          new_password: this.password,
          router: this.$router
        })
      }
    },
    beforeRouteLeaveAction(to, from, next) {
      this.clearErrorAndMessageAction()
      next()
    }
  }
</script>
