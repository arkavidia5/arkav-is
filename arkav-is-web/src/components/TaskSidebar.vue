<template>
  <aside>
    <v-list class="transparent">
      <v-subheader class="text-uppercase">Registrasi</v-subheader>
  
      <v-list-tile @click="">
        <v-list-tile-action>
          <v-icon class="green--text">check_circle</v-icon>
        </v-list-tile-action>
        <v-list-tile-content class="pr-3">
          <v-list-tile-title class="body-2">Anggota Tim</v-list-tile-title>
        </v-list-tile-content>
      </v-list-tile>
  
      <v-list-tile @click="">
        <v-list-tile-action>
          <v-icon class="amber--text">hourglass_full</v-icon>
        </v-list-tile-action>
        <v-list-tile-content class="pr-3">
          <v-list-tile-title class="body-2">Bukti Perkuliahan</v-list-tile-title>
        </v-list-tile-content>
      </v-list-tile>
  
      <v-list-tile @click="">
        <v-list-tile-action>
          <v-icon class="red--text">error</v-icon>
        </v-list-tile-action>
        <v-list-tile-content class="pr-3">
          <v-list-tile-title class="body-2">Pembayaran</v-list-tile-title>
        </v-list-tile-content>
      </v-list-tile>
  
      <v-subheader class="text-uppercase">Penyisihan</v-subheader>
  
      <v-list-tile>
        <v-list-tile-action>
          <v-icon class="grey--text">radio_button_unchecked</v-icon>
        </v-list-tile-action>
        <v-list-tile-content class="pr-3">
          <v-list-tile-title class="body-2">Pengumpulan Makalah</v-list-tile-title>
        </v-list-tile-content>
      </v-list-tile>
  
      <v-list-tile>
        <v-list-tile-action>
          <v-icon class="grey--text">lock</v-icon>
        </v-list-tile-action>
        <v-list-tile-content class="pr-3">
          <v-list-tile-title class="body-2">Pengumpulan Kode Sumber</v-list-tile-title>
        </v-list-tile-content>
      </v-list-tile>
    </v-list>
  </aside>
</template>

<style scoped>
  .task-sidebar {
    max-width: 300px;
  }

  .task-sidebar .v-list__tile__action,
  .task-sidebar .v-list__tile__avatar {
    min-width: 36px;
  }
</style>