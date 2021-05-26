<template>
  <div class="backimg" id="container">
    <br>
      <v-card width="84%" style="margin: 2% 8% 0% 8%">
        <template>
          <v-img src="@/assets/mimi_logo.png" width="80%" style="margin-left: 10%;"></v-img>
          <v-card-title>
            여행지
          </v-card-title>
          <v-card-text>
          <v-row
            align="center"
            class="mx-0"
          >
            <v-rating
              :value="4.5"
              color="amber"
              dense
              half-increments
              readonly
              size="14"
            ></v-rating>
          </v-row>
          <br>
          <div>Small plates, salads & sandwiches - an intimate setting with 12 indoor seats plus patio seating.</div>
        </v-card-text>
        </template>
      </v-card>
  </div>
</template>

<script>
export default {

}
</script>

<style scoped>
.backimg {
  background-image: url(https://i.ibb.co/C6SCsQT/backimg.png);
  min-height: 650px;
}
</style>