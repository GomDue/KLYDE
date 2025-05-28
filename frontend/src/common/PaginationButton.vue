<script setup>
import { computed } from "vue";

const emit = defineEmits(["update:modelValue"]);
const props = defineProps({
  modelValue: Number,
  totalPages: Number
});

const pageModel = computed({
  get: () => props.modelValue,
  set: (val) => {
    if (val >= 1 && val <= props.totalPages) {
      emit("update:modelValue", val);
    }
  }
});
</script>

<template>
  <div class="pagination" v-if="totalPages > 1">
    <button @click="pageModel--" :disabled="pageModel === 1">이전</button>
    <span>{{ pageModel }} / {{ totalPages }}</span>
    <button @click="pageModel++" :disabled="pageModel === totalPages">다음</button>
  </div>
</template>

<style scoped>
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
  margin-top: 20px;
}

.pagination button {
  font-size: 13px;
  padding: 4px 8px;
  border: none;
  background-color: #0c3057;
  color: white;
  border-radius: 100px;
}

.pagination button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
</style>
