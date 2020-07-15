<template>
  <v-data-table
    :expanded.sync="expanded"
    :headers="headers"
    :items="jobs"
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
        <v-dialog v-model="dialog" max-width="500px">
          <template v-slot:activator="{ on, attrs }">
            <v-btn color="success" dark class="mb-2" v-bind="attrs" v-on="on"
              >New Job</v-btn
            >
          </template>
          <v-card>
            <v-card-title>
              <span class="headline">{{ formTitle }}</span>
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-row>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field
                      v-model="editedJob.name"
                      label="Job Name"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field
                      v-model="editedJob.schedule"
                      label="Schedule (UTC)"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field
                      v-model="editedJob.nextrun"
                      label="Next Run (local)"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field
                      v-model="editedJob.action"
                      label="Action"
                    ></v-text-field>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="close">Cancel</v-btn>
              <v-btn color="blue darken-1" text @click="save">Save</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-toolbar>
    </template>
    <template v-slot:item.actions="{ item }">
      <v-icon small class="mr-2" color="green" @click="deleteItem(item)"
        >mdi-play-circle</v-icon
      >
      <v-icon small class="mr-2" color="yellow" @click="editItem(item)"
        >mdi-pencil</v-icon
      >
      <v-icon small color="red" @click="deleteItem(item)"
        >mdi-stop-circle</v-icon
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
                <td>{{ exec.status}}</td>
                <td>{{ exec.output}}</td>
              </tr>
            </tbody>
          </template>
        </v-simple-table>
      </td>
    </template>
    <template v-slot:no-data>
      No data to display
      <v-btn color="primary" @click="initialize">Reset</v-btn>
    </template>
  </v-data-table>
</template>

<script>
export default {
  name: "Jobs",
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
      { text: "Op", value: "op" },
      { text: "Type", value: "type" },
      { text: "Creation Time", value: "ctime" },
      { text: "Status", value: "status" },
      { text: "Schedule", value: "schedule" },
      { text: "Next Run", value: "nextrun" },
      { text: "Actions", value: "actions", sortable: false }
    ],
    selectedRow: null,
    jobs: [],
    editedIndex: -1,
    editedJob: {
      name: "",
      calories: 0,
      fat: 0,
      carbs: 0,
      protein: 0
    },
    defaultJob: {
      name: "",
      calories: 0,
      fat: 0,
      carbs: 0,
      protein: 0
    }
  }),

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? "New Job" : "Edit Job";
    }
  },

  watch: {
    dialog(val) {
      val || this.close();
    }
  },

  created() {
    this.initialize();
  },

  methods: {
    initialize() {
      this.jobs = [
        {
          id: 1,
          name: "SPN 1",
          op: "TestOp",
          type: "Azure.SPNCredentials",
          test: "TestData",
          ctime: new Date().toLocaleString(),
          status: "RUNNING",
          schedule: 4,
          nextrun: new Date(new Date().getTime()+(240*60*1000)).toLocaleString(),
          executions: [
            {
              runtime: new Date().toLocaleString(),
              status: "SUCCESS",
              output: "Random output"
            },
            {
              runtime: new Date().toLocaleString(),
              status: "FAILED",
              output: "Random output"
            },
            {
              runtime: new Date().toLocaleString(),
              status: "SUCCESS",
              output: "Random output"
            }
          ]
        },
        {
          id: 2,
          name: "SPN 2",
          op: "TestOp",
          type: "Azure.SPNCertificate",
          test: "TestData",
          ctime: new Date().toLocaleString(),
          status: "RUNNING",
          schedule: 3,
          nextrun: new Date(new Date().getTime()+(180*60*1000)).toLocaleString()
        },
        {
          id: 3,
          name: "SQL 1",
          op: "TestOp",
          type: "SQL.UserPassword",
          ctime: new Date().toLocaleString(),
          status: "RUNNING",
          schedule: 1,
          nextrun: new Date(new Date().getTime()+(60*1000)).toLocaleString()
        },
        {
          id: 4,
          name: "Storage Account 1",
          op: "TestOp",
          type: "Azure.StorageAccountKey",
          ctime: new Date().toLocaleString(),
          status: "RUNNING",
          schedule: 24,
          nextrun: new Date(new Date().getTime()+(24*3600*1000)).toLocaleString()
        }
      ];
    },

    editItem(item) {
      this.editedIndex = this.jobs.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },

    deleteItem(item) {
      const index = this.jobs.indexOf(item);
      console.log(index);
      confirm("Are you sure you want to delete this item?") &&
        this.jobs.splice(index, 1);
    },

    close() {
      this.dialog = false;
      this.$nextTick(() => {
        this.editedJob = Object.assign({}, this.defaultJob);
        this.editedIndex = -1;
      });
    },

    save() {
      if (this.editedIndex > -1) {
        Object.assign(this.jobs[this.editedIndex], this.editedJob);
      } else {
        this.jobs.push(this.editedJob);
      }
      this.close();
    }
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

.custom-highlight-row{
  background-color: pink
}
</style>