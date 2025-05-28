<script setup>
import { computed, useAttrs, defineProps } from "vue";
import { useRouter } from "vue-router";

// props 정의
const props = defineProps({
  type: String,
  size: String,
  isActive: Boolean,
  to: String,
  class: [String, Array, Object]
});

const router = useRouter();
const attrs = useAttrs();

// computed 값들
const type = computed(() => props.type || "button");
const size = computed(() => props.size || "md");
const isActive = computed(() => props.isActive === true); // 명시적 true

const buttonSizeClass = computed(() => size.value);
const buttonTypeClass = computed(() => type.value);

// 클릭 처리
function handleClick() {
  if (props.to) {
    router.push(props.to);
  }
}
</script>

<template>
  <button
    :class="[
      'toggle-button',
      buttonSizeClass,
      buttonTypeClass,
      props.class,
      { active: isActive }
    ]"
    v-bind="attrs"
    @click="handleClick"
  >
    <slot />
  </button>
</template>

<style scoped lang="scss">
.toggle-button {
  white-space: nowrap;
  padding: 10px 20px;
  font-size: 16px;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  background-color: white;
  color: var(--c-text);
  text-align: center;
  cursor: pointer;
  transition: background-color 0.2s ease, color 0.2s ease, border-color 0.2s;

  &.tag {
    background-color: #f5f5f5;
    cursor: default;
    border: none;
    font-weight: 600;
  }

  &.active {
    background-color: var(--color-primary);
    color: white;
    border-color: var(--color-primary);

    &:hover {
      background-color: rgba(99, 102, 241, 0.9);
    }
  }

  &:hover:not(.active) {
    background-color: var(--color-hover);
  }

  &.sm {
    padding: 4px 10px;
    font-size: 12px;
  }

  &.md {
    padding: 8px 12px;
    font-size: 14px;
  }

  &:disabled {
    pointer-events: none;
    opacity: 0.6;
  }
}
</style>
