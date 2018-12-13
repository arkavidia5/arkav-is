<template>
    <div v-if="!loading">
        <v-layout row>
            <h2>Pertanyaan #{{page}}</h2>
        </v-layout>
        <template v-for="(i,index) in quiz.answers" v-if="index === page-1">
            <v-layout row quiz-question>
                {{i.question.description}}
            </v-layout>
            <v-layout>
                <v-radio-group v-model="answers[i.question.identifier]" :disabled="quiz.finish_time" v-on:change="intermediateSave">
                    <v-radio
                    v-for="item in i.question.selections"
                    :key="item.key"
                    :label="`${item.key_display}. ${item.value}`"
                    :value="item.key"
                    ></v-radio>
                </v-radio-group>

            </v-layout>
        </template>
        <v-layout row justify-center>
        <v-pagination
                v-model="page"
                :length="quiz.answers.length"
        ></v-pagination>
        </v-layout>
        <v-layout row>
            <v-flex xs6 offset-xs3>
                <v-btn block color="primary" @click="dialogBox = true" :disabled="quiz.finish_time">
                    Selesai
                </v-btn>
            </v-flex>
        </v-layout>
        <v-dialog
          v-model="dialogBox"
          max-width="400"

        >
          <v-card>
              <v-card-title>
                <v-card-title class="headline">Apakah anda yakin?</v-card-title>
                        <v-card-text>
                            Jawaban yang telah disimpan tidak dapat diganti.
                        </v-card-text>

              </v-card-title>
            <v-card-actions>
                <v-btn  @click="dialogBox = false" flat color="primary">
                    Cek Lagi
                </v-btn>
                <v-spacer></v-spacer>
                <v-btn  @click="submitForm" flat color="primary">
                    Selesai
                </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
    </div>
    <div v-else>
        <v-layout class="row justify-center">
            <v-progress-circular
              indeterminate
              color="primary"
            ></v-progress-circular>
        </v-layout>

    </div>

</template>

<script>
import {mapState, mapActions} from 'vuex';
export default {
    name: 'CodingClassOnlineTest',
    data: () => ({
        page: 1,
        answers: {},
        dialogBox: false,
    }),
    computed: {
        ...mapState({
            quiz: state => state.codingclass.quiz,
            loading: state => state.codingclass.loading,
        })
    },
    methods: {
        ...mapActions({
            getRegistrationData: 'codingclass/getRegistrationData',
            getQuiz: 'codingclass/getQuiz',
            quickSave: 'codingclass/quickSave',
            finish: 'codingclass/finish'
        }),
        updateData: function(){
            this.quiz.answers.forEach((e) => {
               this.answers[e.question.identifier] = e.answer
            });
        },
        intermediateSave: function(ans) {
            let id = this.quiz.answers[this.page-1].question.identifier
            this.quickSave({identifier: id, answer: ans})
        },
        submitForm: function() {
            this.dialogBox = false;
            let data = []
            Object.keys(this.answers).forEach((key) => {
                let value = this.answers[key];
                data.push({identifier: key, answer: value})
            });
            this.finish(data)
            this.getRegistrationData()
        }
    },
    beforeMount: function(){
        this.getQuiz()
    },
    watch: {
        quiz: function(val) {
            this.updateData()
        }
    }
}
</script>

<style scoped>
    .quiz-question {
        font-size: 1.2rem;
    }
</style>
