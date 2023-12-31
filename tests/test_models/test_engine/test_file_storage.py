#!/usr/bin/python3

"""
Unittest for FileStorage class.
"""

import unittest
import os
import json
from models import storage
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class FileStorage_Test(unittest.TestCase):
    """Tests for File Storge class."""

    def setUp(self):
        """Set up"""
        if os.path.exists("file.json"):
            os.remove("file.json")

    def tearDown(self):
        """Tear down"""
        pass

    def test_private_attrs(self):
        """Validate attributes are private."""
        fs = FileStorage()
        self.assertTrue(hasattr(FileStorage, "_FileStorage__file_path"))
        self.assertTrue(hasattr(FileStorage, "_FileStorage__objects"))

    def test_storage_all(self):
        """Tests the all method"""
        fs = FileStorage()
        self.assertEqual(type(fs.all()), dict)

        b1 = BaseModel()
        b2 = BaseModel()
        b3 = BaseModel()
        fs.new(b1)
        fs.new(b2)
        fs.new(b3)
        obj_dict = fs.all()
        self.assertEqual(type(obj_dict), dict)
        self.assertFalse(obj_dict == {})
        self.assertTrue("BaseModel.{}".format(b1.id) in obj_dict)
        self.assertTrue("BaseModel.{}".format(b2.id) in obj_dict)
        self.assertTrue("BaseModel.{}".format(b3.id) in obj_dict)

    def test_no_args(self):
        """test no args"""
        self.assertEqual(type(FileStorage()), FileStorage)

    def test_new(self):
        """Tests the new method"""
        obj = BaseModel()
        storage.new(obj)
        obj_d = storage.all()
        key = obj.__class__.__name__ + '.' + str(obj.id)
        self.assertEqual(obj_d[key] is obj, True)

    def test_save(self):
        """Tests the save method"""
        fs = FileStorage()
        b = BaseModel()
        fs.new(b)
        upd = b.updated_at
        b.save()
        fs.save()
        self.assertTrue(upd != b.updated_at)
        self.assertTrue(os.path.exists("file.json"))

    def test_reload(self):
        """Test the reload method."""
        fs = FileStorage()
        b = BaseModel()
        key = "BaseModel" + '.' + b.id
        fs.new(b)
        fs.save()
        fs.reload()
        self.assertTrue(fs.all()[key])
        fs.all()

    def test_save_reload(self):
        """Tests the save and reload functions"""
        if os.path.isfile('file.json'):
            os.rename("file.json", "file.jsonSAVE")
        m1 = BaseModel()
        m1.save()
        storage.reload()
        ld = storage.all()
        self.assertDictEqual(ld["BaseModel." + m1.id].to_dict(), m1.to_dict())
        os.remove("file.json")
        if os.path.isfile('file.jsonSAVE'):
            os.rename("file.jsonSAVE", "file.json")

    def test_save(self):
        """ Tests save method with base model """
        with self.assertRaises(Exception):
            with open("file.json", "r") as f:
                self.assertEqual(0, len(f.read()))
        my_model = BaseModel()
        my_model.name = "School"
        my_model.my_number = 89
        my_model.save()
        with open("file.json", "r") as f:
            self.assertNotEqual(0, len(f.read()))

    def test_type(self):
        """test type in storage"""
        self.assertEqual(type(storage), FileStorage)


if __name__ == '__main__':
    unittest.main()
