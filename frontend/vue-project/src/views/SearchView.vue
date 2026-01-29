<template>
  <div class="search">

    <h1 class="title">Recherche de livres</h1>

    <!-- Barre de recherche -->
    <div class="search-box">
      <input 
        v-model="query" 
        type="text" 
        placeholder="Entrez un mot ou une RegEx..."
        @keyup.enter="searchBooks"
      />

      <button @click="searchBooks">
        Mot simple
      </button>

      <button class="regex-btn" @click="openRegexHelpAndSearch">
        RegEx
      </button>
    </div>

    <!-- AIDE REGEX (bien placée ici, PAS dans la search-box) -->
    <div class="regex-help" v-if="showRegexHelp">
      <h3>Aide RegEx</h3>

      <ul>
        <li><code>^mot</code> → commence par "mot"</li>
        <li><code>mot$</code> → finit par "mot"</li>
        <li><code>a|b</code> → a ou b</li>
        <li><code>.</code> → un caractère</li>
        <li><code>.*</code> → n’importe quoi</li>
        <li><code>[abc]</code> → un parmi a, b, c</li>
        <li><code>[a-z]</code> → lettre entre a et z</li>
        <li><code>\d</code> → chiffre</li>
      </ul>

      <button class="close-help" @click="showRegexHelp = false">
        Fermer l’aide
      </button>
    </div>

    <!-- Messages -->
    <p v-if="simpleError" class="error">{{ simpleError }}</p>
    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="loading" class="loading">Recherche en cours...</p>

    <!-- Résultats -->
    <div class="results" v-if="results.length > 0 && !loading">
      <h2>Résultats :</h2>

      <ul>
        <li v-for="book in results.slice(0, visibleCount)" :key="book.id">
          <router-link :to="`/books/${book.id}`" class="result-link">
            <div class="result-card">
              <p class="result-title">📘 Livre {{ book.id }}</p>

              <p class="info">
                🔠 {{ book.occurrences }} occurrences
              </p>

              <p class="info" v-if="book.word">
                🔍 Mot trouvé : "{{ book.word }}"
              </p>

              <p class="info">
                ⭐ PageRank : {{ book.pagerank.toFixed(5) }}
              </p>
            </div>
          </router-link>
        </li>

        <button 
          v-if="visibleCount < results.length"
          class="load-more"
          @click="showMore"
        >
          Voir plus ⬇️
        </button>
      </ul>
    </div>

    <!-- Suggestions -->
    <div
      class="suggestions"
      v-if="suggestions.length > 0 && !loading"
    >
      <h2>Suggestions basées sur votre recherche</h2>

      <ul>
        <li v-for="s in suggestions" :key="s.id">
          <router-link :to="`/books/${s.id}`" class="result-link">
            <div class="result-card suggestion-card">

              <p class="result-title">📗 Livre {{ s.id }}</p>

              <p class="info">
                🔗 Jaccard : {{ s.jaccard.toFixed(3) }}
              </p>

              <p class="info">
                ⭐ PageRank : {{ s.pagerank.toFixed(5) }}
              </p>

            </div>
          </router-link>
        </li>
      </ul>
    </div>

    <!-- Aucun résultat -->
    <div v-else-if="searched && !loading && !error">
      <p class="no-results">Aucun résultat.</p>
    </div>

  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const query = ref(route.query.query || "")
const type = ref(route.query.type || "simple")
const results = ref([])
const suggestions = ref([])
const searched = ref(false)
const error = ref("")
const simpleError = ref("")
const loading = ref(false)
const visibleCount = ref(10)
const showRegexHelp = ref(false)

function looksLikeRegex(text) {
  return ["|", "*", "?", "[", "("].some(c => text.includes(c))
}

function showMore() {
  visibleCount.value += 10
}

// 🔍 Recherche simple
function searchBooks() {
  error.value = ""
  simpleError.value = ""

  if (looksLikeRegex(query.value)) {
    simpleError.value =
      "Cela ressemble à une RegEx. Utilisez plutôt « RegEx »."
    return
  }

  router.push({ path: "/search", query: { query: query.value, type: "simple" } })

  type.value = "simple"
  searched.value = true
  loading.value = true
  results.value = []
  suggestions.value = []

  fetch(`http://127.0.0.1:5000/api/search?query=${query.value}`)
    .then(res => res.json())
    .then(data => {
      loading.value = false
      results.value = data.results || []
      suggestions.value = data.suggestions || []
    })
}


