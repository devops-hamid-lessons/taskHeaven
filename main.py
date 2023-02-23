import grpc
from concurrent import futures
### import the generated classes form the proto file
import redmine_pb2 as pb2
import redmine_pb2_grpc as pb2_grpc
### for logging
import logging
import autologging
### for rest operations
import requests
#####
import time
import datetime
import sys

_ONE_DAY = datetime.timedelta(days=1)


@autologging.traced
@autologging.logged
class RedmineService(pb2_grpc.redmineServicer):

    # function to implement insertIssueRPC
    def insertIssueRPC(self, request, context):
        try:
            if not (
                    request.credential.redmine_username and request.credential.redmine_password and request.credential.redmine_server_ip):
                self.__log.error(
                    "Missing field: one or more Redmine credentials are absent: username, password, or server ip.")
                # self.returnResult(0, "Provide all Redmine credentials: username, password, server ip.")
                return pb2.response(operation_result=pb2.operationResults.FAILURE,
                                    operation_message="Provide all Redmine credentials: username, password, server ip.")

            if not (request.issue.project_name and request.issue.issue_title and request.issue.issue_priority):
                self.__log.error("Missing field: project_name, issue_title, and issue_priority are required fields.")
                return pb2.response(operation_result=pb2.operationResults.FAILURE,
                                    operation_message="project_name, issue_title, and issue_priority are required fields.")

            self.__log.info("Required fields are all provided.")
            project = request.issue.project_name
            title = request.issue.issue_title
            priority = request.issue.issue_priority
            description = request.issue.issue_description

            base_url = f"http://{request.credential.redmine_username}:{request.credential.redmine_password}@{request.credential.redmine_server_ip}"
            issues_url = f"{base_url}/issues.json"
            projects_url = f"{base_url}/projects.json"
            priorities_url = f"{base_url}/enumerations/issue_priorities.json"

            response = requests.get(projects_url)
            project_id = ""
            for item in response.json()['projects']:
                if item['name'] == project:
                    project_id = item['id']
            if not project_id:
                self.__log.error("There is not any project with the specified name.")
                return pb2.response(operation_result=pb2.operationResults.FAILURE,
                                    operation_message="There is not any project with the specified name.")

            response = requests.get(priorities_url)
            priority_id = ""
            for item in response.json()['issue_priorities']:
                if item['name'] == priority:
                    priority_id = item['id']
            if not priority_id:
                self.__log.error("There is not any priority with the specified name.")
                return pb2.response(operation_result=pb2.operationResults.FAILURE,
                                    operation_message="There is not any priority with the specified name.")

            self.__log.info("specified project_name and priority_name checked, and they both exist.")
            issue_json = {"issue": {"project_id": project_id, "priority_id": priority_id, "subject": title,
                                    "description": description}}
            response = requests.post(issues_url, json=issue_json)
            if response.status_code in [200, 201, 202, 204]:
                self.__log.info("Successful operation.")
                return pb2.response(operation_result=pb2.operationResults.SUCCESS,
                                    operation_message="Successful operation.")
            elif response.status_code == 400:
                self.__log.error("Operation failed: Rest 400 error. The request was malformed")
                return pb2.response(operation_result=pb2.operationResults.FAILURE,
                                    operation_message="Operation failed: Rest 400 error. The request was malformed")

            elif response.status_code == 401:
                self.__log.error(
                    "Operation failed: Rest 401 error. The client is not authorized to perform the requested action, or username or pass is wrong. ")
                return pb2.response(operation_result=pb2.operationResults.FAILURE,
                                    operation_message="Operation failed: Rest 401 error. The client is not authorized to perform the requested action, or username or pass is wrong.")

            elif response.status_code == 404:
                self.__log.error("Operation failed: Rest 404 error. The requested resource was not found.")
                return pb2.response(operation_result=pb2.operationResults.FAILURE,
                                    operation_message="Operation failed: Rest 404 error. The requested resource was not found.")

            elif response.status_code == 415:
                self.__log.error(
                    "Operation failed: Rest 415 error. The request data format is not supported by the server.")
                return pb2.response(operation_result=pb2.operationResults.FAILURE,
                                    operation_message="Operation failed: Rest 415 error. The request data format is not supported by the server.")

            elif response.status_code == 422:
                self.__log.error(
                    f"Operation failed: Rest 422 error. The request contained invalid or missing data.\n{response.json()}")
                return pb2.response(operation_result=pb2.operationResults.FAILURE,
                                    operation_message=f"Operation failed: Rest 422 error. The request contained invalid or missing data.\n{response.json()}")

            elif response.status_code == 500:
                self.__log.error(
                    "Operation failed: Rest 500 error. The server threw an error when processing the request.")
                return pb2.response(operation_result=pb2.operationResults.FAILURE,
                                    operation_message="Operation failed: Rest 500 error. The server threw an error when processing the request.")

            else:
                self.__log.error(f"operation failed: Rest {response.status_code} error.")
                return pb2.response(operation_result=pb2.operationResults.FAILURE,
                                    operation_message=f"operation failed: Rest {response.status_code} error.")

        except Exception as exp:
            self.__log.error(f"operation failed. An exception occurred: {str(exp.__class__)}")
            return pb2.response(operation_result=pb2.operationResults.FAILURE,
                                operation_message=f"operation failed. An exception occurred: {str(exp.__class__)}")


# create a gRPC server
def serve(server_address):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=100))
    pb2_grpc.add_redmineServicer_to_server(RedmineService(), server)
    server.add_insecure_port(server_address)
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY.total_seconds())
    except KeyboardInterrupt:
        server.stop(None)


if __name__ == "__main__":
    logging.basicConfig(
        level=autologging.TRACE,
        stream=sys.stderr,
        format="%(levelname)s:%(filename)s,%(lineno)d:%(name)s.%(funcName)s:%(message)s",
    )

    address = sys.argv[1]
    print("[-] Starting the service on", address, "...")
    serve(address)
