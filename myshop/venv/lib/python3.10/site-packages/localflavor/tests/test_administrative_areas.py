from ..administrative_areas import ADMINISTRATIVE_AREAS
from unittest import TestCase


class AdministrativeAreasTest(TestCase):
    def test_administrative_areas(self):
        self.assertEqual(len([code for code in ADMINISTRATIVE_AREAS]), 31)

        self.assertEqual(len([code for code, _ in ADMINISTRATIVE_AREAS.items()
                              if _['used_in_address']]), 8)

        self.assertEqual(len([code for code, _ in ADMINISTRATIVE_AREAS.items()
                              if not _['used_in_address']]), 23)
