<template>
  <div v-if="article" class="detail-container">
    <div class="layout-wrapper">
      
      <!-- 왼쪽: 본문 + 댓글 -->
      <div class="left-section">
        <!-- 본문 -->
        <div class="main">
          <h4 class="category">{{ article.category }}</h4>
          <h2 class="title">{{ article.title }}</h2>
          <p class="meta">
            {{ formatDate(article.write_date) }}
            · ❤️ {{ article.article_interaction?.likes ?? 0 }}
            · 👀 {{ article.article_interaction?.read ?? 0 }}
          </p>
          <p class="content">{{ article.content }}</p>

          <button @click="toggleLike" class="like-btn">
            {{ liked ? '❤️ Unlike' : '🤍 Like' }}
          </button>
        </div>

        <!-- 댓글 섹션 -->
        <div class="comments">
        <!-- 댓글 섹션 헤더 추가 -->
          <h3 class="comments-title">Comments</h3>
          <!-- 댓글 입력 -->
          <div class="comment-form">
            <textarea
              v-model="newComment"
              placeholder="Write a comment..."
              rows="3"
              @keydown.enter.exact.prevent
            ></textarea>
            <button @click="submitComment">Submit</button>
          </div>

          <!-- 댓글 목록 -->
          <div class="comment-list" v-if="comments.length > 0">
            <div class="comment" v-for="comment in comments" :key="comment.id">
              <div class="comment-meta">
                <span class="comment-author">{{ comment.author }}</span>
                ·
                <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
              </div>

              <!-- 댓글 내용 -->
               <div v-if="editingId === comment.id">
                <textarea
                  v-model="editingContent"
                  rows="2"
                  class="edit-textarea"
                ></textarea>
                <div class="edit-actions">
                  <button @click="submitEdit(comment.id)">Save</button>
                  <button @click="editingId = null">Cancel</button>
                </div>
              </div>
              <p class="comment-content" v-else>{{ comment.content }}</p>

              <div class="comment-actions" v-if="canEdit(comment.author)">
                <button @click="startEdit(comment)">Edit</button>
                <button @click="deleteComment(comment.id)">Delete</button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 오른쪽: 관련 기사 사이드바 -->
      <div class="right-section" v-if="article.related_articles?.articles">
        <aside class="sidebar">
          <h3>📌 Related News</h3>
          <div>
            <RouterLink
              v-for="related in article.related_articles.articles"
              :key="related.id"
              :to="`/news/${related.id}`"
              class="related-card"
              @click.prevent="handleRelatedClick(related.id)"
            >
              <p class="related-title">{{ related.title }}</p>
              <small class="related-date">{{ formatDate(related.write_date) }}</small>
              <div class="related-icons">
                ❤️ {{ related.article_interaction?.likes ?? 0 }}
                👀 {{ related.article_interaction?.read ?? 0 }}
              </div>
            </RouterLink>
          </div>
        </aside>
      </div>

    </div>
  </div>

  <div v-else>
    <p>Loading...</p>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { fetchNewsDetail, likeArticle, unlikeArticle, incrementRead } from '@/api/news'
import { fetchComments, postComment } from '@/api/comments'
import { updateComment, deleteComment as apiDeleteComment } from '@/api/comments'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const userEmail = computed(() => userStore.email)

const route = useRoute()
const router = useRouter()
const article = ref(null)
const liked = ref(false)

const newComment = ref('')
const comments = ref([])

const formatDate = (iso) => {
  const d = new Date(iso)
  return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')} ${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`
}

const loadArticle = async () => {
  try {
    const data = await fetchNewsDetail(route.params.id)
    article.value = data
    liked.value = data.is_liked || false
  } catch (e) {
    console.error('뉴스 상세 데이터를 불러오지 못했습니다:', e)
  }
}

onMounted(async () => {
  try {
    await incrementRead(route.params.id)
    await loadArticle()
    if (article.value?.id) {
      comments.value = await fetchComments(article.value.id)
    }
  } catch (e) {
    console.error('초기 로딩 실패:', e)
  }
})

watch(() => route.fullPath, async () => {
  try {
    await incrementRead(route.params.id)
    await loadArticle()
    if (article.value?.id) {
      comments.value = await fetchComments(article.value.id)
    }
  } catch (e) {
    console.error("경로 변경 후 로딩 실패:", e)
  }
})

const handleRelatedClick = async (id) => {
  try {
    await incrementRead(id)
    await router.push(`/news/${id}`)
  } catch (e) {
    console.error("관련 기사 클릭 시 오류", e)
  }
}

const toggleLike = async () => {
  try {
    if (liked.value) {
      await unlikeArticle(article.value.id)
      article.value.article_interaction.likes--
    } else {
      await likeArticle(article.value.id)
      article.value.article_interaction.likes++
    }
    liked.value = !liked.value
  } catch (e) {
    console.error("좋아요 토글 실패:", e)
  }
}

const submitComment = async () => {
  if (!newComment.value.trim()) return

  try {
    const newItem = await postComment(article.value.id, newComment.value)
    comments.value.unshift(newItem)
    newComment.value = ''
  } catch (e) {
    console.error('댓글 작성 실패:', e)
  }
}

const editingId = ref(null)
const editingContent = ref('')

const startEdit = (comment) => {
  editingId.value = comment.id
  editingContent.value = comment.content
}

const canEdit = (author) => {
  return author?.trim() === userEmail.value?.trim()
}

