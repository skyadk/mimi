<template>
  <div id="container" v-if="restaurantItem.sid != 'NULL'">
    <v-container fluid class="backcolor" @click="moveToDetailPage(restaurantItem.sid)" style="border:2px solid; color:#D7CCC8">
      <v-simple-table dense>
        <template v-slot:default>
          <tbody >
            <tr>
              <th style="width: 100px">
                <v-img :src="imageSrc" @error="altImage" style="width: 100px; height: 100px; border-radius: 20px;"></v-img>
              </th>
              <th class="text-left">
                  <div style="margin-left: 2px;">{{restaurantItem.store_name}}</div>
                  <v-rating 
                    color="warning"
                    background-color="warning"
                    readonly
                    half-increments
                    dense
                    size="5"
                    class=""
                    v-model="score"
                  ></v-rating>
                <div style="margin-left: 2px;">{{restaurantItem.category}}</div>
                <div style="margin-left: 2px;">{{restaurantItem.address}}</div>
                <div style="margin-left: 2px;">{{restaurantItem.tel}}</div>
              </th>
              <th class="text-right">
                <v-btn fab dark small color="indigo" @click.stop="dialog = true">
                  <v-icon dark>
                    mdi-plus
                  </v-icon>
                </v-btn>                
                <v-dialog v-model="dialog" max-width="290">
                  <v-card>
                    <v-card-title class="text-h6" style="word-break: keep-all;" id="container1">
                      방문 예정인 음식점을 다이어리에 저장하세요!
                    </v-card-title>
                    <v-menu
                      ref="menu"
                      v-model="menu"
                      :close-on-content-click="false"
                      :return-value.sync="date"
                      transition="scale-transition"
                      offset-y
                      min-width="auto"
                    >
                      <template v-slot:activator="{ on, attrs }">
                        <v-text-field
                          v-model="date"
                          label="날짜 선택"
                          prepend-icon="mdi-calendar"
                          readonly
                          v-bind="attrs"
                          v-on="on"
                          class="ml-6"
                          style="width: 150px;"
                        ></v-text-field>
                      </template>
                      <v-date-picker v-model="date" no-title scrollable>
                        <v-spacer></v-spacer>
                        <v-btn text color="primary" @click="menu = false">
                          Cancel
                        </v-btn>
                        <v-btn text color="primary" @click="$refs.menu.save(date)">
                          OK
                        </v-btn>
                      </v-date-picker>
                    </v-menu>
                    <v-card-text style="height: 100px;">
                      <v-radio-group v-model="dialogm1" class="mt-0 pt-0">
                        <v-radio label="아침" value="0"></v-radio>
                        <v-radio label="점심" value="1"></v-radio>
                        <v-radio label="저녁" value="2"></v-radio>
                      </v-radio-group>
                    </v-card-text>
                    <v-divider></v-divider>

                    <v-card-actions>
                      <v-spacer></v-spacer>

                      <v-btn color="green darken-1" text @click="dialog = false">
                        취소
                      </v-btn>

                      <v-btn color="green darken-1" text @click="saveStore">
                        저장
                      </v-btn>

                    </v-card-actions>
                  </v-card>
                </v-dialog>
              </th>
            </tr>
          </tbody>
        </template>
      </v-simple-table>
    </v-container>
    <div style="line-height:50%;">
      <br>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { mapState } from 'vuex'
// import fs from 'fs'

export default {
  name: 'RestaurantItem',
  props: {
    restaurantItem: Object
  },
  data () {
    return {
      dialogm1: '',
      dialog: false,
      date: new Date().toISOString().substr(0, 10),
      menu: false,
      imageSrc: '',
    }
  },
  methods: {
    moveToDetailPage(id) {
      console.log(this.restaurantItem)
      this.$router.push(`/restaurantdetail/${id}`)
    },
    saveStore() {
      this.dialog = false
      const serverUrl = process.env.VUE_APP_SERVER_URL
      const data = {
        id: this.userEmail,
        savedDate: this.date,
        sid: this.restaurantItem.sid,
        flag: Number(this.dialogm1)
      }
      console.log(data)
      axios.post(`${serverUrl}/recommendroad/save-option-store`, data)
        .then(res => {
          console.log(res)
          alert('다이어리 저장 성공')
        })
        .catch(err => {
          console.log(err)
        })
    },
    getImageSrc() {
      console.log('이미지 경로 탐색')
      this.imageSrc = `https://j4d108.p.ssafy.io/storephoto/${this.restaurantItem.sid}.jpg`
    },
    altImage() {
      console.log("이미지 대체")
      this.imageSrc = require('@/assets/noimage.png')
    }
  },
  computed: {
    ...mapState ([
      'userEmail',
    ]),
    score: function() {
      return Number(this.restaurantItem.review_avg)
    }
  },
  created() {
    this.getImageSrc()
  }
}
</script>

<style scoped>
.backcolor {
  background-color: white;
  border-radius: 20px;
}
</style>