<template>
    <div id="container" class="aaa">
      <div v-if="matchingOption === '전체'">
        <PlaceItem v-for="(item, idx) in recommendOther" :placeItem="item" :key="idx"></PlaceItem>
      </div>
      <div v-else-if="matchingOption === '상'">
        <PlaceItem v-for="(item, idx) in recommendOther.slice(0, this.recommendOtherLengthFirst)" :placeItem="item" :key="idx"></PlaceItem>
      </div>
      <div v-else-if="matchingOption === '중'">
        <PlaceItem v-for="(item, idx) in recommendOther.slice(this.recommendOtherLengthFirst, this.recommendOtherLengthSecond)" :placeItem="item" :key="idx"></PlaceItem>
      </div>
      <div v-else>
        <PlaceItem v-for="(item, idx) in recommendOther.slice(this.recommendOtherLengthSecond, this.recommendOtherLength)" :placeItem="item" :key="idx"></PlaceItem>
      </div>
    </div>
</template>

<script>
import PlaceItem from '@/components/courses/PlaceItem.vue'
export default {
  name: 'PlaceList',
  components: {
    PlaceItem,
  },
  props: {
    recommendOther: Array,
    matchingOption: String,
    recommendOtherLength: Number,
    recommendOtherLengthFirst: Number,
    recommendOtherLengthSecond: Number,
  },
  data () {
    return {
      dialog: false,
    }
  },
}
</script>

<style>
.aaa:last-child{
  margin-bottom: 60px;
}
</style>