const submitEdit = async (commentId) => {
  try {
    await updateComment(commentId, editingContent.value, article.value.id);
    comments.value = await fetchComments(article.value.id);
    editingId.value = null;
  } catch (e) {
    console.error('댓글 수정 실패:', e);
  }
}


const deleteComment = async (commentId) => {
  const confirmed = confirm("Do you really want to delete this comment?");
  if (!confirmed) return;

  try {
    await apiDeleteComment(commentId);
    comments.value = comments.value.filter(c => c.id !== commentId);
  } catch (e) {
    console.error("댓글 삭제 실패:", e);
  }
};

</script>

<style scoped lang="scss">
/* 전체 페이지 여백 및 크기 지정 */
.detail-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
  min-height: 100vh;
}

/* 좌우 영역 배치 */
.layout-wrapper {
  display: flex;
  gap: 30px;
  align-items: flex-start;
  width: 100%;
  align-items: stretch;
}

/* 왼쪽 섹션 (본문 + 댓글) */
.left-section {
  flex: 3;
  display: flex;
  flex-direction: column;
  gap: 30px;
  min-height: 100vh;
}

/* 오른쪽 섹션 (사이드바) */
.right-section {
  flex: 1;
}

/* 본문 영역 */
.main {
  background: white;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.03);
  max-height: 55vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.content {
  overflow-y: auto;
  max-height: 100%;
  margin-top: 10px;
  line-height: 1.6;
  white-space: pre-wrap;
}

/* 사이드바 */
.sidebar {
  position: sticky;
  top: 80px;
  align-self: flex-start;
  background: #f9f9f9;
  padding: 20px;
  width: 300px;
  border-radius: 12px;
}

/* 사이드바 내부 카드들 */
.sidebar h3 {
  margin-bottom: 10px;
  font-size: 20px;
}

.related-card {
  display: block;
  text-decoration: none;
  color: inherit;
  background-color: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: 20px 24px;
  margin-bottom: 16px;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.05);
  transition: box-shadow 0.3s ease, transform 0.2s ease;

  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 20px rgba(99, 102, 241, 0.15);
    border-color: var(--color-primary);
  }
}

.related-title {
  font-weight: 600;
  font-size: 0.95rem;
  margin-bottom: 5px;
}

.related-date {
  font-size: 0.8rem;
  color: #999;
}

.related-icons {
  margin-top: 5px;
  font-size: 0.8rem;
  color: #555;
  display: flex;
  gap: 8px;
}

/* 기타 텍스트 스타일 */
.category {
  font-size: 0.9rem;
  font-weight: bold;
  color: #666;
}

.title {
  font-size: 1.6rem;
  font-weight: 700;
  margin: 10px 0;
}

.meta {
  font-size: 0.85rem;
  color: #999;
  margin-bottom: 20px;
}

/* 좋아요 버튼 */
.like-btn {
  margin-top: 20px;
  padding: 10px 20px;
  font-weight: bold;
  border: none;
  border-radius: 6px;
  background: var(--color-primary);
  color: white;
  cursor: pointer;
  align-self: flex-start;
}

.like-btn:hover {
  background-color: #2c2c6f;
}

.comments {
  background: white;
  border: 1px solid #ddd;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.comments-title {
  font-weight: bold;
  font-size: medium;
  padding-bottom: 15px;
}

/* 입력 영역 */
.comment-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.comment-form textarea {
  resize: none;
  padding: 14px;
  font-size: 1rem;
  line-height: 1.5;
  border: 1px solid #ccc;
  border-radius: 8px;
  background: #f9f9f9;
  transition: border 0.2s ease;
  font-family: inherit;
}

.comment-form textarea:focus {
  outline: none;
  border-color: #333;
  background: #fff;
}

.comment-form button {
  align-self: flex-end;
  padding: 8px 20px;
  background: var(--color-primary);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.2s ease;
  height: 36px
}

.comment-form button:hover {
  background-color: #2c2c6f;
}

/* 댓글 목록 */
.comment-list {
  margin-top: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.comment {
  background: #fafafa;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  padding: 16px 20px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.03);
}

.comment-meta {
  font-size: 0.85rem;
  color: #777;
  margin-bottom: 6px;
}

.comment-content {
  font-size: 1rem;
  line-height: 1.5;
}

.comment-actions {
  display: flex;
  gap: 10px;
  margin-top: 8px;
  justify-content: flex-end;
}

.comment-actions button {
  padding: 8px 20px;
  font-size: 0.9rem;
  font-weight: bold;
  font-size: 14px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

/* Edit 버튼: 회색 */
.comment-actions button:first-child {
  background-color: #e0e0e0;
  color: #333;
}

.comment-actions button:first-child:hover {
  background-color: #d0d0d0;
}

/* Delete 버튼: 빨간색 */
.comment-actions button:last-child {
  background-color: #e03a3e;  /* 더 어둡고 덜 튀는 빨강 */
  color: white;
}

.comment-actions button:last-child:hover {
  background-color: #c53033;
}

.edit-textarea {
  width: 100%;
  padding: 12px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  margin-bottom: 10px;
  background: #fff;
  font-family: inherit;
}

.edit-actions {
  display: flex;
  gap: 10px;
}

.edit-actions button {
  padding: 8px 20px;
  border-radius: 6px;
  border: none;
  background: var(--color-primary);
  color: white;
  font-weight: bold;
  font-size: 14px;
  cursor: pointer;
}

.edit-actions button:hover {
  background-color: #2c2c6f;
}
</style>