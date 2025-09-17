
<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const isInscription = ref(true);

const pseudo = ref('');
const email = ref('');
const password = ref('');

const emailConnexion = ref('');
const passwordConnexion = ref('');

const router = useRouter();

const submitInscription = async () => {
  try {
    const res = await axios.post('/api/postUser', {
      username: pseudo.value,
      email: email.value,
      password: password.value
    });
    localStorage.setItem('userId', res.data.id);
    router.push('/vote');
  } catch (e) {
    alert("Erreur lors de l'inscription");
  }
};

const submitConnexion = async () => {
  try {
    const res = await axios.post('/api/login', {
      email: emailConnexion.value,
      password: passwordConnexion.value
    });
    localStorage.setItem('userId', res.data.id);
    router.push('/vote');
  } catch (e) {
    alert("Erreur lors de la connexion");
  }
};
</script>

<template>
  <div class="identification">
    <div class="toggle-buttons">
      <button :class="{ active: isInscription }" @click="isInscription = true">Inscription</button>
      <button :class="{ active: !isInscription }" @click="isInscription = false">Connexion</button>
    </div>
    <h2 v-if="isInscription">Inscription</h2>
    <h2 v-else>Connexion</h2>

    <form v-if="isInscription" @submit.prevent="submitInscription">
      <input v-model="pseudo" placeholder="Pseudo" required />
      <input v-model="email" type="email" placeholder="Email" required />
      <input v-model="password" type="password" placeholder="Mot de passe" required />
      <button type="submit">S'inscrire</button>
    </form>

    <form v-else @submit.prevent="submitConnexion">
      <input v-model="emailConnexion" type="email" placeholder="Email" required />
      <input v-model="passwordConnexion" type="password" placeholder="Mot de passe" required />
      <button type="submit">Se connecter</button>
    </form>
  </div>
</template>


<style scoped>
.identification {
  max-width: 400px;
  margin: 40px auto;
  background: #fff;
  padding: 2em;
  border-radius: 8px;
  box-shadow: 0 2px 8px #ccc;
}
.toggle-buttons {
  display: flex;
  justify-content: center;
  margin-bottom: 1em;
}
.toggle-buttons button {
  flex: 1;
  padding: 0.7em;
  border: none;
  border-radius: 4px 4px 0 0;
  background: #eee;
  color: #1976d2;
  font-weight: bold;
  cursor: pointer;
  margin: 0 2px;
}
.toggle-buttons button.active {
  background: #1976d2;
  color: #fff;
}
input {
  display: block;
  margin-bottom: 1em;
  width: 100%;
  padding: 0.5em;
}
button[type="submit"] {
  width: 100%;
  padding: 0.7em;
  background: #1976d2;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-weight: bold;
}
</style>
