<template>
   <div>
        <v-layout row>
            <label class="button" @click="$refs.fileInput.value = ''">
                <input type="file" multiple style="display:none" ref="fileInput" @input="uploadFiles">
            </label>
        </v-layout>
   </div>
</template>

<script>
export default {
    name: 'Widget',
    props: ['type']
}
</script>

<style>

</style>
