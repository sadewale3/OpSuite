<template>
  <v-card>
    <v-card-title>
      <span class="headline">Add Job</span>
    </v-card-title>

    <v-form ref="form" v-model="valid">
      <v-container fluid dense grid-list-sm>
        <v-layout row wrap>
          <v-flex d-flex xs12 sm5 child-flex>
            <v-layout row wrap>
              <v-flex d-flex xs12 sm12 child-flex>
                <v-text-field
                  label="Job Name"
                  outlined
                  dense
                  prepend-icon="mdi-clipboard-text"
                  required
                ></v-text-field>
              </v-flex>

              <v-flex d-flex xs12 sm12 child-flex>
                <v-text-field
                  label="Project"
                  outlined
                  dense
                  prepend-icon="mdi-clipboard-text-multiple"
                  required
                ></v-text-field>
              </v-flex>

              <v-flex d-flex xs12 sm12 child-flex>
                <v-select
                  v-model="model"
                  :items="jobClasses"
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
              </v-flex>
            </v-layout>
          </v-flex>

          <v-flex d-flex xs12 sm7 child-flex>
            <v-layout row wrap>
              <v-flex d-flex xs12 sm12 child-flex>
                <v-card
                  v-if="model"
                  color="deep-purple darken-4"
                  class="mx-12 elevation-8"
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
              </v-flex>
            </v-layout>
          </v-flex>

          <v-flex d-flex xs12 sm12 child-flex class="pa-5">
            <v-layout row wrap>
              <v-flex d-flex xs12 sm12 child-flex>
                <div v-if="model">
                  <v-row v-for="(args, idx) in chunkedArgs" :key="idx">
                    <v-text-field
                      v-for="arg in args"
                      :key="arg"
                      :label="arg"
                      outlined
                      dense
                      required
                      class="ma-2"
                    ></v-text-field>
                  </v-row>
                </div>
              </v-flex>
            </v-layout>
          </v-flex>
        </v-layout>

        <v-divider />
        <v-radio-group v-model="recurring" row>
          <v-radio label="Single Run" value="single"></v-radio>
          <v-radio label="Recurring" value="recurring"></v-radio>
        </v-radio-group>

        <v-row v-if="recurring == 'recurring'">
          <v-col cols="12" sm="8">
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
import { mapState } from "vuex";
import { chunk, keys } from "lodash";

export default {
  components: { VueCronEditorBuefy },
  name: "AddJobForm",

  computed: {
    ...mapState("jobs", ["jobClasses"]),

    chunkedArgs() {
      if (this.model) {
        var arr = keys(this.model.arguments);
        return chunk(arr, 3);
      }
      return [];
    }
  },

  data() {
    return {
      cronExpression: "",
      model: null,
      search: null,
      valid: null,
      recurring: "single"
    };
  },

  created() {
    this.$store.dispatch("jobs/loadJobClasses");
  },

  methods: {
    displayArgs: function(obj) {
      var args = "";
      for (const [key, value] of Object.entries(obj)) {
        args += `${key}: ${value}<br/>`;
      }
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

<style>
.enable-bulma {
  background-color: black !important;
  color: white !important;
}
</style>