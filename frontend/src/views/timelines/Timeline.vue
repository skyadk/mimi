<template>
  <div class="backimg" id="container">
      <v-timeline
        align-top
        dense
      >
        <v-timeline-item
          color="#6A1B9A"
          small
          v-for="(item, idx) in this.schedule" :key="idx" class="aaa"
        >
          <v-container>
            <v-row class="pt-1">
              <v-col cols="12">
                <strong>{{ item.savedDate }}</strong>
              </v-col>
              <v-col cols="4" v-if="item.isSavedB === 'True'">
                <v-card
                    class="mx-auto"
                    width="90"
                    @click="moveToDetailPage(item.sidB)"
                >
                    <v-img
                    class="white--text align-end"
                    height="100px"
                    :src="itemSrcs[idx].srcB"
                    >
                    </v-img>
                    <v-badge class="d-inline" content="아침" color="#AD1457" overlap bordered left></v-badge>
                    <v-card-subtitle class="pt-0 pb-0 text-truncate">
                      {{ item.sidBName }}
                    </v-card-subtitle>
                </v-card>
              </v-col>
              <v-col cols="4" v-else-if="item.isSavedB === 'False'">
                <v-card
                    class="mx-auto"
                    width="90"
                    @click="moveToDetailPage(item.sidB)"
                >
                    <v-img
                    class="white--text align-end"
                    height="100px"
                    gradient="to top right, rgba(100,115,201,.33), rgba(68,69,77,.7)"
                    :src="itemSrcs[idx].srcB"
                    >
                    </v-img>
                    <v-badge class="d-inline" content="아침" color="#616161" overlap bordered left></v-badge>
                    <v-card-subtitle class="pt-0 pb-0 text-truncate">
                      {{ item.sidBName }}
                    </v-card-subtitle>
                </v-card>
              </v-col>
              <v-col cols="4" v-if="item.isSavedL === 'True'">
                <v-card
                    class="mx-auto"
                    width="90"
                    @click="moveToDetailPage(item.sidL)"
                >
                    <v-img
                    class="white--text align-end"
                    height="100px"
                    :src="itemSrcs[idx].srcL"
                    >
                    </v-img>
                    <v-badge class="d-inline" content="점심" color="#AD1457" overlap bordered left></v-badge>
                    <v-card-subtitle class="pt-0 pb-0 text-truncate">
                      {{ item.sidLName }}
                    </v-card-subtitle>
                </v-card>
              </v-col>
              <v-col cols="4" v-else-if="item.isSavedL === 'False'">
                <v-card
                    class="mx-auto"
                    width="90"
                    @click="moveToDetailPage(item.sidL)"
                >
                    <v-img
                    class="white--text align-end"
                    height="100px"
                    gradient="to top right, rgba(100,115,201,.33), rgba(68,69,77,.7)"
                    :src="itemSrcs[idx].srcL"
                    >
                    </v-img>
                    <v-badge class="d-inline" content="점심" color="#616161" overlap bordered left></v-badge>
                    <v-card-subtitle class="pt-0 pb-0 text-truncate">
                      {{ item.sidLName }}
                    </v-card-subtitle>
                </v-card>
              </v-col>
              <v-col cols="4" v-if="item.isSavedD === 'True'">
                <v-card
                    class="mx-auto"
                    width="90"
                    @click="moveToDetailPage(item.sidD)"
                >
                    <v-img
                    class="white--text align-end"
                    height="100px"
                    :src="itemSrcs[idx].srcD"
                    >
                    </v-img>
                    <v-badge class="d-inline" content="저녁" color="#AD1457" overlap bordered left></v-badge>
                    <v-card-subtitle class="pt-0 pb-0 text-truncate">
                      {{ item.sidDName }}
                    </v-card-subtitle>
                </v-card>
              </v-col>
              <v-col cols="4" v-else-if="item.isSavedD === 'False'">
                <v-card
                    class="mx-auto"
                    width="90"
                    @click="moveToDetailPage(item.sidD)"
                >
                    <v-img
                    class="white--text align-end"
                    height="100px"
                    gradient="to top right, rgba(100,115,201,.33), rgba(68,69,77,.7)"
                    :src="itemSrcs[idx].srcD"
                    >
                    </v-img>
                    <v-badge class="d-inline" content="저녁" color="#616161" overlap bordered left></v-badge>
                    <v-card-subtitle class="pt-0 pb-0 text-truncate">
                      {{ item.sidDName }}
                    </v-card-subtitle>
                </v-card>
              </v-col>
            </v-row>
          </v-container>
        </v-timeline-item>
      </v-timeline>
  </div>
