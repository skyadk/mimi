<template>
  <div>
    <v-row class="pa-0" justify="center" no-gutters>
      <!-- 첫번째 관광지 -->
      <v-col cols="2" v-if="courses[0].lid != 'NULL'" @click.stop="dialog1 = true">
        <v-row class="flex-column">
          <v-col class="d-flex justify-center pa-0">
            <v-img class="align-center" src="@/assets/pin1.png" max-width="30"></v-img>
          </v-col>
          <v-col class="pa-0">
            <div class="text-center text-truncate" style="font-size: 15px;">{{ courses[0].landmark_name }}</div>
          </v-col>
        </v-row>
      </v-col>
      <v-dialog v-model="dialog1" width="80%" id="container" >
        <v-card>
          <PlaceModal :placeModal="courses[0]" @close-modal="dialog1 = false"></PlaceModal>
        </v-card>
      </v-dialog>
      <!-- 첫번째 - 두번째 관광지 사이 거리 -->
      <v-col cols="1" v-if="distance[0].one_two != 'NULL'">
        <p style="font-size: 0.75rem">{{ distance[0].one_two }}km</p>
        <!-- <v-img src="@/assets/line.png"></v-img> -->
      </v-col>
      <!-- 두번째 관광지 -->
      <v-col cols="2" v-if="courses[1]['lid'] != 'NULL'" @click.stop="dialog2 = true">
        <v-row class="flex-column">
          <v-col class="d-flex justify-center pa-0">
            <v-img class="align-center" src="@/assets/pin2.png" max-width="30"></v-img>
          </v-col>
          <v-col class="pa-0">
            <div class="text-center text-truncate" style="font-size: 15px;">{{ courses[1].landmark_name }}</div>
          </v-col>
        </v-row>
      </v-col>
      <v-dialog v-model="dialog2" width="80%" id="container" >
        <v-card>
          <PlaceModal :placeModal="courses[1]" @close-modal="dialog2 = false"></PlaceModal>
        </v-card>
      </v-dialog>
      <!-- 두번째 - 세번째 관광지 사이 거리 -->
      <v-col cols="1" v-if="distance[1].two_three != 'NULL'">
        <p style="font-size: 0.75rem">{{ distance[1].two_three }}km</p>
        <!-- <v-img src="@/assets/line.png"></v-img> -->
      </v-col>
      <!-- 세번째 관광지 -->
      <v-col cols="2" v-if="courses[2]['lid'] != 'NULL'" @click.stop="dialog3 = true">
        <v-row class="flex-column">
          <v-col class="d-flex justify-center pa-0">
            <v-img class="align-center" src="@/assets/pin3.png" max-width="30"></v-img>
          </v-col>
          <v-col class="pa-0">
            <div class="text-center text-truncate" style="font-size: 15px;">{{ courses[2].landmark_name }}</div>
          </v-col>
        </v-row>
      </v-col>
      <v-dialog v-model="dialog3" width="80%" id="container" >
        <v-card>
          <PlaceModal :placeModal="courses[2]" @close-modal="dialog3 = false"></PlaceModal>
        </v-card>
      </v-dialog>
      <!-- 세번째 - 네번째 관광지 사이 거리 -->
      <v-col cols="1" v-if="distance[2].three_four != 'NULL'">
        <p style="font-size: 0.75rem">{{ distance[2].three_four }}km</p>
        <!-- <v-img src="@/assets/line.png"></v-img> -->
      </v-col>
      <!-- 네번째 관광지 -->
      <v-col cols="2" v-if="courses[3]['lid'] != 'NULL'" @click.stop="dialog4 = true">
        <v-row class="flex-column">
          <v-col class="d-flex justify-center pa-0">
            <v-img class="align-center" src="@/assets/pin4.png" max-width="30"></v-img>
          </v-col>
          <v-col class="pa-0">
            <div class="text-center text-truncate" style="font-size: 15px;">{{ courses[3].landmark_name }}</div>
          </v-col>
        </v-row>
      </v-col>
      <v-dialog v-model="dialog4" width="80%" id="container" >
        <v-card>
          <PlaceModal :placeModal="courses[3]" @close-modal="dialog4 = false"></PlaceModal>
        </v-card>
      </v-dialog>
    </v-row>
  </div>
</template>

<script>
import PlaceModal from "@/components/courses/PlaceModal.vue"
export default {
  name: 'ShowCourse',
  components: {
    PlaceModal,
  },  
  props: {
    courses: Array,
    distance: Array,
  },
  data: () => ({
    dialog1: false,
    dialog2: false,
    dialog3: false,
    dialog4: false,
  }),
  methods: {

  },
}
</script>

<style>

</style>