import gearman
import uuid
import json
class task_client(object):
    
    def __init__(self,build):
        self.build = build
    
    def trigger_builder(self):
        params = self.build.getstaticparams()
        server = self.build.distributor.value
        job_name = self.build.task.name
        
        uniqueid = uuid.uuid1().hex
        gm_client = gearman.GearmanClient([server])
        submitted_job_request = gm_client.submit_job("build:{}".format(job_name),\
                                                     json.dumps(params),unique=uniqueid,\
                                                     priority=gearman.PRIORITY_HIGH,\
                                                     background=True)
        

# gm_client = gearman.GearmanClient(["10.159.212.95:4730"])
# completed_job_request = gm_client.submit_job("build:ut", '{"a":123,"b":"v"}',priority=gearman.PRIORITY_HIGH, background=True)