<template>
  <div>
    <v-row cols=12 class="ma-0 pa-3">
      <v-col cols="1">
        <v-icon color="#AB47BC">mdi-map-marker-radius-outline</v-icon>
      </v-col>
      <v-col cols="10" class="pl-4">
        <p class="mb-0">가게 주소: {{ storeinfos.address }}</p>
      </v-col>
    </v-row>
    <v-row style="width: 90%; margin-left: 5%" class="mt-0 mb-0">
      <v-divider></v-divider>
    </v-row>
    <!-- <v-row cols=12 class="ma-0 pa-3">
      <v-col cols="1">
        <v-icon color="#AB47BC">mdi-clock-time-four-outline</v-icon>
      </v-col>
      <v-col cols="10" class="pl-4">
        <p class="mb-0">가게 영업 시간</p>
      </v-col>
    </v-row>
    <v-row style="width: 90%; margin-left: 5%" class="mt-0 mb-0">
      <v-divider></v-divider>
    </v-row> -->
    <v-row cols=12 class="ma-0 pa-3">
      <v-col cols="1">
        <v-icon color="#AB47BC">mdi-phone-outline</v-icon>
      </v-col>
      <v-col cols="10" class="pl-4">
        <p class="mb-0">가게 전화번호: {{ storeinfos.tel }}</p>
      </v-col>
    </v-row>
    <v-row style="width: 90%; margin-left: 5%" class="mt-0 mb-0">
      <v-divider></v-divider>
    </v-row>
    <v-row cols=12 class="ma-0 pa-3">
      <v-col cols="1">
        <v-icon color="#AB47BC">mdi-silverware</v-icon>
      </v-col>
      <v-col cols="10" class="pl-4">
        <p class="mb-0" >가게 메뉴</p>
          <span v-if="!menuExist">등록된 메뉴가 없습니다.</span>
          <span v-else v-for="(menu, idx) in storemenus" :key="idx"> {{ menu.menu_name }} : {{ menu.price | comma }}<br></span>
      </v-col>
    </v-row>
  </div>
</template>

<script>
// import axios from 'axios'

export default {
  name: 'RestaurantDetailInfo',
  props: {
    storeinfos: Object,
    storemenus: [Array, Object]
  },
  computed: {
    menuExist: function() {
      if (typeof(this.storemenus) == Array) {
        return true
      } else {
        return false
      }
    }
  }
}
</script>

<style scoped>
.justifycenter {
  justify-content: center;
}
</style>