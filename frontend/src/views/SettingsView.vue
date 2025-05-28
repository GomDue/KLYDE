<template>
  <div class="settings-wrapper">
    <div class="settings">
      <h1 class="title">⚙️ Settings</h1>
      <p class="subtitle">
        Manage your preferences — update your password or delete your account.
        <br />Enhance your experience with personalized settings.
      </p>

      <!-- 🔐 Change Password -->
      <div class="settings__section">
        <h2 class="section-title">🔐 Change Password</h2>
        <form class="form">
          <div class="form-group">
            <input type="password" v-model="currentPassword" placeholder="Current Password" />
          </div>
          <div class="form-group">
            <input type="password" v-model="newPassword" placeholder="New Password" />
          </div>
          <button type="button" class="submit-btn" @click="handleChangePassword">Update</button>
        </form>
      </div>

      <!-- 📧 Email Preferences -->
      <div class="settings__section">
        <h2 class="section-title">📧 Email Preferences</h2>
        <p class="email-description">
          We provide a visual report of the top keywords and top categories from the previous day’s articles, delivered directly to your email.
          If you would like to receive this report, please agree to email notifications. Thank you!
        </p>
        <div class="checkbox-center">
          <input type="checkbox" v-model="emailConsent" id="emailConsent" />
          <label for="emailConsent">I would like to receive emails about important updates and features.</label>
        </div>
      </div>

      <!-- 🗑️ Delete Account -->
      <div class="settings__section">
        <h2 class="section-title delete-title">🗑️ Delete Account</h2>
        <p class="delete-warning">
          Once you delete your account, there is no going back. Please be certain.
        </p>
        <button class="delete-btn" @click="confirmDelete">Delete My Account</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { changePassword, deleteAccount } from '@/api/user'
import axios from 'axios'

const currentPassword = ref('')
const newPassword = ref('')

const emailConsent = ref(false)
const emailConsentLoaded = ref(false)

onMounted(async () => {
  try {
    const res = await axios.get("/users/user/", {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("access")}`
      }
    });
    console.log("🎯 서버에서 받은 email_consent:", res.data.email_consent);
    emailConsent.value = res.data.email_consent;
    emailConsentLoaded.value = true;
  } catch (err) {
    console.error("❌ 사용자 정보 로딩 실패:", err);
    emailConsentLoaded.value = true;
  }
});

watch(emailConsent, async (newVal) => {
  console.log("📦 PATCH 보낼 값:", newVal, typeof newVal)
  try {
    await axios.patch("/users/email-consent/", {
      email_consent: Boolean(newVal)
    }, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("access")}`
      }
    })
    console.log("✅ email_consent 서버 저장 완료:", newVal)
  } catch (err) {
    console.error("❌ 서버 저장 실패:", err)
  }
});

const handleChangePassword = async () => {
  try {
    const res = await changePassword(currentPassword.value, newPassword.value)
    alert(res.data.message)
    currentPassword.value = ''
    newPassword.value = ''
  } catch (err) {
    alert(err.response?.data?.detail || "Failed to change password.")
  }
}

const confirmDelete = async () => {
  if (confirm("Are you sure you want to delete your account? This action cannot be undone.")) {
    try {
      const res = await deleteAccount()
      alert(res.data.message)
      localStorage.removeItem("access")
      localStorage.removeItem("refresh")
      window.location.href = "/login"
    } catch (err) {
      alert("Failed to delete account.")
    }
  }
}
</script>

<style scoped lang="scss">
.settings-wrapper {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 60px 20px 40px;
}

.settings {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.title {
  font-size: 2.2rem;
  font-weight: 800;
  color: #333;
  margin-bottom: 10px;
  padding-bottom: 10px;
  border-bottom: 1px solid #e2e2e2;
  width: 100%;
  color: var(--color-text);
}

.subtitle {
  font-size: 1rem;
  color: #666;
  margin-bottom: 40px;
  line-height: 1.8;
  color: var(--color-text-sub);
}

.settings__section {
  // 기존 코드 유지
  margin-bottom: 50px;
  width: 100%;
  max-width: 400px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.section-title {
  font-size: 1.5rem;
  margin-bottom: 25px;
  margin-top: 20px;
  color: black;
  font-weight: bold;
  text-align: center;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 15px;

  .form-group {
    display: flex;
    flex-direction: column;

    label {
      margin-bottom: 5px;
      font-weight: 500;
    }

    input {
      font-size: 0.9rem;        
      padding: 10px 12px;     
      height: 42px;
      width: 280px;             
      border: 1px solid #ccc;
      border-radius: 6px;
    }
  }

  .submit-btn {
    align-self: center;
    padding: 10px 20px;
    font-size: 0.95rem;
    font-weight: bold;
    background-color: var(--color-primary);
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    margin-top: 10px;

    &:hover {
      background-color: #2c2c6f;
    }
  }
}

.email-description {
  font-size: 0.95rem;
  color: var(--color-text-sub);
  line-height: 1.6;
  margin-bottom: 15px;
  text-align: center;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}

.checkbox-center {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  margin-top: 12px;

  input[type="checkbox"] {
    width: 20px;
    height: 20px;
    cursor: pointer;
  }

  label {
    font-size: 0.95rem;
    font-weight: bold;
    color: black;
    text-align: center;
    max-width: 300px;
    line-height: 1.5;
    word-wrap: break-word;
  }
}

.delete-title {
  color: black;
  text-align: center;
  margin-top: 60px;
}

.delete-warning {
  color: #b20000;
  font-size: 0.95rem;
  margin-bottom: 20px;
  text-align: center;
}

.delete-btn {
  background-color: #b20000;
  color: white;
  border: none;
  border-radius: 6px;
  padding: 10px 20px;
  font-weight: bold;
  cursor: pointer;
  display: block;
  margin: 0 auto;
  margin-top: 10px;

  &:hover {
    background-color: #8a0000;
  }
}
</style>
