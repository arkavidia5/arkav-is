<template>
  <v-container fluid fill-height>
    <v-layout align-center justify-center>
      <v-flex xs12 sm8 md4>
        <v-card class="elevation-3 pa-3">
          <v-card-text>
            <h1>Arkavidia 5</h1>
            <v-form class="mt-3" @submit.prevent="login">
              <v-text-field v-model="username" label="Username" autocomplete="username" required></v-text-field>
              <v-text-field v-model="password" label="Password" type="password" autocomplete="current-password" required></v-text-field>
              <v-alert v-for="error in errors" :key="error" :value="true" type="error" outline>
                {{ error }}
              </v-alert>
              <div class="my-3">
                <a href="#" class="body-link">Lupa password?</a>
              </div>
              <v-btn
                depressed
                large
                block
                color="primary"
                type="submit"
                :loading="loading"
                :disabled="loading"
              >
                Login
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
