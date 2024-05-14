"""
Overview
--------


The logging mechanisms for centralized logging configuration.
It supports logging to both the console and files, and uses a queuing system to
manage log message handling asynchronously, with minimal performance impact on
the main application flow.


Features
--------


- Logs are directed to the console and multiple files based on the log level.
- Asynchronous logging with minimal performance impact.
- Easy configuration of logging settings.


Setting Up Logging
-------------------


Import and Initialization
~~~~~~~~~~~~~~~~~~~~~~~~~


To begin using the logging system, import and initialize it using the ``init`` function:


.. code-block:: python


    from your_logging_module import init


    # Initialize logging with the desired log level
    init(app_name="YourAppName", level=logging.INFO)


Directory Structure
~~~~~~~~~~~~~~~~~~~


Ensure that there is a ``logs/`` directory in your application's root directory to store the log files:


.. code-block:: none


    /
    |-- logs/
    |   |-- app.log
    |   |-- errors.log
    |   |-- debug.log


Log Files and Conditions
~~~~~~~~~~~~~~~~~~~~~~~~


- **app.log**: Stores all logs filtered at the INFO level.
- **errors.log**: Contains logs that are of WARNING or ERROR level.
- **debug.log**: When debugging is enabled, it stores copies of all logs regardless of the level.


Console Output
~~~~~~~~~~~~~~


All logs are also printed to the standard output (stdout), ensuring they are visible in the console during execution.


Configuration Details
---------------------


- **Loggers**: Configures a root logger to handle all logging levels, with logs propagating based on settings.
- **Handlers**: Includes handlers for streaming to stdout, and file handlers for ``app.log``, ``errors.log``, and ``debug.log``.
- **Filters**: A filter is applied to direct INFO level messages to ``app.log``.
- **Formatters**: Utilizes JSON formatters for structured logging, enhancing readability and post-processing.


Example Configuration Usage
---------------------------


Incorporate this logging setup into your application's main module or configuration script. Adjust the logging levels and handlers as needed based on the application's complexity and environment.


Notes
-----


- Ensure that the logging system is initialized early in your application to catch and log all relevant information from the start.
- The logging setup can be customized further based on specific needs such as adding more log files, changing the log format, or adjusting the filter conditions.


This documentation should guide developers in integrating a robust logging system into their applications effectively and efficiently.
"""




from logging.config import ConvertingList
from logging.handlers import QueueHandler, QueueListener
from queue import Queue
import atexit
import logging
from pythonjsonlogger import jsonlogger


class InfoFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.INFO


def _resolve_handlers(l):
    if not isinstance(l, ConvertingList):
        return l
    # Indexing the list performs the evaluation.
    resolved_handlers = []
    for i in range(len(l)):
       
        handler = l[i]
       
        if isinstance(handler, dict) and handler.get('class') == 'logging.StreamHandler':
            # Create the StreamHandler manually
            stream_handler = logging.StreamHandler(stream=handler['stream'])
            stream_handler.setLevel(handler.get('level', logging.NOTSET))
            if 'formatter' in handler:
                stream_handler.setFormatter(handler['formatter'])
            handler = stream_handler
           
        resolved_handlers.append(handler)
       
    return resolved_handlers




class QueueListenerHandler(QueueHandler):
    def __init__(self, handlers, respect_handler_level=True, auto_run=True, queue=Queue(1000)):  
        super().__init__(queue)
        handlers = _resolve_handlers(handlers)
        self._listener = QueueListener(
            self.queue,
            *handlers,
            respect_handler_level=respect_handler_level)
        if auto_run:
            self.start()
            atexit.register(self.stop)


    def start(self):
        self._listener.start()


    def stop(self):
        self._listener.stop()




LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'json': {
          '()' : 'pythonjsonlogger.jsonlogger.JsonFormatter',
          'format': '%(asctime)s %(name)-12s %(levelname)-4s %(message)s',
        },
        'debug_json': {
          '()' : 'pythonjsonlogger.jsonlogger.JsonFormatter',
          'format': '%(asctime)s %(name)-12s %(levelname)-4s %(pathname)s %(lineno)d %(funcName)s %(message)s',
        }
    },
    'filters': {
        'info_filter': {
            '()': InfoFilter,
        }
    },
    'handlers': {
        'stream': {
            'class': 'logging.StreamHandler',
            'formatter': 'debug_json',
            'level': logging.INFO,
            'stream': 'ext://sys.stdout',
        },
        'app_handler': {
            'class': 'logging.FileHandler',
            'level': logging.INFO,
            'filters': ['info_filter'],
            'formatter': 'json',
            'filename': 'logs/app.log',
            'mode': 'a',
        },
        'debug_handler': {
            'class': 'logging.FileHandler',
            'level': logging.DEBUG,
            'formatter': 'debug_json',
            'filename': 'logs/debug.log',
            'mode': 'a',
        },
        'error_handler': {
            'class': 'logging.FileHandler',
            'level': logging.WARNING,
            'formatter': 'debug_json',
            'filename': 'logs/errors.log',
            'mode': 'a',
        },
       
        'queue_handler':{
            '()': QueueListenerHandler,
            'handlers':[
                'cfg://handlers.app_handler',
                'cfg://handlers.error_handler'
            ]
        }  
    },
    'loggers': {
        '': {
            'handlers': ['queue_handler'],
            'level': logging.INFO,
            'propagate': False
        }
    }
}



def init(app_name:str, level, disable_existing_loggers:bool=False, propagate: bool=False, console: bool=True):
    """
    Initializes the logging configuration for a Baxi applications.
    This function sets up the logging level, propagation settings, and specifies whether to disable existing loggers.




    Parameters
    ----------
    app_name : str
        The name of the application for which the logger is being initialized.
       
    level : int
        The logging level (e.g., logging.INFO, logging.DEBUG) to set for the logger.
       
    disable_existing_loggers : bool, optional
        Specifies whether to disable all existing loggers upon initialization, by default False.
       
    propagate : bool, optional
        Determines whether log messages should propagate to higher level loggers, by default False.


    console : bool, optional
        Specifies whether to log messages to console (sys.stdout), by default True.
       
    Returns
    -------
    None


    Notes
    -----
    This function modifies global settings based on the parameters and affects all logging activities within the application.
    """
   
    LOGGING_CONFIG['handlers']['stream']['level'] = level
    LOGGING_CONFIG['loggers']['']['level'] = level
   
    # enable the debug handler only when the logging level id set to DEBUG
    if(level==logging.DEBUG and 'cfg://handlers.debug_handler' not in LOGGING_CONFIG['handlers']['queue_handler']['handlers'] ):
        LOGGING_CONFIG['handlers']['queue_handler']['handlers'].append('cfg://handlers.debug_handler')
       
       
    # enable the debug handler only when the logging level id set to DEBUG
    if(console==True and 'stream' not in LOGGING_CONFIG['loggers']['']['handlers'] ):
        LOGGING_CONFIG['loggers']['']['handlers'].append('stream')
     
   
    LOGGING_CONFIG['loggers']['']['propagate'] = propagate
    LOGGING_CONFIG['disable_existing_loggers'] = disable_existing_loggers
   
   
    #logging.setLoggerClass(AppLogger)
    logging.config.dictConfig(LOGGING_CONFIG)