function searchRegex() {
  error.value = ""
  simpleError.value = ""

  router.push({ path: "/search", query: { query: query.value, type: "regex" } })

  showRegexHelp.value = true   // ouvrir l’aide automatiquement

  type.value = "regex"
  searched.value = true
  loading.value = true
  results.value = []
  suggestions.value = []

  fetch(`http://127.0.0.1:5000/api/search-regex?pattern=${query.value}`)
    .then(res => res.json())
    .then(data => {
      loading.value = false

      if (data.error) {
        error.value = data.error
        return
      }

      results.value = data
    })
}

function openRegexHelpAndSearch() {
  showRegexHelp.value = true
  searchRegex()
}

// afficher automatiquement l’aide si l’utilisateur tape une RegEx
watch(query, (val) => {
  if (looksLikeRegex(val)) {
    showRegexHelp.value = true
  }
})

// Restauration si retour / rafraichissement
if (query.value) {
  searched.value = true
  loading.value = true

  if (type.value === "simple") {
    fetch(`http://127.0.0.1:5000/api/search?query=${query.value}`)
      .then(res => res.json())
      .then(data => {
        loading.value = false
        results.value = data.results || []
        suggestions.value = data.suggestions || []
      })
  } else {
    fetch(`http://127.0.0.1:5000/api/search-regex?pattern=${query.value}`)
      .then(res => res.json())
      .then(data => {
        loading.value = false

        showRegexHelp.value = true  // réafficher l’aide automatiquement

        if (data.error) error.value = data.error

        results.value = data
      })
  }
}
</script>

<style scoped>
.search {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 3rem;
  max-width: 1100px;
  margin: 0 auto;
}

.title {
  font-size: 2.2rem;
  font-weight: bold;
  margin-bottom: 2rem;
}

.search-box {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

input {
  padding: 0.8rem;
  width: 260px;
  border-radius: 6px;
  border: none;
  font-size: 1rem;
}

button {
  background-color: #42b983;
  color: black;
  padding: 0.8rem 1.5rem;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font-weight: bold;
}

button:hover {
  background-color: #2ea972;
}

.regex-btn {
  background-color: #8e44ad;
  color: white;
}

.regex-btn:hover {
  background-color: #732d91;
}

.regex-help {
  background: #1f2a34;
  padding: 1rem 1.5rem;
  border-radius: 12px;
  color: #42b983;
  margin-top: 1rem;
  max-width: 600px;
}

.regex-help code {
  background: #2c3e50;
  padding: 2px 5px;
  border-radius: 4px;
  color: #4ddfaf;
}

.close-help {
  margin-top: 1rem;
  background: #2c3e50;
  padding: 0.6rem 1rem;
  border: none;
  border-radius: 8px;
  color: white;
  cursor: pointer;
}

.loading {
  color: #42b983;
  margin-top: 1rem;
  font-style: italic;
}

.results,
.suggestions {
  margin-top: 2rem;
  width: 100%;
}

.results ul,
.suggestions ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
}

.results li,
.suggestions li {
  flex: 1 1 calc(50% - 1.5rem);
}

@media (max-width: 800px) {
  .results li,
  .suggestions li {
    flex: 1 1 100%;
  }
}

.result-card {
  background: #1f2a34;
  padding: 1rem;
  border-radius: 10px;
  transition: 0.2s;
}

.result-card:hover {
  background: #2c3e50;
  color: white;
}

.suggestion-card {
  border: 1px dashed #42b983;
}

.info {
  color: #ccc;
  font-size: 0.9rem;
}

.no-results {
  color: #ccc;
  margin-top: 2rem;
}

.load-more {
  margin: 1.5rem auto;
  display: block;
  background-color: #2c3e50;
  color: white;
  padding: 0.7rem 1.4rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}
</style>
