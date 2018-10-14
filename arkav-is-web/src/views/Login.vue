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
              <div class="my-3">
                <a href="#" class="body-link">Lupa password?</a>
              </div>
              <v-btn depressed large block color="primary">Login</v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
  export default {
    data: () => ({
      username: '',
      password: '',
    })
  }
</script>
