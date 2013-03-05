import os
import unittest
import tempfile
import re
import flask

import game_site as site
from adv_db_methods import SECRET_KEY, DATABASE, DEBUG, app,\
    connect_db, init_db, save_game, get_game, delete_game, create_user


class GameSiteTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.app = app.test_client()
        init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def test_first_get(self):
        """The first get request should create a new user.  
        New game should have a location of Bedroom, and an emptry inventory."""
        gotten = self.app.get('/')
        self.assertTrue(re.findall(("<li>New user successfully created</li>"), gotten.data))
        self.assertTrue(re.findall(('<div class="room">'), gotten.data) and re.findall(('<h3>Bedroom</h3>'), gotten.data))
        self.assertTrue(re.findall(("<h4>Inventory</h4>"), gotten.data) and re.findall(("<ul>"), gotten.data)\
                        and re.findall(("<li>Empty</li>"), gotten.data))

    def test_first_session(self):
        "The initial session id should be set to 1"
        with self.app as test:
            gotten = test.get('/')
            self.assertEquals(flask.session['id'], 1)

    def test_post_action(self):
        "Posting an action should cause it to show up in requests"
        with self.app as test:
            test.get('/')
            test.post('/', data=dict(action='get bed'), follow_redirects=True)
            self.assertEquals(flask.request.form['action'], 'get bed')

    def test_posted_action_renders(self):
        "Posting an action should change the rendered template if appropriate"
        with self.app as test:
            test.get('/')
            test.post('/', data=dict(action='west'), follow_redirects=True)
            closet = test.get('/')
            self.assertTrue(re.findall(('<h3>Closet</h3>'), closet.data))

    def test_post_then_get_id(self):
        "Posting an action and then calling a get request should not change the session id"
        with self.app as test:
            test.get('/')
            first = flask.session['id']
            test.post('/', data=dict(action='west'), follow_redirects=True)
            test.get('/')
            second = flask.session['id']
            self.assertEquals(first, second)

    def test_post_then_get_game(self):
        "Posting an action and then calling a get request should return the previous game and not the base game"
        with self.app as test:
            base = test.get('/')
            updated = test.post('/', data=dict(action='west'), follow_redirects=True)
            gotten = test.get('/')
            self.assertNotEqual(base.data, gotten.data)
            self.assertEquals(gotten.data, updated.data)

    def test_new_game_id(self):
        "Creating a new game should increment the session id"
        self.app2 = app.test_client()
        id_1, id_2 = 0, 0
        with self.app as test:
            test.get('/')
            id_1 = flask.session['id']
        with self.app2 as test:
            test.get('/')
            id_2 = flask.session['id']
        self.assertEquals(id_1 + 1, id_2)

    def test_new_game_game(self):
        "Posting an action and then creating a new game should return the base game"
        with self.app as test:
            base = test.get('/')
            updated = test.post('/', data=dict(action='west'), follow_redirects=True)
            newgame = test.get('/newgame', follow_redirects=True)
            self.assertTrue(re.findall(('<h3>Bedroom</h3>'), newgame.data) and re.findall(('<h3>Bedroom</h3>'), base.data))
            self.assertFalse(re.findall(('<h3>Bedroom</h3>'), newgame.data) and re.findall(('<h3>Bedroom</h3>'), updated.data))

    def test_new_game_flashed(self):
        "Creating a new game should flash a success message across the screen"
        with self.app as test:
            test.get('/')
            newgame = test.get('/newgame', follow_redirects=True)
            self.assertTrue(re.findall(('<li>New user successfully created</li>'), newgame.data))


if __name__ == '__main__':
    unittest.main()