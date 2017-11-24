<template>
  <div class="Welcome">
   <div class="container columns">
    <div class="column is-full">
      <div class="tabs is-centered">
        <ul>
          <li :class="{'is-active' : tabSelected=='subjects'}" @click="tabSelected='subjects'" v-if="isAdmin || isSubjectEditor"><a>Subjects</a></li>
          <li :class="{'is-active' : tabSelected=='samples'}" @click="tabSelected='samples'" v-if="isAdmin || isSampleEditor"><a>Samples</a></li>
          <li :class="{'is-active' : tabSelected=='profile'}"><a @click="tabSelected='profile'">My profile</a></li>
          <li :class="{'is-active' : tabSelected=='admin'}"><a @click="tabSelected='admin'">Admin</a></li>
          <li :class="{'is-active' : tabSelected=='logout'}"><a @click="logout">Logout</a></li>
        </ul>
      </div>
      <div id="subjects" class="tabpanel" v-if="tabSelected==='subjects'">
        <div class="columns is-8">
         <div class="column">
          <table class="table">
            <thead>
              <tr>
                <th> Id</abbr></th>
                <th>Subject code</abbr></th>
                <th>Create date</abbr></th>
                <th> Subject ID</abbr></th>
                <th>Blood type</abbr></th>
                <th>Action</abbr></th>
                <th>Delete</abbr></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="s in subjects">
                <td v-html="s.id"></td>
                <td>
                  <input class="input" type="text" name="" v-model="s.subject_code">
                </td>
                <td>
                  <input class="input" type="text" name="" v-model="s.create_date">
                </td>
                <td v-html="s.created_id"></td>
                <td>
                  <div class="select">
                    <select v-model="s.blood_type">
                     <option>A+</option>
                     <option>A-</option>
                     <option>B+</option>
                     <option>B-</option>
                     <option>O</option>
                     <option>AB+</option>
                   </select> 
                 </div>
               </td>
               <td><div class="button" v-on:click="update_subjects(s)">Update</div></td>
               <td><div class="button" v-on:click="delete_subjects(s)">Delete</div></td>
             </tr>
           </tbody>
         </table><br>
         <div class="columns">
          <div class="column is-2">
           <button class="button is-primary" v-on:click="get_subjects">Subjects</button>
         </div>
       </div><br>
     </div>
   </div>
   <div class="box">
    <div class="columns">
      <div class="column is-8">
        <div class="columns">
          <div class="column is-3">
            <b>Subject Code</b>
          </div>
          <div class="column is-2">
            <input v-model="subjectcode" class="input" type="text">
          </div>
        </div>
        <div class="columns">
          <div class="column is-3">
            <b>DATE</b>
          </div>
          <div class="column is-4">
           <datepicker :input-class="'input'" v-model="dateselected" placeholder="European Format ('d-m-Y')" :config="{ dateFormat: 'd-m-Y', static: true }">
           </datepicker>
         </div>
       </div>
       <div class="columns">
        <div class="column is-3">
          <b>Blood Type</b>
        </div>
        <div class="column is-2">
         <div class="select">
           <select v-model="bloodtype">
             <option>A+</option>
             <option>A-</option>
             <option>B+</option>
             <option>B-</option>
             <option>O</option>
             <option>AB+</option>
           </select>
         </div>
       </div>
     </div>
   </div>
 </div>
</div>
<div class="column is-2">
  <button class="button is-primary"
  v-on:click = 'create_subject'
  >Create Subject</button>
</div>
<br>{{ msgs }}
</div>

<div id="samples" class="tabpanel" v-if="tabSelected==='samples'">
 <div class="columns">
  <div class="column is-8">
    <div class="columns">
      <div class="column is-2">
        <b>SubjectID</b>
      </div>
      <div class="column is-3">
       <div class="select">
         <select v-model="selectedsamplesubject">
           <option :value="s.id" v-for="s in subjects_id"> {{ s.created_id }}</option>
         </select>
       </div>
     </div>
   </div>
   <div class="columns">
     <div class="column is-2">
      <b>Cancer type</b>
    </div>
    <div class="column is-2">
     <label class="checkbox">
      <input type="checkbox" value="heart" v-model="cancertype">&nbsp;Heart</label> 
      <br>
      <label class="checkbox">
        <input type="checkbox" value="bone" v-model="cancertype">&nbsp;Bone</label>
        <br>
        <label class="checkbox">
          <input type="checkbox" value="kidney" v-model="cancertype">&nbsp;Kidney
        </label>
      </div>
    </div>
    <div class="column is-2">
      <button class="button is-primary"
      v-on:click = 'create_sample'
      >Create Sample</button>
    </div>
  </div>
