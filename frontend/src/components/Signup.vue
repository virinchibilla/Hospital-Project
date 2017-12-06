<template>
  <div class="signup">
    <div class="tabpanel">
      <div class="column is-8">
        <div class="columns">
          <div class="column is-4">
        <h1 class="title is-1">{{ title }}</h1>
      </div>
    </div><br>
     <div class="columns">
          <div class="column is-2">
            <b>First Name</b>
          </div>
          <div class="column is-4">
            <input :class="{'input': true, 'is-danger': errors.has('first name') }" v-model="firstname" type="text"
            v-validate="'required|min:2|max:20'" name="first name">
            <span class="text-danger" v-show="errors.has('first name')">{{ errors.first('first name') }}</span>
          </div>
        </div>
        <div class="columns">
          <div class="column is-2">
            <b>Last Name</b>
          </div>
          <div class="column is-4">
            <input :class="{'input': true, 'is-danger': errors.has('last name') }" v-model="lastname" type="text"
            v-validate="'required|min:2|max:20'" name="last name">
            <span class="text-danger" v-show="errors.has('last name')">{{ errors.first('last name') }}</span>
          </div>
        </div>
        <div class="columns">
          <div class="column is-2">
            <b>Email</b>
          </div>
          <div class="column is-4">
            <input :class="{'input': true, 'is-danger': errors.has('email') }" name="email" type="text" v-model="email"
            v-validate="'required|email'">
            <span class="text-danger" v-show="errors.has('email')">{{ errors.first('email') }}</span>
          </div>
        </div>
         <div class="columns">
          <div class="column is-2">
            <b>Password</b>
          </div>
          <div class="column is-4">
            <input :class="{'input': true, 'is-danger': errors.has('password') }" name="password" type="password" v-model="password"
            v-validate="'required|min:2|max:10'">
            <span class="text-danger" v-show="errors.has('password')">{{ errors.first('password') }}</span>
          </div>
        </div>
        <div class="columns">
          <div class="column is-2">
            <b>Confirm password</b>
          </div>
          <div class="column is-4">
            <input :class="{'input': true, 'is-danger': errors.has('confirm password') }" name="confirm password" type="password" v-model= "confirmpassword"
            v-validate="'required|min:2|max:10'">
            <span class="text-danger" v-show="errors.has('confirm password')">{{ errors.first('confirm password') }}</span>
          </div>
        </div>
        <div class="columns">
          <div class="column is-2">
            <b>Username</b>
          </div>
          <div class="column is-4">
            <input :class="{'input': true, 'is-danger': errors.has('user name') }" v-model= "username" type="text"
            v-validate="'required|min:2|max:8'" name="user name">
            <span class="text-danger" v-show="errors.has('user name')">{{ errors.first('user name') }}</span>
          </div>
        </div>
            <div class="columns">
            <div class="column is-2">
              <p class="control">
                <button
                class="button is-primary"
                v-on:click = 'signup'
                >Sign up</button>
              </p>
            </div>
          </div>
          <div class="column is-5">
          <div v-show="error" v-html="error" class="notification box is-danger"> {{ msg }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  import router from '../router'
  import VeeValidate from 'vee-validate'
  import Vue from 'vue'

  Vue.use(VeeValidate)

  export default {
    name: 'signup',
    data () {
      return {
        title: 'Signup',
        firstname: '',
        lastname: '',
        email: '',
        password: '',
        confirmpassword: '',
        username: '',
        error: ''
      }
    },
    methods: {
      signup () {
        /* if (!this.validateFields()) {
          return
        } */
        if (this.confirmpassword !== this.password) {
          this.error = 'Cannot sign up. Password should match'
          return
        }
        const data = { firstname: this.firstname,
          lastname: this.lastname,
          email: this.email,
          password: this.password,
          username: this.username,
          confirmpassword: this.confirmpassword }
        axios.post('http://127.0.0.1:8000/hosapi/v1/signup/', data)
        .then(() => {
          this.msg = 'sign in successful'
          console.log(data)

          router.push('/*')
        })
        .catch((error) => {
          this.msg = error.message
        })
      }
      /* validateFields () {
        this.$validator.validateAll()
        if (!this.errors.any()) {
          return true
        }
        return false
      } */
    },
    beforeMount () {
   // this.loguser();
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss">
@import '~bulma';

.tabpanel {
  margin-left: 2em;
}

</style>
