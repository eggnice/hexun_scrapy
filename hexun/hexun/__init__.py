#! *_* coding: utf-8 *_*

import logging

logging.basicConfig(level=logging.INFO, filename='log.log',
                    filemode='a',
                    format="%(asctime)s[%(levelname)s] -- %(filename)s:%(lineno)d -- %(message)s")
loggers = logging.getLogger(__name__)