</div>
<br>
  <div class="box">
  <div class="columns">
    <div class="column is-8">
      <div class="columns">
        <table class="table" v-if="samples">
          <thead>
            <tr>
              <th> Id</abbr></th>
              <th>Subject_ID</abbr></th>
              <th>Cancer type</abbr></th>
              <th>Action</abbr></th>
              <th>Delete</abbr></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="m in samples">
              <td v-html="m.id"></td>
              <td v-html="m.created_id"></td>
              <td>
                <template v-for="ct in [{'name':'heart'},{'name':'bone'},{'name':'kidney'}]">
                  <label class="checkbox">
                    <input type="checkbox" :value="ct" v-model="m.cancer">&nbsp;{{ ct.name }}
                  </label>
                </template></td>
              <td><div class="button" v-on:click="update_samples(m)">Update</div></td>
              <td><div class="button" v-on:click="delete_samples(m)">Delete</div></td>
            </tr>
          </tbody>
        </table>
      </div>
      </div>
  </div>
</div>
<div class="column is-2">
  <button class="button is-primary" v-on:click="get_samples">Samples</button>
</div>
</div>
<div id="profile" class="tabpanel"  v-if="tabSelected==='profile'">
  <div class="column is-8">
    <div class="columns">
      <div class="column is-2">
       <label class="label paddingtopless">First name</label> 
     </div>
     <div class="column is-2">
       <input v-model="hospuser_data.first_name"  class="input" type="text" placeholder="">
     </div>
   </div>
   <div class="columns">
    <div class="column is-2">
     <label class="label paddingtopless">Last name</label> 
   </div>
   <div class="column is-2">
     <input v-model="hospuser_data.last_name"  class="input" type="text" placeholder="">
   </div>
 </div>
 <div class="columns">
  <div class="column is-2">
   <label class="label paddingtopless">Email</label> 
 </div>
 <div class="column is-3">
   <input v-model="hospuser_data.email"   class="input" type="text" placeholder="">
 </div>
</div>
<div class="columns">
  <div class="column is-2">
   <label class="label paddingtopless">User name</label> 
 </div>
 <div class="column is-2">
   <input v-model="hospuser_data.username"  class="input" type="text" placeholder="">
 </div>
</div>
</div>
</div>
<div id="admin" class="tabpanel" v-if="tabSelected==='admin'">
  <div class="column is-8" v-if="isAdmin">
    <table class="table">
      <thead>
        <tr>
          <th>First Name</abbr></th>
          <th>Lastname</abbr></th>
          <th>Email</abbr></th>
          <th>Role</abbr></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in hospusers_data_all">
          <td v-html="user.first_name"></td>
          <td v-html="user.last_name"></td>
          <td v-html="user.email"></td>
          <td>
            <select class="select" v-model="user.role">
              <option :value="r[0]" v-for="r in roles">
                {{ r[0] }}
              </option>
            </select>
          </td>
        </tr>
      </tbody>
    </table>
    <div class="column is-1">
     <div class="button" v-on:click="update_hospuser" >Update</div>
   </div>
 </div>
 <div class="column is-3" v-else>
  <b>You are not an admin</b>
</div>
</div>
</div>
</div>
</div>
</template>

<script>
import VueSession from 'vue-session'
import Vue from 'vue'
import Datepicker from 'vuejs-datepicker'
import axios from 'axios'
import router from '../router'

Vue.use(VueSession)

