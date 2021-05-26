<template>
  <div>
    <v-bottom-navigation style="height: 75px" app>
      <v-container>
        <v-row justify="space-around" no-gutters>
          <v-col cols="3">
            <!-- <v-btn plain @click="moveToMain" style="margin-right: 3px;" color="#356859"> -->
            <v-btn plain @click="buttonclick('/')">
              <span>홈</span>
              <i class="fas fa-home fa-3x" style="color:#3949AB"></i>
            </v-btn>
          </v-col>
          <v-col cols="3">
            <!-- <v-btn plain @click="moveToCourse" style="margin-left: 3px; margin-right: 3px"> -->
            <v-btn plain @click="buttonclick('/selectoption')">
              <span>여행코스</span>
              <i class="fas fa-suitcase-rolling fa-3x" style="color:#3949AB"></i>
            </v-btn>
          </v-col>
          <v-col cols="3">
            <!-- <v-btn plain @click="moveToTimeline" style="margin-left: 3px; margin-right: 3px"> -->
            <v-btn plain @click="buttonclick('/timeline')">
              <span>타임라인</span>
              <i class="fas fa-camera-retro fa-3x" style="color:#3949AB"></i>
            </v-btn>
          </v-col>  
          <v-col cols="3">
            <!-- <v-btn plain @click="moveToDiary" style="margin-left: 3px"> -->
            <v-btn plain @click="buttonclick('/diary')">
              <span>다이어리</span>
              <i class="far fa-calendar-alt fa-3x" style="color:#3949AB"></i>
            </v-btn>
          </v-col>
        </v-row>
      </v-container>
    </v-bottom-navigation>
  </div>
</template>

<script>
export default {
  name: 'BottomBar',
  components: {

  },
  data() {
    return {
      ismain: true,
      isselect: false,
      istimeline: false,
      isdiary: false,
    }
  },
  methods: {
    buttonclick(path) {
      if (this.$router.currentRoute.path != this.active) {
        if (path == '/') {
          this.ismain = true;
          this.isselect = false;
          this.istimeline = false;
          this.isdiary = false;
          this.gotomain();
        } else if (path == '/selectoption') {
          this.ismain = false;
          this.isselect = true;
          this.istimeline = false;
          this.isdiary = false;
          this.gotoselectoption();
        } else if (path == '/timeline') {
          this.ismain = false;
          this.isselect = false;
          this.istimeline = true;
          this.isdiary = false;
          this.gototimeline();
        } else if (path == '/diary') {
          this.ismain = false;
          this.isselect = false;
          this.istimeline = false;
          this.isdiary = true;
          this.gotodiary();
        }
      }
    },
    gotomain() {
      if (this.$router.currentRoute.path != '/') {
        this.$router.push('/');
      }
    },
    gotoselectoption() {
      if (this.$router.currentRoute.path != '/selectoption') {
        this.$router.push('/selectoption');
      }
    },
    gototimeline() {
      if (this.$router.currentRoute.path != '/timeline') {
        this.$router.push('/timeline');
      }
    },
    gotodiary() {
      if (this.$router.currentRoute.path != '/diary') {
        this.$router.push('/diary');
      }
    },
  }
}
</script>

<style scoped>
.v-btn__content {
  justify-content: flex-end;
}
</style>