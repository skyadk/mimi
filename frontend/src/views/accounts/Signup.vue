<template>
  <div class="bg">
    <v-form>
      <v-container>
        <v-row cols="12">
          <v-col
            cols="12"
            class="pb-0"
          >
            <h2><strong>회원정보를 입력해주세요</strong></h2>
            
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

            <!-- email중복 확인, 인증번호 발송 -->
            <!-- 중복이면 이미 가입된 이메일이라는 팝업 -->
            <!-- 가입되지 않은 이메일이면 인증번호 발송 -->
            <v-btn 
              block
              @click="sendCertNum"
              class="mb-5"
            >이메일 중복 확인 / 인증번호 발송</v-btn>

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
              <v-col cols=4 class="mt-1">
                <v-btn block large @click="checkCert">확인</v-btn>
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
              label="비밀번호"
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
              label="비밀번호 확인"
            ></v-text-field>

            <!-- 성별 -->
            <v-row class="">
              <v-col cols="2" class="pr-0 pb-0">
                <div class="mt-1">성별</div>
              </v-col>
              <v-col cols="10" class="pl-0 pb-0">
                <v-radio-group
                  v-model="form.gender"
                  row
                  class="mt-0"
                >
                  <v-radio
                    label="남성"
                    value="0"
                  ></v-radio>
                  <v-radio
                    label="여성"
                    value="1"
                  ></v-radio>
                </v-radio-group>
              </v-col>
            </v-row>

            <!-- 생년월일 -->
            <v-menu
              ref="menu"
              v-model="menu"
              :close-on-content-click="false"
              :return-value.sync="form.birthday"
              transition="scale-transition"
              offset-y
              min-width="auto"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                  v-model="form.birthday"
                  label="생년월일"
                  prepend-icon="mdi-calendar"
                  readonly
                  v-bind="attrs"
                  v-on="on"
                ></v-text-field>
              </template>
              <v-date-picker
                v-model="form.birthday"
                no-title
                scrollable
              >
                <v-spacer></v-spacer>
                <v-btn
                  text
                  color="primary"
                  @click="menu = false"
                >
                  Cancel
                </v-btn>
                <v-btn
                  text
                  color="primary"
                  @click="$refs.menu.save(form.birthday)"
                >
                  OK
                </v-btn>
              </v-date-picker>
            </v-menu>          
          </v-col>

          <v-col cols="12">
            <v-divider></v-divider>
          </v-col>
          
          <!-- 약관 동의 -->
          <SignupCheckbox :form="form" :enable="enable" />

          <!-- 푸터 -->
          <v-row class="pt-4" cols="10" align="center" justify="center">
            <p>©<strong>MIMI</strong> Team. All rights reserved.</p>
            <!-- <AccountsFooter /> -->
          </v-row>
        </v-row>
      </v-container>
    </v-form>
  </div>
</template>

<script>
import SignupCheckbox from '../../components/accounts/SignupCheckbox.vue'
// import AccountsFooter from '../../components/accounts/AccountsFooter.vue'
import axios from 'axios'

export default {
  components: { SignupCheckbox },
  name: 'Signup',
  data: () => ({
    rePassword: '',
    form: {
      id: '',
      password: '',
      gender: '',
      birthday: '',
    },
    showCert: false,
    menu: false,
    certInput: '',
    certAnswer: '',
  }),
  methods: {
    action() {
      console.log(this.form)
    },
    sendCertNum() {
      if (!!this.form.id == false) {
        alert('이메일을 입력해주세요')
      } else {
        console.log('인증번호 발송')
        this.showCert = true
        const serverUrl = process.env.VUE_APP_SERVER_URL
        console.log(serverUrl)

        axios.get(`${serverUrl}/member/auth-email/${this.form.id}`)
          .then(res => {
            console.log(res.data.message)
            this.certAnswer = res.data.message
          })
          .catch(err => {
            console.log(err)
            alert('이미 등록된 메일입니다.')
          })
      }
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
      if (this.emailRules() == true && this.passwordConfirmationRule() == true && this.min_pw() == true && this.form.gender != '' && !!this.form.birthday == true && this.certStatus == true) {
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

<style scoped>
.v-text-field__slot {
    margin: 10px;
  }

.v-messages__message {
    margin-top: 2px;
  }
  
.mdi-calendar {
    margin-top: 20px;
  }
.bg {
    background-image: linear-gradient(to bottom right, #EDE7F6,#F8BBD0);
    display: flex;
    flex-direction: column;
    align-items: center;
    /* position: fixed;  */
    top: 0; 
    left: 0;
    min-width: 100%;
    min-height: 100%;
  }
</style>