<template>
    <v-container>
        <v-form @submit.prevent="registerCodingClass">
        <h3>Informasi Pribadi</h3>
            <v-layout class="row wrap" pa-2>
                <v-text-field label="Nama Lengkap" disabled :value="user.full_name"/>
            </v-layout>
            <v-layout row pa-2  >
                <v-text-field label="Email" disabled :value="user.email" landscape="true"/>
            </v-layout>

        <!--<h3>Informasi Tambahan</h3>-->
            <v-layout class="row wrap align-center">
                <v-flex class="md4 sm6 xs12 pa-2 d-flex justify-center align-center">
                    <v-text-field
                        required
                        label="Tanggal Lahir"
                        v-model="birthday"
                        :rules="notNull"
                        lazy-validation = true
                    ></v-text-field>
                    <v-btn icon @click="datepicker = true">
                        <v-icon>calendar_today</v-icon>
                    </v-btn>
                </v-flex>
                <v-flex class="md6 sm6 xs12 offset-md2 pa-2">
                    <v-text-field required label="Kota Tempat Tinggal" v-model="domicile" :rules="notNull">
                    </v-text-field>
                </v-flex>
            </v-layout>

        <v-layout class="row wrap">
            <v-flex pa-2 xs12 md6>
            <v-text-field required label="Asal Sekolah" v-model="school" :rules="notNull" >

            </v-text-field>
            </v-flex>
            <v-flex pa-2 xs12 md6>
            <v-text-field required label="Kelas dan Jurusan (contoh: XII IPA)" v-model="grade" :rules="notNull" >

            </v-text-field>
            </v-flex>
        </v-layout>
            <a :href="getDownloadURL()" target="_blank" class="no-decoration" v-if="this.student_card">
            <h4 align="center" class="primary--text">
                Kartu Pelajar
                <sup >
                <v-icon style="font-size: 1rem">
                    open_in_new
                </v-icon>
                </sup>
            </h4>
            </a>
            <h4 align="center" class="primary--text" v-else>
                Kartu Pelajar
            </h4>
        <v-layout class="row mb-4">
            <v-flex xs8 offset-xs2>
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

        </v-layout>

        <v-btn color="primary" block type="submit" :loading="loading" :disabled="loading || !isOpen">
            Daftar
        </v-btn>
            <v-layout>
                <v-flex xs2 offset-xs5>
                <v-alert color="success" value="true" outline v-if="success" icon="check">
                    Success!
                </v-alert>
                </v-flex>
            </v-layout>

        </v-form>
        <v-dialog
          v-model="datepicker"
          max-width="290"
        >
          <v-card>
            <v-date-picker v-model="birthday"></v-date-picker>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" @click="datepicker = false">
                    Done
                </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
    </v-container>


</template>

<script>
import vueDropzone from 'vue2-dropzone'
import { apiConfig, getCsrfToken } from '../api.js'

import {mapState,mapActions} from 'vuex';
  export default {
    props: ['visible', 'registrationData'],
    components: {
      vueDropzone
    },

    data: () => ({
        menu: '',
        formatted: '',
        birthday: '',
        datepicker: false,
        school: '',
        domicile: '',
        grade: '',
        notNull: [v => !!v || 'Tidak Boleh Kosong'],
         dropOptions: {
          url: apiConfig.baseURL + '/upload/',
          maxFiles: 1,
          acceptedFiles: 'image/*,application/pdf,application/zip,application/x-rar-compressed',
          withCredentials: apiConfig.withCredentials,
          maxFilesize: 10, // MB
          addRemoveLinks: true,
        },
        dropzoneError: null,
        student_card: ''
    }),
    methods: {
      ...mapActions({
        register: 'codingclass/register',
      }),
        registerCodingClass: function(){
          console.log('Register..')
            this.register({
                birthday: this.birthday,
                school: this.school,
                domicile: this.domicile,
                grade: this.grade,
                student_card: this.student_card
            })
        },
        getDownloadURL: function() {
          return apiConfig.baseURL + '/upload/download/' + this.student_card + '/'
        },
        refreshData: function() {
          if(this.registrationData.birthday)
            this.birthday = this.registrationData.birthday;
          if(this.registrationData.domicile)
            this.domicile = this.registrationData.domicile;
          if(this.registrationData.school)
            this.school = this.registrationData.school;
          if(this.registrationData.grade)
            this.grade = this.registrationData.grade;
          if(this.registrationData.student_card)
            this.student_card = this.registrationData.student_card;
        },
         uploadFileAdded: function (file) {
            this.dropzoneError = null
          },
          uploadSuccess: function (file, response) {
            this.student_card = response.id
              console.log(response.id)
          },
          uploadError: function (file, message, xhr) {
            this.dropzoneError = message
          },
          uploadComplete: function (file) {
            // Reset the dropzone
            // this.$refs.dropzone.removeAllFiles(true)
          },
    },
    computed: {
        ...mapState({
            user: state => state.auth.user,
            loading: state => state.codingclass.loading,
            error: state => state.codingclass.error,
            success: state => state.codingclass.success,
            isOpen: state => state.codingclass.isOpen
        }),
    },
    mounted: function(){
        this.refreshData();
        this.$refs.dropzone.setOption(
            'headers',
            { [apiConfig.xsrfHeaderName || 'X-CSRFToken']: getCsrfToken() },
        )
    },
    watch: {
        registrationData: function(val) {
            this.refreshData();
        }
    }
  }
</script>

<style scoped>
</style>
