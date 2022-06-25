#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
from ibmcloudant.cloudant_v1 import AllDocsQuery, CloudantV1
from ibm_cloud_sdk_core import ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from dotenv import dotenv_values

import requests

def main(dict):
    config = dotenv_values(".env")
    db_name = "dealerships"

    try:
        authenticator = IAMAuthenticator(config["CAPSTONE_APIKEY"])
        service = CloudantV1(authenticator=authenticator)
        service.set_service_url(config["CAPSTONE_URL"])

        response = service.post_find(
        db=db_name,
        selector={'state': 'Texas'},
        fields=["_id", "city", "full_name", "address"],
        limit=3
        ).get_result()

        """
        response = service.post_explain(
        db=db_name,
        limit=10,
        selector={"state": "Texas"}
        ).get_result()
        """

        #client = CloudantV1.new_instance(service_name="CAPSTONE")
        """client = Cloudant.iam(
            account_name=dict["COUCH_USERNAME"],
            api_key=dict["IAM_API_KEY"],
            connect=True,
        )"""
        """server_information = service.get_server_information(
).get_result()"""

        """
        db_info = service.get_database_information(
            db=db_name
        ).get_result()
        """


        #all_dbs = service.get_all_dbs().get_result()
        print(response)
        #print("Databases: {0}".format(client.all_dbs()))
    except ApiException as ae:
        print("unable to connect")
        return {"error": ae}
    
    return {"dbs": "finished"}

main({})