<template>
  <div class="bg">
    <img src="@/assets/real_logo.png" alt="" class="foodsize">
    <v-form>
      <v-row cols="12" justify="center">
        <v-col
          cols="10"
          class="pb-0"
        >

          <v-text-field
            solo
            flat
            dense
            outlined
            prepend-inner-icon="mdi-email-outline"
            :rules="[rules.required_id, rules.emailRules,]"
            label="아이디(이메일)"
            v-model="form.id"
          ></v-text-field> 
          
          <v-text-field
            solo
            flat
            dense
            outlined
            required
            prepend-inner-icon="mdi-lock-outline"
            :append-icon="show_pw ? 'mdi-eye' : 'mdi-eye-off'"
            :rules="[rules.required_pw, rules.min_pw]"
            :type="show_pw ? 'text' : 'password'"
            label="비밀번호"
            v-model="form.password"
            @click:append="show_pw = !show_pw"
            @keypress.enter="login"
          ></v-text-field> 
        </v-col>
        
        <v-col cols="10">
          <v-row>
            <v-col class="pt-0">
              <span @click="$router.push({ name: 'Signup' })">회원가입</span>
            </v-col>
            <v-col class="pt-0 text-right">
              <span @click="$router.push({ name: 'FindIdPw' })">ID/PW찾기</span>
            </v-col>
          </v-row>
        </v-col>
        
        <v-col cols="10">
          <v-btn style="background-color: #6A1B9A; color: white; 
            font-size: 1.5rem; font-weight: bold; 
            width: 100%; height: 150%;"
            :disabled="!enable"
            @click="login"
          >
            로그인
          </v-btn>
        </v-col>
        
        <v-col cols="10" align="center">
          <p>©<strong>MIMI</strong> Team. All rights reserved.</p>
          <!-- <AccountsFooter /> -->
        </v-col>
      </v-row>
    </v-form>
  </div>
</template>

<script>
import axios from 'axios'

// import AccountsFooter from '@/components/accounts/AccountsFooter.vue'
export default {
  // components: { AccountsFooter },
  name: 'Login',
  data: () => ({
    form: {
      id: '',
      password: '',
    },
    show_pw: false,
    rules: {
      required_id: value => !!value || '아이디(이메일)를 입력해주세요.',
      emailRules: v => /.+@.+\..+/.test(v) || '아이디(이메일)는 이메일 형식으로 입력해주세요.',
      required_pw: value => !!value || '비밀번호를 입력해주세요.',
      min_pw: v => v.length >= 8 || '비밀번호를 8자 이상 작성해주세요.',
    },
  }),
  computed: {
    enable () {
      if (this.rules.emailRules(this.form.id) == true && this.rules.min_pw(this.form.password) == true) {
        return true
      } else {
        return false
      }
    }
  },
  methods: {
    login: function () {
      const serverUrl = process.env.VUE_APP_SERVER_URL
      console.log(serverUrl)
      axios.post(`${serverUrl}/member/sign-in`, {
        id: this.form.id,
        password: this.form.password
      })
        .then(res => {
          console.log(res)
          localStorage.setItem('mimi-authorization', res.data.token);
          const token = localStorage.getItem('mimi-authorization')
          console.log(token)
          this.$store.dispatch("LOGIN", token)
          this.$store.dispatch("SAVEEMAIL", this.form.id)
          this.$router.push({ name: 'Main' })
        })
        .catch(err => {
          console.log(err)
          alert('로그인에 실패하였습니다. 이메일 또는 비밀번호를 확인해주세요.')
        })
    }
  }
}
</script>

<style scoped>
  .bg {
    background-image: linear-gradient(to bottom right, #EDE7F6,#F8BBD0);
    display: flex;
    flex-direction: column;
    align-items: center;
    position: fixed; 
    top: 0; 
    left: 0;
    min-width: 100%;
    min-height: 100%;
  }
  .foodsize {
    width: 320px;
    margin-top: 30%;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .v-text-field--outlined >>> fieldset {
    border-color: #6A1B9A;
  }
  p {
    color: grey;
  }
  span {
    color: #6A1B9A;
  }
</style>