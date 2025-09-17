<template>
  <nav class="nav">
    <router-link to="/">Identification</router-link>
    <router-link to="/vote">Vote</router-link>
    <router-link to="/results">Résultats</router-link>
  </nav>
</template>

<script setup>
// ...rien à ajouter
</script>

<style scoped>
.nav {
  display: flex;
  gap: 2em;
  justify-content: center;
  margin: 2em 0;
}
.router-link-active {
  font-weight: bold;
  color: #1976d2;
}
</style>
