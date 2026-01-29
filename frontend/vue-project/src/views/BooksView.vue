<template>
  <div class="books">

    <h1 class="title"> Tous les livres ({{ books.length }})</h1>

    <!-- BARRE DE CONTROLES -->
    <div class="controls">
      <!-- Filtre rapide -->
      <input
        type="text"
        v-model="filterText"
        placeholder="Filtrer par ID..."
        class="filter-input"
      />

      <!-- Tri -->
      <select v-model="sortBy" class="sort-select">
        <option value="id">Trier par ID</option>
        <option value="word_count">Trier par nombre de mots</option>
        <option value="pagerank">Trier par PageRank</option>
      </select>

      <!-- Ordre -->
      <button class="sort-btn" @click="toggleOrder">
        {{ sortOrder === 'asc' ? '⬆️' : '⬇️' }}
      </button>
    </div>

    <!-- Charger -->
    <p v-if="loading" class="loading">Chargement des livres...</p>

    <!-- LISTE -->
    <div class="list" v-if="!loading">
      <router-link
        v-for="book in visibleBooks"
        :key="book.id"
        :to="`/books/${book.id}`"
        class="book-link"
      >
        <div class="book-card">
          <p class="book-id">📘 Livre {{ book.id }}</p>
          <p class="count">🔠 {{ book.word_count }} mots</p>
          <p class="pr">⭐ PR: {{ book.pagerank.toFixed(5) }}</p>
        </div>
      </router-link>
    </div>

    <!-- Voir plus -->
    <button
      class="load-more"
      v-if="visibleCount < filteredAndSortedBooks.length"
      @click="showMore"
    >
      Voir plus ⬇️
    </button>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const books = ref([])
const loading = ref(true)

const visibleCount = ref(30) // afficher 30 livres au début

const filterText = ref("") // filtre par ID
const sortBy = ref("id") // critère de tri
const sortOrder = ref("asc") // asc | desc


// Charger les livres
onMounted(() => {
  fetch("http://127.0.0.1:5000/api/books")
    .then(res => res.json())
    .then(data => {
      books.value = data
      loading.value = false
    })
})

// ----- Computed -----

// 1) filtrer
const filteredBooks = computed(() => {
  if (!filterText.value) return books.value
  return books.value.filter(b => b.id.startsWith(filterText.value))
})

// 2) trier
const filteredAndSortedBooks = computed(() => {
  const sorted = [...filteredBooks.value].sort((a, b) => {
    let valA = a[sortBy.value]
    let valB = b[sortBy.value]

    // Tri numérique pour PR et ID
    if (sortBy.value === "id") {
      valA = parseInt(valA)
      valB = parseInt(valB)
    }

    if (sortOrder.value === "asc") return valA - valB
    return valB - valA
  })

  return sorted
})

// 3) Pagination
const visibleBooks = computed(() =>
  filteredAndSortedBooks.value.slice(0, visibleCount.value)
)

// ----- Méthodes -----

function showMore() {
  visibleCount.value += 30
}

function toggleOrder() {
  sortOrder.value = sortOrder.value === "asc" ? "desc" : "asc"
}
</script>

<style scoped>
.books {
  padding: 2rem;
  max-width: 1100px;
  margin: auto;
}

.title {
  font-size: 2rem;
  margin-bottom: 1.5rem;
  font-weight: bold;
  text-align: center;
}

/* Barre de tri */
.controls {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  justify-content: center;
}

.filter-input {
  padding: 0.5rem 0.8rem;
  border-radius: 8px;
  border: none;
}

.sort-select {
  padding: 0.5rem;
  border-radius: 8px;
  border: none;
}

.sort-btn {
  padding: 0.5rem 1rem;
  border-radius: 8px;
  background: #1f2a34;
  color: #42b983;
  border: none;
  cursor: pointer;
}

.sort-btn:hover {
  background: #2c3e50;
}

.loading {
  color: #42b983;
  text-align: center;
  margin-top: 2rem;
}

/* Listes */
.list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(210px, 1fr));
  gap: 1rem;
}

.book-link {
  text-decoration: none;
  color: inherit;
}

.book-card {
  background: #1f2a34;
  color: #42b983;
  padding: 1rem;
  border-radius: 10px;
  transition: 0.15s;
  text-align: center;
}

.book-card:hover {
  background: #2c3e50;
  color: white;
}

.book-id {
  font-weight: bold;
}

.count,
.pr {
  font-size: 0.9rem;
  color: #ccc;
}

/* Bouton voir plus */
.load-more {
  margin: 2rem auto;
  display: block;
  background-color: #2c3e50;
  color: white;
  padding: 0.7rem 1.3rem;
  border-radius: 8px;
  border: none;
  cursor: pointer;
}

.load-more:hover {
  background-color: #3b5570;
}
</style>
