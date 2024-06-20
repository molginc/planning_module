#!/usr/bin/env python3
import numpy as np
from .socket_server import SocketServer

class PolarPlanner(SocketServer):
    def __init__(self, host='localhost', port=8014):
        super().__init__(host, port, id="PolarPlanner")
        self.start_server(self.handle_plan_request)

    # def start_server(self):
    #     server = Thread(target=self.run_server)
    #     server.start()
       

    # def run_server(self):
    #     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #         s.bind(self.server_address)
    #         s.listen()
          
    #         while True:
    #             conn, addr = s.accept()
    #             with conn:
    #                 data = conn.recv(8192)  
    #                 if data:
    #                     request = json.loads(data.decode('utf-8'))
    #                     print(f"P Pl received req: {request}")
    #                     start_angles = request['start_angles']
    #                     goal_angles = request['goal_angles']
                     
    #                     response = self.handle_plan_request(request)
    #                     print(f"Polar Pl sending resp: {response}")
    #                     conn.sendall(json.dumps(response).encode('utf-8'))

    def handle_plan_request(self, request):
        path = self.polar_path_planner(request['start_angles'], request['goal_angles'])
      
        return {'valid_path': path}

    def polar_path_planner(self, start, goal, steps=20): #same as LP for now
        
        start = np.array(start)
        goal = np.array(goal)
        t = np.linspace(0, 1, steps)
        path = np.outer(1 - t, start) + np.outer(t, goal)
        return path.tolist()


if __name__ == '__main__':
    PolarPlanner()
