import axios from "axios";

const httpClient = axios.create({
  baseURL: process.env.VUE_APP_API_ENDPOINT + "/afish",
  headers: {
    "Content-Type": "application/json"
  }
});

const jobs = {
  namespaced: true,
  state: {
    jobClasses: [],
    jobList: [],
    jobListLoading: true,
    toastText: ""
  },

  mutations: {
    SET_JOBCLASSES(state, data) {
      state.jobClasses = data;
    },

    SET_JOBLIST(state, data) {
      state.jobList = data;
      state.jobListLoading = false;
    },

    START_JOBLISTLOADING(state) {
      state.jobListLoading = true;
    },

    SET_TOASTTEXT(state, data) {
      state.toastText = data;
    }
  },

  actions: {
    loadJobClasses({ commit }) {
      httpClient
        .get("jobclasses")
        .then(res => {
          commit("SET_JOBCLASSES", res.data);
          console.log(res.data);
        })
        .catch(error => console.log(error));
    },

    getJobs({ commit }) {
      commit("START_JOBLISTLOADING");
      httpClient
        .get("jobs")
        .then(res => {
          commit("SET_JOBLIST", res.data);
        })
        .catch(error => console.log(error));
    },

    pauseJob({ commit }, id) {
      httpClient
        .post(`jobs/${id}`, { action: "pause" })
        .then(res => {
          commit("SET_TOASTTEXT", res.data);
        })
        .catch(error => console.log(error));
    },

    resumeJob({ commit }, id) {
      console.log(id);
      httpClient
        .post(`jobs/${id}`, { action: "resume" })
        .then(res => {
          commit("SET_TOASTTEXT", res.data);
        })
        .catch(error => console.log(error));
    },

    deleteJob({ commit }, id) {
      httpClient
        .delete(`jobs/${id}`)
        .then(res => {
          commit("SET_TOASTTEXT", res.data);
        })
        .catch(error => console.log(error));
    },

    submitJobForm({ commit }, payload) {
      console.log(payload);
      httpClient
        .put("jobs", payload)
        .then(res => {
          commit("SET_TOASTTEXT", res.data);
        })
        .catch(error => console.log(error));
    }
  }
};

const executions = {
  namespaced: true,
  state: {
    executionList: [],
    executionListLoading: true
  },

  mutations: {
    SET_EXECUTIONLIST(state, data) {
      state.executionList = data;
      state.executionListLoading = false;
    },

    START_EXECUTIONLISTLOADING(state) {
      state.executionListLoading = true;
    }
  },

  actions: {
    getExecutions({ commit }) {
      commit("START_EXECUTIONLISTLOADING");
      httpClient
        .get("executions")
        .then(res => {
          commit("SET_EXECUTIONLIST", res.data);
        })
        .catch(error => console.log(error));
    }
  }
};

export { jobs, executions };
