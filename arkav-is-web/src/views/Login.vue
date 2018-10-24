<template>
  <v-container fluid fill-height>
    <v-layout align-center justify-center>
      <v-flex xs12 sm8 md4>
        <v-card class="elevation-3 pa-3">
          <v-card-text>
            <h1>Arkavidia 5</h1>
            <v-form class="mt-3">
              <v-text-field v-model="username" label="Username" required></v-text-field>
              <v-text-field v-model="password" label="Password" type="password" required></v-text-field>
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
                :loading="loading"
                :disabled="loading"
                @click="login"
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

      async login() {
        await this.loginAction({
          username: this.username,
          password: this.password
        })
      }
    },
  }
</script>
