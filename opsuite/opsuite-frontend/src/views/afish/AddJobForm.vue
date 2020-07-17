<template>
  <v-card>
    <v-card-title>
      <span class="headline">Add Job</span>
    </v-card-title>

    <v-form
      ref="form"
      v-model="valid"
      :lazy-validation="lazy"
    >
      <v-container fluid dense>
        <v-row>
          <v-col cols="6" sm="6">
            <v-text-field
              label="Job Name"
              outlined
              dense
              prepend-icon="mdi-clipboard-text"
              required
            ></v-text-field>
          </v-col>
        </v-row>

        <v-row>
          <v-col sm="6">
            <v-select
              v-model="model"
              :items="entries"
              item-text="job_class"
              item-value="job_class"
              prepend-icon="mdi-view-list"
              label="Job Class"
              :hint="model ? model.description : ''"
              persistent-hint
              dense
              outlined
              hide-no-data
              no-gutters
              return-object
              required
            ></v-select>
          </v-col>
          <v-col sm="6">
            <v-card
              v-if="model"
              class="mx-auto elevation-12"
              max-width="344"
            >
              <v-card-title class="h6">
                Arguments
              </v-card-title>
              <v-card-text v-html="displayArgs(model.arguments)">
              </v-card-text>
              <div v-if="model.notes">
                <v-divider />
                <v-card-title class="h6">
                  Notes
                </v-card-title>
                <v-card-subtitle>
                  {{ model.notes }}
                </v-card-subtitle>
             </div>
            </v-card>
          </v-col>
        </v-row>

        <v-radio-group v-model="recurring" row>
          <v-radio label="Single Run" value="single"></v-radio>
          <v-radio label="Recurring" value="recurring"></v-radio>
        </v-radio-group>

        <v-row v-if="recurring == 'recurring'">
          <v-col cols="12" sm="8">
            Cron Scheduler
            <v-divider class="pb-3"></v-divider>
            <VueCronEditorBuefy
              v-bind:isAdvancedTabVisible="false"
              v-model="cronExpression"
            ></VueCronEditorBuefy>
          </v-col>
        </v-row>
      </v-container>
    </v-form>

    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn color="blue darken-1" text @click="closeForm">Cancel</v-btn>
      <v-btn color="blue darken-1" text @click="submitForm">Submit</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import VueCronEditorBuefy from "vue-cron-editor-buefy";
import HttpClient from "@/plugins/axios.js";

export default {
  components: { VueCronEditorBuefy },
  name: "AddJobForm",

  data () {
    return {
      cronExpression: "",
      entries: [],
      model: null,
      search: null,
      valid: null,
      recurring: false
    }
  },

  created () {
     HttpClient.get("/afish/jobs/")
        .then((response) => {
          console.log(response.data);
          this.entries = response.data;
        })
        .catch((error) => {
          console.log(error);
        })
  },

  methods: {
    displayArgs: function(obj) {
      var args = "";
      for (const [ key, value ] of Object.entries(obj)) {
        args += `${key}: ${value}<br/>`;
      }
      console.log(args);
      return args;
    },

    closeForm: function() {
      this.$emit("close");
    },

    submitForm: function() {
      this.$emit("close");
    }
  }
};
</script>

<style scoped>
.enable-bulma {
  background-color: black !important;
  color: white !important;
}

#description {
  overflow: auto;
}
</style>
