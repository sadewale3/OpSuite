<template>
  <v-app id="inspire">
    <app-nav />

    <v-main>
      <router-view />
    </v-main>

    <!-- <v-footer app>
      <span>&copy; {{ new Date().getFullYear() }}</span>
    </v-footer> -->
  </v-app>
</template>

<script>
import AppNav from "@/components/AppNav";

export default {
  name: "App",
  props: {
    source: String
  },
  components: {
    AppNav
  },

  created() {
    this.$vuetify.theme.dark = true;
  }
};
</script>
