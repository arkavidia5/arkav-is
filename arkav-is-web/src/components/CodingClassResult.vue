<template>
    <v-layout v-if="registrationData.status === 4" row wrap>
        <v-flex xs12 d-flex justify-center>
            <v-icon color="success" style="font-size: 5rem;">
                check_circle
            </v-icon>
        </v-flex>
        <v-flex xs12 d-flex justify-center style="font-size: 2rem" success--text>
            Selamat anda lolos
        </v-flex>
    </v-layout>
    <v-layout v-else="registrationData.status === 5" row wrap>
        <v-flex xs12 d-flex justify-center>
            <v-icon color="error" style="font-size: 5rem;">
                error
            </v-icon>
        </v-flex>
        <v-flex xs12 d-flex justify-center style="font-size: 2rem" error--text>
            Mohon maaf anda tidak lulus
        </v-flex>
    </v-layout>
</template>
<script>
    export default {
        name: 'CodingClassResult',
        props: ['registrationData']
    }
</script>