<script setup>
import StateButton from "@/common/StateButton.vue";
import { useDate } from "@/composables/useDate";
import { computed, ref, onMounted } from "vue";
import { likeArticle, unlikeArticle, incrementRead } from "@/api/news";
import { useRouter } from "vue-router";

const router = useRouter();

const props = defineProps({
  data: {
    type: Object,
    required: true
  }
});

onMounted(() => {
  console.log("✅ NewsCard 렌더됨:", props.data.title);
  console.log("🆔 ID:", props.data.id);
  console.log("🔗 링크:", props.data.url);
});

const { formatDate } = useDate();
const date = computed(() => {
  try {
    return props.data.write_date ? formatDate(props.data.write_date) : "Unknown";
  } catch {
    return "Unknown";
  }
});

const isLiked = ref(props.data.is_liked ?? false);
const likeCount = ref(props.data.article_interaction?.likes ?? 0);
const readCount = ref(props.data.article_interaction?.read ?? 0);

const toggleLike = async () => {
  const prevLiked = isLiked.value;
  isLiked.value = !prevLiked;
  likeCount.value += prevLiked ? -1 : 1;

  try {
    if (prevLiked) {
      await unlikeArticle(props.data.id);
    } else {
      await likeArticle(props.data.id);
    }
  } catch (err) {
    isLiked.value = prevLiked;
    likeCount.value += prevLiked ? 1 : -1;
    console.error("좋아요 토글 실패", err);
  }
};

const handleClick = async () => {
  try {
    const res = await incrementRead(props.data.id);
    readCount.value = res.read;
  } catch (err) {
    console.error("조회수 증가 실패:", err);
  } finally {
    router.push({ name: "newsDetail", params: { id: props.data.id } });
  }
};
</script>

<template>
  <div class="card">
    <div class="card__header">
      <StateButton type="state" size="sm" disabled>
        {{ props.data.category || "기타" }}
      </StateButton>
      <span class="card__header-item">{{ props.data.writer || "unknown" }}</span>
      <span class="card__header-item">· {{ date }}</span>
    </div>

    <RouterLink
      v-if="props.data.id"
      :to="{ name: 'newsDetail', params: { id: props.data.id } }"
    >
      <h2 class="title">{{ props.data.title || "No Title" }}</h2>
      <p class="description">{{ props.data.content || "No Content" }}</p>
    </RouterLink>
    <div v-else>
      <h2 class="title">{{ props.data.title || "No Title" }}</h2>
      <p class="description">{{ props.data.content || "No Content" }}</p>
    </div>

    <div class="stats">
      <span @click.stop="toggleLike" style="cursor: pointer">
        {{ isLiked ? "❤️" : "🤍" }} {{ likeCount }}
      </span>
      <span>👀 {{ readCount }}</span>
      <a :href="props.data.url || '#'" target="_blank" rel="noopener noreferrer">
        📄 Read on original site
      </a>
    </div>

    <div class="tags">
      <span
        v-for="tag in props.data.keywords"
        :key="`${props.data.id}-${tag}`"
        class="tag-button"
      >
        {{ `# ${tag}` }}
      </span>
    </div>
  </div>
</template>

<style scoped lang="scss">
@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.card {
  background-color: var(--color-surface);
  width: 80%;
  padding: 20px 24px;
  margin-bottom: 16px;
  border-radius: 12px;
  border: 1px solid var(--color-border);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.05);
  transition: box-shadow 0.3s ease, transform 0.2s ease;
  opacity: 0;
  transform: translateY(30px);
  animation: slideInUp 0.6s ease-out forwards;
  animation-delay: 0s;

  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 20px rgba(99, 102, 241, 0.15);
    border-color: var(--color-primary); // 강조색
  }

  &__header {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.9rem;
    color: var(--color-text-sub);

    &-item {
      font-weight: normal;
    }
  }

  .title {
    margin: 12px 0;
    font-size: 22px;
    font-weight: bold;
    color: var(--color-text);
  }

  .description {
    font-size: 1rem;
    width: 90%;
    color: var(--color-text-sub);
    margin: 15px 0;
    display: -webkit-box;
    -webkit-line-clamp: 4;
    line-clamp: 4;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
    line-height: 1.5;
  }

  .stats {
    display: flex;
    gap: 15px;
    font-size: 0.9rem;
    color: var(--color-text-sub);
    margin-bottom: 15px;
    align-items: center;

    span:first-child {
      transition: color 0.2s;
      &:hover {
        color: var(--color-primary);
      }
    }

    a {
      text-decoration: none;
      color: var(--color-primary);
      font-weight: 500;
    }
  }

  .tags {
    display: flex;
    flex-wrap: wrap;
    padding-bottom: 30px;
    border-bottom: 1px solid var(--color-border);

    .tag-button {
      display: inline-block;
      font-size: 12px;
      font-weight: 600;
      background: var(--color-primary-bg);
      color: var(--color-primary);
      padding: 4px 10px;
      border-radius: 6px;
      margin-right: 10px;
      margin-bottom: 10px;
    }
  }
}
</style>

