<template>
  <div id="container">
    <v-container>
      <v-row style="padding-top: 3px;">
        <v-col cols="9">
          <h2 id="container3">여행 코스 추천</h2>
        </v-col>
        <v-col cols="3">
          <v-dialog v-model="dialog" max-width="290">
            <template v-slot:activator="{ on, attrs }">
              <v-col class="pt-0" align="end" style="margin-right: 10px;" v-bind="attrs" v-on="on">
                <i class="fas fa-info-circle fa-2x" style="color: #6A1B9A;"></i>
              </v-col>
            </template>
            <v-card>
              <v-card-title id="container1">미미여지도 사용설명서</v-card-title>
              <v-divider></v-divider>
              <v-card-text id="container5">
                <br>
                미미여지도가 추천해주는 여행코스가 마음에 드시나요?<br>
                앞서 선택한 장소와 테마를 기반으로 <span style="font-weight: bold;">매칭도(상, 중, 하)에</span> 따라 다른 여행지도 추천해 드립니다.<br>
                <span style="font-weight: bold;">+ 버튼을</span> 눌러 코스를 변경해보세요~!<br>
                그리고 <span style="font-weight: bold;">코스 확인을</span> 누르면 여행경로를 지도에서 볼 수 있습니다!
              </v-card-text>
              <v-card-actions>
                <v-btn color="black" text @click="dialog = false" id="container1">
                  닫기
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-col>
      </v-row>
    </v-container>
    
    <v-container>
      <v-row>
        <v-col align="end">
          <v-btn
              class="ma-3"
              color="#EDE7F6"
              @click="moveToSelectOption"
              >
              <span class="ts">다른 코스</span>
          </v-btn>
          <v-btn
              class="ma-3"
              color="#EDE7F6"
              @click="moveToCourseCheck"
              >
              <span class="ts">코스 확인</span>
          </v-btn>
        </v-col>
    </v-row>
    </v-container>
    <Course align="center" :recommend="recommend" v-if="recommend.length > 0" ></Course>
    <MatchingCategory v-on:postMatchingOption="getMatchingOption" ></MatchingCategory>
    <PlaceList 
      v-if="recommendOther.length > 0" 
      :recommendOther="recommendOther" 
      :matchingOption="matchingOption"
      :recommendOtherLength="recommendOtherLength"
      :recommendOtherLengthFirst="recommendOtherLengthFirst"
      :recommendOtherLengthSecond="recommendOtherLengthSecond"
      ></PlaceList>
  </div>
</template>

<script>
import Course from '@/components/courses/Course.vue'
import MatchingCategory from '@/components/courses/MatchingCategory.vue'
import PlaceList from '@/components/courses/PlaceList.vue'
import { mapState } from 'vuex'
import axios from 'axios'

export default {
  name: 'TravelingCourse',
  components: {
      Course,
      MatchingCategory,
      PlaceList,
  },
  props: {
    location: String,
    thema: String,
  },
  data: () => ({
    // recommend: [],
    recommendOther: [],
    matchingOption: '전체',
    recommendOtherLength: null,
    recommendOtherLengthFirst: null,
    recommendOtherLengthSecond: null,
    dialog: false,
  }),
  methods: {
    moveToCourseCheck() {
      console.log('코스확인으로 이동')
      this.$router.push({name : "CourseCheck"})
    },
    moveToSelectOption() {
      console.log('코스추천 다시 받기')
      this.$router.push({name : "SelectOption"})
    },
    getRecommendTravel() {
      console.log('관광지 추천')
      const serverUrl = process.env.VUE_APP_SERVER_URL
      const data = {
        user_location: Number(this.location),
        user_thema: this.thema,
      }
      console.log(data)
      axios.post(`${serverUrl}/recommendroad/recommend-travle`, data)
        .then(res => {
          console.log(res.data)
          // this.recommend = res.data.recommend
          this.recommendOther = res.data.recommend_other
          this.$store.dispatch('RECOMMENDCOURSE', res.data.recommend)
          this.$store.commit('SET_LOADER_FALSE');
        })
        .catch(err => {
          console.log(err)
          this.$store.commit('SET_LOADER_FALSE');
          alert('다시 여행코스를 골라주세요.')
          history.go(-1)
        })
    },
    getMatchingOption(matchingOption) {
      this.matchingOption = matchingOption
      this.recommendOtherLength = this.recommendOther.length
      this.recommendOtherLengthFirst = ~~(this.recommendOther.length / 3)
      this.recommendOtherLengthSecond = (~~(this.recommendOther.length / 3)) * 2
    },
  },
  computed: {
    ...mapState([
      'recommendCourse'
    ]),
    recommend: function() {
      return this.recommendCourse
    }
  },
  created() {
    this.$store.dispatch('resetCourse')
    this.getRecommendTravel()
    this.$store.commit('SET_LOADER_TRUE');
  },
  watch: {
    $router(to, from) {
      if (to.path != from.path) {
        this.$store.commit('SET_LOADER_FALSE');
      }
    }
  },
}
</script>

<style scoped>
.ts {
    color: #6A1B9A;
    font-weight: 900;
}
</style>