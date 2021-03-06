"""
# @file data_source.py
# @Synopsis  classes of data source, which would be fetched from outside
# datasources and cached in local disk, for the usage of calculation.
# @author Ming Gu(guming@itv.baidu.com))
# @version 1.0
# @date 2016-07-04
"""
import os
import ConfigParser
import logging
from conf.env_config import EnvConfig
from bll.data.table_file import TableFile
from dal.mysql_conn import MySQLConn
from dal.get_instance_by_service import getInstanceByService

class CachedMySQLTable(TableFile):
    """
    # @Synopsis  subclass of datasource, defining the update method, which is
    # overwrite the local cached data with the data downloaded from mysql
    """

    def __init__(self, field_list, file_path, db_name, table_name,
            condition_str):
        """
        # @Synopsis  init
        #
        # @Args field_list
        # @Args file_path
        # @Args db_name
        # @Args table_name
        # @Args condition_str
        #
        # @Returns   None
        """
        self.field_list = field_list
        self.file_path = file_path
        self.db_name = db_name
        self.table_name = table_name
        self.condition_str = condition_str

    def update(self, source_db_type):
        """
        # @Synopsis  update local cached file, by overwriting it with mysql
        # downloaded file
        #
        # @Returns   succeeded or not
        """
        conn = MySQLConn(self.db_name, source_db_type)
        ret = conn.select(self.table_name, self.field_list, self.condition_str)
        output_obj = open(self.file_path, 'w')
        for line in ret:
            output_fields = map(lambda x: u'{0}'.format(x), line)
            output_fields = map(lambda x: x.replace('\n', ''), output_fields)
            output_line = u'\t'.join(output_fields) + u'\n'
            output_obj.write(output_line.encode('utf8'))
        output_obj.close()
        return True
