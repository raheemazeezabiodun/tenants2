import datetime
from freezegun import freeze_time

from users.tests.factories import UserFactory
from .factories import HPActionDocumentsFactory, UploadTokenFactory
from ..models import (
    HPActionDocuments, UploadToken, UPLOAD_TOKEN_LIFETIME,
    get_upload_status_for_user, HPUploadStatus)


class TestUploadToken:
    def test_they_are_time_limited_and_expired_ones_can_be_removed(self, db):
        with freeze_time('2018-01-01') as time:
            token = UploadTokenFactory()
            UploadToken.objects.remove_expired()
            assert UploadToken.objects.find_unexpired(token.id) == token
            assert token.is_expired() is False

            time.tick(delta=datetime.timedelta(seconds=1) + UPLOAD_TOKEN_LIFETIME)
            assert UploadToken.objects.find_unexpired(token.id) is None
            assert token.is_expired() is True

            UploadToken.objects.remove_expired()
            assert UploadToken.objects.count() == 0

    def test_create_documents_from_works(self, db, django_file_storage):
        token = UploadTokenFactory()
        user = token.user
        token_id = token.id
        docs = token.create_documents_from(
            xml_data=b'i am xml',
            pdf_data=b'i am pdf'
        )
        assert django_file_storage.read(docs.xml_file) == b'i am xml'
        assert django_file_storage.read(docs.pdf_file) == b'i am pdf'
        assert docs.user == user
        assert docs.id == token_id

        # Make sure the token was deleted.
        assert token.id is None

    def test_get_upload_url_works(self, db):
        token = UploadToken(id='boop')
        assert token.get_upload_url() == 'https://example.com/hp/upload/boop'


class TestHPActionDocuments:
    def create_docs(self, django_file_storage):
        docs = HPActionDocumentsFactory()
        xml_filepath = django_file_storage.get_abs_path(docs.xml_file)
        pdf_filepath = django_file_storage.get_abs_path(docs.pdf_file)
        return (docs, xml_filepath, pdf_filepath)

    def test_purging_works(self, db, django_file_storage):
        docs, xml_filepath, pdf_filepath = self.create_docs(django_file_storage)
        HPActionDocuments.objects.purge()
        assert HPActionDocuments.objects.count() == 1
        assert xml_filepath.exists()
        assert pdf_filepath.exists()

        docs.schedule_for_deletion()
        HPActionDocuments.objects.purge()
        assert HPActionDocuments.objects.count() == 0
        assert not xml_filepath.exists()
        assert not pdf_filepath.exists()

    def test_purging_works_on_partially_deleted_docs(self, db, django_file_storage):
        docs, xml_filepath, pdf_filepath = self.create_docs(django_file_storage)

        # Suppose we tried purging the docs before and deleting the XML file
        # worked, but deleting the PDF failed...
        docs.schedule_for_deletion()
        docs.xml_file.delete()
        assert not xml_filepath.exists()
        assert pdf_filepath.exists()

        # We should be able to purge again and complete the process.
        HPActionDocuments.objects.purge()
        assert not xml_filepath.exists()
        assert not pdf_filepath.exists()

    def test_get_latest_for_user_works(self, db, django_file_storage):
        user = UserFactory()

        docs = HPActionDocuments.objects.get_latest_for_user(user)
        assert docs is None

        with freeze_time('2018-01-01'):
            HPActionDocumentsFactory(user=user, id='older')

        docs = HPActionDocuments.objects.get_latest_for_user(user)
        assert docs and docs.id == 'older'

        with freeze_time('2019-01-01'):
            HPActionDocumentsFactory(user=user, id='newer')

        docs = HPActionDocuments.objects.get_latest_for_user(user)
        assert docs and docs.id == 'newer'


class TestGetUploadStatusForUser:
    def test_it_returns_not_started(self, db):
        assert get_upload_status_for_user(UserFactory()) == HPUploadStatus.NOT_STARTED

    def test_it_returns_started(self, db):
        token = UploadTokenFactory()
        assert get_upload_status_for_user(token.user) == HPUploadStatus.STARTED

    def test_it_returns_errored_when_token_has_errored_set(self, db):
        token = UploadTokenFactory()
        token.errored = True
        token.save()
        assert get_upload_status_for_user(token.user) == HPUploadStatus.ERRORED

    def test_it_returns_errored_when_token_is_expired(self, db):
        with freeze_time('2018-01-01') as time:
            token = UploadTokenFactory()
            time.tick(delta=datetime.timedelta(days=1))
            assert get_upload_status_for_user(token.user) == HPUploadStatus.ERRORED

    def test_it_returns_succeeded(self, db, django_file_storage):
        docs = HPActionDocumentsFactory()
        assert get_upload_status_for_user(docs.user) == HPUploadStatus.SUCCEEDED

    def test_it_ignores_old_docs(self, db, django_file_storage):
        with freeze_time('2018-01-01') as time:
            docs = HPActionDocumentsFactory()
            time.tick(delta=datetime.timedelta(days=1))
            token = UploadTokenFactory(user=docs.user)
            assert get_upload_status_for_user(token.user) == HPUploadStatus.STARTED

    def test_it_ignores_old_tokens(self, db, django_file_storage):
        with freeze_time('2018-01-01') as time:
            token = UploadTokenFactory()
            time.tick(delta=datetime.timedelta(days=1))
            HPActionDocumentsFactory(user=token.user)
            assert get_upload_status_for_user(token.user) == HPUploadStatus.SUCCEEDED