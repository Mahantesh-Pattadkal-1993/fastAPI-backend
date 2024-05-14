"""
The purpose of this file is to test the logging framework

"""



from logging_module import init
import logging

# Initialise the logging framework cofiguration
init("test",level=logging.DEBUG)

# Set up the logger
logger = logging.getLogger(__name__)

# Debug message for testing
logger.debug("hello first error")