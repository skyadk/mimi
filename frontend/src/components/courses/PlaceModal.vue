<template>
  <div class="backimg" id="container" >
    <br />
    <v-card width="90%" height="90%" style="margin: 5% 5% 5% 5%; border-radius: 30px;">
      <template>
        <br>
        <v-img
          :src="`https://j4d108.p.ssafy.io/landphoto/${placeModal.lid}.png`"
          width="70%"
          style="margin-left: 15%; border-radius: 30px;"
        ></v-img>
        <v-card-title>
          {{ placeModal.landmark_name }}
        </v-card-title>
        <v-card-text>
          <div>
            <p>{{ placeModal.tel }}</p>
            <p>{{ placeModal.addr }}</p>
            <p>{{ placeModal.desc }}</p>
          </div>
          <br>
        </v-card-text>
      </template>
      <v-card-actions>
        <v-row justify="center">
          <v-btn color="black" text plain @click="$emit('close-modal')">
            닫기
          </v-btn>
        </v-row>
      </v-card-actions>
    </v-card>
    <br>
  </div>
</template>

<script>
export default {
  props: {
    placeModal: Object,
  },
};
</script>

<style scoped>
.backimg {
  background-color: #dbdbdb;
}
</style>
