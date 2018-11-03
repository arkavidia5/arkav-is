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
      Competitions,
  }
}
</script>
