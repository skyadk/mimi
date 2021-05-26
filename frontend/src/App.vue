<template>
  <v-app>
    <Loader></Loader>
    <v-main>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script>
import Loader from "./components/common/Loader.vue";
export default {
  name: 'App',

  components: {
    Loader,
  },

  data: () => ({
    //
  }),
};
</script>
<style>
/* id에 container ~ container5 까지 폰트 적용 */
#container {
  font-family: "Do Hyeon", sans-serif;
}
@font-face {
  font-family: "NanumBarunGothic";
  src: local("NanumBarunGothic"),
  url(./fonts/NanumBarunGothic.ttf) format("truetype");
}
#container1 {
  font-family: 'NEXON Lv1 Gothic OTF';
}
@font-face {
  font-family: 'NEXON Lv1 Gothic OTF';  /* 원하는 이름 입력 */
  src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_20-04@2.1/NEXON Lv1 Gothic OTF.woff') format('woff');  /* 폰트 경로 */
  font-weight: normal;  /* 폰트 두께 설정 */
  font-style: normal;    /* 폰트 스타일 */
}
#container2 {
  font-family: 'Cafe24Oneprettynight';
}
@font-face {
  font-family: 'Cafe24Oneprettynight';
  src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_twelve@1.1/Cafe24Oneprettynight.woff') format('woff');
  font-weight: normal;
  font-style: normal;
}
#container3 {
  font-family: 'MapoGoldenPier';
}
@font-face {
  font-family: 'MapoGoldenPier';
  src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_2001@1.1/MapoGoldenPierA.woff') format('woff');
  font-weight: normal;
  font-style: normal;
}
#container4 {
  font-family: 'MapoFlowerIsland';
}
@font-face {
  font-family: 'MapoFlowerIsland';
  src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_2001@1.1/MapoFlowerIslandA.woff') format('woff');
  font-weight: normal;
  font-style: normal;
}
#container5 {
  font-family: 'NEXON Lv2 Gothic';
}
@font-face {
  font-family: 'NEXON Lv2 Gothic';
  src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_20-04@2.1/NEXON Lv2 Gothic.woff') format('woff');
  font-weight: normal;
  font-style: normal;
}

/* 상단바 밑에 부터 화면 시작 */
.top {
  position: static;
}
.main {
  position: relative;
  top: 0px;
}
</style>