</template>

<script>
import { getSchedule } from '@/api/timeline'

export default {
  name: 'Timeline',
  methods: {
    moveToDetailPage(id) {
        this.$router.push(`/restaurantdetail/${id}`)
    },
    altImage() {
      console.log('이미지대체')
    }
  },
  data() {
    return {
      schedule: Array,
      itemSrcs: [],
      deleteNum: [],
    };
  },
  async created() {
    this.$store.commit('SET_LOADER_TRUE');
    const id = this.$store.state.user;
    const userSchedule = await getSchedule(id);
    this.$store.commit('SET_LOADER_FALSE');
    this.schedule = userSchedule.data.message.sort(date_descending)
    function date_descending(a, b) {
      let dateA = new Date(a['savedDate']).getTime();
      let dateB = new Date(b['savedDate']).getTime();
      return dateA < dateB ? 1 : -1;
    }

    function getToday(){
      var date = new Date();
      var year = date.getFullYear();
      var month = ("0" + (1 + date.getMonth())).slice(-2);
      var day = ("0" + date.getDate()).slice(-2);

      return Number(year + month + day);
  }

    let today = getToday();
    for (let i=0; i<this.schedule.length; i++) {

      let elementDate = new Date(this.schedule[i]['savedDate']);
      var year = elementDate.getFullYear();
      var month = ("0" + (1 + elementDate.getMonth())).slice(-2);
      var day = ("0" + elementDate.getDate()).slice(-2);

      elementDate = Number(year  + month  + day);

      if (elementDate > today){
        this.schedule.shift();
        i--;
      }else {
        break;
      }
    }
    console.log(this.schedule)
    console.log("asdfghj")
    for (let i=0; i<this.schedule.length; i++) {
      console.log(this.schedule[i])
      if (this.schedule[i].sidB == null && this.schedule[i].sidL == null && this.schedule[i].sidD == null){
        this.deleteNum.push(i)
      }
    }
    for (let i=0; i<this.deleteNum.length; i++) {
      this.schedule.splice(this.deleteNum[i], 1);
    }
    console.log(this.schedule)

    // 이미지 Url을 미리 계산
    this.schedule.forEach(item => {
      let itemSrc = {
        srcB: null,
        srcL: null,
        srcD: null,
      }
      if (item.sidB != null) {
        try {
          itemSrc.srcB = `https://j4d108.p.ssafy.io/storephoto/${item.sidB}.jpg`
        } catch {
          itemSrc.srcB = require('@/assets/noimage.png')
        }
      }
      if (item.sidL != null) {
        try {
          itemSrc.srcL = `https://j4d108.p.ssafy.io/storephoto/${item.sidL}.jpg`
        } catch {
          itemSrc.srcL = require('@/assets/noimage.png')
        }
      }
      if (item.sidD != null) {
        try {
          itemSrc.srcD = `https://j4d108.p.ssafy.io/storephoto/${item.sidD}.jpg`
        } catch {
          itemSrc.srcD = require('@/assets/noimage.png')
        }
      }
      this.itemSrcs.push(itemSrc)
    })
  },
  watch: {
    $router(to, from) {
      if (to.path != from.path) {
        this.$store.commit('SET_LOADER_FALSE');
      }
    }
  }
}
</script>

<style scoped>
.aaa:last-child{
  margin-bottom: 70px;
}
</style>