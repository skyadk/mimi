<template>
  <div id="map" class="map-container" style="max-width:800px;height:200px;"></div>
</template>

<script>
import { mapState } from 'vuex'
export default {
    name: 'CourseMap',
    computed: {
        ...mapState([
            'recommendCourse'
        ])
    },
    async mounted() {
        
        const container = document.getElementById('map');
        
        const options = {
            center: new window.kakao.maps.LatLng(this.recommendCourse[1].latitude, this.recommendCourse[1].longitude),
            level: 8
        };
        
        const map = new window.kakao.maps.Map(container, options);
        console.log(map);

        const positions = [
            {
                title: this.recommendCourse[0].landmark_name, 
                latlng: new window.kakao.maps.LatLng(this.recommendCourse[0].latitude, this.recommendCourse[0].longitude)
            },
            {
                title: this.recommendCourse[1].landmark_name, 
                latlng: new window.kakao.maps.LatLng(this.recommendCourse[1].latitude, this.recommendCourse[1].longitude)
            },
            {
                title: this.recommendCourse[2].landmark_name,
                latlng: new window.kakao.maps.LatLng(this.recommendCourse[2].latitude, this.recommendCourse[2].longitude)
            },
            {
                title: this.recommendCourse[3].landmark_name,
                latlng: new window.kakao.maps.LatLng(this.recommendCourse[3].latitude, this.recommendCourse[3].longitude)
            },
        ];
        
        const linePath = []
        for (let i = 0; i < positions.length; i ++) {
            linePath.push(positions[i].latlng)
        }

        const polyline = new window.kakao.maps.Polyline({
            path: linePath, // 선을 구성하는 좌표배열
            strokeWeight: 5, // 선의 두께
            strokeColor: '#4A148C', // 선의 색깔
            strokeOpacity: 0.8, // 선의 불투명 - 1에서 0 사이의 값이며 0에 가까울수록 투명
            strokeStyle: 'solid' // 선의 스타일
        });

        polyline.setMap(map);

        const imageSize = new window.kakao.maps.Size(24, 35);

        for (let i = 0; i < positions.length; i ++) {
    
            let imageSrc = "";
            if (i == 0) {
                imageSrc = "https://i.ibb.co/6RxfQyd/pin1.png";
            } else if (i == 1) {
                imageSrc = "https://i.ibb.co/jy9g2LX/pin2.png";
            } else if (i == 2) {
                imageSrc = "https://i.ibb.co/1MLCC3s/pin3.png";
            } else {
                imageSrc = "https://i.ibb.co/fMMxB05/pin4.png";
            }
            console.log(positions[i])
            addMarker(positions[i], imageSrc)

        }
        
        function addMarker(position, imageSrc) {
            const markerImage = new window.kakao.maps.MarkerImage(imageSrc, imageSize);
            
            const marker = new window.kakao.maps.Marker({
                map: map,
                position: position.latlng,
                title : position.title,
                image : markerImage
            });
            marker.markerImage = markerImage;

        }
    },

}
</script>

<style scoped>
.map-container {
  display: flex;
  justify-content: center;
  margin-bottom: 30px;
  margin-left: auto;
  margin-right: auto;
}
</style>