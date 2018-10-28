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
              <h1 class="text-xs-center">Daftar</h1>
            </v-flex>
            
            
            <v-form class="mt-3" @submit.prevent="login">
              <v-text-field label="Nama Lengkap"></v-text-field>
              <v-text-field v-model="username" label="Username" autocomplete="username" required></v-text-field>
              <v-text-field v-model="school" label="Universitas/Sekolah"></v-text-field>
              <v-text-field v-model="password" label="Password" type="password" autocomplete="current-password" required></v-text-field>
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
      username: '',
      password: '',
    }),
    computed: {
      ...mapState({
        errors: state => state.auth.errors,
        loading: state => state.auth.loading
      })
    },
    methods: {
      ...mapActions({
        loginAction: 'auth/login'
      }),

      login() {
        this.loginAction({
          username: this.username,
          password: this.password,
          router: this.$router
        })
      }
    },
  }
</script>
