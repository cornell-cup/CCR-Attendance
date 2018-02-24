import json
import jsonschema
from jsonschema import validate
from CCRResources import res
import time
import itertools

class CCRAttendanceDB:
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

        active_data =  result.get("values",[])

        active_users = []
        for user_data in active_data:
            active_users.append({"user":user_data[0],"time_in":user_data[1],"row":user_data[2]})

        return active_users
        
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

    def log_swipe_in(self,userID,project,team):
        values = [[userID,project,team,time.time()]]
        body = {'values': values}

        resp = self._service.spreadsheets().values().append(
            spreadsheetId = self._config["sheet_id"], range=self._config["swipes_log_range"],valueInputOption="RAW",
            body=body).execute()

        if resp != []:
            return {"success":True,"user:":userID,"direction":"IN"}

    def validate_uid(self,uid):
        pass

    def log_timeout(self,row):
        values = [['TIMEOUT']]
        body = {'values': values}
        self._service.spreadsheets().values().update(
            spreadsheetId=self._config["sheet_id"], range="F"+str(row),
            valueInputOption="RAW", body=body).execute()


    def log_swipe_out(self,userID,sessionRow=None,cached_active_users=None):
        if sessionRow == None:
            swiped_in_users =  cached_active_users if cached_active_users != None else self.get_active_users()
            for swiped_data in swiped_in_users:
                if swiped_data["user"] == userID:
                    sessionRow = swiped_data["row"]

        values = [[time.time()]]
        body = {'values': values}
        resp = self._service.spreadsheets().values().update(
            spreadsheetId=self._config["sheet_id"], range="E"+str(sessionRow),
            valueInputOption="RAW", body=body).execute()
            
        if resp != []:
            return {"success":True,"user:":userID,"direction":"OUT"}

    def get_projects_list(self):
        result = self._service.spreadsheets().values().get(
            spreadsheetId=self._config["sheet_id"], range=self._config["projects_list_range"]).execute()
        return list(itertools.chain(*result.get("values",[])))

    def get_meetings_list(self):
        result = self._service.spreadsheets().values().get(
            spreadsheetId=self._config["sheet_id"], range=self._config["meetings_list_range"]).execute()
        return list(itertools.chain(*result.get("values",[])))
        
    def get_user_id_map(self):
        result = self._service.spreadsheets().values().get(
            spreadsheetId=self._config["sheet_id"], range=self._config["users_list_range"]).execute()
        return result.get("values",[])

    def get_name_from_ID(self,id,user_cache=None):
        users =  user_cache if user_cache != None else self.get_user_id_map()
        for user_id_map in users:
            if user_id_map[0] == id:
                return user_id_map[1]

    def register_user(self,name,uid):
        values = [[name,uid]]
        body = {'values': values}

        self._service.spreadsheets().values().append(
            spreadsheetId=self._config["sheet_id"], range=self._config["users_list_range"],valueInputOption="RAW",
            body=body).execute()