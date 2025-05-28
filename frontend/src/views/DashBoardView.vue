<script setup>
import { onMounted, ref } from "vue";
import { Bar, Doughnut } from "vue-chartjs";
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from "chart.js";
import ContentBox from "@/common/ContentBox.vue";
import ArticlePreview from "@/components/ArticlePreview.vue";
import { fetchLikedArticles } from "@/api/news";
import { fetchDashboard } from "@/api/dashboard";

ChartJS.register(
  ArcElement,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend
);

const categoryData = ref({
  labels: [],
  datasets: [
    {
      data: [],
      backgroundColor: [],
    },
  ],
});
const categories = ref([]);

const favoriteArticles = ref([]);

const keywordData = ref({
  labels: [],
  datasets: [
    {
      label: "키워드 빈도수",
      data: [],
      backgroundColor: "#C7E4B8",
    },
  ],
});

const readData = ref({
  labels: [],
  datasets: [
    {
      label: "일별 기사 수",
      data: [],
      backgroundColor: "#DBB8E4",
    },
  ],
});

const chartColors = [
  "#6366F1", // primary indigo
  "#EF4444", // red
  "#10B981", // green
  "#F59E0B", // amber
  "#3B82F6", // blue
  "#8B5CF6"  // violet
];

const options = {
  plugins: {
    legend: {
      display: true,
      position: "right",
      labels: {
        padding: 15,
        boxWidth: 20,
        font: {
          size: 14,
        },
      },
    },
    tooltip: {
      callbacks: {
        label: (context) => {
          const label = context.label || "";
          const value = context.raw;
          return `${label}: ${value}개`;
        },
      },
    },
    layout: {
      padding: {
        right: 40,
      },
    },
  },
};

const barOptions = {
  indexAxis: "y",
  scales: {
    x: {
      beginAtZero: true,
    },
  },
  plugins: {
    legend: {
      display: false,
    },
  },
};

const readBarOptions = {
  maintainAspectRatio: false,
  indexAxis: "x",
  scales: {
    x: {
      beginAtZero: true,
    },
  },
  plugins: {
    legend: {
      display: false,
    },
  },
};

onMounted(async () => {
  try {
    // 좋아요 기사 먼저 따로 유지
    const articles = await fetchLikedArticles();
    favoriteArticles.value = articles;

    // 대시보드 나머지 데이터
    const dashboard = await fetchDashboard();

    // 관심 카테고리
    const sorted = Object.entries(dashboard.category_stats || {}).sort((a, b) => b[1] - a[1]);
    categoryData.value = {
      labels: sorted.map(([k]) => k),
      datasets: [
        {
          data: sorted.map(([, v]) => v),
          backgroundColor: sorted.map((_, i) => chartColors[i % chartColors.length])
        }
      ]
    };
    categories.value = sorted.slice(0, 3);


    // 키워드
    const keywordSorted = Object.entries(dashboard.keyword_stats).sort((a, b) => b[1] - a[1]).slice(0, 5);
    keywordData.value = {
      labels: keywordSorted.map(([k]) => k),
      datasets: [
        {
          label: "키워드 빈도수",
          data: keywordSorted.map(([, v]) => v),
          backgroundColor: "#6366F1"
        }
      ]
    };

    // 주간 읽은 기사
    const readSorted = Object.entries(dashboard.read_by_day || {}).sort(([a], [b]) => new Date(a) - new Date(b));
    if (readSorted.length === 1) {
      const onlyDate = new Date(readSorted[0][0]);
      const dummyDate = new Date(onlyDate);
      dummyDate.setDate(dummyDate.getDate() - 1);

      const dummyKey = dummyDate.toISOString().slice(0, 10);
      readSorted.unshift([dummyKey, 0]);
    }
    readData.value.labels = readSorted.map(([date]) => date);
    readData.value.datasets[0].data = readSorted.map(([, count]) => count);
    readData.value.datasets[0].backgroundColor = "#60A5FA";
  } catch (error) {
    console.error("대시보드 데이터 로딩 실패", error);
  }
  console.log("readData.value 확인:", readData.value);
});
</script>

