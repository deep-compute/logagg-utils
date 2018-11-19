import time
import json

import requests
from deeputil import keeprunning

from . import utils

class NSQSender(object):
    NSQ_MAX_DEPTH = 1000000 # Depth after which nsq_sender won't send msgs and wait to clear
    NSQ_READY_CHECK_INTERVAL = 1 # Wait time to check nsq readiness (alive and not full)
    MPUB_URL = 'http://{nsqd_http_address}/mpub?topic={topic_name}' # Url to post msgs to NSQ


    def __init__(self,
            nsqd_http_address,
            nsq_topic,
            log=utils.DUMMY):
        self.nsqd_http_address = nsqd_http_address
        self.topic_name = nsq_topic
        self.log = log

        self._ensure_topic(self.topic_name)


    @keeprunning(NSQ_READY_CHECK_INTERVAL,
                 exit_on_success=True,
                 on_error=utils.log_exception)
    def _ensure_topic(self, topic_name):
        '''
        Check connection to NSQ via topic creation
        '''
        u = 'http://{}/topic/create?topic={}'.format(self.nsqd_http_address, topic_name)
        try:
            requests.post(u, timeout=1)
        except requests.exceptions.RequestException as e:
            self.log.exception('could_not_create_topic__will_try_again', topic=topic_name)
            raise
        self.log.info('created_topic', topic=topic_name)


    @keeprunning(NSQ_READY_CHECK_INTERVAL,
                 exit_on_success=True,
                 on_error=utils.log_exception)
    def _is_ready(self, topic_name):
        '''
        Is NSQ running and have space to receive messages
        '''
        url = 'http://{}/stats?format=json&topic={}'.format(self.nsqd_http_address, topic_name)
        # Cheacking for ephmeral channels
        if '#' in topic_name: topic_name, tag =topic_name.split("#", 1)

        try:
            data = requests.get(url).json()
            '''
            data = {u'start_time': 1516164866, u'version': u'1.0.0-compat', \
                    u'health': u'OK', u'topics': [{u'message_count': 19019, \
                    u'paused': False, u'topic_name': u'test_topic', u'channels': [], \
                    u'depth': 19019, u'backend_depth': 9019, u'e2e_processing_latency': {u'count': 0, \
                    u'percentiles': None}}]}
            '''
            topics = data.get('topics', [])
            topics = [t for t in topics if t['topic_name'] == topic_name]
            if not topics: raise Exception('topic_missing_at_nsq')
            topic = topics[0]
            depth = topic['depth']
            depth += sum(c.get('depth', 0) for c in topic['channels'])
            self.log.debug('nsq_depth_check', topic=topic_name,
                            depth=depth, max_depth=self.NSQ_MAX_DEPTH)

            if depth < self.NSQ_MAX_DEPTH: return
            else: raise Exception('nsq_is_full_waiting_to_clear')

        except: raise


    @keeprunning(NSQ_READY_CHECK_INTERVAL,
                 exit_on_success=True,
                 on_error=utils.log_exception)
    def _send_message(self, msgs, topic_name):
        '''
        Send message to NSQ
        '''
        url = self.MPUB_URL.format(nsqd_http_address=self.nsqd_http_address,
                                    topic_name=topic_name)
        try:
            requests.post(url, data=msgs, timeout=5)
        except (SystemExit, KeyboardInterrupt): raise
        except requests.exceptions.RequestException as e:
            raise
        self.log.debug('NSQ_push_done', nbytes=len(msgs))


    def handle_logs(self, msgs):
        '''
        Prepare message from a list of logs & send to NSQ
        '''
        self._is_ready(topic_name=self.topic_name)
        msgs = '\n'.join(m['log'] for m in msgs)
        self._send_message(msgs, topic_name=self.topic_name)


    def handle_heartbeat(self, heartbeat):
        '''
        Send message to ephmeral topic
        '''
        msg = json.dumps(heartbeat)
        msg = msg + '\n'
        self._is_ready(topic_name=self.topic_name)
        self._send_message(msg, topic_name=self.topic_name)
