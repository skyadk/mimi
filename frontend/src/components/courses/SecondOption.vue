<template>
  <div>
    <h3>Q. 어느 지역으로 여행을 떠나시나요?</h3>
    <v-row justify="center">
        <v-col cols="12">
            <div class="pa-6">
            <v-chip-group
                active-class="#AD1457"
                column
                mandatory
                v-model="locationOption"
            >
                <v-chip
                v-for="(tag, idx) in tags"
                :key="idx"
                :value="idx"
                outlined
                color="#AD1457"
                @click="chipClick(idx)"
                >
                {{ tag }}
                </v-chip>
            </v-chip-group>
            </div>
        </v-col>
    </v-row>
  </div>
</template>

<script>
export default {
    name: 'SecondOption',
    data: () => ({
      tags: [
        '서울',
        '부산',
        '인천',
        '대구',
        '대전',
        '광주',
        '울산',
        '제주',
        '경기',
        '강원',
        '충남',
        '충북',
        '경남',
        '경북',
        '전북',
        '전남',
      ],
      locationOption: '',
    }),
    methods: {
      chipClick(value) {
        this.locationOption = value
        console.log(this.locationOption)
        this.$emit("location", this.locationOption)
      }
    },
}
</script>

<style scoped>
</style>