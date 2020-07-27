import Vue from "vue";
import Vuetify from "vuetify/lib";
import VuetifyConfirm from "vuetify-confirm";

const vuetify = new Vuetify({
  theme: {
    options: {
      customProperties: true
    },
    themes: {
      light: {
        primary: "#ee44aa",
        secondary: "#424242",
        accent: "#82B1FF",
        error: "#FF5252",
        info: "#2196F3",
        success: "#4CAF50",
        warning: "#FFC107"
      }
    }
  }
});

Vue.use(Vuetify);
Vue.use(VuetifyConfirm, {
  vuetify
});

export default vuetify;
