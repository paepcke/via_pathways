import os
import json
import logging
import re

from ..constants import PROJ_ROOT

class ParamsOperation:
    """
    Superclass for all classes that use params.json files.
    """
    def __init__(self, params_dir, proj_root=None):
        
        params_dir = self.resolve_path(params_dir, proj_root)
        
        # Resolve env vars:
        params_path = os.path.join(os.path.realpath(params_dir), "params.json")

        with open(params_path) as f:
            params = json.load(f)
            
            # Resolve files and directories in the param set.
            # This is a bad hack! Breaks if we add new file/dir
            # entries in params.json specs: 
            pathways_path = params.get('pathways_path', None)
            if pathways_path is not None:
                params['pathways_path'] = self.resolve_path(pathways_path)
            dataset_dir  = params.get('dataset_dir', None)
            if dataset_dir is not None:
                params['dataset_dir'] = self.resolve_path(dataset_dir)
                
            self.__dict__.update(params)
            print(params)
        self.dir = params_dir

        set_logger(
            os.path.join(params_dir, "process.log"),
            level=logging.INFO, console=True
        )
        log_title(type(self))

    def run(self):
        raise NotImplementedError

    @staticmethod
    def resolve_path(the_path, dir_root=None):
        '''
        Given a directory or file path, and an optional origin path.
        Resolve tilde and environment variables. If the_path
        is absolute, it is then returned. Else, if dir_root is provided,
        the return path will be relative to that root. Without
        a dir_root a relative the_path is resolved relative to
        the project root, which is available from run.py
        
        @param the_path: directory or file path to resolve
        @type the_path: string
        @param dir_root: optional diretory root relative to which 
            relative params_dir values are resolved
        @type dir_root: str
        @return resolved file or directory path
        @rtype: str
        '''
        the_path = os.path.expanduser(os.path.expandvars(the_path))
        if not os.path.isabs(the_path):
            if dir_root is not None:
                # Path relative to project root
                # Resolve env vars, and ~ home directory indicators:
                dir_root = os.path.expandvars(os.path.expanduser(dir_root))
                the_path = os.path.realpath(os.path.join(dir_root, the_path))
            else:
                # Relative with without a given directory root.
                # Use project root:
                the_path = os.path.normpath(os.path.join(PROJ_ROOT, the_path))
        else:
            # Path the_path is absolute:
            the_path = os.path.expandvars(os.path.expanduser(the_path))
        
        return the_path


def set_logger(log_path, level=logging.INFO, console=True):
    """Sets the logger to log info in terminal and file `log_path`.

    In general, it is useful to have a logger so that every output to the terminal is saved
    in a permanent file. Here we save it to `experiment_dir/process.log`.

    Example:
    ```
    logging.info("Starting training...")
    ```

    Args:
        log_path: (string) where to log
    """
    logger = logging.getLogger()
    logger.setLevel(level)

    if not logger.handlers:
        # Logging to a file
        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s:%(levelname)s: %(message)s'))
        logger.addHandler(file_handler)

        # Logging to console
        if console:
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(logging.Formatter('%(message)s'))
            logger.addHandler(stream_handler)


def log_title(title):
    """
    """
    logging.info("{}".format(title))
    logging.info("Geoffrey Angus and Richard Diehl")
    logging.info("Carta – Stanford University – 2018")
    logging.info("---------------------------------")


def enrich_projection_txt(projection_dir):
    """
    Utility function purely to prep projections for Cytoscape visualizations.
    """
    newlines = []
    projection_dir = ParamsOperation.resolve_path(projection_dir)
    with open(os.path.join(projection_dir, 'projection.txt'), "r") as f:
        header = f.readline()
        for line in f:
            attrs = line.split('\t')
            idx = re.search("\d", attrs[0]).start()
            newsrc = attrs[0][:idx]
            idx = re.search("\d", attrs[1]).start()
            newdst = attrs[1][:idx]
            is_internal = 'internal' if newsrc == newdst else 'external'
            newlines.append(
                '\t'.join(
                    [is_internal, newsrc, attrs[0], newdst, attrs[1], attrs[2]]
                )
            )
    with open(os.path.join(projection_dir, 'projection_enriched.txt'), 'w') as f:
        f.write('\t'.join(
            ['is_internal', 'department', 'prereq', 'department', 'course', 'weight']
        ))
        f.write('\n')
        for newline in newlines:
            f.write(newline)


def get_prefix(course_id):
    return course_id[:re.search("\d", course_id).start()]

    
