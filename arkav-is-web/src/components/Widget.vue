<template>
   <div :id="task.id">
       <v-form @submit.prevent="submitTask"> 
       <v-container v-if="task.widget == 'file_upload'">
           <v-flex>
           <input type="file" style="display: none" :id="`uploader-${task.id}`" accept="image/jpg, image/png, .pdf" @change="fileChange($event.target.name, $event.target.files)" :disabled="saving">
            <label :for="`uploader-${task.id}`" class="v-btn large primary theme--light white--text cursor-pointer" color="primary" v-bind:class="{'v-btn--disabled': saving}"> 
                <v-icon color="white">insert_drive_file</v-icon>
                Upload
            </label>
            {{taskData.name}}
           </v-flex>
       </v-container>
        <v-layout row justify-center>
            <v-flex md4>
            <v-btn large block color="primary" :loading="saving" type="submit">
                submit
            </v-btn>
            </v-flex>
        </v-layout>
       </v-form>
            
   </div>
</template>

<script>
import {mapState, mapActions} from 'vuex'
export default {
    name: 'Widget',
    props: ['task'],
    data: () => ({
        taskData: '',
    }),
    computed: {
        ...mapState({
            saving: state => state.team.saving
        })
    },
    methods: {
        ...mapActions({
            submit: 'team/submitTask'
        }),
        fileChange: function(e, f){
            this.taskData = f[0]
        },
        submitTask: function() {
            this.submit({
                task: this.task, 
                data: this.taskData
            })
        },
    }
}
</script>