export default {
  components: {
    Datepicker
  },
  name: 'welcome',
  data () {
    return {
      title: 'Welcome to Your Vue.js App',
      tabSelected: '',
      hospusers_data_all: '',
      hospuser_data: '',
      subjectcode: '',
      bloodtype: '',
      dateselected: '',
      subjectsid: '',
      msg: '',
      msgs: '',
      subjects: [],
      cancertype: [],
      selectedsamplesubject: '',
      samples: [],
      isAdmin: '',
      isSubjectEditor: '',
      isSampleEditor: ''
      // hospusers_data_all: ''
        // shoppingData: {
        //   itemname: ['xj'],
        //   quantity: '',
        //   price: '',
        // },
    }
  },
  computed: {

  },
  methods: {
    logout () {
      this.$session.destroy()
      router.push('/*')
    },
    get_hospuser_data () {
      const username = this.$session.get('username')
      axios({
        method: 'GET',
        url: `http://127.0.0.1:8000/hosapi/v1/hospuser_data/${username}/`,
        headers: {
          Authorization: `Token ${this.$session.get('token')}`,
          'Content-Type': 'application/json'
        }
      })
        .then((response) => {
          this.hospuser_data = response.data
        })
        .catch((error) => {
          this.msg = error.message
        })
    },
    get_hospusers_data_all () {
      axios({
        method: 'GET',
        url: 'http://127.0.0.1:8000/hosapi/v1/hospuser_data/all/',
        headers: {
          Authorization: `Token ${this.$session.get('token')}`,
          'Content-Type': 'application/json'
        }
      })
        .then((response) => {
          this.hospusers_data_all = response.data.hospusers_data
          this.roles = response.data.roles
        })
        .catch((error) => {
          this.msg = error.message
        })
    },
    update_hospuser () {
      axios({
        method: 'PUT',
        url: 'http://127.0.0.1:8000/hosapi/v1/hospuser_data/update/',
        headers: {
          Authorization: `Token ${this.$session.get('token')}`,
          'Content-Type': 'application/json'
        },
        data: this.hospusers_data_all
      })
        .then(() => {
          this.msg = 'users is updated'
        })
        .catch((error) => {
          this.msg = error.message
        })
    },
    create_subject () {
      axios({
        method: 'POST',
        url: 'http://127.0.0.1:8000/hosapi/v1/subjectcreation/',
        headers: {
          Authorization: `Token ${this.$session.get('token')}`,
          'Content-Type': 'application/json'
        },
        data: { subjectcode: this.subjectcode,
          bloodtype: this.bloodtype,
          subjectsid: this.subjectsid,
          date: this.dateselected }
      })
        .then(() => {
          this.msgs = ''
          this.get_subjects()
          this.subjectcode = ''
          this.bloodtype = ''
          this.dateselected = ''
        })
        .catch((error) => {
          this.msg = error.message
        })
    },
    get_subjects () {
      axios({
        method: 'GET',
        url: 'http://127.0.0.1:8000/hosapi/v1/subjectsall/',
        headers: {
          Authorization: `Token ${this.$session.get('token')}`,
          'Content-Type': 'application/json'
        }
      })
        .then((response) => {
          this.subjects = response.data.subjects_data
        })
        .catch((error) => {
          this.msg = error.message
        })
    },
    update_subjects (s) {
      console.log(s)
      axios({
        method: 'PUT',
        url: 'http://127.0.0.1:8000/hosapi/v1/subjectupdate/',
        headers: {
          Authorization: `Token ${this.$session.get('token')}`,
          'Content-Type': 'application/json'
        },
        data: s
      })
        .then(() => {
          this.msg = ''
          this.get_subjects()
        })
        .catch((error) => {
          this.msg = error.message
        })
    },
    delete_subjects (s) {
      console.log(s)
      axios({
        method: 'DELETE',
        url: 'http://127.0.0.1:8000/hosapi/v1/subjectdelete/',
        headers: {
          Authorization: `Token ${this.$session.get('token')}`,
          'Content-Type': 'application/json'
        },
        data: s
      })
        .then(() => {
          this.msg = ''
          this.get_subjects()
        })
        .catch((error) => {
          this.msg = error.message
        })
    },
    create_sample () {
      axios({
        method: 'POST',
        url: 'http://127.0.0.1:8000/hosapi/v1/samplecreation/',
        headers: {
          Authorization: `Token ${this.$session.get('token')}`,
          'Content-Type': 'application/json'
        },
        data: { subject_id: this.selectedsamplesubject,
          cancertype: this.cancertype }
      })
        .then(() => {
          this.msg = ''
          this.get_samples()
          this.selectedsamplesubject = ''
          this.cancertype = []
        })
        .catch((error) => {
          this.msg = error.message
        })
    },
    get_samples () {
      axios({
        method: 'GET',
        url: 'http://127.0.0.1:8000/hosapi/v1/samplessall/',
        headers: {
          Authorization: `Token ${this.$session.get('token')}`,
          'Content-Type': 'application/json'
        }
      })
        .then((response) => {
          this.samples = response.data.samples_data
        })
        .catch((error) => {
          this.msg = error.message
        })
    },
    update_samples (m) {
      console.log(m)
      axios({
        method: 'PUT',
        url: 'http://127.0.0.1:8000/hosapi/v1/sampleupdate/',
        headers: {
          Authorization: `Token ${this.$session.get('token')}`,
          'Content-Type': 'application/json'
        },
        data: m
      })
        .then(() => {
          this.msg = ''
        })
        .catch((error) => {
          this.msg = error.message
        })
    },
    delete_samples (m) {
      console.log(m)
      axios({
        method: 'DELETE',
        url: 'http://127.0.0.1:8000/hosapi/v1/sampledelete/',
        headers: {
          Authorization: `Token ${this.$session.get('token')}`,
          'Content-Type': 'application/json'
        },
        data: m
      })
        .then(() => {
          this.msg = ''
          this.get_samples()
        })
        .catch((error) => {
          this.msg = error.message
        })
    },
    get_subject_id () {
      axios({
        method: 'GET',
        url: 'http://127.0.0.1:8000/hosapi/v1/subject_id/',
        headers: {
          Authorization: `Token ${this.$session.get('token')}`,
          'Content-Type': 'application/json'
        }
      })
        .then((response) => {
          this.subjects_id = response.data.subjects_id_data
        })
        .catch((error) => {
          this.msg = error.message
        })
    },
    refactorsubjectsample (m) {
      return m
    }
  },
  beforeMount () {
    this.get_hospuser_data()
    this.isAdmin = this.$session.get('role') === 'Admin'
    if (this.isAdmin) {
      this.get_hospusers_data_all()
      this.get_subjects()
      this.get_samples()
      this.get_subject_id()
    }
    this.isSubjectEditor = this.$session.get('role') === 'Subject editor'
    if (this.isSubjectEditor) {
      this.get_subjects()
    }
    this.isSampleEditor = this.$session.get('role') === 'Sample editor'
    if (this.isSampleEditor) {
      this.get_samples()
      this.get_subject_id()
    }
  }
}
</script>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss">
@import '~bulma';

.tabpanel {
  margin-left: 4em;
}

</style>
