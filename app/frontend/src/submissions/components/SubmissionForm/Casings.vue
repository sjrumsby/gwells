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
      <b-col cols="12" lg="6">
        <legend :id="id">Casing Details</legend>
      </b-col>
      <b-col cols="12" lg="6">
        <div class="float-right">
          <b-btn v-if="isStaffEdit" variant="primary" class="ml-2" @click="$emit('save')" :disabled="saveDisabled">Save</b-btn>
          <a href="#top" v-if="isStaffEdit">Back to top</a>
        </div>
      </b-col>
    </b-row>
    <div class="table-responsive" id="casingTable">
      <table class="table table-sm">
        <thead>
          <tr>
            <th class="font-weight-normal">From ft (bgl)</th>
            <th class="font-weight-normal">To ft (bgl)</th>
            <th class="font-weight-normal">Casing Type</th>
            <th class="font-weight-normal">Casing Material</th>
            <th class="font-weight-normal">Diameter (in)</th>
            <th class="font-weight-normal">Wall Thickness (in)</th>
            <th class="font-weight-normal">Drive Shoe</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(casing, index) in casingsInput" :key="casing.id">
            <td class="pb-0">
              <form-input
                group-class="my-0"
                :id="'casingFrom_' + index"
                type="number"
                v-model="casing.start"
                :errors="getCasingError(index).start"
                :loaded="getFieldsLoaded(index).start"/>
            </td>
            <td class="pb-0">
              <form-input
                group-class="my-0"
                :id="'casingTo_' + index"
                type="number"
                v-model="casing.end"
                :errors="getCasingError(index).end"
                :loaded="getFieldsLoaded(index).end"/>
            </td>
            <td class="pb-0">
              <b-form-group
                :id="'casingCode_' + index"
                class="my-0"
                :aria-describedby="`casingCodeInvalidFeedback${index}`">
                <b-form-select
                    v-model="casing.casing_code"
                    :options="codes.casing_codes"
                    value-field="code"
                    text-field="description"
                    :state="getCasingError(index).casing_code ? false : null">
                  <template slot="first">
                    <option :value="null" disabled>Select a type</option>
                  </template>
                </b-form-select>
                <b-form-invalid-feedback :id="`casingCodeInvalidFeedback${index}`">
                  <div v-for="(error, error_index) in getCasingError(index).casing_code" :key="`Casing type input error ${error_index}`">
                    {{ error }}
                  </div>
                </b-form-invalid-feedback>
              </b-form-group>
            </td>
            <td class="pb-0">
              <b-form-group
                :id="'casingMaterial_' + index"
                class="my-0"
                :aria-describedby="`casingMaterialInvalidFeedback${index}`">
                <b-form-select
                    v-model="casing.casing_material"
                    :options="codes.casing_materials"
                    value-field="code"
                    text-field="description"
                    :state="getCasingError(index).casing_material ? false : null">
                  <template slot="first">
                    <option :value="null" disabled>Select a material</option>
                  </template>
                </b-form-select>
                <b-form-invalid-feedback :id="`casingCodeInvalidFeedback${index}`">
                  <div v-for="(error, error_index) in getCasingError(index).casing_material" :key="`Material input error ${error_index}`">
                    {{ error }}
                  </div>
                </b-form-invalid-feedback>
              </b-form-group>
            </td>
            <td class="pb-0">
              <form-input
                group-class="my-0"
                :id="'casingDiameter_' + index"
                type="number"
                v-model="casing.diameter"
                :errors="getCasingError(index).diameter"
                :loaded="getFieldsLoaded(index).diameter"/>
            </td>
            <td class="pb-0">
              <form-input
                group-class="my-0"
                :id="'casingWallThickness_' + index"
                type="number"
                v-model="casing.wall_thickness"
                :errors="getCasingError(index).wall_thickness"
                :loaded="getFieldsLoaded(index).wall_thickness"/>
            </td>
            <td class="pt-0 py-0">
              <b-form-radio-group v-model="casing.drive_shoe"
                                  :name="'drive_shoe_' + index"
                                  :id="'casingDriveShoe_' + index">
                <b-form-radio :value="false">No</b-form-radio>
                <b-form-radio :value="true">Yes</b-form-radio>
              </b-form-radio-group>
            </td>
            <td class="pt-1 py-0">
              <b-btn size="sm" variant="primary" :id="`removeCasingRowBtn${index}`" @click="removeRowIfOk(casing)" class="mt-2"><i class="fa fa-minus-square-o"></i> Remove</b-btn>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <b-btn size="sm" id="addCasingRowBtn" variant="primary" @click="addRow"><i class="fa fa-plus-square-o"></i> Add row</b-btn>
    <b-modal
        v-model="confirmRemoveModal"
        centered
        title="Confirm remove"
        @shown="focusRemoveModal">
      Are you sure you want to remove this row?
      <div slot="modal-footer">
        <b-btn variant="secondary" @click="confirmRemoveModal=false;rowIndexToRemove=null" ref="cancelRemoveBtn">
          Cancel
        </b-btn>
        <b-btn variant="danger" @click="confirmRemoveModal=false;removeRowByIndex(rowIndexToRemove)">
          Remove
        </b-btn>
      </div>
    </b-modal>
  </fieldset>
</template>

<script>
import { mapGetters } from 'vuex'
import inputBindingsMixin from '@/common/inputBindingsMixin.js'
export default {
  name: 'Casings',
  mixins: [inputBindingsMixin],
  props: {
    casings: Array,
    errors: {
      type: Object,
      default: () => ({})
    },
    fieldsLoaded: {
      type: Object,
      default: () => ({})
    },
    id: {
      type: String,
      isInput: false
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
      confirmRemoveModal: false,
      rowIndexToRemove: null
    }
  },
  methods: {
    addRow () {
      this.casingsInput.push({})
    },
    removeRowByIndex (index) {
      this.casingsInput.splice(index, 1)
      this.rowIndexToRemove = null
    },
    removeRowIfOk (instance) {
      const index = this.casingsInput.findIndex(item => item === instance)
      if (this.rowHasValues(this.casingsInput[index])) {
        this.rowIndexToRemove = index
        this.confirmRemoveModal = true
      } else {
        this.removeRowByIndex(index)
      }
    },
    getCasingError (index) {
      if (this.errors && 'casing_set' in this.errors && index in this.errors['casing_set']) {
        return this.errors['casing_set'][index]
      }
      return {}
    },
    getFieldsLoaded (index) {
      if (this.fieldsLoaded && 'casing_set' in this.fieldsLoaded && index in this.fieldsLoaded['casing_set']) {
        return this.fieldsLoaded['casing_set'][index]
      }
      return {}
    },
    rowHasValues (row) {
      let keys = Object.keys(row)
      if (keys.length === 0) return false
      // Check that all fields are not empty.
      return !keys.every((key) => !row[key])
    },
    focusRemoveModal () {
      // Focus the "cancel" button in the confirm remove popup.
      this.$refs.cancelRemoveBtn.focus()
    }
  },
  computed: {
    ...mapGetters(['codes'])
  },
  created () {
    // When component created, add an initial row of casings.
    if (!this.casingsInput.length) {
      this.casingsInput.push({}, {}, {})
    }
  }
}
</script>

<style>

</style>
