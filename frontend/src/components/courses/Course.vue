<template>
  <div class="my-7">
    <v-row class="pa-0" justify="center" no-gutters>
      <!-- 첫번째 관광지 -->
      <v-col cols="2" v-if="recommend[0]['lid'] != 'NULL'" @click.stop="dialog1 = true">
        <v-row class="flex-column">
          <v-col class="d-flex justify-center pa-0">
            <v-img class="align-center" src="@/assets/pin1.png" max-width="30"></v-img>
          </v-col>
          <v-col class="pa-0">
            <div class="text-center text-truncate" style="font-size: 15px;">{{ recommend[0].landmark_name }}</div>
          </v-col>
        </v-row>
      </v-col>
      <v-dialog v-model="dialog1" width="80%" id="container" >
        <v-card>
          <PlaceModal :placeModal="recommend[0]" @close-modal="dialog1 = false"></PlaceModal>
        </v-card>
      </v-dialog>
      <!-- 첫번째 - 두번째 관광지 사이 거리 -->
      <v-col cols="1" v-if="recommend[4].one_two != 'NULL'">
        <p style="font-size: 0.75rem">{{ recommend[4].one_two }}km</p>
        <!-- <v-img src="@/assets/line.png"></v-img> -->
      </v-col>
      <!-- 두번째 관광지 -->
      <v-col cols="2" v-if="recommend[1]['lid'] != 'NULL'" @click.stop="dialog2=true">
        <v-row class="flex-column">
          <v-col class="d-flex justify-center pa-0">
            <v-img class="align-center" src="@/assets/pin2.png" max-width="30"></v-img>
          </v-col>
          <v-col class="pa-0">
            <div class="text-center text-truncate" style="font-size: 15px;">{{ recommend[1].landmark_name }}</div>
          </v-col>
        </v-row>
      </v-col>
      <v-dialog v-model="dialog2" width="80%" id="container" >
        <v-card>
          <PlaceModal :placeModal="recommend[1]" @close-modal="dialog2=false"></PlaceModal>
        </v-card>
      </v-dialog>
      <!-- 두번째 - 세번째 관광지 사이 거리 -->
      <v-col cols="1" v-if="recommend[4].two_three != 'NULL'">
        <p style="font-size: 0.75rem">{{ recommend[4].two_three }}km</p>
        <!-- <v-img src="@/assets/line.png"></v-img> -->
      </v-col>
      <!-- 세번째 관광지 -->
      <v-col cols="2" v-if="recommend[2]['lid'] != 'NULL'" @click.stop="dialog3=true">
        <v-row class="flex-column">
          <v-col class="d-flex justify-center pa-0">
            <v-img class="align-center" src="@/assets/pin3.png" max-width="30"></v-img>
          </v-col>
          <v-col class="pa-0">
            <div class="text-center text-truncate" style="font-size: 15px;">{{ recommend[2].landmark_name }}</div>
          </v-col>
        </v-row>
      </v-col>
      <v-dialog v-model="dialog3" width="80%" id="container" >
        <v-card>
          <PlaceModal :placeModal="recommend[2]" @close-modal="dialog3=false"></PlaceModal>
        </v-card>
      </v-dialog>
      <!-- 세번째 - 네번째 관광지 사이 거리 -->
      <v-col cols="1" v-if="recommend[4].three_four != 'NULL'">
        <p style="font-size: 0.75rem">{{ recommend[4].three_four }}km</p>
        <!-- <v-img src="@/assets/line.png"></v-img> -->
      </v-col>
      <!-- 네번째 관광지 -->
      <v-col cols="2" v-if="recommend[3]['lid'] != 'NULL'" @click.stop="dialog4=true">
        <v-row class="flex-column">
          <v-col class="d-flex justify-center pa-0">
            <v-img class="align-center" src="@/assets/pin4.png" max-width="30"></v-img>
          </v-col>
          <v-col class="pa-0">
            <div class="text-center text-truncate" style="font-size: 15px;">{{ recommend[3].landmark_name }}</div>
          </v-col>
        </v-row>
      </v-col>
      <v-dialog v-model="dialog4" width="80%" id="container" >
        <v-card>
          <PlaceModal :placeModal="recommend[3]" @close-modal="dialog4=false"></PlaceModal>
        </v-card>
      </v-dialog>
    </v-row>
  </div>
</template>

<script>
import PlaceModal from "@/components/courses/PlaceModal.vue";
export default {
    name: 'Course',
    components: {
      PlaceModal,
    },
    props: {
      recommend: Array,
    },
    data() {
      return {
        dialog1: false,
        dialog2: false,
        dialog3: false,
        dialog4: false,
      };
    },
    methods: {

    },

}
</script>

<style>

</style>