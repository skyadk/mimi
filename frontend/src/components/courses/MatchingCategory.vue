<template>
  <div>
    <div class="text-center category-background">
      <v-chip-group
        v-model="matchingOption"
        column
        mandatory
      >
        <v-chip
          v-for="tag in tags"
          :key="tag"
          :value="tag"
          outlined
          color="#AD1457"
          @click="chipClick(tag)"
          >
          {{ tag }}
          </v-chip>
      </v-chip-group>
    </div>
  </div>
</template>

<script>
export default {
    name: 'MatchingCategory',
    data: () => ({
      tags: [
        '전체',
        '상',
        '중',
        '하',
      ],
      matchingOption: '',
    }),
    methods: {
      chipClick(value) {
        this.matchingOption = value
        this.$emit("postMatchingOption", this.matchingOption)
      }
    },
}
</script>

<style scoped>
.category-color {
  font-weight: 700;
  color: rgb(50, 121, 67);
  font-size: 125%;
}
.categoty-imfo {
  padding-left: 60px;
  padding-right: 60px;
}
.category-background {
  background-color: #EEEEEE;
}

</style>