<script setup>
import { ref, computed, onMounted, watch } from "vue"
import ContentBox from "@/common/ContentBox.vue"
import NewsCard from "@/components/NewsCard.vue"
import StateButton from "@/common/StateButton.vue"
import { fetchNewsList, fetchRecommendedNews, fetchNewsSearch } from "@/api/news"
import { tabs } from "@/assets/data/tabs"

const newsList = ref([])
const sortBy = ref("latest")
const activeTab = ref(tabs[0].id)
const currentPage = ref(1)
const totalPages = ref(1)
const pageSize = 10

const searchQuery = ref("")
const searchedQuery = ref("")
const searchResults = ref([])
const searchError = ref("")
const isSearching = ref(false)

const hasSearchResults = computed(() =>
  Array.isArray(searchResults.value) && searchResults.value.length > 0
)

const paginatedSearchResults = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return searchResults.value.slice(start, start + pageSize)
})

const computedTotalPages = computed(() => {
  if (isSearching.value) {
    return Math.ceil(searchResults.value.length / pageSize)
  }
  return totalPages.value
})

const onSearch = async () => {
  const keyword = searchQuery.value.trim()
  if (!keyword) {
    searchError.value = "Please enter a keyword."
    isSearching.value = false
    searchResults.value = []
    return
  }

  try {
    const res = await fetchNewsSearch(keyword)
    const articles = res.data.data?.articles || []
    searchResults.value = articles
    searchedQuery.value = keyword
    isSearching.value = true
    searchError.value = ""
    currentPage.value = 1
  } catch (e) {
    console.error("검색 실패:", e)
    searchError.value = "Search error occurred."
  }
}

const goToPage = (page) => {
  if (page >= 1 && page <= computedTotalPages.value) {
    currentPage.value = page
    if (!isSearching.value) {
      if (sortBy.value === 'recommend') {
        fetchData()
      } else {
        loadNews()
      }
    }
  }
}

const fetchData = async () => {
  try {
    const selectedTab = tabs.find(tab => tab.id === activeTab.value)
    const category = selectedTab?.value || ""

    if (sortBy.value === 'recommend') {
      const res = await fetchRecommendedNews(category);
      newsList.value = res.articles;
      totalPages.value = res.pagination.total_pages;
    } else {
      const res = await fetchNewsList({
        page: currentPage.value,
        limit: 10,
        sort_by: sortBy.value,
        category,
      });
      newsList.value = res.articles;
      totalPages.value = res.pagination.total_pages;
    }
  } catch (err) {
    console.error("뉴스 불러오기 실패", err);
  }
}

const loadNews = async () => {
  try {
    const selectedTab = tabs.find(tab => tab.id === activeTab.value)
    const category = selectedTab?.value || ""

    const response = await fetchNewsList({
      category,
      page: currentPage.value,
      limit: pageSize,
      sort_by: sortBy.value,
    })

    newsList.value = response.articles || []
    totalPages.value = response.pagination?.total_pages || 1
  } catch (err) {
    console.error("뉴스 불러오기 실패:", err)
    newsList.value = []
    totalPages.value = 1
  }
}

watch(sortBy, () => {
  currentPage.value = 1
  if (sortBy.value === 'recommend') {
    fetchData()
  } else {
    loadNews()
  }
})

watch(activeTab, () => {
  currentPage.value = 1
  if (sortBy.value === 'recommend') {
    fetchData()
  } else {
    loadNews()
  }
})

onMounted(() => {
  if (sortBy.value === 'recommend') {
    fetchData()
  } else {
    loadNews()
  }
})
</script>

<template>
  <div class="news">
    <div>
      <h1 class="news__title">🎯 AI-Powered Personalized News Recommendations</h1>
      <p class="news__description">
        Get the news you truly care about — curated just for you by AI! Discover <strong>NEWSMATE</strong>, your personal news curation service that
        <br />delivers only the articles tailored to your interests. Chat with our AI assistant, and explore your reading
        <br />habits through a smart, easy-to-use dashboard.
      </p>

      <ContentBox class="news__tabs" v-if="!isSearching">
        <StateButton
          v-for="tab in tabs"
          :key="tab.id"
          type="state"
          :is-active="activeTab === tab.id"
          @click="activeTab = tab.id"
        >
          {{ tab.label }}
        </StateButton>
      </ContentBox>
    </div>

    <div class="search-wrapper">
      <div class="search-bar">
        <input
          v-model="searchQuery"
          @keyup.enter="onSearch"
          placeholder="Search news by title..."
          class="search-box"
        />
      </div>
      <button class="search-button" @click="onSearch">Search</button>
    </div>
    <p v-if="searchError" class="error-text">{{ searchError }}</p>

    <ContentBox class="news__box">
      <div class="news__box__title-container" v-if="!isSearching">
        <div class="filters__container">
          <select class="filters" v-model="sortBy">
            <option value="latest">Latest</option>
            <option value="recommend">Recommended</option>
          </select>
        </div>
      </div>

      <template v-if="isSearching">
        <p class="result-text" v-if="hasSearchResults">
          🔎 Results for "{{ searchedQuery }}"
        </p>
        <p class="no-result" v-else>
          ❌ No results found for "{{ searchedQuery }}"
        </p>

        <div class="news__box__cards">
          <NewsCard
            v-for="(item, idx) in paginatedSearchResults"
            :key="item.id || item.url || idx"
            :data="item"
            :style="{ animationDelay: `${idx * 0.05}s` }"
          />
        </div>
      </template>

      <template v-else>
        <div class="news__box__cards">
          <NewsCard
            v-for="(news, idx) in newsList"
            :key="news.id"
            :data="news"
            :style="{ animationDelay: `${idx * 0.05}s` }"
          />
        </div>
      </template>

      <div class="pagination" v-if="computedTotalPages > 1">
        <button @click="goToPage(currentPage - 1)" :disabled="currentPage === 1">Prev</button>
        <button
          v-for="page in computedTotalPages"
          :key="page"
          :class="{ active: currentPage === page }"
          @click="goToPage(page)"
        >
          {{ page }}
        </button>
        <button @click="goToPage(currentPage + 1)" :disabled="currentPage === computedTotalPages">Next</button>
      </div>
    </ContentBox>
  </div>
