<template>
  <v-flex>
    <h2>{{ task.name }}</h2>
    <p>{{ task.widget_parameters }}</p>
    <br />
    
    <v-form @submit.prevent="submitResponse">
      <v-textarea label="Jawaban Anda" multi-line v-model="response">
        
      </v-textarea>
      <v-btn block color="primary" type="submit" :loading="loading">Submit</v-btn>
    </v-form>
    <v-flex v-if="taskResponse">
      <v-alert v-if="taskResponse.status === 'completed'"
       :value="true"
          type="success"
          outline
          >
        Jawaban anda telah diterima oleh panitia
      </v-alert>
      <v-alert v-else-if="taskResponse.status === 'awaiting_validation'"
          :value="true"
          type="info"
          outline
          >
        Jawaban anda akan segera divalidasi oleh panitia
      </v-alert>
      <v-alert v-else-if="taskResponse.status === 'cancelled'"           
          :value="true"
          type="error"
          outline>
        Jawaban anda ditolak oleh panitia
      </v-alert>
      
      
    </v-flex>
    
  </v-flex>
</template>

<script>
import { mapState, mapActions } from 'vuex'
export default {
  name: 'TextInputWidget',
  props: [
    "task", "team", "taskResponse"
  ],
  data: () => ({
    response: '',
  }),
  created: function() {
    if(this.taskResponse) {
      this.response = this.taskResponse.response;
    }
  },
  computed: {
    ...mapState({
      loading: state => state.team.loading
    })
  },
  methods: {
    ...mapActions({
      submitTaskResponseAction: 'team/submitTaskResponse',
    }),
 
    submitResponse: function() {
        this.submitTaskResponseAction({
          team_id: this.team.id,
          task_id: this.task.id,
          response: this.response,
        })
      },
  }
}
</script>

