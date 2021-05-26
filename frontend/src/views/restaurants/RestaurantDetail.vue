<template>
  <div id="container">
    <v-img :src="imageSrc" class="alignend" height="250px">
      <div class="fill-height bottom-gradient text-type">
        <span
          >{{storeinfo.store_name}}
          <v-btn fab dark small color="indigo" @click.stop="dialog = true">
            <v-icon dark>
              mdi-plus
            </v-icon>
          </v-btn>
          <v-dialog v-model="dialog" max-width="290">
            <v-card>
              <v-card-title class="text-h6" style="word-break: keep-all;">
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
        </span>
      </div>
    </v-img>
    <RestaurantDetailCategory :category1="storeinfo" :category2="storemenu" :category3="Number(sid)"></RestaurantDetailCategory>
  </div>
</template>

<script>
import RestaurantDetailCategory from "@/components/restaurants/RestaurantDetailCategory.vue";
import axios from 'axios'
import { mapState } from 'vuex'
export default {
  name: "RestaurantDetail",
  components: {
    RestaurantDetailCategory,
  },
  data () {
    return {
      dialog: false,
      dialogm1: "",
      date: new Date().toISOString().substr(0, 10),
      menu: false,
      storeinfo: {},
      storemenu: [],
      sid: this.$route.params.id,
      imageSrc: '',
    };
  },
  methods: {
    saveStore() {
      this.dialog = false
      const serverUrl = process.env.VUE_APP_SERVER_URL
      const data = {
        id: this.userEmail,
        savedDate: this.date,
        sid: this.sid,
        flag: Number(this.dialogm1)
      }
      console.log(data)
      axios.post(`${serverUrl}/recommendroad/save-option-store`, data)
        .then(res => {
          console.log(res)
        })
        .catch(err => {
          console.log(err)
        })
    },
    restaurantInfo() {
      const serverUrl = process.env.VUE_APP_SERVER_URL
      axios.get(`${serverUrl}/recommendroad/get-store-info/${this.sid}`)
      .then(res => {
        this.storeinfo = res.data.message[0]
        this.storemenu = res.data.message[1]
      })
      .catch(err => {
        console.log(err)
      })
    },
    getImageSrc() {
      try { 
        this.imageSrc = `https://j4d108.p.ssafy.io/storephoto/${this.sid}.jpg`
      } catch {
        this.imageSrc = require('@/assets/noimage.png')
      }
    },
  },
  computed: {
    ...mapState ([
      'userEmail',
    ])
  },
  created() {
    this.restaurantInfo()
    this.getImageSrc()
  }  
};
</script>

<style scoped>
.bottom-gradient {
  background-image: linear-gradient(
    to top,
    rgba(0, 0, 0, 0.6) 10%,
    transparent 100px
  );
}
.text-type {
  color: white;
  font-size: 40px;
}
.alignend {
  align-items: flex-end;
}
</style>
