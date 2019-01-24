<template>
  <v-card class="elevation-3" v-if="true">
    <header class="task-header px-4 py-3">
      <v-btn flat icon color="gray" class="ma-0 mr-3" v-show="shouldCollapseSidebar" @click.native="sidebarActive = !sidebarActive">
        <v-icon>menu</v-icon>
      </v-btn>
      <v-layout row align-center>
        <img src="https://static.arkavidia.id/5/images/icons/seminar.svg" alt="" height="50" class="mr-3" v-show="!shouldCollapseSidebar">
        <div>
          <h2 class="display-1 font-weight-bold">ArkavTalk</h2>
          <!--<div class="caption font-weight-bold primary&#45;&#45;text">Umum</div>-->
        </div>
      </v-layout>
    </header>

    <div class="task-container">
        <section class="task-content px-4 py-3" v-show="!shouldCollapseSidebar || !sidebarActive">
          <div class="ticket-purchase">
          <h1 class="title primary--color">Pemesanan Tiket </h1>
                <v-alert v-for="error in errors" :key="error" :value="true" type="error" outline>
                {{ error }}
              </v-alert>
              <v-list
                subheader
                three-line
              >
                <v-list-tile @click="">
                  <v-list-tile-action>
                    <v-checkbox v-if="!registrationData || editOrder"
                      v-model="is_register_session_one"
                    ></v-checkbox>
                    <v-checkbox v-else
                      v-model="registrationData.is_register_session_one"
                      disabled
                    ></v-checkbox>

                  </v-list-tile-action>

                  <v-list-tile-content @click.prevent="is_register_session_one = !is_register_session_one">
                    <v-list-tile-title>Sesi 1 (08.30 - 11.25 WIB)</v-list-tile-title>
                    <v-list-tile-sub-title>{{format(configuration.session_one_normal_price)}} <br> Tersisa {{configuration.session_one_current_capacity}} tiket</v-list-tile-sub-title>
                  </v-list-tile-content>
                </v-list-tile>

                <v-list-tile @click="">
                  <v-list-tile-action>
                      <v-checkbox v-if="!registrationData || editOrder"
                      v-model="is_register_session_two"
                    ></v-checkbox>
                    <v-checkbox v-else
                      v-model="registrationData.is_register_session_two"
                      disabled
                    ></v-checkbox>
                  </v-list-tile-action>

                  <v-list-tile-content @click.prevent="is_register_session_two = !is_register_session_two">
                  <v-list-tile-title>Sesi 2 (12.15 - 16.45 WIB)</v-list-tile-title>
                    <v-list-tile-sub-title>{{format(configuration.session_two_price)}} <br> Tersisa {{configuration.session_two_current_capacity}} tiket</v-list-tile-sub-title>
                  </v-list-tile-content>
                </v-list-tile>
              </v-list>
            <v-layout class="row justify-end">
                <h3 v-if="!registrationData || editOrder">
                  {{format(is_register_session_one*configuration.session_one_normal_price + is_register_session_two*configuration.session_two_price)}}
                </h3>
                <h3 v-else>
                  {{format(registrationData.is_register_session_one*configuration.session_one_normal_price + registrationData.is_register_session_two*configuration.session_two_price)}}
                </h3>
            </v-layout>
            <v-layout class="row justify-end">
          <v-btn color="primary" class="" @click="submitForm" v-if="!registrationData || editOrder" :loading="loading">Pesan</v-btn>
              <v-btn color="primary" class="" @click="editOrder = !editOrder" v-if="registrationData && !editOrder && registrationData.status != 2" :loading="loading">Ubah Pesanan</v-btn>
            </v-layout>
            </div>
            <div class="payment-receipt" v-if="registrationData">
              <h1 class="title primary--color">Bukti Pembayaran</h1>
               <div>
                 Pembayaran dapat dilakukan dengan melakukan Bank Transfer ke 90012355185 (BTPN a/n Rinda Nur Hafizha) atau Cashtag $rindanrh
               </div>
              <br>
               <v-flex xs8 offset-xs2 v-show="registrationData.status < 1 || editPayment">
                <vue-dropzone
                  ref="dropzone"
                  id="dropzone"
                  :options="dropOptions"
                  @vdropzone-file-added="uploadFileAdded"
                  @vdropzone-success="uploadSuccess"
                  @vdropzone-error="uploadError"
                  @vdropzone-complete="uploadComplete"
                />
                </v-flex>
                <v-flex v-if="registrationData.status >= 1 && !editPayment">
                    <span>
                        Bukti Pembayaran anda: <a :href="getDownloadURL()" target="_blank">Download</a>
                    </span>
                    <v-layout class="row">
                        <v-btn color="primary" v-if="registrationData.status != 2" @click="editPayment = !editPayment">Ubah Bukti Pembayaran</v-btn>
                    </v-layout>
                    <v-alert :value="true"  type="info" outline v-if="registrationData.status < 2">
                        Menunggu validasi dari panitia
                    </v-alert>
                </v-flex>
            </div>
            <br>
            <div v-if="registrationData.status == 2">
                <h1 class="title primary--color">Tiket ArkavTalk:</h1>
                <v-layout class="row">
                    <v-flex>
                        Silahkan tunjukkan nomor ini kepada panitia registrasi acara.
                    </v-flex>
                </v-layout>
                <v-layout class="row justify-center">
                    <h1 align="center">{{registrationData.ticket.booking_number}}</h1>
                </v-layout>
            </div>
            <div v-if="registrationData.status == 3">
                <v-alert :value="true"  type="error" outline v-if="registrationData.status != 2">
                    Mohon Maaf pesanan anda telah dibatalkan oleh panitia
                </v-alert>
            </div>
        </section>

    </div>

  </v-card>
  <v-layout v-else-if="loading" row justify-center>
     <v-progress-circular
      indeterminate
      color="primary"
    ></v-progress-circular>
  </v-layout>
  <v-layout v-else-if="errors">
      <v-alert v-for="error in errors" :key="error" :value="true" type="error" outline>
        {{error}}
      </v-alert>
  </v-layout>
