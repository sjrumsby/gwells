from django.test import TestCase
#from unittest import mock
from .models import WellOwner, ProvinceState, Well 
from .search import Search

class SearchTestCase(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        #well_owner = mock.Mock(spec=WellOwner)
        #well_owner._state = mock.Mock()

        prov = ProvinceState.objects.create(sort_order=1)
        prov.save()

        owner = WellOwner.objects.create(province_state_id=prov)
        owner.full_name = 'John Smith'
        owner.save()

        owner2 = WellOwner.objects.create(province_state_id=prov)
        owner2.full_name = 'Joe Smith'
        owner2.save()

        w = Well.objects.create(well_owner_id=owner)
        w.identification_plate_number = 123
        w.well_tag_number = 456
        w.street_address = '123 Main St.'
        w.legal_plan = '7789'
        w.save()

        w = Well.objects.create(well_owner_id=owner)
        w.identification_plate_number = 3456332
        w.well_tag_number = 890
        w.street_address = '555 Government Street'
        w.legal_district_lot = '789'
        w.save()

        w = Well.objects.create(well_owner_id=owner2)
        w.identification_plate_number = 55555
        w.well_tag_number = 123
        w.street_address = '200 Main Street'
        w.save()



    def test_well_search_well_number(self):
   	    wells = Search.well_search('123', '', '', '')
   	    self.assertEqual(wells.count(), 2)



    def test_well_search_address(self):
   	    wells = Search.well_search('', 'gov', '', '')
   	    self.assertEqual(wells.count(), 1)



    def test_well_search_legal(self):
   	    wells = Search.well_search('', '', '78', '')
   	    self.assertEqual(wells.count(), 2)



    def test_well_search_owner(self):
   	    wells = Search.well_search('', '', '', 'smi')
   	    self.assertEqual(wells.count(), 3)



    def test_well_search_well_number_owner(self):
   	    wells = Search.well_search('123', '', '', 'john')
   	    self.assertEqual(wells.count(), 3)

