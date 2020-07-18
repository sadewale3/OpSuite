<template>
  <v-app id="inspire">
    <app-nav />

    <v-main>
      <router-view />
    </v-main>
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

<style>
html {
  overflow-y: auto !important;
}

::-webkit-scrollbar {
  width: 15px;
}

::-webkit-scrollbar-track {
  background: #202020;
  border-left: 1px solid #2c2c2c;
}

::-webkit-scrollbar-thumb {
  background: #3e3e3e;
  border: solid 3px #202020;
  border-radius: 7px;
}

::-webkit-scrollbar-thumb:hover {
  background: white;
}
</style>