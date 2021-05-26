<template>
  <div class="bg main" style="justify-center">
    <img src="@/assets/real_logo.png" alt="" class="foodsize">
    <div>
      <input v-model="searchKeyword" type="text" value="" placeholder="맛집 주소를 입력하세요.  : )" id="searchBar" @keypress.enter="searchstore">
      <button @click="searchstore()"><i class="fas fa-search"></i></button>
    </div>
	<v-dialog 
		v-model="dialog"
		scrollable
		width="80%"
		id="container"
	>
		<v-card>
			<v-card-title>찾으시는 곳이 여기인가요?</v-card-title>
			<v-divider></v-divider>
			<v-list>
				<v-list-item-group
					color="#6A1B9A"
				>
					<v-list-item
						v-for="(item, i) in locationList"
						:key="i"
					>
						<v-list-item-content @click="selectLocation(item)">
							<v-list-item-title v-text="item.address_name"></v-list-item-title>
						</v-list-item-content>
					</v-list-item>
				</v-list-item-group>
			</v-list>
		</v-card>
	</v-dialog>
	<div class="tc">
		<p>★맛집 검색 꿀팁!을 알려드립니다★</p>
		<p>가고싶은 음식점의 '시(도)'와 장소를 함께 적으면</p> 
		<p>더 정확한 음식점을 추천받을 수 있습니다.</p>
		<p>예) 부산 해운대</p>
	</div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Main',
  components: {
  },
  data() {
    return {
		store: '',
		searchKeyword: '',
		dialog: false,
		locationList: Array,
    }
  },
	methods: {
		async selectLocation (item) {
			const arr = item.address_name.split(" ");
			const key = arr[arr.length-1];
			this.$router.push(`/restaurantsearch/${key}/${item.y}/${item.x}`)

		},
		searchstore () {
			let searchKeyword = this.searchKeyword
			let searchUrl = `https://dapi.kakao.com/v2/local/search/address.json?analyze_type=similar&page=1&size=10&query=${searchKeyword}`
			let headers = {
				'Authorization': `KakaoAK ${process.env.VUE_APP_KAKAO_REST_API_KEY}`
			}
			
			axios({
				method: 'get',
				url: searchUrl,
				headers: headers,
			}).then(res => {
				this.locationList = res.data.documents
				this.dialog = true;

			}).catch(err => {
				console.log(err)
			})
		}
	}
}
</script>

<style scoped>
.bg {
  background-image: linear-gradient(to bottom right, #EDE7F6,#F8BBD0);
  /* min-height: 750px; */
  display: flex;
  flex-direction: column;
  align-items: center;
  top: 0;
  left: 0; 
    
  /* Preserve aspet ratio */
  min-width: 100%;
  min-height: 100%;
}

h1 {
	color: #4A148C;
	font-weight: bold;
	font-size: 48pt;
	margin-top: 30%;
	clear: right;
}

input {
	margin: 70px 0;
	background: none;
	border-bottom: 1px solid #6A1B9A;
	border-top: none;
	border-left: none;
	border-right: none;
	width: 250px;
	height: 30px;
}

input:focus {
	outline: none;
	border-bottom: 3px solid #6A1B9A;
	color: #6A1B9A;
}

::-webkit-input-placeholder {
	color: #6A1B9A;
	font-weight: normal;
}

:-moz-placeholder {
	color: #6A1B9A;
	font-weight: normal;
}

::-moz-placeholder {
	color: #6A1B9A;
	font-weight: normal;
}

:-ms-input-placeholder {
	color: #6A1B9A;
	font-weight: normal;
}

/* button {
	width: 50px;
	height: 50px;
	background: none;
	border: none;
	position: absolute;
	top: 200px;
	left: 275px;
} */

button:focus {
	outline: none;
}

.fas {
	color: #6A1B9A;
	font-size: 2em;
}

.foodsize {
  width: 320px;
  margin-top: 30%;
}
.tc {
	color: #616161;
	line-height: 5px;
	text-align: center;
}
</style>