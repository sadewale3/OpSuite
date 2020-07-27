<template>
  <div>
    <v-data-table
      :headers="headers"
      :items="executionList"
      :search="search"
      class="elevation-6 ma-3"
      item-key="eid"
      no-data-text="No data to display"
    >
      <template v-slot:top>
        <v-toolbar flat color="indigo darken-4" class="elevation-6">
          <v-toolbar-title>{{ title }}</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-text-field
            v-model="search"
            append-icon="mdi-magnify"
            label="Search"
            class="shrink"
            style="width:400px"
            single-line
            hide-details
          ></v-text-field>
        </v-toolbar>
      </template>
      <template v-slot:no-data>
        No data to display
        <!-- <v-btn color="primary" @click="initialize">Reset</v-btn> -->
      </template>
    </v-data-table>
  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "Executions",

  computed: {
    ...mapState("executions", ["executionList", "executionListLoading"])
  },

  data: () => ({
    title: "Executions",
    search: "",
    headers: [
      { text: "Execution ID", value: "eid" },
      { text: "Job ID", value: "job_id", align: " d-none" },
      { text: "Job Name", value: "name" },
      { text: "Project", value: "project" },
      { text: "Module", value: "module" },
      { text: "Run Time", value: "scheduled_time" },
      { text: "State", value: "state" },
      { text: "Ouput", value: "output" }
    ]
  }),

  created() {
    var self = this;
    self.refreshExecutions();

    this.interval = setInterval(function() {
      self.refreshExecutions();
    }, 5000);
  },

  beforeDestroy() {
    clearInterval(this.interval);
  },

  methods: {
    refreshExecutions() {
      this.$store.dispatch("executions/getExecutions");
    },

    showError(err) {
      window.alert(err);
    },

    save() {}
  }
};
</script>

<style>
tbody tr:nth-of-type(even) {
  background-color: rgba(46, 46, 46, 0.842);
}

thead {
  background-color: black;
}

.custom-highlight-row {
  background-color: pink;
}
</style>
