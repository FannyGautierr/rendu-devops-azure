<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const votes = ref([]);
const loading = ref(true);
const percentOui = ref(0);
const percentNon = ref(0);

onMounted(async () => {
  try {
    const res = await axios.get('/api/votes');
    votes.value = res.data;
    const oui = votes.value.filter(v => v.choix === 'Oui').length;
    const non = votes.value.filter(v => v.choix === 'Non').length;
    const total = votes.value.length;
    percentOui.value = total ? Math.round((oui / total) * 100) : 0;
    percentNon.value = total ? Math.round((non / total) * 100) : 0;
  } catch (e) {
    alert('Erreur lors du chargement des résultats');
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
          <strong>{{ vote.pseudo }}</strong> : {{ vote.choix }}
        </li>
      </ul>
      <div class="stats">
        <p>Total votes : {{ votes.length }}</p>
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
