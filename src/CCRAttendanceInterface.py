import json
import jsonschema
from jsonschema import validate
from CCRResources import res
import time



class CCRAttendanceInterface:
    def __init__(self,service, configFile):
        self._service = service
        self._configFile = configFile
        self.config_schema = json.load(open(res("config_schema.json")))
        self.reload_config_file()

    def clear_attendence_log(self):
        '''
            Clears the cells in the range specified as "swipes_log_range"
            in the provided configuration file.
        '''

        body = {
            'ranges': [self._config["swipes_log_range"],self._config["timeout_log_range"]]
        }
        self._service.spreadsheets().values().batchClear(
            spreadsheetId=self._config["sheet_id"],body=body).execute()

    def get_active_users(self):
        '''
            Returns a array of structures describing users who have 
            swiped in but not out in the form:

            [[id_1,time_in_1,log_row_1],[id_2,time_in_2,log_row_2],...]

            Array items are sorted by time_in order.
        '''

        result = self._service.spreadsheets().values().get(
            spreadsheetId=self._config["sheet_id"], range=self._config["active_table_range"]).execute()
        return result.get("values",[])
        
    def reload_config_file(self):
        '''
            Reloads the provided configuration file, if the file matches 
            the config_schema.
        '''
        try:
            config = json.load(open(self._configFile))
            validate(config,self.config_schema)
            self._config = json.load(open(self._configFile))
        except jsonschema.ValidationError:
            print("Invalid config file: " + self._config)

    def _log_swipe_in(self,userID):
        values = [[userID,time.time()]]
        body = {'values': values}

        self._service.spreadsheets().values().append(
            spreadsheetId=self._config["sheet_id"], range=self._config["swipes_log_range"],valueInputOption="RAW",
            body=body).execute()

    def log_timeout(self,userID,row):
        values = [[userID,row]]
        body = {'values': values}
        self._service.spreadsheets().values().append(
            spreadsheetId=self._config["sheet_id"], range=self._config["timeout_log_range"],valueInputOption="RAW",
            body=body).execute()

    def _log_swipe_out(self,sessionRow):
        values = [[time.time()]]
        body = {'values': values}
        self._service.spreadsheets().values().update(
            spreadsheetId=self._config["sheet_id"], range="C"+str(sessionRow),
            valueInputOption="RAW", body=body).execute()

    def log_swipe(self,userID,cached_active_users=None):
        '''
            Logs a user swipe. Will be logged as a swipe-in if the user is
            current in the list of active users and a swipe out otherwise.
        '''
        swiped_in_users =  cached_active_users if cached_active_users != None else self.get_active_users()
        for log in swiped_in_users:
            if log[0] == userID:
                self._log_swipe_out(log[2])
                return 
        self._log_swipe_in(userID)

    
