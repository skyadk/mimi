<template>
  <div id="container">
    <v-container fluid class="backcolor" style="border:2px solid; color:#D7CCC8">
      <v-simple-table dense>
        <template v-slot:default>
          <tbody>
            <tr>
              <th style="width: 100px">
                <v-img
                  :src="`https://j4d108.p.ssafy.io/landphoto/${placeItem.lid}.png`"
                  @click.stop="dialog1 = true"
                  style="width: 100px; border-radius: 20px; height: 100px;"
                ></v-img>
                <v-dialog v-model="dialog1" width="80%" id="container" >
                  <v-card>
                    <PlaceModal :placeModal="placeItem" @close-modal="dialog1 = false"></PlaceModal>
                  </v-card>
                </v-dialog>
              </th>
              <th class="text-left">
                <p @click.stop="dialog1 = true">
                  {{ placeItem.landmark_name }}<br />
                  {{ placeItem.tel }}<br />
                  {{ placeItem.addr }}<br />
                </p>

                <v-dialog v-model="dialog1" width="80%" id="container" >
                  <v-card>
                    <PlaceModal :placeModal="placeItem" @close-modal="dialog1 = false"></PlaceModal>
                  </v-card>
                </v-dialog>
              </th>
              <th class="text-right" style="width: 5px">
                <v-dialog v-model="dialog" max-width="290">
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn
                      fab
                      dark
                      small
                      color="indigo"
                      v-bind="attrs"
                      v-on="on"
                    >
                      <v-icon dark>
                        mdi-plus
                      </v-icon>
                    </v-btn>
                  </template>
                  <v-card>
                    <v-card-title>관광지 번호에 저장하세요.</v-card-title>
                    <v-divider></v-divider>
                    <v-card-text style="height: 100px;">
                      <v-radio-group v-model="dialogtravel">
                        <v-radio label="1번 관광지" value="one"></v-radio>
                        <v-radio label="2번 관광지" value="two"></v-radio>
                        <v-radio label="3번 관광지" value="three"></v-radio>
                        <v-radio label="4번 관광지" value="four"></v-radio>
                      </v-radio-group>
                    </v-card-text>
                    <br>
                    <v-card-actions>
                      <v-btn color="black" text @click="dialog = false" >
                        닫기
                      </v-btn>
                      <v-btn color="black" text @click="custom" >
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
      <br />
    </div>
  </div>
</template>

<script>
import PlaceModal from "@/components/courses/PlaceModal.vue";
export default {
  name: "RestaurantItem",
  components: {
    PlaceModal,
  },
  props: {
    placeItem: Object,
  },
  data() {
    return {
      dialogtravel: "",
      dialog: false,
      dialog1: false,
    };
  },
  methods: {
    custom() {
      if (this.dialogtravel == 'one') {
        console.log(this.placeItem)
        this.dialog = false
        this.$store.dispatch('courseChange1', this.placeItem)
      } else if (this.dialogtravel == 'two') {
        console.log('2번')
        this.dialog = false
        this.$store.dispatch('courseChange2', this.placeItem)
      } else if (this.dialogtravel == 'three') {
        console.log('3번')
        this.dialog = false
        this.$store.dispatch('courseChange3', this.placeItem)
      } else {
        console.log('4번')
        this.dialog = false
        this.$store.dispatch('courseChange4', this.placeItem)
      }
    }
  },
};
</script>

<style scoped>
.backcolor {
  background-color: white;
  border-radius: 20px;

}
.container--fluid:last-child{
  margin-bottom: 70px;
}

</style>
