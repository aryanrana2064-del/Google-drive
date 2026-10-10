"""Automatic copy of finished backups into a cloud-synced folder (Google Drive / OneDrive / Dropbox)."""
import os
from pathlib import Path

from tests.helpers import ServiceTestCase


class TestCloudBackup(ServiceTestCase):
    def setUp(self):
        super().setUp()
        self.mgr = self.svc.backups
        self.cloud = Path(self.tmp.name) / "GoogleDrive" / "VX7 Backup"

    def test_off_by_default(self):
        st = self.mgr.cloud_status()
        self.assertFalse(st.configured)
        self.svc.auto_backup_if_due(force=True)
        self.assertFalse(self.cloud.exists())

    def test_backup_is_copied_to_cloud_folder(self):
        self.cloud.parent.mkdir()
        self.mgr.set_cloud_folder(str(self.cloud))
        path = self.svc.auto_backup_if_due(force=True)
        self.assertTrue((self.cloud / path.name).is_file())
        st = self.mgr.cloud_status()
        self.assertTrue(st.available)
        self.assertEqual((st.pending, st.error), (0, ""))
        self.assertIsNotNone(st.last_success)
        self.assertFalse(list(self.cloud.glob("*.part")))

    def test_offline_then_retry(self):
        self.mgr.set_cloud_folder(str(self.cloud))            # parent folder (the drive) does not exist yet
        path = self.svc.auto_backup_if_due(force=True)        # local backup still succeeds
        self.assertTrue(path.is_file())
        st = self.mgr.cloud_status()
        self.assertFalse(st.available)
        self.assertEqual(st.pending, 1)
        self.assertIn("cloud folder", st.error.lower())
        self.cloud.parent.mkdir()                             # Google Drive starts / comes online
        self.assertEqual(self.mgr.sync_cloud(), 1)
        self.assertTrue((self.cloud / path.name).is_file())
        self.assertEqual(self.mgr.cloud_status().pending, 0)
        self.assertEqual(self.mgr.cloud_status().error, "")

    def test_timer_retries_when_nothing_is_due(self):
        self.svc.auto_backup_if_due(force=True)               # a local backup exists and is not due again
        self.cloud.parent.mkdir()
        self.mgr.set_cloud_folder(str(self.cloud))
        self.assertIsNone(self.svc.auto_backup_if_due())      # not due, but the missing cloud copy is made
        self.assertEqual(len(list(self.cloud.glob("SJB_KHATA_BACKUP_*.db"))), 1)

    def test_turning_it_off_and_old_files_are_kept(self):
        self.cloud.parent.mkdir()
        self.mgr.set_cloud_folder(str(self.cloud))
        path = self.svc.auto_backup_if_due(force=True)
        self.mgr.set_cloud_folder(None)
        self.assertFalse(self.mgr.cloud_status().configured)
        self.assertTrue((self.cloud / path.name).is_file())   # nothing is deleted from the cloud folder
