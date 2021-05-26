<template>
  <!-- 캘린더 조작 바 -->
  <div>
    <v-sheet height="">
      <v-toolbar
        flat
      >
        <v-btn
          outlined
          class="mr-4"
          color="grey darken-2"
          @click="setToday"
        >
          Today
        </v-btn>
        <v-btn
          fab
          text
          small
          color="grey darken-2"
          @click="prev"
        >
          <v-icon small>
            mdi-chevron-left
          </v-icon>
        </v-btn>
        <v-btn
          fab
          text
          small
          color="grey darken-2"
          @click="next"
        >
          <v-icon small>
            mdi-chevron-right
          </v-icon>
        </v-btn>
        <v-toolbar-title v-if="$refs.calendar">
          {{ $refs.calendar.title }}
        </v-toolbar-title>
        <v-spacer></v-spacer>
        <v-dialog v-model="dialog" max-width="290">
          <template v-slot:activator="{ on, attrs }">
            <div align="end" v-bind="attrs" v-on="on">
              <i class="fas fa-info-circle fa-2x" style="color: #6A1B9A;"></i>
            </div>
          </template>
          <v-card>
            <v-card-title id="container1">미미여지도 사용설명서</v-card-title>
            <v-divider></v-divider>
            <v-card-text id="container5">
              <br>
              저장된 맛집과 여행코스는 달력에 표시됩니다 ^_^<br>
              리뷰와 평점의 정확도를 높이기 위해 <span style="font-weight: bold;">방문체크를</span> 눌러야 리뷰를 작성할 수 있습니다.
            </v-card-text>
            <v-card-actions>
              <v-btn color="black" text @click="dialog = false" id="container1">
                닫기
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
        
      </v-toolbar>
    </v-sheet>
    <!-- 캘린더 -->
    <v-sheet height="450">
      <v-calendar
        ref="calendar"
        v-model="focus"
        color="purple"
        :events="events"
        :type="type"
        class="text-center"
        @click:event="changeFocus"
      ></v-calendar>
    </v-sheet>
  </div>
</template>

<script>
import axios from 'axios'
import { mapState } from 'vuex'
export default {
  name: 'Calendar',
  props: {
    // focus: String,
  },
  data: () => ({
    focus: '',
    type: 'month',
    events: [],
    colors: ['blue', 'indigo', 'deep-purple', 'cyan', 'green', 'orange', 'grey darken-1'],
    dialog: false,
  }),
  methods: {
    setToday () {
      let today = new Date()
      let todayString = ''
      let year = today.getFullYear()
      let month = today.getMonth() + 1
      if (month < 10) {
        month = "0".concat(month)
      }
      let date = today.getDate()
      if (date < 10) {
        date = "0".concat(date)
      }
      this.focus = todayString.concat(year, "-", month, "-", date)      
    },
    prev () {
      this.$refs.calendar.prev()
    },
    next () {
      this.$refs.calendar.next()
    },
    changeFocus (event) {
      this.focus = event.event.start
    },    
    getEvents () {
      // 저장된 이벤트 받아오기
      const serverUrl = process.env.VUE_APP_SERVER_URL
      const userId = this.user
      // const userId = 949437
      // console.log(userId)
      this.$store.commit('SET_LOADER_TRUE')
      axios.get(`${serverUrl}/recommendroad/get-user-schedule/${userId}`)
        .then(res => {
          // console.log(res.data.message)
          const schedules = res.data.message
          schedules.forEach(schedule => {
            // console.log(schedule)
            const tmp = {
              name: '♥',
              start: schedule.savedDate,
              color: this.colors[Math.floor(Math.random() * this.colors.length)],
              // visit: schedule.isSavedD === 'False' ? false : true,
              reviewId: schedule.id
            }
            this.events.push(tmp)
          })
          // console.log(this.events)
          this.$emit('get-events', this.events)
          this.$store.commit('SET_LOADER_FALSE')
        })
        .catch(err => {
          console.log(err)
          this.$store.commit('SET_LOADER_FALSE')
        })
    },    
  },
  watch: {
    focus: function() {
      this.$emit('change-focus', this.focus)
    }
  },
  computed: {
    ...mapState ([
      'user',
    ])
  },
  created() {
    this.setToday()
    this.getEvents()
  },
  mounted () {
    this.$refs.calendar.checkChange()
  },
}
</script>

<style>
>>> .v-event {
  width: 100%;
}
</style>