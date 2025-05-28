import axios from './axios'

export async function fetchNewsList({ category = '', page = 1, limit = 10, sort_by = 'latest' }) {
  const res = await axios.get('/news-list/', {
    params: { category, page, limit, sort_by }
  })
  return res.data.data
}

export async function fetchNewsDetail(id) {
  const res = await axios.get(`/news/${id}/`)
  return res.data.data
}

export async function likeArticle(article_id) {
  const res = await axios.post('/news/like/', { article_id })
  return res.data.message
}

export async function unlikeArticle(article_id) {
  const res = await axios.delete('/news/like/', {
    data: { article_id }
  })
  return res.data.message
}

export async function incrementRead(article_id) {
  const res = await axios.post(`/news/${article_id}/read/`)
  return res.data
}

export async function fetchLikedArticles() {
  const response = await axios.get("/news/liked/", {
    headers: {
      Authorization: `Bearer ${localStorage.getItem("access")}`,
    },
  });  
  return response.data.data;
}

export async function fetchRecommendedNews(category = "") {
  const res = await axios.get("/news/recommend/", {
    headers: {
      Authorization: `Bearer ${localStorage.getItem("access")}`,
    },
    params: {
      category,
    },
  });
  return res.data.data;
}

export async function fetchNewsSearch(query) {
  return await axios.get("/news/search", {
    params: { q: query }
  });
}
