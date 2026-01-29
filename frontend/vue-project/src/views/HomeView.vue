<template>
  <div class="home">

    <!-- Titre principal -->
    <h1 class="title"> DAAR Library</h1>

    <!-- Sous-titre -->
    <p class="subtitle">
      Explorez <strong>{{ totalBooks }}</strong> livres indexés.<br />
      Recherchez, analysez et découvrez des œuvres similaires grâce<br>
      à la recherche textuelle, aux RegEx, et aux graphes de similarité.
    </p>

    <!-- Menu principal -->
    <div class="menu">
      <router-link to="/search" class="menu-item">
         Chercher un livre
      </router-link>

      <router-link to="/books" class="menu-item">
         Voir tous les livres
      </router-link>
    </div>

    <!-- Encadré d'information -->
    <div class="info-box">
      <p>
        Cette application utilise des techniques avancées :<br />
        <strong>Index inversé</strong> ・ <strong>Recherche RegEx</strong> ・ 
        <strong>Graphe de Jaccard</strong> ・ <strong>PageRank</strong><br />
        pour offrir une navigation intelligente dans les livres du
        <em>Projet Gutenberg</em>.
      </p>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const totalBooks = ref(0)

onMounted(() => {
  // Récupère le nombre total de livres
  fetch("http://127.0.0.1:5000/api/books")
    .then(res => res.json())
    .then(data => {
      totalBooks.value = data.length
    })
})
</script>

<style scoped>
.home {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  text-align: center;
  padding: 2rem;
  color: white;
}

.title {
  font-size: 3.2rem;
  font-weight: 800;
  margin-bottom: 1rem;
  color: #42b983;
}

.subtitle {
  font-size: 1.3rem;
  max-width: 600px;
  margin-bottom: 3rem;
  line-height: 1.7em;
  opacity: 0.85;
}

.menu {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
  width: 100%;
  max-width: 300px;
  margin-bottom: 2rem;
}

.menu-item {
  background: #1f2a34;
  padding: 1rem;
  border-radius: 12px;
  text-decoration: none;
  color: #42b983;
  font-size: 1.2rem;
  font-weight: bold;
  transition: 0.25s;
  border: 1px solid transparent;
}

.menu-item:hover {
  background: #2c3e50;
  border: 1px solid #42b983;
  color: white;
}

/* Encadré d'info */
.info-box {
  background: #1f2a34;
  padding: 1.2rem;
  max-width: 600px;
  border-radius: 12px;
  color: #ccc;
  font-size: 0.95rem;
  line-height: 1.5em;
  border-left: 4px solid #42b983;
  opacity: 0.95;
}
</style>
