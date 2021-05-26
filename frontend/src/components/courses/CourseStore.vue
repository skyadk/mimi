<template>
  <div class="my-7">
    <v-row class="pa-0" justify="center" no-gutters>
      <!-- 첫번째 관광지 -->
      <v-col cols="2" v-if="recommend[0]['lid'] != 'NULL'" @click="changeLocationInfo(0)">
        <v-row class="flex-column">
          <v-col class="d-flex justify-center pa-0">
            <v-img class="align-center" src="@/assets/pin1.png" max-width="30"></v-img>
          </v-col>
          <v-col class="pa-0">
            <div class="text-center text-truncate" style="font-size: 15px;">{{ recommend[0].landmark_name }}</div>
          </v-col>
        </v-row>
      </v-col>
      <!-- 첫번째 - 두번째 관광지 사이 거리 -->
      <v-col cols="1" v-if="recommend[4].one_two != 'NULL'">
        <p style="font-size: 0.75rem">{{ recommend[4].one_two }}km</p>
        <!-- <v-img src="@/assets/line.png"></v-img> -->
      </v-col>
      <!-- 두번째 관광지 -->
      <v-col cols="2" v-if="recommend[1]['lid'] != 'NULL'" @click="changeLocationInfo(1)">
        <v-row class="flex-column">
          <v-col class="d-flex justify-center pa-0">
            <v-img class="align-center" src="@/assets/pin2.png" max-width="30"></v-img>
          </v-col>
          <v-col class="pa-0">
            <div class="text-center text-truncate" style="font-size: 15px;">{{ recommend[1].landmark_name }}</div>
          </v-col>
        </v-row>
      </v-col>
      <!-- 두번째 - 세번째 관광지 사이 거리 -->
      <v-col cols="1" v-if="recommend[4].two_three != 'NULL'">
        <p style="font-size: 0.75rem">{{ recommend[4].two_three }}km</p>
        <!-- <v-img src="@/assets/line.png"></v-img> -->
      </v-col>
      <!-- 세번째 관광지 -->
      <v-col cols="2" v-if="recommend[2]['lid'] != 'NULL'" @click="changeLocationInfo(2)">
        <v-row class="flex-column">
          <v-col class="d-flex justify-center pa-0">
            <v-img class="align-center" src="@/assets/pin3.png" max-width="30"></v-img>
          </v-col>
          <v-col class="pa-0">
            <div class="text-center text-truncate" style="font-size: 15px;">{{ recommend[2].landmark_name }}</div>
          </v-col>
        </v-row>
      </v-col>
      <!-- 세번째 - 네번째 관광지 사이 거리 -->
      <v-col cols="1" v-if="recommend[4].three_four != 'NULL'">
        <p style="font-size: 0.75rem">{{ recommend[4].three_four }}km</p>
        <!-- <v-img src="@/assets/line.png"></v-img> -->
      </v-col>
      <!-- 네번째 관광지 -->
      <v-col cols="2" v-if="recommend[3]['lid'] != 'NULL'" @click="changeLocationInfo(3)">
        <v-row class="flex-column">
          <v-col class="d-flex justify-center pa-0">
            <v-img class="align-center" src="@/assets/pin4.png" max-width="30"></v-img>
          </v-col>
          <v-col class="pa-0">
            <div class="text-center text-truncate" style="font-size: 15px;">{{ recommend[3].landmark_name }}</div>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { mapState } from 'vuex'
export default {
    name: 'CourseStore',
    data() {
      return {
      };
    },
    methods: {
      changeLocationInfo(idx) {
        alert('선택한 관광지 주변의 맛집이 추천됩니다.')
        console.log(idx)
        const data = {
          address: this.recommend[idx].addr.split(" ")[1],
          latitude: this.recommend[idx].latitude,
          logitude: this.recommend[idx].longitude
        }
        this.$store.dispatch('changeLocationInfo', data)
      }
    },
    computed: {
        ...mapState([
          'recommendCourse',
          'locationInfo',
        ]),
        recommend: function() {
        return this.recommendCourse
        }
    },

}
</script>

<style>

</style>