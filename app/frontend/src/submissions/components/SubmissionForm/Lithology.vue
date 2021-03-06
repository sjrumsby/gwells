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
        <legend :id="id">Lithology</legend>
      </b-col>
      <b-col cols="12" lg="6">
        <div class="float-right">
          <b-btn v-if="isStaffEdit" variant="primary" class="ml-2" @click="$emit('save')" :disabled="saveDisabled">Save</b-btn>
          <a href="#top" v-if="isStaffEdit">Back to top</a>
        </div>
      </b-col>
    </b-row>
    <div class="table-responsive">
      <table class="table table-sm">
        <thead>
          <tr>
            <th class="font-weight-normal">
              <div>From</div><div>ft (bgl)</div>
            </th>
            <th class="font-weight-normal">
              <div>To</div><div>ft (bgl)</div>
            </th>
            <th class="font-weight-normal">
              Primary Surficial Material
            </th>
            <th class="font-weight-normal">
              Secondary Surficial Material
            </th>
            <th class="font-weight-normal">
              Bedrock
            </th>
            <th class="font-weight-normal">
              Descriptor
            </th>
            <th class="font-weight-normal">
              Bedding
            </th>
            <th class="font-weight-normal">
              Colour
            </th>
            <th class="font-weight-normal">
              Hardness
            </th>
            <th class="font-weight-normal">
              Moisture
            </th>
            <th class="font-weight-normal">
              Water Bearing Flow
            </th>
            <th class="font-weight-normal">
              Observations
            </th>
            <th>
            </th>
          </tr>
        </thead>
        <tbody>
          <template v-for="(row, index) in lithology.length">
            <tr  :key="`lithology row ${index}`" :id="`lithologyRow${index}`">
              <td class="input-width-small">
                <b-input aria-label="Depth from (feet)" v-model="lithology[index].from"/>
              </td>
              <td class="input-width-small">
                <b-input aria-label="Depth to (feet)" v-model="lithology[index].to"/>
              </td>
              <td>
                <b-select aria-label="Primary surficial material" :options="['Gravel', 'Sand', 'Silt', 'Clay']" v-model="lithology[index].primary"></b-select>
              </td>
              <td>
                <b-select aria-label="Secondary surficial material" :options="['Gravel', 'Sand', 'Silt', 'Clay']" v-model="lithology[index].secondary"></b-select>
              </td>
              <td>
                <b-select aria-label="Bedrock" :options="['Granite', 'Sandstone', 'Gneiss', 'Granodiorite']" v-model="lithology[index].bedrock"></b-select>
              </td>
              <td>
                <b-select aria-label="Descriptor" :options="['Weathered', 'Competent']" v-model="lithology[index].descriptor"></b-select>
              </td>
              <td>
                <b-select aria-label="Bedding" :options="['Thinly bedded']" v-model="lithology[index].bedding"></b-select>
              </td>
              <td>
                <b-select aria-label="Colour" :options="['Grey', 'Brown']" v-model="lithology[index].colour"></b-select>
              </td>
              <td>
                <b-select aria-label="Hardness" :options="['Hard', 'Soft']" v-model="lithology[index].hardness"></b-select>
              </td>
              <td>
                <b-select aria-label="Moisture" :options="['Dry', 'Damp', 'Moist', 'Wet']" v-model="lithology[index].moisture"></b-select>
              </td>
              <td class="input-width-medium">
                <b-input aria-label="Water bearing flow" v-model="lithology[index].water_bearing_flow"></b-input>
              </td>
              <td class="input-width-medium">
                <b-input aria-label="Observations" v-model="lithology[index].observations"></b-input>
              </td>
              <td class="align-middle">
                <b-btn size="sm" variant="primary" @click="removeRowIfOk(index)" :id="`removeRowButton${index}`"><i class="fa fa-minus-square-o"></i> Remove</b-btn>
              </td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>
    <b-btn size="sm" variant="primary" @click="addLithologyRow" id="addLithologyRowButton"><i class="fa fa-plus-square-o"></i> Add row</b-btn>
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
  name: 'Lithology',
  mixins: [inputBindingsMixin],
  props: {
    lithology: {
      type: Array,
      default: () => ([])
    },
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
  computed: {
    ...mapGetters(['codes'])
  },
  methods: {
    addLithologyRow () {
      this.lithologyInput.push({})
    },
    removeRowByIndex (index) {
      this.lithologyInput.splice(index, 1)
      this.rowIndexToRemove = null
    },
    removeRowIfOk (rowNumber) {
      if (this.rowHasValues(this.lithologyInput[rowNumber])) {
        this.rowIndexToRemove = rowNumber
        this.confirmRemoveModal = true
      } else {
        this.removeRowByIndex(rowNumber)
      }
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
  created () {
    // When component created, add an initial row of lithology.
    if (!this.lithologyInput.length) {
      this.lithologyInput.push({}, {}, {})
    }
  }
}
</script>

<style lang="scss">

</style>
