# NEON AI (TM) SOFTWARE, Software Development Kit & Application Development System
#
# Copyright 2008-2021 Neongecko.com Inc. | All Rights Reserved
#
# Notice of License - Duplicating this Notice of License near the start of any file containing
# a derivative of this software is a condition of license for this software.
# Friendly Licensing:
# No charge, open source royalty free use of the Neon AI software source and object is offered for
# educational users, noncommercial enthusiasts, Public Benefit Corporations (and LLCs) and
# Social Purpose Corporations (and LLCs). Developers can contact developers@neon.ai
# For commercial licensing, distribution of derivative works or redistribution please contact licenses@neon.ai
# Distributed on an "AS IS” basis without warranties or conditions of any kind, either express or implied.
# Trademarks of Neongecko: Neon AI(TM), Neon Assist (TM), Neon Communicator(TM), Klat(TM)
# Authors: Guy Daniels, Daniel McKnight, Regina Bloomstine, Elon Gasper, Richard Leeds
#
# Specialized conversational reconveyance options from Conversation Processing Intelligence Corp.
# US Patents 2008-2021: US7424516, US20140161250, US20140177813, US8638908, US8068604, US8553852, US10530923, US10530924
# China Patent: CN102017585  -  Europe Patent: EU2156652  -  Patents Pending

import sys
import os
import unittest
from glob import glob

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from neon_utils.configuration_utils import *

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
CONFIG_PATH = os.path.join(ROOT_DIR, "configuration")

TEST_DICT = {"section 1": {"key1": "val1",
                           "key2": "val2"},
             "section 2": {"key_1": "val1",
                           "key_2": "val2"}}


