<template>
  <div>
    <v-data-table
      :expanded.sync="expanded"
      :headers="headers"
      :items="jobList"
      class="elevation-6 ma-3"
      item-key="id"
      no-data-text="No data to display"
      show-expand
      sort-by="ctime"
    >
      <template v-slot:top>
        <v-toolbar flat color="indigo darken-4" class="elevation-6">
          <v-toolbar-title>{{ title }}</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-dialog
            v-model="dialog"
            max-width="1000px"
            :persistent="persistent"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                color="success"
                dark
                class="mb-2"
                v-bind="attrs"
                @click="dialog = true"
                >New Job</v-btn
              >
            </template>
            <template>
              <add-job-form v-if="dialog" v-on:close="close" />
            </template>
          </v-dialog>
        </v-toolbar>
      </template>
      <template v-slot:item.actions="{ item }">
        <v-icon
          v-if="item.status == 'PAUSED'"
          small
          class="mr-2"
          color="green"
          @click="resumeJob(item)"
          >mdi-play-circle</v-icon
        >
        <v-icon
          v-if="item.status == 'RUNNING'"
          small
          class="mr-2"
          color="yellow"
          @click="pauseJob(item)"
          >mdi-pause-circle</v-icon
        >
        <v-icon small color="red" @click="deleteJob(item)"
          >mdi-trash-can</v-icon
        >
      </template>
      <template v-slot:expanded-item="{ headers, item }">
        <td :colspan="headers.length" class="pa-3">
          <v-simple-table dense>
            <template v-slot:default>
              <thead>
                <tr>
                  <th class="text-left">Runtime</th>
                  <th class="text-left">Status</th>
                  <th class="text-left">Output</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="exec in item.executions" :key="exec.runtime">
                  <td>{{ exec.runtime }}</td>
                  <td>{{ exec.status }}</td>
                  <td>{{ exec.output }}</td>
                </tr>
              </tbody>
            </template>
          </v-simple-table>
        </td>
      </template>
      <template v-slot:no-data>
        No data to display
        <!-- <v-btn color="primary" @click="initialize">Reset</v-btn> -->
      </template>
    </v-data-table>
  </div>
</template>

<script>
import AddJobForm from "@/views/afish/AddJobForm";
import { mapState } from "vuex";

export default {
  components: { AddJobForm },
  name: "Jobs",

  computed: {
    ...mapState("jobs", ["jobList", "jobListLoading"])
  },

  data: () => ({
    expanded: [],
    dialog: false,
    title: "Persistence Jobs",
    headers: [
      {
        text: "Job Name",
        align: "start",
        value: "name"
      },
      { text: "Project", value: "project" },
      { text: "Module", value: "module" },
      { text: "Creation Time", value: "ctime" },
      { text: "Status", value: "status" },
      { text: "Schedule", value: "schedule" },
      { text: "Next Run", value: "nextrun" },
      { text: "Actions", value: "actions", sortable: false }
    ],
    selectedRow: null,
    editedIndex: -1,
    persistent: true,
    interval: undefined
  }),

  watch: {
    dialog(val) {
      val || this.close();
    }
  },

  created() {
    var self = this;
    self.refreshJobs();

    this.interval = setInterval(function() {
      self.refreshJobs();
    }, 5000);
  },

  beforeDestroy() {
    clearInterval(this.interval);
  },

  methods: {
    resumeJob: function(job) {
      this.$store.dispatch("jobs/resumeJob", job.id);
      this.refreshJobs();
    },

    pauseJob: function(job) {
      this.$store.dispatch("jobs/pauseJob", job.id);
      this.refreshJobs();
    },

    deleteJob: function(job) {
      this.$confirm("Do you really want to delete this job?", {
        title: `Delete Job - ${job.name} | ${job.project}`,
        buttonTrueColor: "error"
      }).then(res => {
        if (res) {
          this.$store.dispatch("jobs/deleteJob", job.id);
        }
      });
      this.refreshJobs();
    },

    refreshJobs() {
      this.$store.dispatch("jobs/getJobs");
    },

    showError(err) {
      window.alert(err);
    },

    close() {
      this.dialog = false;
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
</style>
