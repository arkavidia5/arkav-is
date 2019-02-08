<template>
    <v-container>
        <template v-if="authorized">
            <v-layout class="row justify-center">
                    <img src="https://static.arkavidia.id/5/images/logo-full.svg" alt="" height="54">
            </v-layout>
            <v-form @submit.prevent="submitForm">
                <v-layout class="row justify-center">
                    <h1 class="heading">ArkavTalk Gate</h1>
                </v-layout>
                <v-layout class="row ">
                    <v-flex class="xs4 offset-xs4">
                        <v-select :items="items" label="Session" v-model="selected"></v-select>
                    </v-flex>
                </v-layout>
                <v-layout class="row">
                    <v-text-field  placeholder="Booking Number" v-model="booking_number" class="booking-input">

                    </v-text-field>
                </v-layout>
                <v-layout class="row justify-center">
                <v-btn color="primary" type="submit" :loading="loading" :disabled="loading">
                    Check In
                </v-btn>
                </v-layout>
            </v-form>
            <v-layout class="row">
                <v-flex>
                      <v-alert v-for="error in errors" :key="error" :value="true" type="error" outline>
                        {{ error }}
                      </v-alert>
                </v-flex>
            </v-layout>
            <v-layout class="row" v-if="userData.user">
                <v-flex class="xs10 offset-xs1 d-flex justify-center">
                    <table style="border: 1px solid black">
                        <tr>
                            <td>Name</td>
                            <td>:</td>
                            <td>{{userData.user.full_name}}</td>
                        </tr>
                        <tr>
                            <td>Email</td>
                            <td>:</td>
                            <td>{{userData.user.email}}</td>
                        </tr>
                        <tr>
                            <td>Register Session 1</td>
                            <td>:</td>
                            <td><v-icon color="green" v-if="userData.registrant.is_register_session_one">check</v-icon> <v-icon color="red" v-else>close</v-icon></td>
                        </tr>
                        <tr>
                            <td>Check In Session 1</td>
                            <td>:</td>
                            <td>{{userData.registrant.ticket.check_in_session_one}}</td>
                        </tr>
                        <tr>
                            <td>Register Session 2</td>
                            <td>:</td>
                            <td><v-icon color="green" v-if="userData.registrant.is_register_session_two">check</v-icon> <v-icon color="red" v-else>close</v-icon></td>
                        </tr>
                           <tr>
                            <td>Check In Session 2</td>
                            <td>:</td>
                            <td>{{userData.registrant.ticket.check_in_session_two}}</td>
                        </tr>
                    </table>
                </v-flex>
            </v-layout>
        </template>
        <template v-else>
            unauthorized access
        </template>
    </v-container>
</template>

<script>
  import { mapState, mapActions } from 'vuex'
    export default {
        name: "Gate",
        data: () => ({
            items: [1,2],
            selected: 0,
            booking_number: '',
        }),
        methods: {
          ...mapActions({
            ping: 'arkavtalk/ping',
            checkUser: 'arkavtalk/checkUser',
          }),
            submitForm: function(){
                this.checkUser({session: this.selected, booking_number: this.booking_number.toUpperCase()})
            }
        },
        computed: {
             ...mapState({
                authorized: state => state.arkavtalk.authorized,
                 loading: state => state.arkavtalk.loading,
                 errors: state => state.arkavtalk.errors,
                 userData: state => state.arkavtalk.userData,
              })
        },
        beforeMount: function(){
            this.ping()
        }
    }
</script>

<style>
    .booking-input {
        text-align: center !important;
    }
    .booking-input input {
        text-align: center;
        text-transform: uppercase;
    }
</style>