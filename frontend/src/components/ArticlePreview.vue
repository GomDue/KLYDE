<script setup>
import ContentBox from "@/common/ContentBox.vue";
import StateButton from "@/common/StateButton.vue";
import { useDate } from "@/composables/useDate";
import { defineProps, computed } from "vue";
import { RouterLink } from "vue-router";

const props = defineProps({
  news: {
    type: Object,
    required: true,
  },
  to: {
    type: String,
    default: null,
  }
});

const { formatDate } = useDate();
const linkComponent = computed(() => (props.to ? RouterLink : "div"));
const hasInteraction = computed(() => {
  return (
    props.news &&
    "article_interaction" in props.news &&
    !!props.news.article_interaction
  );
});
</script>

<template>
  <component
    :is="linkComponent"
    v-bind="props.to ? { to: props.to } : {}"
    v-if="props.news"
  >
    <ContentBox>
      <div class="top">
        <h1>{{ props.news.title || '제목 없음' }}</h1>
      </div>
      <div class="bottom">
        <div>
          <StateButton type="tag" size="sm">
            {{ props.news.writer || '작성자 없음' }}
          </StateButton>
          {{ formatDate(props.news.write_date) || '날짜 없음' }}
        </div>

        <div v-if="hasInteraction" class="bottom__icons">
          <div>
            ❤️ {{ props.news.article_interaction?.likes ?? 0 }}
          </div>
          <div>
            👀 {{ props.news.article_interaction?.read ?? 0 }}
          </div>
        </div>
      </div>
    </ContentBox>
  </component>
</template>

<style scoped lang="scss">
.top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 5px;

  h1 {
    font-size: 15px;
    text-align: left;
    margin-right: auto;
  }
}

.bottom {
  display: flex;
  align-items: baseline;
  gap: 10px;
  justify-content: space-between;

  &__icons {
    display: flex;
    gap: 10px;
  }
}
</style>
