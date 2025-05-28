// src/api/comments.js
import axios from './axios'  // 공통 axios 인스턴스

// 댓글 목록 불러오기 (article_id 기준)
export async function fetchComments(article_id) {
  const res = await axios.get('/news/comments/', {
    params: { article_id }
  })
  return res.data  // → [{ id, author, content, created_at }, ...]
}

// 댓글 작성
export async function postComment(article_id, content) {
  const res = await axios.post('/news/comments/', {
    article: article_id,
    content: content
  })
  return res.data  // → 작성된 댓글 객체 반환
}

// 댓글 수정
export async function updateComment(id, content, articleId) {
  return await axios.put(`/news/comments/${id}/`, {
    content,
    article: articleId
  });
}


// 댓글 삭제
export async function deleteComment(commentId) {
  await axios.delete(`/news/comments/${commentId}/`)
}