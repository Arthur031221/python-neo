from math import floor, ceil

import quantities as pq
from neo.core.regionofinterest import RectangularRegionOfInterest, CircularRegionOfInterest, PolygonRegionOfInterest
from neo.core.imagesequence import ImageSequence
import unittest


class Test_CircularRegionOfInterest(unittest.TestCase):

    def test_result(self):
        seq = ImageSequence([[[]]], spatial_scale=1, frame_duration=20 * pq.ms)
        self.assertEqual(
            (CircularRegionOfInterest(seq, 6, 6, 1).pixels_in_region()), [[6, 5], [5, 6], [6, 6], [7, 6], [6, 7]]
        )
        self.assertEqual(
            (CircularRegionOfInterest(seq, 6, 6, 1.01).pixels_in_region()), [[6, 5], [5, 6], [6, 6], [7, 6], [6, 7]]
        )

    def test_pixels_in_region_agrees_with_is_inside(self):
        # pixels_in_region is a bounded search for the pixels is_inside accepts,
        # so any pixel is_inside accepts has to come back in the list.
        seq = ImageSequence([[[]]], spatial_scale=1, frame_duration=20 * pq.ms)
        for centre, radius in ((6, 1), (6, 2), (6, 3), (10, 5), (6.5, 2), (6, 2.5), (6.25, 1.75)):
            roi = CircularRegionOfInterest(seq, centre, centre, radius)
            returned = {tuple(p) for p in roi.pixels_in_region()}
            lo = int(floor(centre - radius)) - 2
            hi = int(ceil(centre + radius)) + 2
            expected = {(x, y) for y in range(lo, hi + 1) for x in range(lo, hi + 1) if roi.is_inside(x, y)}
            self.assertEqual(returned, expected, f"centre={centre} radius={radius}")

    def test_pixels_in_region_is_symmetric_about_the_centre(self):
        # A circle is symmetric about its centre, so for an integer centre the
        # set of pixels has to be unchanged by reflection through it.
        seq = ImageSequence([[[]]], spatial_scale=1, frame_duration=20 * pq.ms)
        for radius in (1, 2, 3, 4, 5):
            roi = CircularRegionOfInterest(seq, 10, 10, radius)
            returned = {tuple(p) for p in roi.pixels_in_region()}
            reflected = {(20 - x, 20 - y) for x, y in returned}
            self.assertEqual(returned, reflected, f"radius={radius}")


class Test_RectangularRegionOfInterest(unittest.TestCase):

    def test_result(self):
        seq = ImageSequence([[[]]], spatial_scale=1, frame_duration=20 * pq.ms)
        self.assertEqual(
            RectangularRegionOfInterest(seq, 5, 5, 2, 2).pixels_in_region(), [[4, 4], [5, 4], [4, 5], [5, 5]]
        )


class Test_PolygonRegionOfInterest(unittest.TestCase):

    def test_result(self):
        seq = ImageSequence([[[]]], spatial_scale=1, frame_duration=20 * pq.ms)
        self.assertEqual(
            PolygonRegionOfInterest(seq, (3, 3), (2, 5), (5, 5), (5, 1), (1, 1)).pixels_in_region(),
            [(1, 1), (2, 1), (3, 1), (4, 1), (2, 2), (3, 2), (4, 2), (3, 3), (4, 3), (3, 4), (4, 4)],
        )


if __name__ == "__main__":
    unittest.main()
