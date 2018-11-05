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
              <h1 class="text-xs-center">Daftar</h1>
            </v-flex>

            <v-form class="mt-3" @submit.prevent="register" v-if="messages.length === 0">
              <v-text-field label="Name" v-model="full_name"></v-text-field>
              <v-text-field label="Email" type="mail" required :rules="emailRules" v-model="email"></v-text-field>
              <v-text-field v-model="password" label="Password" type="password" autocomplete="current-password" required></v-text-field>
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
                Daftar
              </v-btn>
              <router-link to="/login" class="body-link">
                Sudah punya akun? Daftar disini
              </router-link>
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
      full_name: '',
      email: '',
      password: '',
      confirm_password: '',
      emailRules: [
          (v) => !!v || 'E-mail is required',
          (v) => /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(v) || 'E-mail must be valid'
      ],
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
        registerAction: 'auth/register',
        clearErrorAndMessageAction: 'auth/clearErrorAndMessage',
      }),

      register() {
        this.registerAction({
          full_name: this.full_name,
          email: this.email,
          password: this.password,
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
