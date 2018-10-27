<template>
  <nav class="navbar">
    <div class="logo">Arkavidia</div>
    <ul>
      <li><router-link to="/competitions" class="body-link hover-only">Lomba</router-link></li>
      <li><router-link to="/seminar" class="body-link hover-only">Seminar</router-link></li>
      <li>
        <v-menu offset-y>
          <a slot="activator" href="#" class="body-link hover-only">
            {{ user.username }}<v-icon style="float: right">arrow_drop_down</v-icon>
          </a>
          <v-list>
            <v-list-tile @click="logout">
              <v-list-tile-title>Logout</v-list-tile-title>
            </v-list-tile>
          </v-list>
        </v-menu>
      </li>
    </ul>
  </nav>
</template>

<script>
  import { mapState, mapActions } from 'vuex'

  export default {
    data: () => ({

    }),
    computed: mapState({
      user: state => state.auth.user,
    }),
    methods: {
      ...mapActions({
        logoutAction: 'auth/logout'
      }),

      logout() {
        this.logoutAction({ router: this.$router })
      }
    }
  }
</script>

<style scoped>
  .navbar {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    flex-wrap: wrap;
    margin-bottom: 24px;
  }

  .logo {
    margin-right: 16px;
  }

  .navbar > ul {
    display: flex;
    list-style: none;
    flex-wrap: wrap;
    padding: 0;
  }

  .navbar > ul > li {
    margin-right: 2.4vw;
  }

  .navbar > ul > li:last-child {
    margin-right: 0;
  }

  .navbar > ul > li a {
    font-weight: bold;
    font-size: 16px;
    color: #555;
  }

  .logo {
    font-weight: bold;
    text-transform: uppercase;
    font-size: 20px;
  }
</style>