<template>
  <div class="dashboard">
    <h1 class="title">📊 Personalized Dashboard</h1>
    <p class="subtitle">
      Discover your interests based on your browsing and likes, and get personalized
      <br />article recommendations. Let us guide you on your career journey with a tailored roadmap.
    </p>

    <div class="layout">
      <ContentBox class="category">
        <h1>🐤 My Interests</h1>
        <p class="card_description">
          We analyze the articles you've read to highlight your top news categories
          <br />— such as politics, economy, and culture — all in one view.
        </p>
        <div class="category__chart">
          <Doughnut :data="categoryData" :options="options" />
          <div class="category__labels">
            <span
              v-for="(category, index) in categories"
              :key="index"
              :style="{
                borderColor: categoryData.datasets[0]?.backgroundColor?.[index] || '#ccc',
                color: categoryData.datasets[0]?.backgroundColor?.[index] || '#ccc',
              }"
              class="category__label"
            >
              Rank {{ index + 1 }}: {{ category[0] }}({{ category[1] }})
            </span>
          </div>
        </div>
      </ContentBox>

      <ContentBox class="keyword">
        <h1>⭐️ Main Keywords</h1>
        <p class="card_description">
          By extracting the most frequent keywords from the articles
          <br />you’ve shown interest in, we reveal your current areas of interest.
        </p>
        <div class="bar-wrapper">
          <Bar :data="keywordData" :options="barOptions" />
        </div>
      </ContentBox>
    </div>

    <div class="layout">
      <ContentBox>
        <h1>📰 Weekly Read Articles</h1>
        <p class="card_description">
          Track your news consumption habits with a daily reading graph
          <br />that shows how many articles you read each day over the past week.
        </p>
        <div class="bar-wrapper">
          <Bar v-if="readData.labels.length" :data="readData" :options="readBarOptions" />
        </div>
      </ContentBox>

      <ContentBox class="like-news">
        <h1>❤️ Liked Articles</h1>
        <p class="card_description">
          Easily revisit your liked articles — all gathered in one place for quick access.
        </p>
        <div class="liked-scroll-wrapper">
          <ArticlePreview
            v-for="(article, index) in favoriteArticles"
            :key="index"
            :to="`/news/${article.id}`"
            :news="article"
          />
        </div>
      </ContentBox>
    </div>
  </div>
</template>

<style scoped lang="scss">
.dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 60px 20px 40px;
  text-align: center;
  display: flex;
  flex-direction: column;
}
.title {
  font-size: 2.2rem;
  font-weight: 800;
  color: #333;
  text-align: center;
  padding-bottom: 10px;
  margin-bottom: 10px;
  border-bottom: 1px solid #e2e2e2;
}
.subtitle {
  font-size: 1rem;
  color: #666;
  margin-top: 0;
  margin-bottom: 30px;
  line-height: 1.8;
}
.like-news {
  display: flex;
  flex-direction: column;
  height: 100%;
  box-sizing: border-box;

  .liked-scroll-wrapper {
    flex: 1;
    overflow-y: auto;
    padding-right: 5px;
    margin-top: 10px;
  }
}
.card_description {
  margin: 10px;
}
.layout {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
  > * {
    height: 450px;
  }

  @media (max-width: 768px) {
    flex-direction: column;
  }
}
.category {
  &__chart {
    height: 300px;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-bottom: 10px;
  }
  &__label {
    background-color: rgba(0, 0, 0, 0.04);
    color: var(--color-text);
    border-radius: 12px;
    padding: 6px 10px;
    font-size: 0.9rem;
    font-weight: 500;
    display: inline-block;
    margin: 6px;
  }
}
.bar-wrapper {
  margin-top: 30px;
  height: 300px;
  position: relative;
}
</style>