</template>

<style scoped lang="scss">
.news {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  padding: 60px 20px;

  &__title {
    font-size: 2.2rem;
    font-weight: 800;
    color: var(--color-text);
    margin-bottom: 10px;
    text-align: center;
    border-bottom: 1px solid var(--color-border);
    padding-bottom: 10px;
  }

  &__description {
    font-size: 1rem;
    color: var(--color-text-sub);
    line-height: 1.8;
    text-align: center;
    margin-bottom: 30px;

    &--job {
      color: var(--color-primary);
      margin-bottom: 20px;
    }
  }

  &__tabs {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(115px, 1fr));
    gap: 12px;
    padding: 15px 30px !important;
    max-width: 1200px;
    margin: 0 auto;
  }

  &__box {
    width: 100%;
    max-width: 1200px;
    padding: 40px 30px !important;
    background-color: var(--color-surface);
    border-radius: 12px;
    box-shadow: 0 0 10px rgba(0,0,0,0.02);

    &__title-container {
      position: relative;
      display: flex;
      justify-content: flex-end;
      align-items: center;
    }

    &__cards {
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 24px;
      margin-top: 30px;
    }

    .filters__container {
      position: absolute;
      right: 0;

      select.filters {
        padding: 8px 36px 8px 12px;
        font-size: 0.95rem;
        border: 1px solid var(--color-border);
        border-radius: 8px;
        background-color: var(--color-surface);
        color: var(--color-text);
        font-weight: 500;
        appearance: none;

        background-image: url("data:image/svg+xml;utf8,<svg fill='%236366f1' height='20' viewBox='0 0 24 24' width='20' xmlns='http://www.w3.org/2000/svg'><path d='M7 10l5 5 5-5z'/></svg>");
        background-repeat: no-repeat;
        background-position: right 12px center;
        background-size: 16px;

        transition: border-color 0.2s ease, box-shadow 0.2s ease;

        &:hover {
          border-color: var(--color-primary);
          box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.15);
        }

        &:focus {
          outline: none;
          border-color: var(--color-primary);
          box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.25);
        }
      }
    }
  }
}

.search-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
  width: 100%;
  max-width: 1200px;
  margin: 0px auto;
}

.search-bar {
  flex: 1;
  border-radius: 12px;
  border: 1px solid var(--color-border);
  background-color: var(--color-surface);
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.02); // ✅ news__box 스타일과 일치
  transition: box-shadow 0.2s ease, border-color 0.2s ease;

  display: flex;
  align-items: center;

  &:focus-within {
    border-color: var(--color-primary);
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
  }
}

.search-box {
  flex: 1;
  border: none;
  outline: none;
  padding: 12px 16px;
  font-size: 1rem;
  background: transparent;
  color: var(--color-text);
}

.search-button {
  border: none;
  background-color: var(--color-primary);
  color: white;
  font-weight: bold;
  padding: 12px 20px;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s;

  &:hover {
    background-color: #2c2c6f;
  }
}

.result-text,
.no-result {
  text-align: center;
  font-size: 1rem;
  font-weight: bold;
  margin-top: 20px;
}

.no-result {
  color: #999;
}

.error-text {
  color: red;
  font-size: 0.95rem;
  text-align: center;
  margin-top: -10px;
  margin-bottom: 10px;
}

.pagination {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-top: 30px;

  button {
    padding: 6px 12px;
    border: none;
    border-radius: 6px;
    background-color: var(--color-border);
    color: var(--color-text);
    cursor: pointer;

    &.active {
      background-color: var(--color-primary);
      color: white;
      font-weight: bold;
    }

    &:disabled {
      background-color: #ccc;
      cursor: not-allowed;
    }
  }
}
</style>
