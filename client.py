import asyncio
# from jupyter_client import AsyncKernelManager
import requests
# import sys
import websockets
import json

async def execute_remote_code():
    # Connect to the Jupyter server via the remote kernel gateway
    base_url = "192.168.55.1:8888"  # Replace with your actual remote Jupyter server IP
    kernel_url = f"http://{base_url}/api/kernels"

    # Start a new kernel by making a POST request to the remote Jupyter server
    headers = {'Content-Type':'application/json'}
    response = requests.post(kernel_url, headers=headers)
    print(f"Initial response code: {response.status_code}")

    if response.status_code == 201:
        kernel_info = response.json()
        kernel_id = kernel_info['id']
        print(f"Kernel started with ID: {kernel_id}")
    else:
        print(f"Error starting kernel: {response.status_code}")
        return
    
    # Websocket URL to connect to the remote kernel for communication (using kernel_id)
    ws_url = f"ws://{base_url}/api/kernels/{kernel_id}/channels"
    # print(ws_url)
    async with websockets.connect(ws_url) as websocket:
        print(f"Connected to WebSocket for Kernel ID: {kernel_id}")
        with open('cudacode.py',"r") as file:
            code_to_execute = file.read()

        # Prepare the execution request
        exec_request = {
            "header":{
                "msg_id": "execute_code",
                "username": "cohitherewer",
                "session": kernel_id,
                "msg_type": "execute_request",
                "version": "5.3"
            },
            "parent_header": {},
            "metadata": {},
            "content":{
                "code": code_to_execute,
                "silent": False,
                "store_history": True,
                "user_expressions": {},
                "allow_stdin": False
            }
        }
        # send the execution request to the kernel over websocket
        await websocket.send(json.dumps(exec_request))
        print("Execution request sent.")

        # Lsiten for output messages from the kernel
        while True:
            try:
                response = await websocket.recv()
                message = json.loads(response)
                # handle different message types
                msg_type = message['header']['msg_type']
                if msg_type == 'stream':
                    print(f"Output: {message['content']['text']}")
                elif msg_type == "execute_result":
                    print(f"Execution result: {message['content']['data']}")
                elif msg_type == "error":
                    print(f"Error: {message["content"]["evalue"]}")
                elif msg_type == 'status' and message['content']['execution_state'] == 'idle':
                    print("Kernel is idle, execution complete")
                    # break
            except KeyError as err:
                print("Some Key Probelm")
                continue
            # except websocket.connection_lost:
            #     print("Websocket connection closed.")
            #     break
            except Exception as err:
                print(f"Error recieving messages: {err}")
                break
if __name__=="__main__":
    asyncio.run(execute_remote_code())

# sdk and stuff => how things are deployed 
# 