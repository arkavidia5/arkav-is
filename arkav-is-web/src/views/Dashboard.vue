<template>
    <div>
        <v-card></v-card>
    </div>
</template>
<script>
import {mapState, mapActions} from 'vuex'
export default {
    computed: {
      ...mapState({
        competitions: state => state.competitions.competitions
      })
    },
    methods: {
        ...mapActions({
            fetch: 'competition/fetch_competitions'
        })
    }, 
    mounted: function() {
        this.fetch();   
    }
}
</script>
