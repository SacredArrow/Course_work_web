<template>
<div id="app-5">
  <div class="container">
    <!-- <p>{{ message }}</p> -->
    <section class="hero is-primary">
      <div class="hero-body">
        <div class="container">
          <h1 class="title">
            {{message}}
          </h1>
          <h2 class="subtitle">
            ID of your sequence is: {{id}}
          </h2>
        </div>
      </div>
    </section>
    <!-- <p>{{ id }}</p> -->
    <div class="box">
      <textarea class="textarea" placeholder="Your sequence here" v-model="seq"></textarea>
    </div>
    <article class="message is-danger">
      <div class="message-body" v-if="error">
        Your sequence contains <strong> invalid characters</strong>! Should only contain A, C, G and U.
      </div>
    </article>
    <div class = "columns">
      <div class = "column">
<label class="label">Sensitivity of alignment</label>
        <div class="field is-grouped is-grouped-centered">

  <div class="control ">
    <input class="input"  type="text" v-model="sens">
  </div>
</div>
  </div>
  <div class = "column">
    <label class="label">Minimum number of matches in local alignment</label>
            <div class="field is-grouped is-grouped-centered">

      <div class="control ">
        <input class="input"  type="text" v-model="num_matches">
      </div>
    </div>
  </div>
  </div>
    <div class="buttons is-centered">
      <button class="button is-warning" v-bind:class="{ 'is-loading': isLoading}" v-on:click="sendSequence">Send sequence</button>
      <button class="button is-success" v-on:click="pasteExample">Example sequence</button>
    </div>
    <div class="box">
      <h1 class="title">Aligned result</h1>
      <textarea class="textarea is-family-monospace" style="white-space:pre;" readonly v-model="result">This content is readonly</textarea>
    </div>
    <div class="box">
      <h1 class="title">Unaligned result</h1>
      <textarea class="textarea is-family-monospace" readonly v-model="raw_result" ref="prev">This content is readonly</textarea>
    </div>
    <!-- <button class="button is-warning" v-on:click="reverseMessage">Перевернуть сообщение</button> -->

    <section class="section">
      <div class="columns" v-if="show_images">
        <div class="column">
          <figure class="image container is-256x256">
            <img :src="'data:image/jpeg;base64,'+img1" alt="Base64 encoded image" />
            <span class="tag" v-bind:class="{ 'is-warning': isLoading, 'is-success' : !isLoading}">Raw image</span>
          </figure>
        </div>
        <div class="column">
          <figure class="image container is-256x256">
            <img :src="'data:image/jpeg;base64,'+img2" alt="Binarized image">
            <span class="tag " v-bind:class="{ 'is-warning': isLoading, 'is-success' : !isLoading}">Binarized image</span>
          </figure>
        </div>
      </div>
    </section>
    <footer class="footer">
      <div class="content has-text-centered">
        <p>
          Some useful info. Or <strong>useful</strong>. <a href="https://math.spbu.ru/rus/">Links</a> maybe.
        </p>
        <a href="https://github.com/LuninaPolina/SecondaryStructureAnalyzer">
          <font-awesome-icon :icon="['fab', 'github']" />
        </a>
      </div>
    </footer>
    <!-- <button class="button is-warning" v-on:click="getSequence">Получить результат</button> -->
  </div>

</div>
</template>

<script>
export default { // TODO: Sanitizing, beautfying
  name: 'Example',
  el: '#app-5',
  data() {
    return {
      message: 'RNA secondary structure prediction',
      img1: '',
      img2: '',
      show_images: false,
      // ip: "142.93.128.77",
      ip: "localhost",
      port: 8000,
      seq: '',
      id: 0,
      result: 'Result will be shown here',
      raw_result: 'Unaligned result will be shown here',
      isLoading: false,
      error: false,
      sens: 0.3,
      num_matches: 3,
      width: null,
      num_symbols: null
    }
  },
  computed: {
    address: function() {
      return 'http://' + this.ip + ':' + this.port + '/neuro'
    },
    // result_with_original: function() {
    //   return this.seq + "\n" + this.result
    // }
  },
  mounted() {
    this.getWindowWidth();
  },
  methods: {
    // reverseMessage: function () {   // Testing
    //   this.message = this.message.split('').reverse().join('')
    // },
    getWindowWidth() {
      this.width = this.$refs.prev.clientWidth;
      this.num_symbols = Math.floor(this.width / 11);
    }
  ,
    sendSequence: function() { // Post
      this.seq = this.seq.toUpperCase()
      // this.show_images = false
      var goodCharacters = new Array("A", "C", "G", "U");
      for (const c of this.seq) {
        if (goodCharacters.indexOf(c) == -1) {
          this.error = true;
          return

        }
      }
      this.error = false
      this.isLoading = true
      this.$http
        .post(this.address, {
          sequence: this.seq,
          sens: this.sens,
          num_matches: this.num_matches
        })
        .then(response => {
          this.img1 = response.data.img1;
          this.img2 = response.data.img2;
          this.show_images = true;
          this.id = response.data.id;
          // this.result = this.seq + "\n" + response.data.seq;
          var re = new RegExp('.{1,' + this.num_symbols+ '}', 'g');

          var slices1 = this.seq.match(re);
          // console.log(this.seq.match(re));
          var slices2 = response.data.seq.match(re);
          this.result = '';
          for (var i = 0; i < slices1.length; i++) {
            this.result+=slices1[i] + "\n" + slices2[i]+ "\n";
          }
          slices2 = response.data.raw_dot.match(re);
          this.raw_result = '';
          for (i = 0; i < slices1.length; i++) {
            this.raw_result+=slices1[i] + "\n" + slices2[i]+ "\n";
          }
          // console.log(this.result);
          this.isLoading = false;
          // console.log(response.data);
        })
        .catch(function(error) {
          console.log(error);
        });
    },
    pasteExample: function() {
      this.seq = "GCUUACGGCCAUACCACCUUAGGCGUGCCCGAUCUCGUCUGAUCUCGGAAGCUAAGCAGGGUCGGGCCUGGUUAGUA"
    }
    // getSequence: function() {
    // this.$http
    //   .get(this.address, {params: {id: this.id}})
    //   .then(response => {
    //   this.result = response.data;
    //   console.log(response.data);
    //   })
    //   .catch(function (error) {
    //   console.log(error);
    // });
    // }
  }
  // mounted() { // Testing
  //     this.$http
  //       .get('https://api.coindesk.com/v1/bpi/currentprice.json')
  //       .then(response => (this.message = response.data.time.updated));
  //   }
  //
}
</script>

<style lang="scss">
$color: red;
$box-shadow: 0;
</style>