</template>

<script>
  import vueDropzone from 'vue2-dropzone'
  import { mapState, mapActions } from 'vuex'
  import { apiConfig, getCsrfToken } from '../api.js'
  import FileUploadWidget from "../components/FileUploadWidget";
  export default {
    components: {
        FileUploadWidget,
        vueDropzone,
    },
    data() {
      return {
        is_register_session_one: false,
        is_register_session_two: false,
        editPayment: false,
        dropOptions: {
          url: apiConfig.baseURL + '/upload/',
          maxFiles: 1,
          acceptedFiles: 'image/*,application/pdf,application/zip,application/x-rar-compressed',
          withCredentials: apiConfig.withCredentials,
          maxFilesize: 10, // MB
          addRemoveLinks: true,
        },
        editOrder: false,
        dropzoneError: null,
      }
    },
    computed: {
      ...mapState({
        loading: state => state.seminar.loading,
        errors: state => state.seminar.errors,
        registrationData: state => state.seminar.registrationData,
        configuration: state => state.seminar.configuration,

      }),
      shouldCollapseSidebar() {
        return this.$vuetify.breakpoint.smAndDown
      },
    },
    methods: {
      ...mapActions({
        register: 'seminar/register',
        pay: 'seminar/uploadPaymentReceipt',
        getRegistrationData: 'seminar/getRegistrationData',
        getSeminarConfiguration: 'seminar/getConfiguration',
      }),
      format: function(x) {
          const formatter = new Intl.NumberFormat('id-ID', {
              style: 'currency',
              currency: 'IDR',
              minimumFractionDigits: 2
          });
          return formatter.format(x)
      },
     uploadFileAdded: function (file) {
        this.dropzoneError = null
      },
      uploadSuccess: function (file, response) {
        this.pay(response.id)
      },
      uploadError: function (file, message, xhr) {
        this.dropzoneError = message
      },
      uploadComplete: function (file) {
        // Reset the dropzone
        this.$refs.dropzone.removeAllFiles(true)
      },
        getDownloadURL: function() {
          return apiConfig.baseURL + '/upload/download/' + this.registrationData.payment_receipt + '/'
        },
        submitForm: function() {
          // console.log(this.is_register_session_one);
          // console.log(this.is_register_session_two)
          this.register({is_register_session_one: this.is_register_session_one, is_register_session_two: this.is_register_session_two})
        }
    },
    beforeMount: function () {
        this.getSeminarConfiguration()
        this.getRegistrationData();
    },
    watch: {
        registrationData: function(val) {
            this.is_register_session_one = val.is_register_session_one;
            this.is_register_session_two = val.is_register_session_two;
        }
    },
    mounted: function(){
      this.$refs.dropzone.setOption(
        'headers',
        { [apiConfig.xsrfHeaderName || 'X-CSRFToken']: getCsrfToken() },
      )
    }

  }
</script>

<style scoped>
  .task-header {
    border-bottom: solid 1px #eee;
    display: flex;
    align-items: center;
  }    bg</v-flex>bg

  .task-sidebar {
    z-index: 99;
    flex: 1;
  }

  .task-container {
    display: flex;
    flex: 1
  }

  .task-content {
    flex: 3;
  }

  .task-content.slide-x-transition-leave-active {
    position: absolute;
  }

  .task-sidebar .v-list__tile__action,
  .task-sidebar .v-list__tile__avatar {
    min-width: 36px;
  }
</style>
