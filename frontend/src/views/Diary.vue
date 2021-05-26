<template>
  <div class="" id="container">
    <v-container>
      <v-row class="ma-0" style="width: 100%">
        <v-col class="pa-0">
          <Calendar @change-focus="changeFocus" @get-events="getEvents" />
          <!-- 해당일자 일정 조회 -->
          <div style="">
            <h4 class="ml-3 mt-3">{{ this.focus }} 일정</h4>
            <v-container>
              <v-row class="mt-1">
                <v-col cols="12"><h5>방문예정 맛집</h5></v-col>
                <v-container>
                  <v-row class="">
                    <v-col 
                      v-for="(store, idx) in stores"
                      :key="idx"
                      cols="4"
                    ><ShowStore class="" :store="store" :user="user" :idx="idx" :reviewId="reviewId" /></v-col>
                  </v-row>
                </v-container>
                <v-col cols="12"><h5>방문예정 여행코스</h5></v-col>
                <v-col class="pa-0" cols="12">
                  <ShowCourse
                    v-if="courses.length > 0"
                    class="pt-3"
                    :courses="courses"
                    :distance="distance" 
                  />
                </v-col>
              </v-row>
              <div style="height: 100px;"></div>
            </v-container>
          </div>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import axios from 'axios'
import { mapState } from 'vuex'
import Calendar from '@/components/diary/Calendar.vue'
import ShowStore from '@/components/diary/ShowStore.vue'
import ShowCourse from '@/components/diary/ShowCourse.vue'
export default {
  name : "Diary",
  components: {
    Calendar,
    ShowStore,
    ShowCourse,
  },
  data: () => ({
    focus: '',
    stores: [],
    courses: [],
    distance: [],
    events: [],
    reviewId: null,
  }),
  methods: {
    showSchedule () {
      const serverUrl = process.env.VUE_APP_SERVER_URL
      const userId = String(this.user)
      this.$store.commit('SET_LOADER_TRUE')
      axios.get(`${serverUrl}/recommendroad/get-user-schedule-detail/${userId},${this.focus}`)
      .then(res => {
        console.log(res.data)
        this.stores = res.data.store_info
        this.courses = res.data.land_info
        this.distance = res.data.distance
        this.events.forEach(event => {
          if (event.start == this.focus) {
            this.reviewId = event.reviewId
          }
        })
        this.$store.commit('SET_LOADER_FALSE');
      })
      .catch(err => {
        console.log(err)
        this.$store.commit('SET_LOADER_FALSE');
        alert('error')
      })
    },
    changeFocus(focus) {
      this.focus = focus
    },
    getEvents(events) {
      console.log(events)
      // console.log('이벤트가 있는 날 확인')
      this.events = events
      this.events.forEach(event => {
        if (event.start == this.focus) {
          // console.log('해당 일자에 이벤트가 있습니다.')
          this.showSchedule()
        }
      })
    }
  },
  computed: {
    ...mapState ([
      'user',
    ])
  },
  watch: {
    focus: function () {
      // console.log('focus 변화 감지')
      this.stores = []
      this.courses = []
      this.distance = []
      this.events.forEach(event => {
        if (event.start == this.focus) {
          // console.log('해당 일자에 이벤트가 있습니다.')
          this.showSchedule()
        }
      })
      // console.log('focus 변화 감지 종료')
    },
    // 라우터 이동시 로딩창 끄기
    $router(to, from) {
      if (to.path != from.path) {
        this.$store.commit('SET_LOADER_FALSE');
      }
    },
  },
  
}
</script>

<style scoped>
.backimg {
  background-image: url(https://i.ibb.co/C6SCsQT/backimg.png);
  min-height: 650px;
}
.pl-1 {
  margin-right: 5px;
}
.highlight {
  border-bottom: 7px solid #dbdbdb;
  width: 30%;
  margin: auto;
}
</style>