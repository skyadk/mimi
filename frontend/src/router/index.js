import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/accounts/Login.vue')
  },
  {
    path: '/signup',
    name: 'Signup',
    component: () => import('../views/accounts/Signup.vue')
  },
  {
    path: '/findidpw',
    name: 'FindIdPw',
    component: () => import('../views/accounts/FindIdPw.vue')
  },
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue'),    
    // 상단바와 하단바가 있는 views는 아래에 children으로 등록되어야 합니다.
    children: [
      {
        path: '',
        name: 'Main',
        component: () => import('../views/Main.vue')
      },
      {
        path: '/diary',
        name: 'Diary',
        component: () => import('../views/Diary.vue')
      },
      {
        path: '/selectoption',
        name: 'SelectOption',
        component: () => import('../views/courses/SelectOption.vue')
      },
      {
        path: '/travelingcourse/:location/:thema',
        name: 'TravelingCourse',
        component: () => import('../views/courses/TravelingCourse.vue'),
        props: true
      },
      {
        path: '/coursecheck',
        name: 'CourseCheck',
        component: () => import('../views/courses/CourseCheck.vue')
      },
      {
        path: '/restaurantdetail/:id',
        name: 'RestaurantDetail',
        component: () => import('../views/restaurants/RestaurantDetail.vue')
      },
      {
        path: '/timeline',
        name: 'Timeline',
        component: () => import('../views/timelines/Timeline.vue')
      },
      {
        path: '/traveldetail',
        name: 'TravelDetail',
        component: () => import('../views/travels/TravelDetail.vue')
      },
      {
        path: '/restaurantsearch/:word/:lat/:log',
        name: 'RestaurantSearch',
        component: () => import('../views/restaurants/RestaurantSearch.vue'),
        props: true,
      },
    ]
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,

  // 스크롤 초기화
  scrollBehavior() { 
    return { x: 0, y: 0 } 
  },
})

export default router
