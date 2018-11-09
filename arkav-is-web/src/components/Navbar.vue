<template>
  <!-- <v-menu class="navbar">
    <div class="logo d-flex align-center">
      <img src="https://static.arkavidia.id/5/images/logo.svg" height=40>
      <span class="title">ARKAVIDIA 5.0 </span>
    </div>
    <ul>
      <li><router-link to="/competitions" class="body-link hover-only">Lomba</router-link></li>
      <li><router-link to="/seminar" class="body-link hover-only">Seminar</router-link></li>
      <li>
        <v-menu offset-y>
          <a slot="activator" href="#" class="body-link hover-only">
            {{ user.email }}<v-icon style="float: right">arrow_drop_down</v-icon>
          </a>
          <v-list>
            <v-list-tile @click="logout">
              <v-list-tile-title>Logout</v-list-tile-title>
            </v-list-tile>
          </v-list>
        </v-menu>
      </li>
    </ul>
  </v-menu> -->
  <v-toolbar fixed flat toolbar color="primary" class="navbar" dark style="z-index: 999">
    <v-toolbar-title>
        <router-link to="/" style="text-decoration: none;">
          <div class="logo d-flex align-center my-3">
            <img src="https://static.arkavidia.id/5/images/logo.svg" height="36">
            <span class="white--text ml-3">ARKAVIDIA 5.0</span>
          </div>
        </router-link>
    </v-toolbar-title>
    <v-spacer></v-spacer>
    <router-link to="/">
      <v-btn flat >Home</v-btn>
    </router-link>
    <v-menu flat offset-y>
      <v-btn flat slot="activator">
        {{user.full_name}}
        <v-icon>arrow_drop_down</v-icon>
      </v-btn>
      <v-list>
        <v-list-tile @click="logout">
          <v-list-tile-title>Logout</v-list-tile-title>
        </v-list-tile>
      </v-list>
    </v-menu>

  </v-toolbar>
</template>

<script>
  import { mapState, mapActions } from 'vuex'

  export default {
    data: () => ({
      name: 'Dev'
    }),
    computed: mapState({
      user: state => state.auth.user,
    }),
    methods: mapActions({
      logout: 'auth/logout'
    }),
  }
</script>

<style scoped>
  .logo {
    font-weight: bold;
    text-transform: uppercase;
    font-size: 20px;
  }
</style>
