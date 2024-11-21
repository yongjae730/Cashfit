<template>
  <nav class="finance-menu">
    <v-container class="menu-container" fluid>
      <v-row justify="center" align="center" class="menu-grid">
        <v-col cols="12" class="menu-wrapper">
          <router-link v-for="(item, index) in menuItems" :key="index" :to="item.route" class="menu-link">
            <v-btn class="menu-btn" variant="flat" size="large">
              <v-icon class="menu-icon" size="24">
                {{ item.icon }}
              </v-icon>
              <span class="menu-label">{{ item.label }}</span>
            </v-btn>
          </router-link>
        </v-col>
      </v-row>
    </v-container>
  </nav>
</template>

<script setup>
import { ref } from "vue";

const menuItems = ref([
  {
    label: "금융상품",
    route: { name: "fin" },
    icon: "mdi-bank",
  },
  {
    label: "커뮤니티",
    route: { name: "stock" },
    icon: "mdi-forum-outline",
  },
  //   {
  //     label: "비트코인",
  //     route: { name: "crypto" },
  //     icon: "mdi-currency-btc",
  //   },
  {
    label: "Exchange",
    route: { name: "exchange" },
    icon: "mdi-chart-line",
  },
]);
</script>

<style scoped>
.finance-menu {
  background: linear-gradient(to right, #f4f7f6, #f1f3f2);
  padding: 15px 0;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.menu-container {
  max-width: 1200px;
}

.menu-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 25px;
  flex-wrap: wrap;
}

.menu-link {
  text-decoration: none;
}

.menu-btn {
  background-color: white;
  color: #37474f;
  font-weight: 600;
  letter-spacing: 0.5px;
  text-transform: capitalize;
  padding: 10px 20px;
  border-radius: 12px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
}

.menu-btn:hover {
  background-color: #f5f5f5;
  transform: translateY(-3px);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
}

.menu-icon {
  color: #2196f3;
  margin-right: 10px;
}

.menu-label {
  font-size: 15px;
}

/* Responsive adjustments */
@media (max-width: 600px) {
  .menu-wrapper {
    flex-direction: column;
    gap: 15px;
  }

  .menu-btn {
    width: 100%;
    max-width: 250px;
  }
}
</style>
