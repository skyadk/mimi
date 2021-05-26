<template>
  <v-form>
    <v-container>
      <v-row>
        <v-col
          cols="12"
          class="pb-0"
        >    
          <!-- email -->
          <v-text-field
            style="margin-top: 1rem;"
            solo
            flat
            dense
            outlined
            prepend-inner-icon="mdi-email-outline"
            :rules="[required_id, emailRules,]"
            label="아이디(이메일)"
            v-model="form.id"
          ></v-text-field>

          <v-btn 
            block
            @click="sendCertNum"
            class="mb-5"
          >인증번호 발송</v-btn>

          <!-- 인증번호 입력 -->
          <v-row v-if="showCert">
            <v-col cols=8>
              <v-text-field
                v-model="certInput"
                solo
                flat
                dense
                outlined
                prepend-inner-icon="mdi-key"
                label="인증번호"
              ></v-text-field>
            </v-col>
            <v-col cols=4 class="">
              <v-btn block @click="checkCert">확인</v-btn>
            </v-col>
          </v-row>
          
          <!-- 비밀번호 입력 -->
          <v-text-field
            v-model="form.password"
            solo
            flat
            dense
            outlined
            required
            prepend-inner-icon="mdi-lock-outline"
            :rules="[required, min_pw]"
            type="password"
            label="새 비밀번호"
          ></v-text-field> 

          <!-- 비밀번호 확인 -->
          <v-text-field
            solo
            flat
            dense
            outlined
            required
            prepend-inner-icon="mdi-lock-check-outline"
            :rules="[passwordConfirmationRule]"
            v-model="rePassword"
            type="password"
            label="새 비밀번호 확인"
          ></v-text-field>
        </v-col>

        <v-col cols="12">
          <v-btn style="background-color: #0275d8; color: white; 
            font-size: 1.5rem; font-weight: bold; 
            width: 100%; height: 150%;"
            :disabled="!enable"
            @click="changePw"
          >
            비밀번호 재설정
          </v-btn>
        </v-col>         
      </v-row>
    </v-container>
  </v-form>
</template>

<script>
import axios from 'axios'
export default {
  name: 'FindPw',
  components: {

  },
  data: () => ({
    rePassword: '',
    form: {
      id: '',
      password: '',
    },
    showCert: false,
    certInput: '',
    certAnswer: '',
  }),
  methods: {
    sendCertNum() {
      console.log('인증번호 발송')
      this.showCert = true
      const serverUrl = process.env.VUE_APP_SERVER_URL
      axios.get(`${serverUrl}/member/find-auth-email/${this.form.id}`)
        .then(res => {
          console.log(res.data.message)
          this.certAnswer = res.data.message
        })
        .catch(err => {
          console.log(err)
          alert('메일 정보를 찾을 수 없습니다.')
        })
    },
    changePw() {
      console.log('비밀번호 재설정')
      const serverUrl = process.env.VUE_APP_SERVER_URL
      axios.put(`${serverUrl}/member/update-pw/${this.form.id},${this.form.password}`)
        .then(res => {
          console.log(res)
          alert('비밀번호 재설정 완료')
          this.$router.push({name: 'Login'})
        })
        .catch(err => {
          console.log(err)
        })
    },
    checkCert() {
      if (this.certInput === this.certAnswer) {
        alert("인증완료")
      } else {
        alert("인증번호를 다시 확인해주세요")
      }
    }
  },
  computed: {
    required() {
      return () => !!this.form.password || '비밀번호를 입력해주세요.'
    },
    required_id() {
      return () => !!this.form.id || '아이디(이메일)를 입력해주세요.'
    },
    min_pw() {
      return () => this.form.password.length >= 8 || '비밀번호를 8자 이상 작성해주세요.'
    },
    emailRules() {
      return () => /.+@.+\..+/.test(this.form.id) || '아이디(이메일)는 이메일 형식으로 입력해주세요.'
    },
    passwordConfirmationRule() {
      return () => (this.form.password === this.rePassword) || '비밀번호가 일치하지 않습니다.'
    },
    enable() {
      if (this.emailRules() == true && this.passwordConfirmationRule() == true && this.min_pw() == true) {
        return true
      } else {
        return false
      }
    },
    certStatus() {
      if (this.certInput === this.certAnswer) {
        return true
      } else {
        return false
      }
    }    
  }  
}
</script>

<style>

</style>