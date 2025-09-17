import { createRouter, createWebHistory } from 'vue-router';
import Identification from '../views/Identification.vue';
import Vote from '../views/Vote.vue';
import Results from '../views/Results.vue';

const routes = [
  { path: '/', name: 'Identification', component: Identification },
  { path: '/vote', name: 'Vote', component: Vote },
  { path: '/results', name: 'Results', component: Results }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
