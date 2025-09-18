<script setup>
import { ref } from 'vue';
import axios from 'axios';

const voted = ref(false);

const vote = async (vote) => {
  const userId = localStorage.getItem('userId');
  if (!userId) {
    alert('Veuillez vous identifier.');
    return;
  }
  try {
    await axios.post('/api/postVote', { userId, vote });
    voted.value = true;
  } catch (e) {
    alert('Erreur lors du vote');
  }
};
</script>

<template>
  <div class="vote">
    <h2>Vote</h2>
    <p><strong>Est-ce que François Bayrou nous manque ?</strong></p>
    <button @click="vote('Oui')" :disabled="voted">Oui</button>
    <button @click="vote('Non')" :disabled="voted">Non</button>
    <div v-if="voted">
      <p>Merci pour votre vote !</p>
      <router-link to="/results">Voir les résultats</router-link>
    </div>
  </div>
</template>

<style scoped>
.vote {
  max-width: 400px;
  margin: 40px auto;
  background: #fff;
  padding: 2em;
  border-radius: 8px;
  box-shadow: 0 2px 8px #ccc;
  text-align: center;
}
button {
  margin: 1em;
  padding: 0.7em 2em;
  background: #43a047;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-weight: bold;
  font-size: 1.1em;
}
</style>
