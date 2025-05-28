<script setup></script>

<template>
  <div class="footer">
    <a href="#">Terms of Service</a>
    <a href="#">Privacy Policy</a>
    <p>© 2025 NEWSMATE. All rights reserved.</p>
  </div>
</template>

<style scoped lang="scss">
.footer {
  margin: 100px 0 50px 0;
  padding: 20px 0;
  background-color: var(--color-primary-bg);
  text-align: center;
  font-size: 0.8rem;
  color: var(--color-text-sub);
  border-top: 1px solid var(--color-border);

  a {
    color: var(--color-text-sub);
    text-decoration: none;
    margin: 0 10px;
    transition: color 0.2s ease;

    &:hover {
      color: var(--color-primary);
    }
  }

  p {
    margin-top: 8px;
    color: var(--color-text-sub);
  }
}
</style>
