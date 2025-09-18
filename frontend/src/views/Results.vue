<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const votes = ref([]);
const loading = ref(true);
const totalVotes = ref(0)
const percentOui = ref(0);
const percentNon = ref(0);

onMounted(async () => {
  try {
    const res = await axios.get('/api/getVote');
    votes.value = res.data.votes;
    totalVotes.value = res.data.totalVotes || 0;
    percentOui.value = res.data.percentageYes || 0
    percentNon.value = res.data.percentageNo || 0
  } catch (e) {

  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <div class="results">
    <h2>Résultats</h2>
    <div v-if="loading">Chargement...</div>
    <div v-else>
      <ul>
        <li v-for="vote in votes" :key="vote.id">
          <strong>{{ vote.pseudo }}</strong> : {{ vote.vote }}
        </li>
      </ul>
      <div class="stats">
        <p>Total votes : {{ totalVotes }}</p>
        <p>Oui : {{ percentOui }}%</p>
        <p>Non : {{ percentNon }}%</p>
      </div>
    </div>
  </div>
</template>



<style scoped>
.results {
  max-width: 500px;
  margin: 40px auto;
  background: #fff;
  padding: 2em;
  border-radius: 8px;
  box-shadow: 0 2px 8px #ccc;
}
ul {
  list-style: none;
  padding: 0;
}
li {
  margin-bottom: 0.5em;
}
.stats {
  margin-top: 2em;
  background: #e3f2fd;
  padding: 1em;
  border-radius: 6px;
}
</style>
