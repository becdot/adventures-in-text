from adventure import Object, Openable, Lightable, \
                        Bed, Dresser, Lamp

import unittest

class TestObjects(unittest.TestCase):

    def setUp(self):
        self.dresser = Dresser()
        self.bed = Bed()
        self.lamp = Lamp()

    def tearDown(self):
        pass

    # test bed
    def test_bed_description(self):
        "bed.description returns the description"
        self.bed.description = "A self.bed."
        self.assertEquals(self.bed.description, "A self.bed.")
    def test_bed_look(self):
        "bed.look() returns the item description"
        self.bed.description = "A self.bed."
        self.assertEquals(self.bed.look(), "A self.bed.")
    def test_bed_stand(self):
        "bed.stand() returns the specified message"
        # TODO make this so it is not hard-coded
        self.assertEquals(self.bed.stand(), "Didn't your mother teach you anything?")
    def test_bed_climb_equals_stand(self):
        "bed.climb() returns the same result as bed.stand()"
        self.assertEquals(self.bed.climb(), self.bed.stand())

    # test dresser
    def test_dresser_starts_closed(self):
        "dresser.is_open defaults to false"
        self.assertFalse(self.dresser.is_open)
    def test_dresser_descriptions(self):
        """dresser returns the description + closed_description when dresser.is_open is False
         and description + open_description when dresser.is_open is True"""
        # closed description
        self.assertEquals(str(self.dresser), self.dresser.description + '  ' + self.dresser.closed_description)
        # open description
        self.dresser.is_open = True
        self.assertEquals(str(self.dresser), self.dresser.description + '  ' + self.dresser.open_description)
    def test_dresser_look(self):
        "dresser.look() returns the dresser.description + open/closed description (based on dresser.is_open)"
        self.assertEquals(self.dresser.look(), str(self.dresser))
        self.dresser.is_open = True
        self.assertEquals(self.dresser.look(), str(self.dresser))
    def test_open_dresser(self):
        """Opening a closed dresser sets dresser.is_open to True and returns dresser.open_description
            Opening an already open dresser returns a message"""
        # dresser is closed
        self.assertEquals(self.dresser.open(), self.dresser.open_description)
        self.assertTrue(self.dresser.is_open)
        # dresser is already open
        self.assertEquals(self.dresser.open(), "That object is as open as it can get!")
        self.assertTrue(self.dresser.is_open)
    def test_close_dresser(self):
        """Closing an open dresser sets dresser.is_open to False and returns dresser.closed_description
            Closing an already closed dresser returns a message"""
        # dresser is open
        self.dresser.is_open = True
        self.assertEquals(self.dresser.close(), self.dresser.closed_description)
        self.assertFalse(self.dresser.is_open)
        # dresser is already closed
        self.assertEquals(self.dresser.close(), "That object can't get any more closed.")
        self.assertFalse(self.dresser.is_open)

    # test lamp
    def test_lamp_starts_off(self):
        "lamp.is_lit defaults to false"
        self.assertFalse(self.lamp.is_lit)
    def test_lamp_descriptions(self):
        """lamp returns the description + off_description when lamp.is_lit is False
         and description + on_description when lamp.is_lit is True"""
        # off description
        self.assertEquals(str(self.lamp), self.lamp.description + '  ' + self.lamp.off_description)
        # on description
        self.lamp.is_lit = True
        self.assertEquals(str(self.lamp), self.lamp.description + '  ' + self.lamp.on_description)
    def test_lamp_look(self):
        "lamp.look() returns the lamp.description + on/off description (based on lamp.is_lit)"
        self.assertEquals(self.lamp.look(), str(self.lamp))
        self.lamp.is_lit = True
        self.assertEquals(self.lamp.look(), str(self.lamp))
    def test_light_lamp(self):
        """Lighting a lamp that is off sets lamp.is_lit to True and returns lamp.on_description
            Lighting an already lit lamp returns a message"""
        # lamp is lit
        self.assertEquals(self.lamp.light(), self.lamp.on_description)
        self.assertTrue(self.lamp.is_lit)
        # lamp is already light
        self.assertEquals(self.lamp.light(), "The object is already glowing brightly")
        self.assertTrue(self.lamp.is_lit)
    def test_snuff_lamp(self):
        """Snuffing a lit lamp sets lamp.is_lit to False and returns lamp.off_description
            Snuffing a lamp that is already off returns a message"""
        # lamp is lit
        self.lamp.is_lit = True
        self.assertEquals(self.lamp.snuff(), "The glow fades into blackness.")
        self.assertFalse(self.lamp.is_lit)
        # lamp is off
        self.assertEquals(self.lamp.snuff(), "The object cannot get any darker.")
        self.assertFalse(self.lamp.is_lit)

    # test openable
    def test_openable_synonyms(self):
        "Calling dresser.pull = dresser.open; dresser.shut and dresser.push = dresser.close"
        pull_if_closed = self.dresser.pull()
        self.dresser.is_open = False
        open_if_closed = self.dresser.open()
        self.assertEquals(pull_if_closed, open_if_closed)
        self.dresser.is_open = False
        self.assertEquals(self.dresser.shut(), self.dresser.close())
        self.assertEquals(self.dresser.push(), self.dresser.close())

    # test lightable
    def test_lightable_synonyms(self):
        "Calling lamp.turn_on = lamp.light; lamp.turn_off = lamp.snuff"
        turn_on_if_off = self.lamp.turn_on()
        self.lamp.is_lit = False
        light_if_off = self.lamp.light()
        self.assertEquals(turn_on_if_off, light_if_off)
        self.lamp.is_lit = False
        self.assertEquals(self.lamp.turn_off(), self.lamp.snuff())


if __name__ == "__main__":
    unittest.main()