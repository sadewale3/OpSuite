import Vue from "vue";
import Vuex from "vuex";
import { jobs, executions } from "./modules/afish";

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    jobs,
    executions
  }
});
