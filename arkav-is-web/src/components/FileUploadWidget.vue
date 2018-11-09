<template>
  <v-flex>
    <h2>{{ task.name }}</h2>
    <p>{{ task.widget_parameters }}</p>
    <br />
    <v-form @submit.prevent="submitResponse">
      <v-flex>
        <vue-dropzone
          ref="dropzone"
          id="dropzone"
          :options="dropOptions"
          @vdropzone-file-added="uploadFileAdded"
          @vdropzone-success="uploadSuccess"
          @vdropzone-error="uploadError"
          @vdropzone-complete="uploadComplete"
          v-if="team.competition.is_registration_open"
        />
        <v-alert v-if="dropzoneError" :value="true" type="error" outline>{{ dropzoneError }}</v-alert>
        <br />
        <div v-if="taskResponse">
          File berhasil diupload pada {{uploadTime}} -
          <a :href="downloadUrl" class="body-link" target="_blank">download <v-icon>cloud_download</v-icon></a>
        </div>
        <div v-else>Belum ada file yang diupload</div>

        <br />
        <v-alert
          v-if="taskResponse && taskResponse.status === 'rejected'"
          :value="true"
          type="error"
          outline
        >
          File yang Anda upload tidak memenuhi syarat. Silakan coba upload file lainnya, atau hubungi panitia untuk keterangan lebih lanjut.
        </v-alert>
        <v-alert
          v-if="taskResponse && taskResponse.status === 'awaiting_validation'"
          :value="true"
          type="info"
          outline
        >
          Panitia akan mengecek file yang Anda upload.
        </v-alert>
        <v-alert
          v-if="taskResponse && taskResponse.status === 'completed'"
          :value="true"
          type="success"
          outline
        >
          Panitia telah memverifikasi file yang ada upload.
        </v-alert>
      </v-flex>
    </v-form>
  </v-flex>
</template>

<script>
  import { mapState, mapActions } from 'vuex'
  import vueDropzone from 'vue2-dropzone'
  import moment from 'moment'
  import { apiConfig, getCsrfToken } from '../api.js'

  export default {
    name: 'FileUploadWidget',
    props: ['team', 'task', 'taskResponse'],
    components: {
      vueDropzone
    },
    watch: {
      task: function (newTask, oldTask) {
        if (newTask && oldTask && newTask.id !== oldTask.id) {
          // Reset the dropzone on task change
          this.$refs.dropzone.removeAllFiles(true)
        }
      }
    },
    data: function () {
      return {
        name: this.team.name,
        institution: this.team.institution,
        category: this.team.category,
        dropOptions: {
          url: apiConfig.baseURL + '/upload/',
          maxFiles: 1,
          acceptedFiles: 'image/*,application/pdf,application/zip,application/x-rar-compressed',
          withCredentials: apiConfig.withCredentials,
          maxFilesize: 10, // MB
          addRemoveLinks: true,
        },
        dropzoneError: null,
      }
    },
    computed: {
      ...mapState({
        loading: state => state.team.loading
      }),
      downloadUrl: function () {
        if (!this.taskResponse) return false
        return apiConfig.baseURL + '/upload/download/' + this.taskResponse.response + '/'
      },
      uploadTime: function () {
        if (!this.taskResponse) return false
        return moment(this.taskResponse.last_submitted_at).format('D MMMM YYYY, hh:mm:ss')
      }
    },
    methods: {
      ...mapActions({
        submitTaskResponseAction: 'team/submitTaskResponse',
      }),
      uploadFileAdded: function (file) {
        this.dropzoneError = null
      },
      uploadSuccess: function (file, response) {
        this.submitTaskResponseAction({
          team_id: this.team.id,
          task_id: this.task.id,
          response: response.id,
        })
      },
      uploadError: function (file, message, xhr) {
        this.dropzoneError = message
      },
      uploadComplete: function (file) {
        // Reset the dropzone
        this.$refs.dropzone.removeAllFiles(true)
      },
    },
    mounted: function () {
      // Read CSRF token
      this.$refs.dropzone.setOption(
        'headers',
        { [apiConfig.xsrfHeaderName || 'X-CSRFToken']: getCsrfToken() },
      )
    },
  }
</script>