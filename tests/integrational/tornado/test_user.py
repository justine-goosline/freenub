import tornado
from tornado.testing import AsyncTestCase

from pubnub.pubnub_tornado import PubNubTornado, TornadoEnvelope
from pubnub.models.consumer.user import PNGetUsersResult
from pubnub.models.consumer.common import PNStatus
from tests.helper import pnconf_copy
from tests.integrational.vcr_helper import pn_vcr


class TestGetUsers(AsyncTestCase):
    def setUp(self):
        AsyncTestCase.setUp(self)
        config = pnconf_copy()
        self.pn = PubNubTornado(config, custom_ioloop=self.io_loop)

    @pn_vcr.use_cassette('tests/integrational/fixtures/tornado/user/users_get.yaml',
                         filter_query_parameters=['uuid', 'seqn', 'pnsdk'])
    @tornado.testing.gen_test
    def test_single_channel(self):
        envelope = yield self.pn.get_users().include(['externalId', 'profileUrl', 'email',
                                                      'custom', 'created', 'updated', 'eTag']).future()

        assert(isinstance(envelope, TornadoEnvelope))
        assert not envelope.status.is_error()
        assert isinstance(envelope.result, PNGetUsersResult)
        assert isinstance(envelope.status, PNStatus)
        data = envelope.result.data
        assert len(data) == 2
        assert set(['name', 'id', 'externalId', 'profileUrl', 'email',
                    'custom', 'created', 'updated', 'eTag']) == set(data[0])
        assert set(['name', 'id', 'externalId', 'profileUrl', 'email',
                    'custom', 'created', 'updated', 'eTag']) == set(data[1])
        self.pn.stop()
