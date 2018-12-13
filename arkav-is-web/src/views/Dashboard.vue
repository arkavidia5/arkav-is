<template>
    <div class="dashboard">
        <Competitions/>
        <Preevent/>
    </div>
</template>
<script>
import {mapState, mapActions} from 'vuex'
import Competitions from '../components/Competitions'
import Preevent from '../components/Preevent'
export default {
  components: {
      Competitions,
      Preevent
  }
}
</script>
<style scoped>

</style>

