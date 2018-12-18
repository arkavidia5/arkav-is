<template>
    <div v-if="!loading">
        <template v-if="page > 0">
        <v-layout row>
            <h2>Pertanyaan #{{page}}</h2>
        </v-layout>
        <template v-for="(i,index) in quiz.answers" v-if="index === page-1">
            <pre row quiz-question v-html="i.question.description"></pre>
            <v-layout>
                <v-radio-group :key="i.question.identifier" v-model="answers[i.question.identifier]" v-on:change="intermediateSave" :disabled="!!quiz.finish_time">
                    <v-radio
                    v-for="item in i.question.selections"
                    :key="`${i.question.identifier}:${item.key}`"
                    :value="item.key"
                    style="display: flex !important; align-items: start;"
                    >
                      <template slot="label" class="radio-label">
                          <v-layout class="row align-start">
                          <pre class="mr-1">{{item.key_display}}.</pre>
                          <pre v-html="item.value"></pre>
                          </v-layout>
                      </template>
                    </v-radio>
                </v-radio-group>

            </v-layout>
        </template>

        <v-layout row justify-center>
        <button class="v-pagination__item" :active="true" style="margin-left: -34px;" :class="{'v-pagination__item--active primary white--text': page==0}" @click="page = 0">
            Tut
        </button>
        <v-pagination
                v-model="page"
                :length="quiz.answers.length"
        ></v-pagination>
        </v-layout>
        <v-layout row>
            <v-flex xs6 offset-xs3>
                <v-btn block color="primary" @click="dialogBox = true" :disabled="!!quiz.finish_time">
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
        </template>
         <template v-else>
            <h1>
            PETUNJUK PENGERJAAN
            </h1>
            <v-flex xs8>
            Test ini bertujuan untuk menilai kemampuan logika peserta dengan bahasa pemrograman python-like dan pengetahuan umum berkaitan HTML dan CSS. Untuk test akan terdiri dari pilihan ganda. Peserta diharapkan memilih jawaban yang benar diantara pilihan jawaban yang disediakan. Berikut tutorial singkat pengerjaan soal dengan bahasa yang akan digunakan:
            </v-flex>
            <v-flex class="xs12">
                <a href="../assets/onlinetesttut.jpg" target="_blank">
                <img src="../assets/onlinetesttut.jpg" alt="" height="527" >
                </a>
            </v-flex>
             <v-btn block color="primary" @click="page = 1">
                 Mulai test
             </v-btn>
        </template>
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
        page: 0,
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
