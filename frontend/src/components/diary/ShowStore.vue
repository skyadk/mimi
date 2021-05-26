<template>
  <div>
    <!-- 저장된 음식점이 있을 때 -->
    <div v-if="store[sidX] && store[sidX] != 'NULL'" @click="moveToDetailPage(store[sidX])" class="">
      <p class="text-center">{{ meal }}</p>
      <v-card
        height="180"
      >
        <template slot="progress">
          <v-progress-linear
            color="deep-purple"
            height="10"
            indeterminate
          ></v-progress-linear>
        </template>
        <v-img
          height="100"
          :src="imageSrc"
        ></v-img>
        <v-card-text class="pa-1 text-center">
          <div>
            <p class="text-truncate mb-0 pl-1">{{ store.store_name }}</p>
            <div class="pl-1 blue--text text-truncate">
              {{ store.tel }}
            </div>
            <div class="grey--text pl-1">
              리뷰: {{ store.review_cnt }}개
            </div>
          </div>
        </v-card-text>
      </v-card>
      <!-- 방문체크 및 리뷰 작성 -->
      <div class="text-center">
        <v-dialog
          v-model="dialog"
          persistent
        >
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              class=""
              icon
              large
              v-on="on"
              v-bind="attrs"
              
            >
              <v-icon v-if="visited" style="color: blue;">mdi-map-marker-check</v-icon>
              <v-icon v-else>mdi-map-marker-check-outline</v-icon>
              방문
            </v-btn>
          </template>
          <v-card>
            <v-card-title>
              <span class="headline">방문 리뷰작성</span>
            </v-card-title>
            <v-card-text v-if="!visited">
              <v-container>
                <v-row>
                  <v-col cols=12>
                    <v-text-field
                      label="리뷰"
                      required
                      v-model="content"
                    ></v-text-field>
                  </v-col>
                  <v-col cols=12>
                    <v-rating color="warning" background-color="warning" v-model="score"></v-rating>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>
            <v-card-text v-else>
              <div>이미 방문하고 리뷰를 남긴 음식점입니다.</div>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                color="purple darken-1"
                text
                @click="dialog = false"
              >
                취소
              </v-btn>
              <v-btn
                v-if="!visited"
                color="purple darken-1"
                text
                @click="saveReview"
              >
                저장
              </v-btn>
            </v-card-actions>                  
          </v-card>              
        </v-dialog>
      </div>
    </div>
    <div v-else>
      <p class="text-center">{{ meal }}</p>
      <v-card max-width="100" height="180" class="d-flex align-center">
        <v-img :src="require('@/assets/nodata.png')"></v-img>
      </v-card>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'ShowStore',
  props: {
    store: Object,
    idx: Number,
    user: String,
    reviewId: Number,
  },
  data: () => ({
    dialog: false,
    meal: '',
    sidX: '',
    isSavedX: '',
    imageSrc: '',
    score: 5,
    content: '',
    visited: false,
  }),
  methods: {
    visitCheck () {
      console.log('방문 리뷰작성')
      if (this.store[this.isSavedX] == 'True') {
        this.visited = true
      }
    },
    moveToDetailPage(id) {
      this.$router.push(`/restaurantdetail/${id}`)
    },
    changeStatus () {
      // console.log('상태 변경')
      // 아침, 점심, 저녁 구분
      if (this.idx === 0) {
        this.meal = "아침"
        this.sidX = 'sidB'
        this.isSavedX = 'isSavedB'
      } else if (this.idx === 1) {
        this.meal = '점심'
        this.sidX = 'sidL'
        this.isSavedX = 'isSavedL'
      } else {
        this.meal = "저녁"
        this.sidX = 'sidD'
        this.isSavedX = 'isSavedD'
      }
      // 이미지 경로
      
      if (this.store[this.sidX] != 'NULL') {
        try {
          this.imageSrc = `https://j4d108.p.ssafy.io/storephoto/${this.store[this.sidX]}.jpg`
        } catch {
          this.imageSrc = require('@/assets/noimage.png')
        }
      }
      // console.log(this.imageSrc)
    },
    saveReview() {
      this.dialog = false
      const serverUrl = process.env.VUE_APP_SERVER_URL
      const data = {
        num: String(this.user),
        sid: String(this.store[this.sidX]),
        total_score: String(this.score),
        content: this.content,
        flag: 'false',
        predate: '',
        review_type: String(this.idx),
        review_id: String(this.reviewId),
      }
      console.log(data)
      axios.post(`${serverUrl}/recommendroad/post-review`, data)
        .then(res => {
          console.log(res.data)
          // console.log('리뷰 저장 완료!')
          this.visited = true
          alert('리뷰가 저장되었습니다.')
        })
        .catch(err => {
          console.log(err)
        })
    },
  },
  async created() {
    await this.changeStatus()
    this.visitCheck()
  }
}
</script>

<style>

</style>