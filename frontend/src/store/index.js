import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'
import jwt_decode from "jwt-decode";

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    login: false,
    user: null,
    userEmail: null,
    recommendCourse: [],
    // 로더
    loader: {
      load: false,
    },
    dataloader: {
      dataload: false,
    },
    // 로더
    // address, latitude, logitude순
    selectInfo: ['', '', ''],
  },
  mutations: {
    logout(state) {
      state.login = false;
      state.user = null;
    },
    login(state, token) {
      let decode = jwt_decode(token);
      console.log('디코딩')
      console.log(decode)
      state.login = true;
      // console.log(state.login)
      state.user = decode.user
      // console.log(state.user)
    },
    saveEmail(state, data) {
      state.userEmail = data
      console.log(state.userEmail)
    },
    recommendCourse(state, data) {
      state.recommendCourse = data
    },
    // 로더
    SET_LOADER_TRUE(state) {
      state.loader.load = true;
    },
    SET_LOADER_FALSE(state) {
      state.loader.load = false;
    },
    SET_DATALOADER_TRUE(state) {
      state.dataloader.dataload = true;
    },
    SET_DATALOADER_FALSE(state) {
      state.dataloader.dataload = false;
    },
    // 로더
    RESET_COURSE(state) {
      state.recommendCourse = []
    },
    COURSE_CHANGE1(state, data) {
      state.recommendCourse.splice(0, 1, data)
      state.recommendCourse[4].one_two = '?'
    },
    COURSE_CHANGE2(state, data) {
      state.recommendCourse.splice(1, 1, data)
      state.recommendCourse[4].one_two = '?'
      state.recommendCourse[4].two_three = '?'
    },
    COURSE_CHANGE3(state, data) {
      state.recommendCourse.splice(2, 1, data)
      state.recommendCourse[4].two_three = '?'
      state.recommendCourse[4].three_four = '?'
    },
    COURSE_CHANGE4(state, data) {
      state.recommendCourse.splice(3, 1, data)
      state.recommendCourse[4].three_four = '?'
    },
    CHANGE_LOCATION_INFO(state, data) {
      console.log(data)
      state.selectInfo.splice(0, 1, data.address)
      state.selectInfo.splice(1, 1, data.latitude)
      state.selectInfo.splice(2, 1, data.logitude)
    }
  },
  actions: {
    LOGOUT({ commit }) {
      commit("logout");
      localStorage.removeItem("mimi-authorization")
    },
    LOGIN({ commit }, token) {
      commit("login", token);
    },
    SAVEEMAIL({ commit }, data) {
      commit("saveEmail", data)
    },
    RECOMMENDCOURSE({ commit }, data) {
      commit('recommendCourse', data)
    },
    resetCourse({ commit }) {
      commit('RESET_COURSE')
    },
    courseChange1({ commit }, data) {
      commit('COURSE_CHANGE1', data);
    },
    courseChange2({ commit }, data) {
      commit('COURSE_CHANGE2', data);
    },
    courseChange3({ commit }, data) {
      commit('COURSE_CHANGE3', data);
    },
    courseChange4({ commit }, data) {
      commit('COURSE_CHANGE4', data);
    },
    changeLocationInfo({ commit }, data) {
      commit('CHANGE_LOCATION_INFO', data)
    }
  },
  modules: {
  },
  getters: {
    getLoader(state) {
      return state.loader.load;
    },
    getDataLoader(state) {
      return state.dataloader.dataload;
    },
  },
  plugins: [
    createPersistedState()
  ]
})
