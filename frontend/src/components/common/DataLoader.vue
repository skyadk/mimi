<template>
  <div class="text-center">
    <v-dialog
      v-model="$store.state.dataloader.dataload"
      hide-overlay
      persistent
      width="300"
    >
      <v-card color="#5C6BC0" dark>
        <v-card-text style="text-align: center;">
          빅데이터 분석중입니다.
          <v-progress-linear
            indeterminate
            color="white"
            class="mb-0"
          ></v-progress-linear>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
export default {
  methods: {
    aaa() {
      this.$store.commit('SET_DataLoader');
      setTimeout(() => (this.$store.state.dataloader.dataload = false), 4000);
    },
  },
  computed: {
    ...mapGetters(['getDataLoader']),
  },
  data() {
    return {
      dialog: false,
    };
  },

  watch: {
    dialog(val) {
      if (!val) return;

      setTimeout(() => (this.dialog = false), 4000);
    },
  },
};
</script>

<style>

</style>