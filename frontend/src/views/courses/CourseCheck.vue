<template>
    <div id="container">
        <v-container>
            <v-row style="padding-top: 3px;">
                <v-col>
                    <h2 id="container3">여행 코스 확인</h2>
                </v-col>
                <v-col>
                    <v-dialog v-model="dialog1" max-width="290">
                        <template v-slot:activator="{ on, attrs }">
                            <v-col class="pt-0" align="end" style="margin-right: 10px;" v-bind="attrs" v-on="on">
                                <i class="fas fa-info-circle fa-2x" style="color: #6A1B9A;"></i>
                            </v-col>
                        </template>
                        <v-card>
                            <v-card-title id="container1">미미여지도 사용설명서</v-card-title>
                            
                            <v-divider></v-divider>

                            <v-card-text id="container5">
                                <br>
                                커스텀한 여행코스의 <span style="font-weight: bold;">경로를 최적화</span>할 수 있습니다!<br>
                                경로를 확인하시고 다이어리 저장 버튼을 눌러 <span style="font-weight: bold;">여행코스를 다이어리에 저장</span>해보세요 :)<br>
                                그리고 1, 2, 3, 4번 <span style="font-weight: bold;">여행지를 클릭</span>하면 <span style="font-weight: bold;">주변 맛집과 키워드별 맛집을 추천</span>해 드립니다<br>
                                맛집도 <span style="font-weight: bold;">+버튼</span>을 눌러 <span style="font-weight: bold;">다이어리에 저장</span>할 수 있어요!<br>
                                <span style="font-weight: bold; color: #FF7043;">★ 경로 최적화 기능은 실제 길찾기 경로를 기반으로 최적화되었으며 일직선으로 표시된 지도 경로와는 조금 다를 수 있습니다. ★</span>
                            </v-card-text>
                            <v-card-actions>
                                <v-btn color="black" text @click="dialog1 = false" id="container1">
                                    닫기
                                </v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-dialog>
                </v-col>
            </v-row>
        </v-container>
        <v-container>
            <v-row>
                <v-col align="end" class="pt-2">
                    <v-btn
                        class="ma-2"
                        color="#6A1B9A"
                        outlined
                        @click="moveToBack"
                    >
                        <span class="ts">이전</span>
                    </v-btn>            
                    <v-btn
                        class="ma-2"
                        color="#6A1B9A"
                        outlined
                        @click="optimizeCourse"
                    >
                        <span class="ts" >경로 최적화</span>
                    </v-btn>
                    <v-btn
                        class="ma-2"
                        color="#6A1B9A"
                        outlined
                        @click="dialog = true"
                        >
                        <span class="ts">다이어리 저장</span>
                    </v-btn>
                    <v-dialog v-model="dialog" max-width="290">
                        <v-card>
                        <v-card-title class="text-h6" style="word-break: keep-all;">
                            코스가 마음에 든다면 다이어리에 저장하세요!
                        </v-card-title>
                        <v-menu
                            ref="menu"
                            v-model="menu"
                            :close-on-content-click="false"
                            :return-value.sync="date"
                            transition="scale-transition"
                            offset-y
                            min-width="auto"
                        >
                            <template v-slot:activator="{ on, attrs }">
                            <v-text-field
                                v-model="date"
                                label="날짜 선택"
                                prepend-icon="mdi-calendar"
                                readonly
                                v-bind="attrs"
                                v-on="on"
                                class="ml-6"
                                style="width: 150px;"
                            ></v-text-field>
                            </template>
                            <v-date-picker v-model="date" no-title scrollable>
                            <v-spacer></v-spacer>
                            <v-btn text color="primary" @click="menu = false">
                                Cancel
                            </v-btn>
                            <v-btn text color="primary" @click="$refs.menu.save(date)">
                                OK
                            </v-btn>
                            </v-date-picker>
                        </v-menu>

                        <v-divider></v-divider>

                        <v-card-actions>
                            <v-spacer></v-spacer>

                            <v-btn color="green darken-1" text @click="dialog = false">
                            취소
                            </v-btn>

                            <v-btn color="green darken-1" text @click="saveCourse">
                            저장
                            </v-btn>

                        </v-card-actions>
                        </v-card>
                    </v-dialog>        
                </v-col>
            </v-row>
        </v-container>
        <CourseStore align="center" class="pt-2 pb-1" :recommend="recommendCourse" v-if="recommendCourse.length > 0"></CourseStore>
        <CourseMap align="center"></CourseMap>
        <Category :address="selectInfo[0]" :latitude="selectInfo[1]" :logitude="selectInfo[2]" ></Category>
    </div>
</template>

<script>
import Category from '@/components/restaurants/Category.vue'
import CourseStore from '@/components/courses/CourseStore.vue'
import CourseMap from '@/components/courses/CourseMap.vue'
import axios from 'axios'
import { mapState } from 'vuex'
export default {
    name: 'CourseCheck',
    components: {
        Category,
        CourseStore,
        CourseMap,
    },
    data: () => ({
        dialog: false,
        dialog1: false,
        date: new Date().toISOString().substr(0, 10),
        menu: false,
        // 주석
        // latitude: '',
        // logitude: '',
        // address: '',
        // 주석
    }),
    methods: {
        saveCourse() {
            this.dialog = false
            const serverUrl = process.env.VUE_APP_SERVER_URL
            const data = {
                id: this.userEmail,
                lid1: this.recommendCourse[0].lid,
                lid2: this.recommendCourse[1].lid,
                lid3: this.recommendCourse[2].lid,
                lid4: this.recommendCourse[3].lid,
                savedDate: this.date,
            }
            console.log(data)
            axios.post(`${serverUrl}/recommendroad/save-option-land`, data)
                .then(res => {
                console.log(res)
                alert('다이어리 저장 성공')
                })
                .catch(err => {
                console.log(err)
                })
        },
        saveLocation() {
            const data = {
                address: this.recommendCourse[0].addr.split(" ")[1],
                latitude: this.recommendCourse[0].latitude,
                logitude: this.recommendCourse[0].longitude,
            }
            console.log(data)
            this.$store.dispatch('changeLocationInfo', data)            
        },
        optimizeCourse() {
            const serverUrl = process.env.VUE_APP_SERVER_URL
            const data = {
                id: this.userEmail,
                lid1: this.recommendCourse[0].lid,
                lid2: this.recommendCourse[1].lid,
                lid3: this.recommendCourse[2].lid,
                lid4: this.recommendCourse[3].lid
            }
            // console.log(data)
            axios.post(`${serverUrl}/recommendroad/road-sort`, data)
                .then(res => {
                    // console.log(res.data.sort_value)
                    this.$store.dispatch('RECOMMENDCOURSE', res.data.sort_value)
                    alert('경로 최적화 완료')
                    // this.$router.go(this.$router.currentRoute);
                })
                .catch(err => {
                    console.log(err)
                })
        },
        moveToBack() {
            history.back()
        },
    },
    computed: {
        ...mapState ([
            'userEmail',
            'recommendCourse',
            'selectInfo'
        ])
    },
    created() {
        this.saveLocation()
    }
}
</script>

<style scoped>
    .ts {
        color: #6A1B9A;
        font-weight: 900;
    }
</style>