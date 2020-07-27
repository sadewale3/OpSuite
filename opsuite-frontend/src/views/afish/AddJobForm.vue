<template>
  <v-card>
    <v-card-title>
      <span class="headline">Add Job</span>
    </v-card-title>
    <ValidationObserver ref="observer" v-slot="{ handleSubmit, invalid }">
      <v-form ref="form" @submit.prevent="handleSubmit(submitForm)">
        <v-container fluid dense grid-list-sm>
          <v-layout row wrap>
            <v-flex d-flex xs12 sm5 child-flex>
              <v-layout row wrap>
                <v-flex d-flex xs12 sm12 child-flex>
                  <ValidationProvider
                    rules="required"
                    name="Name"
                    v-slot="{ errors }"
                  >
                    <v-text-field
                      label="Job Name"
                      outlined
                      dense
                      prepend-icon="mdi-clipboard-text"
                      v-model="form.name"
                      :error-messages="errors"
                      autocomplete="new-password"
                    ></v-text-field>
                  </ValidationProvider>
                </v-flex>

                <v-flex d-flex xs12 sm12 child-flex>
                  <ValidationProvider
                    rules="required"
                    name="Project"
                    v-slot="{ errors }"
                  >
                    <v-text-field
                      label="Project"
                      outlined
                      dense
                      prepend-icon="mdi-clipboard-text-multiple"
                      v-model="form.project"
                      :error-messages="errors"
                      autocomplete="new-password"
                    ></v-text-field>
                  </ValidationProvider>
                </v-flex>

                <v-flex d-flex xs12 sm12 child-flex>
                  <ValidationProvider
                    rules="required"
                    name="Job Class"
                    v-slot="{ errors }"
                  >
                    <v-select
                      v-model="model"
                      :items="jobClasses"
                      item-text="module"
                      item-value="module"
                      prepend-icon="mdi-view-list"
                      label="Job Class"
                      :hint="model ? model.description : ''"
                      :error-messages="errors"
                      persistent-hint
                      dense
                      outlined
                      hide-no-data
                      no-gutters
                      return-object
                    ></v-select>
                  </ValidationProvider>
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
                    <v-card-text v-html="displayArgs(model.args)">
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

            <v-flex d-flex xs12 sm12 child-flex class="pa-5 pb-0">
              <v-layout row wrap>
                <v-flex d-flex xs12 sm12 child-flex>
                  <div v-if="model">
                    <v-divider />
                    <v-row v-for="(args, idx) in chunkedArgs" :key="idx">
                      <v-text-field
                        v-model="form.args[arg]"
                        v-for="arg in args"
                        :key="arg"
                        :label="arg"
                        outlined
                        dense
                        required
                        class="ma-2"
                        autocomplete="new-password"
                      ></v-text-field>
                    </v-row>
                  </div>
                </v-flex>
              </v-layout>
            </v-flex>

            <v-flex d-flex xs12 sm12 child-flex>
              <v-layout row wrap>
                <v-flex d-flex xs12 sm12 child-flex>
                  <v-radio-group v-model="form.recurring" row>
                    <v-radio label="Single Run" value="single"></v-radio>
                    <v-radio label="Recurring" value="recurring"></v-radio>
                  </v-radio-group>
                </v-flex>
              </v-layout>
            </v-flex>
          </v-layout>

          <v-row v-if="form.recurring == 'recurring'">
            <v-col cols="12" sm="8">
              <VueCronEditorBuefy
                v-bind:isAdvancedTabVisible="false"
                v-model="form.cronExpression"
              ></VueCronEditorBuefy>
            </v-col>
            <v-col cols="12" sm="2" class="mt-5">
              <ValidationProvider
                rules="positive"
                name="Jitter"
                v-slot="{ errors }"
              >
                <v-text-field
                  v-model="form.jitter"
                  label="Jitter (sec)"
                  append-outer-icon="mdi-plus"
                  @click:append-outer="increment"
                  prepend-icon="mdi-minus"
                  @click:prepend="decrement"
                  :rules="[numberRule]"
                  placeholder="0"
                  :error-messages="errors"
                ></v-text-field>
              </ValidationProvider>
            </v-col>
          </v-row>
        </v-container>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="closeForm()">Cancel</v-btn>
          <v-btn
            color="blue darken-1"
            text
            @click="submitForm(form)"
            :disabled="invalid"
            >Submit</v-btn
          >
        </v-card-actions>
      </v-form>
    </ValidationObserver>
  </v-card>
</template>

<script>
import VueCronEditorBuefy from "vue-cron-editor-buefy";
import { required } from "vee-validate/dist/rules";
import {
  extend,
  ValidationProvider,
  ValidationObserver
  // setInteractionMode
} from "vee-validate";
import { mapState } from "vuex";
import { chunk, keys } from "lodash";

// setInteractionMode("eager");

extend("required", {
  ...required,
  message: "{_field_} can not be empty"
});

extend("positive", value => {
  return value >= 10;
});

export default {
  components: { VueCronEditorBuefy, ValidationProvider, ValidationObserver },
  name: "AddJobForm",

  computed: {
    ...mapState("jobs", ["jobClasses"]),

    chunkedArgs() {
      if (this.model) {
        var arr = keys(this.model.args);
        return chunk(arr, 3);
      }
      return [];
    }
  },

  data() {
    return {
      model: null,
      // valid: null,
      form: {
        name: "",
        project: "",
        module: "",
        args: {},
        recurring: "single",
        jitter: "10",
        cronExpression: "0 12 */1 * *"
      }
    };
  },

  created() {
    this.$store.dispatch("jobs/loadJobClasses");
  },

  watch: {
    model() {
      this.form.module = this.model.module;
      this.form.args = {};
      for (const key in this.model.args) {
        this.$set(this.form.args, key, "");
      }
    }
  },

  methods: {
    displayArgs: function(obj) {
      var args = "";
      for (const [key, value] of Object.entries(obj)) {
        args += `${key}: ${value}<br/>`;
      }
      return args;
    },

    increment() {
      this.form.jitter = parseInt(this.form.jitter, 10) + 1;
    },

    decrement() {
      if (this.form.jitter <= 10) {
        this.form.jitter = 10;
      } else this.form.jitter = parseInt(this.form.jitter, 10) - 1;
    },

    numberRule: v => {
      if (!isNaN(parseInt(v)) && v >= 0) return true;
      return "Number has to be greater or equal to 10.";
    },

    closeForm: function() {
      this.$emit("close");
    },

    submitForm: function() {
      console.log(this.form);
      this.$store.dispatch("jobs/submitJobForm", this.form);
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
