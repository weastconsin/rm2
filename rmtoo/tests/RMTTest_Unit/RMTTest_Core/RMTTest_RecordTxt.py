'''
 rmtoo
   Free and Open Source Requirements Management Tool

 Record Text Test Class

 (c) 2010-2011,2017 by flonatel GmbH & Co. KG

 For licensing details see COPYING
'''
import StringIO
import unittest

from rmtoo.lib.storagebackend.txtfile.TxtRecord import TxtRecord
from rmtoo.lib.storagebackend.txtfile.TxtIOConfig import TxtIOConfig
from rmtoo.lib.storagebackend.RecordEntry import RecordEntry


dp1 = """# Comment for whole record

# ... with empty lines.
"""

dp2 = """Name: meiner
# Comment for Name
"""

dp3 = """Rationale: It's because.
 And another reason.
 And maybe a third one.
# Comment for Rationale 1
# Comment for Rationale 2
"""

dp4 = """Note: This is my Note.
# Comment for Note 1 (before empty line)

# Comment for Note 2 (after empty line)
"""

dpA = """Hinzu: This is quite new.
"""

doc1 = dp1 + dp2 + dp3 + dp4
doc2 = dp1 + dp2 + dp3 + dpA + dp4
doc3 = dp1 + dp2 + dp3
doc4 = dp1 + dp2 + dp3 + dp4 + dpA

dpC1 = """ Comment for whole record

 ... with empty lines.
"""


class RMTTest_RecordTxt(unittest.TestCase):

    def rmttest_pos_01(self):
        "Check top level RecordAsDict (string)"

        txt_doc = TxtRecord.from_string(doc1, "Nothing", TxtIOConfig())
        txt_doc_dict = txt_doc.get_dict()

        self.assertEqual(dpC1, txt_doc.get_comment())
        self.assertEqual("meiner", txt_doc_dict["Name"].get_content())
        self.assertEqual("This is my Note.",
                         txt_doc_dict["Note"].get_content())
        self.assertEqual(doc1, txt_doc.to_string())

    def rmttest_pos_02(self):
        "Check top level RecordAsDict (fd)"

        fd = StringIO.StringIO(doc1)
        txt_doc = TxtRecord.from_fd(fd, "Nothing", TxtIOConfig())
        txt_doc_dict = txt_doc.get_dict()

        self.assertEqual(dpC1, txt_doc.get_comment())
        self.assertEqual("meiner", txt_doc_dict["Name"].get_content())
        self.assertEqual("This is my Note.",
                         txt_doc_dict["Note"].get_content())
        self.assertEqual(doc1, txt_doc.to_string())

    def rmttest_pos_03(self):
        "Check top level Record: insert entry"

        txt_doc = TxtRecord.from_string(doc1, "Nothing", TxtIOConfig())
        txt_doc.insert(2, RecordEntry("Hinzu", "This is quite new."))
        txt_doc_dict = txt_doc.get_dict()

        self.assertEqual(dpC1, txt_doc.get_comment())
        self.assertEqual("meiner", txt_doc_dict["Name"].get_content())
        self.assertEqual("This is my Note.",
                         txt_doc_dict["Note"].get_content())
        self.assertEqual(doc2, txt_doc.to_string())

    def rmttest_pos_04(self):
        "Check top level Record: append entry"

        txt_doc = TxtRecord.from_string(doc1, "Nothing", TxtIOConfig())
        txt_doc.append(RecordEntry("Hinzu", "This is quite new."))
        txt_doc_dict = txt_doc.get_dict()

        self.assertEqual(dpC1, txt_doc.get_comment())
        self.assertEqual("meiner", txt_doc_dict["Name"].get_content())
        self.assertEqual("This is my Note.",
                         txt_doc_dict["Note"].get_content())
        self.assertEqual(doc4, txt_doc.to_string())

    def rmttest_pos_05(self):
        "Check top level Record: remove entry"

        txt_doc = TxtRecord.from_string(doc1, "Nothing", TxtIOConfig())
        del(txt_doc[2])
        txt_doc_dict = txt_doc.get_dict()

        self.assertEqual(dpC1, txt_doc.get_comment())
        self.assertEqual("meiner", txt_doc_dict["Name"].get_content())
        # 'Note' is not available - it was deleted.
        try:
            txt_doc_dict["Note"].get_content()
            self.assertTrue(False)
        except KeyError:
            pass
        self.assertEqual(doc3, txt_doc.to_string())

    def rmttest_pos_06(self):
        "Check top level Record: is_tag_available"

        txt_doc = TxtRecord.from_string(doc1, "Nothing", TxtIOConfig())
        txt_doc.insert(2, RecordEntry("Hinzu", "This is quite new."))

        self.assertTrue(txt_doc.is_tag_available("Hinzu"))
        self.assertFalse(txt_doc.is_tag_available("NichtDa"))
