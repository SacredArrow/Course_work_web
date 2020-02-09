<template>
  <div id="app-5">
    <p>{{ message }}</p>
    <p>{{ id }}</p>
    <textarea class="textarea" placeholder="e.g. Hello world" v-model="seq"></textarea>
    <textarea class="textarea" readonly v-model="result">This content is readonly</textarea>
    <button class="button is-warning" v-on:click="reverseMessage">Перевернуть сообщение</button>
    <button class="button is-warning" v-on:click="sendSequence">Отправить последовательность</button>
    <button class="button is-warning" v-on:click="getSequence">Получить результат</button>
  </div>
</template>

<script>
export default {
name: 'Example',
el: '#app-5',
data() {
  return {
  message: 'Привет, Vue.js!',
  ip: "142.93.128.77",
  port: 8000,
  seq:'',
  id : 0,
  result: 'Result will be shown here'
  }
},
computed: {
  address: function() {
  return 'http://' + this.ip + ':' + this.port+'/neuro'
  }
},
methods: {
  reverseMessage: function () {
    this.message = this.message.split('').reverse().join('')
  },
  sendSequence: function () {
  this.$http
    .post(this.address, {sequence: this.seq})
    .then(response => {
    this.id = response.data;
    console.log(response.data);
    })
    .catch(function (error) {
    console.log(error);
  });
  },
  getSequence: function() {
  this.$http
    .get(this.address, {params: {id: this.id}})
    .then(response => {
    this.result = response.data;
    console.log(response.data);
    })
    .catch(function (error) {
    console.log(error);
  });
  }
},
mounted() {
    this.$http
      .get('https://api.coindesk.com/v1/bpi/currentprice.json')
      .then(response => (this.message = response.data.time.updated));
  }

}
</script>
