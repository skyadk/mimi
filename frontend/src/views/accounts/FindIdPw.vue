<template>
  <div class="bg">
    <h1 class="text-center mt-16">
      <v-row v-if="isFindId" cols="12">
        <v-col cols="5" class="tc text-right" id="container3" @click="showFindId">ID찾기</v-col>
        <v-col cols="2">/</v-col>
        <v-col cols="5" class="text-left" id="container3" @click="showFindPw">PW찾기</v-col>
      </v-row>
      <v-row v-if="isFindPw">
        <v-col cols="5" class="text-right" id="container3" @click="showFindId">ID찾기</v-col>
        <v-col cols="2">/</v-col>
        <v-col cols="5" class="tc text-left" id="container3" @click="showFindPw">PW찾기</v-col>
      </v-row>
      
    </h1>
    <FindId v-if="isFindId" />
    <FindPw v-if="isFindPw" />
  </div>
</template>

<script>
import FindId from '@/components/accounts/FindId.vue'
import FindPw from '@/components/accounts/FindPw.vue'

export default {
  name: 'FindIdPw',
  components: {
    FindId,
    FindPw,
  },
  data: () => ({
    isFindId: true,
    isFindPw: false,
  }),
  methods: {
    showFindId() {
      this.isFindId = true
      this.isFindPw = false
    },
    showFindPw() {
      this.isFindId = false
      this.isFindPw = true
    }
  },
}
</script>

<style scoped>
.tc {
  color: #4A148C;
}
.bg {
  background-image: linear-gradient(to bottom right, #EDE7F6,#F8BBD0);
  /* display: flex;
  flex-direction: column;
  align-items: center; */
  position: fixed; 
  top: 0; 
  left: 0; 
  min-width: 100%;
  min-height: 100%;
}
</style>