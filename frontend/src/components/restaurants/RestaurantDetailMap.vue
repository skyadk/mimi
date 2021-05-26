<template>
  <div id="map" class="map-container mt-5" style="width:340px;height:300px;"></div>
</template>

<script>
export default {
  name: 'RestaurantDetailMap',
  props: {
    storeinfo: Object,
  },
  async mounted() {
    var mapContainer = document.getElementById('map'),
        mapOption = { 
            center: new window.kakao.maps.LatLng(this.storeinfo.latitude, this.storeinfo.logitude),
            level: 3
        };

    var map = new window.kakao.maps.Map(mapContainer, mapOption);

    var markerPosition  = new window.kakao.maps.LatLng(this.storeinfo.latitude, this.storeinfo.logitude); 

    const imageSrc = "https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markerStar.png";
    const imageSize = new window.kakao.maps.Size(24, 35);
    const markerImage = new window.kakao.maps.MarkerImage(imageSrc, imageSize);

    var marker = new window.kakao.maps.Marker({
        position: markerPosition,
        image : markerImage
    });

    marker.setMap(map);
    
  },
}
</script>

<style scoped>
.map-container {
  display: flex;
  justify-content: center;
  margin-bottom: 5px;
  margin-left: auto;
  margin-right: auto;
}
</style>