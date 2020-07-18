import axios from "axios";

const httpClient = axios.create({
  baseURL: process.env.VUE_APP_API_ENDPOINT + "/afish",
  headers: {
    "Content-Type": "application/json",
  },
});

const jobs = {
  namespaced: true,
  state: {
    jobClasses: [],
  },
  mutations: {
    SET_JOBCLASSES(state, data) {
      state.jobClasses = data;
    },
  },
  actions: {
    loadJobClasses({ commit }) {
      httpClient
        .get("jobs/getJobClasses")
        .then((res) => {
          commit("SET_JOBCLASSES", res.data);
        })
        .catch((error) => console.log(error));
    },
  },
};

export default jobs;
