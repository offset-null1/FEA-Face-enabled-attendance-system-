#!/usr/bin/python3

import mysql.connector
from mysql.connector import errorcode

import logging
import sys
import os


fileName = sys.argv[0]

cwd = os.getcwd()

if fileName.startswith("."):
    PATH = cwd + fileName[1:]
elif fileName.startswith("/"):
    PATH = fileName
else:
    PATH = cwd + "/" + fileName

logging.info(f" PATH to executable {PATH}")

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)


logging.basicConfig(
    filename=PATH + "-application.log",
    format="%(asctime)s.%(msecs)-3d:%(filename)s:%(funcName)s:%(levelname)s:%(lineno)d:%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG
)


class MysqlConnector:
    def __init__(self, **kwargs):
        """
        USAGE: Accepts dict -> (user='', password='', host='', ....)
        """

        try:

            self.conn = mysql.connector.connect(**kwargs)
            logging.info(f" Connecting with :{self.conn}")
            self.cursor = self.conn.cursor()
            logging.info(f" Cursor at :{self.cursor}")

        except mysql.connector.Error as err:
            logging.critical(" Connection Failed")
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                logging.critical(" Please check your username or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                logging.critical(" Database doesn't exist")
            elif err.errno == errorcode.ER_BAD_FIELD_ERROR:
                logging.critical(" Invalid field")
            elif err.errno == errorcode.ER_BAD_TABLE_ERROR:
                logging.critical(" Table doesn't exist")
            else:
                logging.critical(err)

    def config(self, **kwargs):
        self.conn.config(**kwargs)
        self.conn.reconnect()
        logging.info(f"Reconnected with :{self.getConnection()}")

    def getConnectionId(self):
        return self.conn.connection_id

    def getConnection(self):
        return self.conn

    def getCursor(self):
        return self.cursor

    def closeConnection(self):
        self.cursor.close()
        self.conn.close()
        logging.info(" Connection closed")

    def commit(self):
        self.conn.commit()
        logging.warning(" Commit")

    @staticmethod
    def addTicks(params=None):
        """
        To add ticks to the user identifiers
        USAGE: Accepts params of list or str type
        RETURN TYPE: str
        """

        logging.info(f" Adding ticks to params :{params} :: Of type:{type(params)}")

        if params:
            try:
                assert type(params) is list or type(params) is str
                if type(params) is list:
                    tickParam = []
                    for i in params:
                        if i.isdigit():
                            tickParam.append(i)
                        else:
                            tickParam.append("`" + i + "`")
                    logging.debug(f" After adding ticks :{tickParam}")

                    return tickParam

                elif type(params) is str:
                    ticks = ""
                    ticks = "`" + params + "`"
                    logging.debug(f" After adding ticks :{ticks}")

                    return ticks

            except AssertionError as err:
                logging.critical(
                    f" Params given should be either list or string, but given type is :{type(params)}"
                )
        else:
            logging.debug(" Empty parameters list")

    @staticmethod
    def getConstraint(column=None):
        """
        Utility function to add the passed key constraint in the query.
        USAGE: Accepts dictionary of the form : {field1 : {dataType:' ',constraint: ' '/[]}, field2: {... , ...}, ...}
        constraint key could be a str (if one constraint) or list of stings (for more than one constraint)
        RETURN TYPE: dict
        """
        if column:          #need to update this, not an ideal way so
            key_constraint_pair = {}
            for col in column.items():
                for j in col:
                    if type(j) is str:
                        key = j
                    elif type(j) is dict:
                        try:
                            constraint = j["constraint"]
                        except KeyError as err:
                            logging.info(f" No Contra for the field :{key} ")
                            logging.info(" Continuing to next field..")
                            key_constraint_pair[key] = "empty"
                            break

                        if type(constraint) is str:
                            logging.debug(
                                f" Constraint fetch successful of type {type(constraint)}"
                            )
                            logging.debug(f"key: {key} :: constraint :{constraint}")
                            key_constraint_pair[key] = constraint

                        elif type(constraint) is list:
                            try:
                                assert all(type(i) is str for i in constraint)
                                constraint = ",".join(constraint)
                                logging.debug(
                                    f" Constraint fetch successful of type {type(constraint)}"
                                )
                                logging.debug(f"key:{key} :: constraint :{constraint}")
                                key_constraint_pair[key] = constraint

                            except AssertionError as err:
                                logging.critical(
                                    f'The contraint list for "{key}" should containt string values, but given :{constraint}'
                                )
                                logging.critical("Returning none")
                                return

                        else:
                            logging.critical(
                                f"Contraint type should be either sting or a list of sting, given type :{type(constraint)}"
                            )
                            logging.critical("Returning none")
                            return

            return key_constraint_pair
        else:
            logging.critical(" Column passed is null")

    def executeQuery(self, operation=None, params=None, multi=False):
        """
        [PYTHON MYSQL CONNECTOR UTILITY FUNCTION]
        Function to execute query in the db engine
        USAGE: operation->query(str), params->list, multi->bool
        """

        if operation:
            if multi:
                try:
                    logging.info(
                        f" Query in execution : {operation} :: Params: {params} :: Multi: {multi}"
                    )

                    for result in self.cursor.execute(operation, params):
                        if result.is_rows():
                            logging.debug(
                                f" Rows produced by statement '{result.statement}':"
                            )
                            logging.debug(result.fetchall())
                        else:
                            logging.debug(
                                f" Number of rows affected by statement '{result.statement}': {result.rowcount}"
                            )

                except mysql.connector.ProgrammingError as err:
                    logging.info(
                        f" Query execution failed :{operation} :: Params: {params} :: Multi: {multi}"
                    )

                    if err.errno == errorcode.ER_SYNTAX_ERROR:
                        logging.debug(" Check your syntax")
                    elif err.errno == errorcode.ER_BAD_DB_ERROR:
                        logging.debug(" Database doesn't exist")
                    else:
                        logging.debug(err)

            else:
                try:
                    self.cursor.execute(operation, params)
                    logging.info(
                        f" Query in execution :{operation} :: Params: {params} :: Multi: {multi}"
                    )

                except mysql.connector.ProgrammingError as err:

                    if err.errno == errorcode.ER_SYNTAX_ERROR:
                        logging.debug("Check your syntax")
                    elif err.errno == errorcode.ER_BAD_DB_ERROR:
                        logging.debug("Database doesn't exist")
                    else:
                        logging.critical(err)

    def executeMany(self, operation=None, paramsSeq=None):
        if operation:
            try:
                self.cursor.executemany(operation, paramsSeq)

            except mysql.connector.ProgrammingError as err:
                if err.errno == errorcode.ER_SYNTAX_ERROR:
                    logging.debug(" Check your syntax")
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    logging.debug(" Database doesn't exist")
                else:
                    logging.debug(err)

    def use(self, databaseName):

        if databaseName:
            logging.debug(f" Using database: {databaseName}")
            self.executeQuery(f"USE {databaseName}")
        else:
            logging.debug(" Using database failed, no database passed for use.")

    def getCurrentDatabase(self):

        self.executeQuery("SELECT DATABASE();")
        res = self.cursor.fetchall()
        logging.info(f" Current database in use :{res}")
        if res[0][0] == None:
            logging.critical("No database is currently in use")
        return res

    def show(self):
        logging.info(" Show databases in use.")
        self.executeQuery(" SHOW DATABASES")
        res = self.cursor.fetchall()
        logging.info(f" Database selected : {res}")

        databases = []

        for database in res:
            for stringName in database:
                if stringName in ["information_schema", "performance_schema"]:
                    continue
                databases.append(stringName)

        final = {}
        tables = []
        for database in databases:
            self.use(database)

            self.executeQuery(" SHOW TABLES")
            res = self.cursor.fetchall()
            for table in res:
                for stringName in table:
                    tables.append(stringName)
        final.update({database: tables})

        return final

    def create(self, **kwargs):
        """
        [DDL] To create table or database.
        USAGE: Accepts dict -> (operation= table/database, tableName/databaseName= '', columns={field1 : {dataType:' ', constraint: ' '/[]}, field2: {... , ...}, ...})
        To create table or database.
        Table:  set global innodb_file_per_table=1; (default)
                default engine = innodb
                default row format = DYNAMIC
        """

        logging.info(" In creation.")
        try:
            if kwargs["operation"] == "table":

                logging.debug(f"Passed kwargs :{kwargs}")

                try:
                    query = (
                        "CREATE TABLE "
                        + MysqlConnector.addTicks(kwargs["tableName"])
                        + " ("
                    )
                    keys = list(kwargs["columns"].keys())
                    logging.debug(f" Fields name :{keys}")

                    keyDataType = [i["dataType"] for i in kwargs["columns"].values()]
                    logging.debug(f" Data type name :{keyDataType}")
                except KeyError as err:
                    logging.critical(" (Table name) or (Datatype for fields) not given")
                    logging.critical("Retruning none")
                    return

                keyConstraint = MysqlConnector.getConstraint(kwargs["columns"])

                for i in range(len(keys)):
                    query += MysqlConnector.addTicks(keys[i]) + " " + keyDataType[i]
                    if keyConstraint[keys[i]] is not "empty":
                        query += " " + keyConstraint[keys[i]]
                    if i != len(keys) - 1:
                        query += ", "
                    else:
                        query += ")"
                try:
                    rowFormat = kwargs["column"]["rowFormat"]
                    query += f" ROW_FORMAT={rowFormat}"
                except KeyError as err:
                    query += f"ROW_FORMAT=DYNAMIC"
                    logging.info("Using default row format: DYNAMIC")
                query += ";"

                logging.debug(f" Create table query :{query}")

            elif kwargs["operation"] == "database":
                query = (
                    "CREATE DATABASE "
                    + MysqlConnector.addTicks(kwargs["databaseName"])
                    + ";"
                )
                logging.debug(f" Create Database query: { query }")

            elif kwargs["operation"] == "view":

                query = (
                    "CREATE VIEW "
                    + MysqlConnector.addTicks(kwargs["viewName"])
                    + " AS SELECT "
                    + MysqlConnector.addTicks(kwargs["columns"])
                    + " FROM "
                    + kwargs["tableName"]
                    + " INNER JOIN "
                    + MysqlConnector.addTicks(kwargs["fields"])
                    + " USING "
                    + "("
                    + MysqlConnector.addTicks(kwargs["using"])
                    + ")"
                )

        except KeyError as err:
            logging.critical(" Specify operation on table or database, exiting..")
            return

    def desc(self, tableName):
        logging.info(" o describe.")
        if tableName:
            query = "DESC " + MysqlConnector.addTicks(tableName) + ";"
            logging.debug(f"Query : {query}")

            self.executeQuery(query)
            res = self.cursor.fetchall()

            logging.info(f"Response fetchall: {res}")
            return res

        else:
            logging.critical(f" Tablename passed in DESC :{tableName}")

    def insert(self, **kwargs):
        """

        [DML] To insert content in db table.
        USAGE: Accepts dict -> (tableName=' ', values= ' ' / ('val1', 'val2', ....))
        CAUTION: Table field sequence and given values sequence should match !!

        """
        if kwargs:
            column = kwargs.get('column')
            if type(column) is dict:
                
                keys = column.keys()
                values = column.values()
                query = "INSERT INTO "+ MysqlConnector.addTicks(kwargs["tableName"]) + '('+ MysqlConnector.addTicks(keys) +')' + " VALUES ("+values +');'
                # self.executeQuery(query)
                # logging.debug(f" Inserting successful with query: {query}")        
    
                    # query += "', '".join(str(i) for i in values) + "');"
                   

                # else:
                #     if type(entries[0]) is tuple:
                #         query = ""
                #         value = list(kwargs["values"])
                #         query = (
                #             "INSERT O "
                #             + MysqlConnector.addTicks(kwargs["name"])
                #             + " VALUES ("
                #         )

                #         sizeOfEntry = [len(i) for i in value]

                #         for i in range(sizeOfEntry[0]):
                #             query += "%s"
                #             # query += str(kwargs['values'][i])
                #             if i < sizeOfEntry[0] - 1:
                #                 query += ","
                #             elif i == sizeOfEntry[0] - 1:
                #                 query += ")"

                execute = kwargs.get("execute")
                if execute:
                    self.executeQuery(query)
                    logging.debug(f" Inserting successful with query: {query}")
                    logging.info(
                        f" Inserting into {kwargs['name']} values :{kwargs['values']}"
                    )
                else:
                    logging.debug(
                        f' Returning query as "execute" field passed as {execute}'
                    )
                    return query     
            else:
                logging.critical(
                    f" Column field,value should be of type dict")
                         
        else:
            logging.debug(f" No Parameters passed ")

    def select(self, **kwargs):
        """
        Select query.
        USAGE: Accepts dict -> (columnName= '*' / 'cols' / list(cols), tableName='', where='',
        groupby='', having='')
        """
        if kwargs:
            colOption = kwargs.get("columnName")
            tableName = kwargs.get("tableName")
            where = kwargs.get("where")
            groupBy = kwargs.get("groupBy")
            having = kwargs.get("having")
            inner_join = kwargs.get("inner_join")
            if colOption and tableName:
                query = "SELECT "
                if colOption is "*":
                    query += "*"
                elif type(colOption) is str:
                    query += MysqlConnector.addTicks(colOption)
                elif type(colOption) is list:
                    tickedList = MysqlConnector.addTicks(colOption)
                    tickedCol = ",".join(tickedList)
                    query += tickedCol
                query += " FROM " + "`" + tableName + "`"

                if where is None:
                    pass
                else:
                    try:
                        assert type(where) is str
                        query += " WHERE " + where
                    except AssertionError as err:
                        logging.critical(
                            f" Where clause should be of type str/None but given type is :{type(where)}"
                        )
                        return

                if groupBy is None:
                    pass
                else:
                    try:
                        # ofType = type(groupBy)
                        assert type(groupBy) is str
                        query += "GROUP BY " + MysqlConnector.addTicks(groupBy)
                    except AssertionError as err:
                        logging.critical(
                            f" Group by clause should be of type str or list but give type is :{type(groupBy)}"
                        )
                        return

                if having is None:
                    pass
                else:
                    try:
                        assert type(having) is str
                        query += " HAVING " + having

                    except AssertionError as err:
                        logging.critical(
                            f" Having clause should be of type str or list but give type is :{type(having)}"
                        )
                        return
                if inner_join is None:
                    pass
                else:
                    try:
                        assert type(inner_join) is str
                        query += "INNER JOIN " + inner_join
                    except AssertionError as err:
                        logging.critical(
                            f" Join clause should be of type str or list but give type is :{type(inner_join)}"
                        )
                        return
                self.executeQuery(query)
                res = self.cursor.fetchall()
                return res

            else:
                logging.critical("Column name and table name is not passed")
        else:
            logging.debug("No parameters passed to select from")

    def update(self, **kwargs):
        """
        [DML] To update table.
        USAGE: Accepts dict -> (tableName='', columns={ 'colName' : 'setCondition', : , ... }, where='')

        """
        if kwargs:
            tableName = kwargs.get("tableName")
            columns = kwargs.get("columns")
            where = kwargs.get("where")
            if tableName and columns:
                try:
                    assert type(columns) is dict
                    query = "UPDATE " + "`" + tableName + "`" + " SET "
                    for i, j in columns.items():
                        query += "`" + i + "` =" + " '" + j + "'"
                    if where:
                        try:
                            assert type(where) is str
                            query += " WHERE " + where

                        except AssertionError as err:
                            logging.critical(
                                f" Where clause should of the type str but given type is: {type(where)}"
                            )
                            return
                    execute = kwargs.get("execute")
                    if execute:
                        self.executeQuery(query)
                        logging.warning(f" Execute passed as {execute}")
                        logging.debug(f"Query: {query}")
                    else:
                        logging.debug(f"Returning query, execute passed as {execute}")
                        logging.debug(f"Query: {query}")
                        return query

                except AssertionError as err:
                    logging.critical(
                        f"Columns field to 'SET' should be of the type DICT but given type is {type(columns)}"
                    )

    def index(self, **kwargs):

        if kwargs:
            try:
                if kwargs["colName"] and kwargs["tableName"]:

                    operation = kwargs.get("operation", False)
                    if operation == "create":
                        logging.debug(
                            f"Passed --> Table name: {kwargs['tableName']} :: Attribute name: {kwargs['colName']}"
                        )
                        query = (
                            "CREATE INDEX "
                            + "`"
                            + kwargs["colName"]
                            + "`"
                            + " ON "
                            + kwargs["tableName"]
                            + "("
                            + kwargs["colName"]
                            + ")"
                        )

                        self.executeQuery(query)

                    elif operation == "drop":
                        # ALGORITHM [=] {DEFAULT|INPLACE|COPY}
                        algo = kwargs.get("algorithm", False)
                        # LOCK [=] {DEFAULT|NONE|SHARED|EXCLUSIVE}
                        lock = kwargs.get("lock", False)

                        logging.debug(
                            f"Passed --> Table name: {kwargs['tableName']} :: Attribute name: {kwargs['colName']} :: Algorithm: {kwargs.get('algorithm')} :: Lock: {kwargs.get('lock')}"
                        )

                        if algo and lock:
                            query = (
                                "DROP INDEX "
                                + "`"
                                + kwargs["colName"]
                                + "`"
                                + " "
                                + " ON "
                                + "`"
                                + kwargs["tableName"]
                                + "`"
                                + " ALGORITHM = "
                                + kwargs["algorithm"]
                                + " LOCK = "
                                + kwargs["lock"]
                                + " ;"
                            )
                        elif algo:
                            query = (
                                "DROP INDEX "
                                + "`"
                                + kwargs["colName"]
                                + "`"
                                + " "
                                + " ON "
                                + "`"
                                + kwargs["tableName"]
                                + "`"
                                + " ALGORITHM = "
                                + kwargs["algorithm"]
                                + " ;"
                            )
                        elif lock:
                            query = (
                                "DROP INDEX "
                                + "`"
                                + kwargs["colName"]
                                + "`"
                                + " "
                                + " ON "
                                + "`"
                                + kwargs["tableName"]
                                + "`"
                                + " ALGORITHM = "
                                + " LOCK = "
                                + kwargs["lock"]
                                + " ;"
                            )
                        else:
                            query = (
                                "DROP INDEX "
                                + "`"
                                + kwargs["colName"]
                                + "`"
                                + " "
                                + " ON "
                                + "`"
                                + kwargs["tableName"]
                                + "` ;"
                            )
                        self.executeQuery(query)

                    elif operation == "show":
                        databaseName = kwargs.get("databaseName", False)
                        if databaseName:
                            query = (
                                "SHOW INDEXES FROM "
                                + "`"
                                + kwargs["databaseName"]
                                + "`"
                                + " .`"
                                + kwargs["tableName"]
                                + "`"
                            )
                        else:
                            databaseName = (self.getCurrentDatabase())[0][0]
                            if databaseName:
                                logging.info(
                                    f" Showing indexes of the default selected Database "
                                )
                                query = (
                                    "SHOW INDEXES FROM "
                                    + "`"
                                    + databaseName
                                    + "`"
                                    + ".`"
                                    + kwargs["tableName"]
                                    + "`"
                                )
                            else:
                                logging.critical(
                                    " No database is selected, please select/pass database "
                                )
                        self.executeQuery(query)

                    else:
                        logging.critical(" Operation field is empty")

            except KeyError as err:
                logging.critical(f" Both Table and column name should be passed ")

    def procedure(self, **kwargs): #only made for insert and update for now
        name = kwargs.get("name")
        handler_action = kwargs.get("handler_action")
        condition_val = kwargs.get("condition_val")
        transaction = kwargs.get("transaction")
        if all([name, handler_action, condition_val, transaction]):
            proc = (
                "DELIMITER $$ CREATE PROCEDURE "
                + MysqlConnector.addTicks(name)
                + " () BEGIN DECLARE exit handler for sqlexception BEGIN ROLLBACK; END; DECLARE exit handler for sqlwarning BEGIN ROLLBACK; END; START TRANSACTION "
            )
            if "insert" in transaction:
                tableName = kwargs.get("tableName")
                values = kwargs.get("values")
                in_query = self.insert(tableName=tableName, values=values, execute=None)
                proc += in_query + "; "
            if "update" in transaction:
                tableName = kwargs.get("tableName")
                columns = kwargs.get("columns")
                where = kwargs.get("where")
                up_query = self.update(
                    tableName=tableName, columns=columns, where=where
                )
                proc += up_query + "; "
            proc += "COMMIT; END $$ DELIMITER ;"
            logging.debug(f" Procedure created: {proc}")
            execute = kwargs.get("execute")
            if execute:
                self.cursor.execute(proc)
                logging.debug(f"Execute passed as {execute}")
            else:
                logging.debug(f" Execute passed as {execute}")
                return proc

    def drop(self, tableName=None, databaseName=None):
        if tableName:
            logging.warning(f" Dropping table :{tableName}")
            query = "DROP TABLE " + "`" + tableName + "`"
            self.executeQuery(query)
        elif databaseName:
            logging.warning(f" Dropping database :{databaseName}")
            query = "DROP DATABASE " + "`" + databaseName + "`"
            self.executeQuery(query)
        else:
            logging.debug(" No table/database passed to drop")


if __name__ == "__main__":
    print("Raw query class")
else:
    pass
