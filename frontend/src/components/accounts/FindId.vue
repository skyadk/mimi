<template>
  <v-container>
    <v-row>
      <v-col>
        <v-form>
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
        </v-form>
      </v-col>

      <v-col cols="12">
        <v-btn style="background-color: #0275d8; color: white; 
          font-size: 1.5rem; font-weight: bold; 
          width: 100%; height: 150%;"
          :disabled="!enable"
          @click="findId"
        >
          가입여부 확인하기
        </v-btn>
      </v-col>      
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios'
export default {
  name: 'FindId',
  components: {

  },
  data: () => ({
    form : {
      id: '',
      birthday: '',
    },
    menu: false,
  }),
  methods: {
    findId() {
      console.log('가입여부 확인하기')
      const serverUrl = process.env.VUE_APP_SERVER_URL
      axios.get(`${serverUrl}/member/find-id/${this.form.id},${this.form.birthday}`)
        .then(res => {
          console.log(res)
          alert('가입된 유저입니다.')
        })
        .catch(err =>{
          console.log(err)
          alert('가입된 정보가 없습니다.')
        })
    }
  },
  computed: {
    required_id() {
      return () => !!this.form.id || '아이디(이메일)를 입력해주세요.'
    },
    emailRules() {
      return () => /.+@.+\..+/.test(this.form.id) || '아이디(이메일)는 이메일 형식으로 입력해주세요.'
    },
    dateRules() {
      return console.log('test')
    },
    enable() {
      if (this.emailRules() == true && !!this.form.birthday == true) {
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