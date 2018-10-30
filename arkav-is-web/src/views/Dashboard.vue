<template>
    <div>
        <Competitions/>
    </div>
</template>
<script>
import {mapState, mapActions} from 'vuex'
import Competitions from '../components/Competitions'
export default {
    components: {
        Competitions
    },
    computed: {
      ...mapState({
        competitions: state => state.competitions.competitions
      })
    },
    methods: {
        ...mapActions({
            fetch: 'competition/getTeams'
        })
    }, 
    mounted: function() {
        this.fetch();   
    }
}
</script>
