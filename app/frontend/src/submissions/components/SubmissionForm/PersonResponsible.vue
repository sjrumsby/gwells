/*
Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
*/
<template>
    <fieldset>
      <b-row>
        <b-col xs="12">
          <legend :id="id">
            Person Responsible for Work
          </legend>
        </b-col>
        <b-col xs="12">
          <div class="float-right">
            <b-btn v-if="isStaffEdit" variant="primary" class="ml-2" @click="$emit('save')" :disabled="saveDisabled">Save</b-btn>
            <a href="#top" v-if="isStaffEdit">Back to top</a>
          </div>
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="12" md="12" lg="4">
          <b-form-group
              label="Person Responsible for Drilling *"
              aria-describedby="personResponsibleInvalidFeedback"
              :state="false">
            <v-select
                :class="errors.driller_responsible?'border border-danger dropdown-error-border':''"
                id="personResponsibleSelect"
                :filterable="false"
                :options="personOptions"
                label="name"
                v-model="personResponsibleInput"
                @search="onPersonSearch">
              <template slot="no-options">
                  Type to search registry...
              </template>
              <template slot="option" slot-scope="option">
                <div>
                  {{ option.name }}
                  </div>
              </template>
              <template slot="selected-option" slot-scope="option">
                <div>
                  {{ option.name }}
                </div>
              </template>
            </v-select>
            <b-form-text id="personResponsibleInvalidFeedback" v-if="errors.driller_responsible">
              <div v-for="(error, index) in errors.driller_responsible" :key="`personResponsible error ${index}`" class="text-danger">
                {{ error }}
              </div>
            </b-form-text>
          </b-form-group>
        </b-col>
        <b-col cols="12" md="6" lg="4">
          <form-input
              id="drillerName"
              label="Name of Person Who Did the Drilling"
              type="text"
              :disabled="drillerSameAsPersonResponsible"
              v-model="drillerNameInput"
              :errors="errors['driller_name']"
              :loaded="fieldsLoaded['driller_name']"
          ></form-input>
        </b-col>
        <b-col cols="12" md="6" lg="4">
          <b-form-group class="pt-md-4 mt-md-2">
            <b-form-checkbox id="checkbox1"
                  v-model="drillerSameAsPersonResponsibleInput"
                  :value="true"
                  :unchecked-value="false"
                  :disabled="!personResponsible">
              Same as Person Responsible for Drilling
            </b-form-checkbox>
          </b-form-group>
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="12" md="6">
          <form-input
              id="consultantName"
              label="Consultant Name"
              type="text"
              v-model="consultantNameInput"
              :errors="errors['consultant_name']"
              :loaded="fieldsLoaded['consultant_name']"
          ></form-input>
        </b-col>
        <b-col cols="12" md="6">
          <form-input
              id="consultantCompany"
              label="Consultant Company"
              type="text"
              v-model="consultantCompanyInput"
              :errors="errors['consultant_company']"
              :loaded="fieldsLoaded['consultant_company']"
          ></form-input>
        </b-col>
      </b-row>
    </fieldset>
</template>

<script>
import debounce from 'lodash.debounce'
import { mapGetters } from 'vuex'
import inputBindingsMixin from '@/common/inputBindingsMixin.js'
import ApiService from '@/common/services/ApiService.js'
export default {
  name: 'PersonResponsible',
  mixins: [inputBindingsMixin],
  props: {
    personResponsible: Object,
    drillerName: String,
    consultantName: String,
    consultantCompany: String,
    drillerSameAsPersonResponsible: Boolean,
    id: {
      type: String,
      isInput: false
    },
    errors: {
      type: Object,
      default: () => ({}),
      inInput: true
    },
    fieldsLoaded: {
      type: Object,
      default: () => ({}),
      inInput: true
    },
    isStaffEdit: {
      type: Boolean,
      isInput: false
    },
    saveDisabled: {
      type: Boolean,
      isInput: false
    }
  },
  data () {
    return {
      personOptions: []
    }
  },
  computed: {
    ...mapGetters(['userRoles'])
  },
  methods: {
    onPersonSearch (search, loading) {
      loading(true)
      this.drillerSearch(loading, search, this)
    },
    drillerSearch: debounce((loading, search, vm) => {
      ApiService.query(`drillers/names/?search=${escape(search)}`).then((response) => {
        vm.personOptions = response.data
        loading(false)
      })
    }, 500)
  },
  watch: {
    personResponsible (val, prev) {
      // reset list of people when user finished selecting a person
      this.personOptions = []
      if (prev) {
        this.drillerSameAsPersonResponsibleInput = false
      }
    },
    drillerSameAsPersonResponsible (val) {
      // keep driller name disabled & set to "person responsible", or leave it enabled and blank
      this.drillerNameInput = (this.personResponsible && this.drillerSameAsPersonResponsible) ? this.personResponsible.name : ''
    }
  }
}
</script>

<style>
.dropdown-error-border {
  border-radius: 5px;
}
</style>