class ConfigurationUtilTests(unittest.TestCase):
    def doCleanups(self) -> None:
        for file in glob(os.path.join(CONFIG_PATH, "*.lock")):
            os.remove(file)
        for file in glob(os.path.join(CONFIG_PATH, "*.tmp")):
            os.remove(file)
        if os.path.exists(os.path.join(CONFIG_PATH, "old_user_info.yml")):
            os.remove(os.path.join(CONFIG_PATH, "old_user_info.yml"))

    def test_load_config(self):
        local_conf = NGIConfig("ngi_local_conf", CONFIG_PATH)
        self.assertIsInstance(local_conf.content, dict)
        self.assertIsInstance(local_conf.content["devVars"], dict)
        self.assertIsInstance(local_conf.content["prefFlags"]["devMode"], bool)

    def test_make_equal_keys(self):
        old_user_info = os.path.join(CONFIG_PATH, "old_user_info.yml")
        ngi_user_info = os.path.join(CONFIG_PATH, "ngi_user_info.yml")
        shutil.copy(ngi_user_info, old_user_info)
        user_conf = NGIConfig("ngi_user_info", CONFIG_PATH)
        self.assertEqual(user_conf.content["user"]["full_name"], 'Test User')
        self.assertNotIn("phone_verified", user_conf.content["user"])
        self.assertIn('bad_key', user_conf.content["user"])

        user_conf.make_equal_by_keys(NGIConfig("clean_user_info", CONFIG_PATH).content)
        self.assertIn("phone_verified", user_conf.content["user"])
        self.assertNotIn('bad_key', user_conf.content["user"])
        self.assertFalse(user_conf.content["user"]["phone_verified"])
        self.assertEqual(user_conf.content["user"]["full_name"], 'Test User')

        new_user_info = NGIConfig("ngi_user_info", CONFIG_PATH)
        self.assertEqual(user_conf.content, new_user_info.content)
        shutil.copy(old_user_info, ngi_user_info)

    def test_update_keys(self):
        old_user_info = os.path.join(CONFIG_PATH, "old_user_info.yml")
        ngi_user_info = os.path.join(CONFIG_PATH, "ngi_user_info.yml")
        shutil.copy(ngi_user_info, old_user_info)
        user_conf = NGIConfig("ngi_user_info", CONFIG_PATH)
        self.assertEqual(user_conf.content["user"]["full_name"], 'Test User')
        self.assertNotIn("phone_verified", user_conf.content["user"])
        self.assertIn('bad_key', user_conf.content["user"])

        user_conf.update_keys(NGIConfig("clean_user_info", CONFIG_PATH).content)
        self.assertIn("phone_verified", user_conf.content["user"])
        self.assertIn('bad_key', user_conf.content["user"])
        self.assertFalse(user_conf.content["user"]["phone_verified"])
        self.assertEqual(user_conf.content["user"]["full_name"], 'Test User')

        new_user_info = NGIConfig("ngi_user_info", CONFIG_PATH)
        self.assertEqual(user_conf.content, new_user_info.content)
        shutil.copy(old_user_info, ngi_user_info)

    def test_update_key(self):
        old_user_info = os.path.join(CONFIG_PATH, "old_user_info.yml")
        ngi_user_info = os.path.join(CONFIG_PATH, "ngi_user_info.yml")
        shutil.copy(ngi_user_info, old_user_info)
        user_conf = NGIConfig("ngi_user_info", CONFIG_PATH)

        self.assertEqual(user_conf.content["user"]["full_name"], 'Test User')
        user_conf.update_yaml_file("user", "full_name", "New Name", multiple=False, final=True)
        self.assertEqual(user_conf.content["user"]["full_name"], 'New Name')
        new_user_conf = NGIConfig("ngi_user_info", CONFIG_PATH)
        self.assertEqual(user_conf.content["user"]["full_name"], new_user_conf.content["user"]["full_name"])
        shutil.copy(old_user_info, ngi_user_info)

    def test_export_json(self):
        user_conf = NGIConfig("ngi_user_info", CONFIG_PATH)
        json_file = user_conf.export_to_json()
        with open(json_file, "r") as f:
            from_disk = json.load(f)
        self.assertEqual(from_disk, user_conf.content)
        os.remove(json_file)

    def test_import_dict(self):
        test_conf = NGIConfig("test_conf", CONFIG_PATH).from_dict(TEST_DICT)
        self.assertEqual(test_conf.content, TEST_DICT)
        from_disk = NGIConfig("test_conf", CONFIG_PATH)
        self.assertEqual(from_disk.content, test_conf.content)
        os.remove(test_conf.file_path)

    def test_import_json(self):
        json_path = os.path.join(CONFIG_PATH, "mycroft.conf")
        test_conf = NGIConfig("mycroft", CONFIG_PATH).from_json(json_path)
        parsed_json = load_commented_json(json_path)
        self.assertEqual(parsed_json, test_conf.content)
        from_disk = NGIConfig("mycroft", CONFIG_PATH)
        self.assertEqual(from_disk.content, test_conf.content)
        os.remove(test_conf.file_path)

    def test_delete_recursive_dictionary_keys_simple(self):
        test_dict = deepcopy(TEST_DICT)
        test_dict = delete_recursive_dictionary_keys(test_dict, ["key_1", "key1"])
        self.assertEqual(test_dict, {"section 1": {"key2": "val2"},
                                     "section 2": {"key_2": "val2"}})

    def test_delete_recursive_dictionary_keys_section(self):
        test_dict = deepcopy(TEST_DICT)
        test_dict = delete_recursive_dictionary_keys(test_dict, ["section 1"])
        self.assertEqual(test_dict, {"section 2": {"key_1": "val1",
                                                   "key_2": "val2"}})

    def test_dict_merge(self):
        to_update = deepcopy(TEST_DICT)
        new_keys = {"section 2": {"key_2": "new2",
                                  "key_3": "val3"}}
        updated = dict_merge(to_update, new_keys)
        self.assertEqual(updated["section 2"], {"key_1": "val1",
                                                "key_2": "new2",
                                                "key_3": "val3"})

    def test_dict_make_equal_keys(self):
        to_update = deepcopy(TEST_DICT)
        new_keys = {"section 2": {"key_2": "new2",
                                  "key_3": "val3"}}
        updated = dict_make_equal_keys(to_update, new_keys)
        self.assertEqual(updated, {"section 2": {"key_2": "val2",
                                                 "key_3": "val3"}
                                   })

    def test_dict_update_keys(self):
        to_update = deepcopy(TEST_DICT)
        new_keys = {"section 2": {"key_2": "new2",
                                  "key_3": "val3"}}
        updated = dict_update_keys(to_update, new_keys)
        self.assertEqual(updated["section 2"], {"key_1": "val1",
                                                "key_2": "val2",
                                                "key_3": "val3"})

    def test_write_json(self):
        file_path = os.path.join(CONFIG_PATH, "test.json")
        write_to_json(TEST_DICT, file_path)
        with open(file_path, "r") as f:
            from_disk = json.load(f)
        self.assertEqual(from_disk, TEST_DICT)
        os.remove(file_path)


if __name__ == '__main__':
    unittest.main()
