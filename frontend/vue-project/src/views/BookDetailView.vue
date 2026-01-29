<template>
  <div class="book-detail">

    <!-- Titre -->
    <h1 class="title"> {{ book.title }}</h1>

    <!-- Bouton retour -->
    <button class="back-btn" @click="goBack">
      ⬅️ Retour
    </button>

    <!-- Carte du livre -->
    <div class="card" v-if="!loadingBook">

      <p><strong>ID :</strong> {{ book.id }}</p>

      <p><strong>Nombre total de mots :</strong>  
        {{ book.word_count.toLocaleString() }}
      </p>

      <p><strong>⭐ PageRank :</strong>  
        {{ book.pagerank.toFixed(6) }}
      </p>

      <h3> Extrait</h3>
      <p class="excerpt">{{ book.excerpt }}</p>

      <h3>Mots les plus fréquents</h3>
      <ul class="top-words">
        <li v-for="(item, index) in book.top_words" :key="index">
          <strong>{{ item[0] }}</strong> : {{ item[1] }}
        </li>
      </ul>
    </div>

    <!-- Loader -->
    <p v-else class="loading">Chargement du livre...</p>

    <!-- Suggestions -->
    <div class="suggestions">
      <h2> Livres similaires</h2>

      <p v-if="loadingSuggestions" class="loading">
        Recherche de suggestions...
      </p>

      <div v-else-if="suggestions.length === 0">
        <p class="no-suggestions">
          Aucune suggestion disponible pour ce livre.
        </p>
      </div>

      <div v-else class="suggestions-list">
        <router-link
          v-for="s in suggestions"
          :key="s.id"
          :to="`/books/${s.id}`"
          class="suggestion-card"
        >
          <p class="suggestion-id">📘 Livre {{ s.id }}</p>
          <p class="suggestion-info">🔗 Jaccard : {{ s.score.toFixed(3) }}</p>
          <p class="suggestion-info">⭐ PageRank : {{ s.pagerank.toFixed(5) }}</p>
        </router-link>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const bookId = route.params.id

const book = ref({
  id: '',
  title: '',
  excerpt: '',
  word_count: 0,
  top_words: [],
  pagerank: 0
})

const suggestions = ref([])
const loadingBook = ref(true)
const loadingSuggestions = ref(true)

//  Retour conservant les résultats de recherche
function goBack() {
  if (router.options.history.state.back) {
    router.back()
  } else {
    router.push("/search")
  }
}

function loadBook(id) {
  loadingBook.value = true
  loadingSuggestions.value = true

  fetch(`http://127.0.0.1:5000/api/book/${id}`)
    .then(res => res.json())
    .then(data => {
      book.value = data
      loadingBook.value = false
    })

  fetch(`http://127.0.0.1:5000/api/suggestions/${id}`)
    .then(res => res.json())
    .then(data => {
      suggestions.value = data
      loadingSuggestions.value = false
    })
}

onMounted(() => {
  loadBook(bookId)
})

watch(
  () => route.params.id,
  (newId) => loadBook(newId)
)
</script>

<style scoped>
.book-detail {
  padding: 2rem;
  max-width: 850px;
  margin: auto;
}

.title {
  text-align: center;
  font-size: 2.6rem;
  margin-bottom: 1rem;
}

.back-btn {
  background: #1f2a34;
  border: none;
  padding: 0.6rem 1.2rem;
  color: #42b983;
  border-radius: 8px;
  cursor: pointer;
  margin-bottom: 1.5rem;
}

.back-btn:hover {
  background: #2c3e50;
}

.card {
  background: #1f2a34;
  padding: 2rem;
  border-radius: 12px;
  color: #42b983;
  margin-bottom: 2rem;
}

.excerpt {
  margin-top: 0.5rem;
  padding: 1rem;
  background: #2c3e50;
  border-left: 4px solid #42b983;
  border-radius: 8px;
  color: white;
}

.top-words {
  list-style: none;
  padding: 0;
  margin-top: 1rem;
}

.top-words li {
  padding: 0.3rem 0;
  color: white;
}

.external-link {
  display: inline-block;
  margin-top: 1.2rem;
  text-decoration: none;
  padding: 0.6rem 1rem;
  border-radius: 8px;
  background: #42b983;
  color: black;
  font-weight: bold;
}

.external-link:hover {
  background: #2ea972;
  color: white;
}

.suggestions {
  margin-top: 3rem;
}

.suggestions-list {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  justify-content: center;
}

.suggestion-card {
  background: #1f2a34;
  padding: 1rem 1.5rem;
  border-radius: 10px;
  text-decoration: none;
  color: #42b983;
  min-width: 160px;
  transition: 0.2s;
}

.suggestion-card:hover {
  background: #2c3e50;
  color: white;
}

.suggestion-info {
  color: #ccc;
  margin-top: 0.2rem;
}

.loading {
  color: #42b983;
  text-align: center;
}

.no-suggestions {
  text-align: center;
  color: #ccc;
  font-style: italic;
}
</style>
