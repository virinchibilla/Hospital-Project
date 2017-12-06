<template>
	<div class="signin">
		<div class="tabpanel">
			<div class="column is-8">
				<div class="columns">
					<div class="column is-4">
						 <h1 class="title is-1">{{ title }}</h1>
					</div>
				</div><br>
				<div class="columns">
					<div class="column is-1">
						<b>Username</b>
					</div>
					<div class="column is-4">
                     <input v-model= "username" class="input" type="text">
                     </div>
				</div>
				<div class="columns">
					<div class="column is-1">
						<b>Password</b>
					</div>
					<div class="column is-4">
                     <input v-model= "password" class="input" type="password">
                     </div>
				</div>
				<form class="column is-half">
				<div class="columns">
            <div class="column is-2">
              <p class="control">
                <button class="button is-primary" v-on:click = 'userlog'>Sign in</button>
              </p>
            </div> <br>
            <div class="column is-2">
              <p class="control">
                <button
                class="button is-primary"
                v-on:click = 'signup'
                >Sign up</button>
              </p>
            </div>
          </div>
      </form>
        <div class="column is-4">
          <div v-show="error"  class="notification box is-danger"> {{ error }}</div>
        </div>
			</div>
		</div>
	</div>
</template>

<script>
  import VueSession from 'vue-session'
  import Vue from 'vue'
  import axios from 'axios'
  import router from '../router'

  Vue.use(VueSession)

  export default {
    name: 'signin',
    data () {
      return {
        title: 'Login',
        username: '',
        password: '',
        loginFailed: false,
        error: ''
      }
    },
    methods: {
      userlog () {
        const data = { username: this.username, password: this.password }
        axios.post('http://127.0.0.1:8000/hosapi/v1/userlog/', data)
        .then((response) => {
          this.msg = 'log in successfull'
          this.$session.start()
          this.$session.set('username', response.data.username)
          this.$session.set('token', response.data.token)
          this.$session.set('role', response.data.role)
          console.log(response)
          router.push('/welcome')
        })
        .catch((error) => {
          if (error.response.status === 403) {
            this.error = 'Check username & Password'
          }
        })
      },
      signup () {
        router.push('/signup')
      }
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
